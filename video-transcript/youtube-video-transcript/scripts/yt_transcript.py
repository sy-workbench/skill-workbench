#!/usr/bin/env python3
"""yt_transcript.py: YouTube video -> Whisper transcript, with the platform's captions kept for comparison.

# Input format
  python3 yt_transcript.py <YouTube link> [options]   full run
  python3 yt_transcript.py --reindex [--out-root DIR]  rebuild index.md only (no Whisper needed)
  python3 yt_transcript.py --analyze <whisper.json>    report repeated segments (debugging)

  Options:
    --out-root DIR     where per-video folders and index.md go (default: ~/video-transcripts)
    --model NAME       Whisper model (default: small)
    --lang CODE        force the transcription language, e.g. en, zh, ja (default: from YouTube, else Whisper detects)
    --sub-langs LIST   caption languages to ask YouTube for, comma separated (default: en,en-orig)
    --force            run even if this video already failed twice in the last 24 hours
    --keep-audio       keep the downloaded audio after a successful run (default: delete it)

# Workflow
  1. Download (platform-specific): one yt-dlp call fetches audio, captions and metadata.
     No browser, no sign-in, no cookies. Only captions in the video's own language are kept.
  2. Transcribe (shared by any platform): Whisper with default settings. If it repeats the same
     segment 3+ times in a row, run again with condition_on_previous_text False and keep the better run.
  3. Write transcript files, delete the audio (unless --keep-audio), write source-metadata.md
     and meta.json, then rebuild index.md.

### Edge Cases
  - yt-dlp, whisper, ffmpeg or ffprobe missing: stop and say which one to install.
  - Whisper fails or runs past its time limit: stop. Not counted against the video (the cause is local).
  - Captions: the downloader keeps every caption it got as a candidate; after transcription the one
    matching the transcript's language is kept (exact code first, auto "-orig" captions last), the rest deleted.
  - A broken meta.json in one video folder: that folder is skipped in index.md, with a log line.
  - No network (common in agent sandboxes): stop and say so; the run does not count as a failure.
  - yt-dlp fails (HTTP 429, sign-in required, region lock, removed video): stop, no automatic retry.
  - Same video failed 2 times in 24 hours: refuse unless --force.
  - No audio track: stop with "no speech to transcribe".
  - Audio is deleted only after the transcript files are written. On any failure it stays, so a rerun
    can reuse it (yt-dlp skips a file that is already there). If deleting fails, log it and carry on.
  - An unexpected error is logged in access_log.jsonl as "error"; only "fail" counts toward the 24-hour limit.

# Output files
  <out-root>/<video id>/: transcript_<lang>.txt/.srt, platform_subtitle_<lang>.srt (if any),
  source-metadata.md, meta.json; the audio file only with --keep-audio or after a failed run.  <out-root>/index.md and <out-root>/access_log.jsonl.
  Log: /tmp/yt_transcript.log, lines formatted [YYYY-MM-DD HH:MM:SS] message.

# Reference
  yt-dlp: https://github.com/yt-dlp/yt-dlp   Whisper: https://github.com/openai/whisper

# Dependencies
  Python 3.9+ (standard library only), yt-dlp, openai-whisper, ffmpeg and ffprobe on PATH.
  yt-dlp also needs a JavaScript runtime (Deno recommended) for YouTube.
"""
import argparse
import json
import os
import re
import shutil
import site
import subprocess
import sys
import time

LOG = "/tmp/yt_transcript.log"
DEFAULT_OUT_ROOT = os.path.expanduser("~/video-transcripts")
# Rough worst-case Whisper time per second of audio on a laptop CPU, by model. Sets the time limit.
MODEL_SLOWNESS = {"tiny": 0.5, "base": 0.8, "small": 1.5, "turbo": 2, "medium": 4, "large": 8}
REPEAT_THRESHOLD = 3      # rerun Whisper when one segment repeats this many times in a row
MAX_FAILS_PER_VIDEO = 2   # refuse after this many failures for one video within 24 hours (since the last success)
YT_ID = re.compile(r"(?:v=|youtu\.be/|/shorts/|/live/|/embed/)([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])")

# Tools installed with Homebrew or `pip install --user` are often missing from PATH in agent shells.
# They are added after the existing PATH, so a tool the user put on PATH (for example in a venv) still wins.
os.environ["PATH"] = os.pathsep.join(
    [os.environ.get("PATH", ""), "/opt/homebrew/bin", "/usr/local/bin",
     os.path.join(site.getuserbase(), "bin"), os.path.expanduser("~/.local/bin")])


class Fail(Exception):
    pass


class State:
    vid = None
    out_root = DEFAULT_OUT_ROOT
    count_failure = True  # False for failures that are not the video's fault (no network, missing tool)


def redact(s):
    return re.sub(r"(sign|token|sig)=[^&\s\"']+", r"\1=***", str(s))


def log(msg):
    line = "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), redact(msg))
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def notify(text):
    """Desktop notification on macOS; silently skipped elsewhere."""
    if sys.platform != "darwin":
        return
    try:
        subprocess.run(["osascript", "-e", 'display notification "%s" with title "yt-transcript"'
                        % text.replace('"', "'")], timeout=10, capture_output=True)
    except Exception:
        pass


def run(cmd, timeout=None):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


# ---------- access log: one place to stop repeated failing runs ----------
def access_log_path():
    return os.path.join(State.out_root, "access_log.jsonl")


def read_access():
    rows = []
    try:
        with open(access_log_path(), encoding="utf-8") as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return rows


def log_access(vid, result, note=""):
    os.makedirs(State.out_root, exist_ok=True)
    row = {"t": int(time.time()), "at": time.strftime("%Y-%m-%d %H:%M:%S%z"), "platform": "youtube",
           "video_id": vid, "result": result, "note": redact(note)[:200]}
    with open(access_log_path(), "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def check_allowed(vid):
    now = int(time.time())
    mine = [r for r in read_access() if r.get("video_id") == vid and now - r.get("t", 0) < 86400]
    last_ok = max([r["t"] for r in mine if r.get("result") == "ok"] or [0])
    fails = [r for r in mine if r.get("result") == "fail" and r["t"] > last_ok]
    if len(fails) >= MAX_FAILS_PER_VIDEO:
        return False, ("this video failed %d times in the last 24 hours (limit %d). Stopping without retry; "
                       "wait a while, or run again with --force if you are sure" % (len(fails), MAX_FAILS_PER_VIDEO))
    return True, "ok"


# ---------- repeat detection ----------
def norm(t):
    return re.sub(r"[\s,.，。!！?？、:：;；「」『』\"'…-]+", "", t)


def max_repeat(texts):
    best = run_len = 0
    prev = None
    for t in texts:
        n = norm(t)
        if not n:
            continue
        run_len = run_len + 1 if n == prev else 1
        prev = n
        best = max(best, run_len)
    return best


def analyze_json(path):
    with open(path, encoding="utf-8") as f:
        segs = json.load(f).get("segments", [])
    texts = [s.get("text", "") for s in segs]
    dup = sum(1 for i in range(1, len(texts)) if norm(texts[i]) and norm(texts[i]) == norm(texts[i - 1]))
    return {"segments": len(segs), "max_consecutive_repeat": max_repeat(texts), "duplicate_segments": dup}


# ---------- transcription (shared by any platform) ----------
def whisper_run(media, outdir, model, language, nocond, timeout):
    os.makedirs(outdir, exist_ok=True)
    cmd = ["whisper", media, "--model", model, "--output_dir", outdir, "--output_format", "all"]
    if language:
        cmd += ["--language", language]
    if nocond:
        cmd += ["--condition_on_previous_text", "False"]
    t0 = time.time()
    wlog = "/tmp/yt_transcript_whisper_%s.log" % State.vid
    with open(wlog, "w", encoding="utf-8") as lf:
        try:
            p = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, timeout=timeout)
        except subprocess.TimeoutExpired:
            State.count_failure = False  # a local problem, not the video's fault
            raise Fail("Whisper did not finish within %d seconds and was stopped; try a smaller --model" % timeout)
    if p.returncode != 0:
        State.count_failure = False
        raise Fail("Whisper failed, see %s" % wlog)
    stem = os.path.splitext(os.path.basename(media))[0]
    jpath = os.path.join(outdir, stem + ".json")
    if not os.path.exists(jpath):
        State.count_failure = False
        raise Fail("Whisper produced no output")
    stats = analyze_json(jpath)
    stats["seconds"] = round(time.time() - t0)
    with open(jpath, encoding="utf-8") as f:
        stats["detected_language"] = json.load(f).get("language")
    return stem, stats


def pick_caption(subs, lang):
    """Choose the caption that matches the transcript language: the exact code first (more often
    uploaded by the creator), then regional variants, automatic "-orig" captions last."""
    if not lang or lang == "und":
        return None
    lang = lang.lower()
    cands = [c for c in subs if c.split("-")[0].lower() == lang]
    order = list(subs)  # the downloader adds captions in the user's order of preference
    cands.sort(key=lambda c: (c.lower() != lang, c.lower().endswith("-orig"), order.index(c)))
    return cands[0] if cands else None


def model_timeout(model, dur):
    slow = next((v for k, v in MODEL_SLOWNESS.items() if model.startswith(k)), MODEL_SLOWNESS["large"])
    return int(dur * slow + 300)  # +300 s covers loading, and downloading the model on its first use


def transcribe(source, out, media, dur, subs, model, keep_audio=False):
    """Shared back half. `source` is a dict any platform downloader fills in:
    platform, video_id, title, author, link, description, tags, language (or None).
    Optional in `source`: chapters (a list of chapter titles).
    `subs` maps caption language codes to candidate .srt files (may be empty), in order of preference;
    the one matching the transcript language is kept as platform_subtitle_<code>.srt and the rest are deleted."""
    language = (source.get("language") or "").lower() or None

    timeout = model_timeout(model, dur)
    tmp1 = os.path.join(out, "_tmp", "run1")
    stem, st1 = whisper_run(media, tmp1, model, language, False, timeout)
    log("Whisper run 1: %(seconds)d s, %(segments)d segments, longest repeat %(max_consecutive_repeat)d" % st1)
    chosen, chosen_dir, st, rerun = 1, tmp1, st1, False
    if st1["max_consecutive_repeat"] >= REPEAT_THRESHOLD:
        rerun = True
        log("repeated segments found, running again with condition_on_previous_text False")
        tmp2 = os.path.join(out, "_tmp", "run2")
        _, st2 = whisper_run(media, tmp2, model, language, True, timeout)
        log("Whisper run 2: %(seconds)d s, %(segments)d segments, longest repeat %(max_consecutive_repeat)d" % st2)
        if st2["max_consecutive_repeat"] <= st1["max_consecutive_repeat"]:
            chosen, chosen_dir, st = 2, tmp2, st2
    final_lang = language or (st.get("detected_language") or "und").lower()
    for ext in ("txt", "srt"):
        shutil.copyfile(os.path.join(chosen_dir, stem + "." + ext),
                        os.path.join(out, "transcript_%s.%s" % (final_lang, ext)))
    shutil.rmtree(os.path.join(out, "_tmp"), ignore_errors=True)

    sub_lang = pick_caption(subs, final_lang)
    sub_path = None
    if sub_lang:
        sub_path = os.path.join(out, "platform_subtitle_%s.srt" % sub_lang)
        shutil.copyfile(subs[sub_lang], sub_path)
    for p in subs.values():
        try:
            os.remove(p)
        except OSError:
            pass
    shutil.rmtree(os.path.join(out, "_subs"), ignore_errors=True)
    log("captions kept: %s (candidates: %s)" % (sub_lang or "none", ", ".join(sorted(subs)) or "none"))

    if keep_audio:
        audio_note = "kept (--keep-audio)"
        log("audio kept: %s" % os.path.basename(media))
    else:
        try:
            os.remove(media)
            audio_note = "deleted after transcription"
            log("audio deleted: %s" % os.path.basename(media))
        except OSError as e:
            audio_note = "could not be deleted, still on disk"
            log("audio delete failed: %s" % e)

    md = ["# %s" % (source.get("title") or source["video_id"]), "",
          "- Platform: %s" % source["platform"],
          "- Video ID: %s" % source["video_id"],
          "- Author: %s" % (source.get("author") or "(unknown)"),
          "- Link: %s" % source.get("link", ""),
          "- Duration: %.0f s" % dur,
          "- Tags: %s" % ", ".join(source.get("tags") or []),
          "- Language: %s" % final_lang,
          "- Chapters: %s" % (" / ".join(source.get("chapters") or []) or "(none)"),
          "- Description: %s" % ((source.get("description") or "").strip() or "(none)"), "",
          "## Transcription", "",
          "- Model: Whisper %s, language: %s" % (model, language or "auto-detected"),
          "- Run 1: %d s, %d segments, longest repeat %d" % (st1["seconds"], st1["segments"], st1["max_consecutive_repeat"]),
          "- Second run (condition_on_previous_text False): %s, using run %d" % ("yes" if rerun else "no", chosen),
          "- Platform captions: %s" % (("yes (%s), for comparison only; may be manual or automatic" % sub_lang)
                                      if sub_path else "none, or download failed"),
          "- Audio: %s" % audio_note,
          "- Name and term corrections: not done yet"]
    with open(os.path.join(out, "source-metadata.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    meta = {"platform": source["platform"], "video_id": source["video_id"], "title": source.get("title", ""),
            "author": source.get("author", ""), "link": source.get("link", ""),
            "processed_at": time.strftime("%Y-%m-%d"), "duration": int(round(dur)), "language": final_lang}
    with open(os.path.join(out, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    log_access(source["video_id"], "ok")
    log("index.md updated (%d videos)" % reindex())
    log("done: %s" % out)
    notify("Done: %s" % (source.get("title") or source["video_id"])[:30])
    print(out)


def reindex():
    """Rebuild index.md from every <out-root>/*/meta.json. The file list reflects what is on disk."""
    root = State.out_root
    os.makedirs(root, exist_ok=True)
    rows = []
    for d in sorted(os.listdir(root)):
        mp = os.path.join(root, d, "meta.json")
        if not os.path.isfile(mp):
            continue
        try:
            with open(mp, encoding="utf-8") as f:
                meta = json.load(f)
        except (OSError, ValueError) as e:
            log("index: skipping %s, meta.json unreadable (%s)" % (d, e))
            continue
        names = os.listdir(os.path.join(root, d))
        files = []
        if any(n.startswith("transcript_") and n.endswith(".txt") and "_corrected" not in n for n in names):
            files.append("transcript")
        if any(n.endswith("_corrected.txt") for n in names):
            files.append("corrected")
        if any(n.startswith("platform_subtitle_") for n in names):
            files.append("captions")
        if any(n.startswith("audio.") for n in names):
            files.append("audio")
        rows.append((meta.get("processed_at", ""), meta, d, files))
    rows.sort(key=lambda r: r[0], reverse=True)
    lines = ["# Video transcripts", "",
             "One row per video. Generated by the script and `--reindex`; do not edit by hand (it is overwritten). "
             "Look a video up by its ID (11 characters for YouTube).", "",
             "| Platform | Video ID | Title | Link | Processed | Duration (s) | Folder | Files |",
             "|:--|:--|:--|:--|:--|:--|:--|:--|"]
    for _, meta, d, files in rows:
        title = str(meta.get("title", "")).replace("|", "\\|").replace("\n", " ")
        lines.append("| %s | %s | %s | %s | %s | %s | %s/ | %s |" % (
            meta.get("platform", ""), meta.get("video_id", d), title, meta.get("link", ""),
            meta.get("processed_at", ""), meta.get("duration", ""), d, ", ".join(files)))
    tmp = os.path.join(root, "index.md.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(tmp, os.path.join(root, "index.md"))
    return len(rows)


# ---------- download (YouTube-specific) ----------
def download_youtube(url, args):
    """One yt-dlp call: audio, captions and metadata. No sign-in, no cookies. Stops on the first failure."""
    mm = YT_ID.search(url or "")
    if not mm:
        State.count_failure = False
        raise Fail("cannot find a YouTube video ID in the link; paste the full link (with watch?v= or youtu.be/)")
    vid = mm.group(1)
    State.vid = vid
    allowed, why = check_allowed(vid)
    if not allowed and not args.force:
        State.count_failure = False
        raise Fail(why)
    for tool in ("yt-dlp", "whisper", "ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            State.count_failure = False
            raise Fail("%s not found on PATH; install it first (see the skill README)" % tool)
    clean = "https://www.youtube.com/watch?v=%s" % vid  # drop &t= and similar: always the whole video
    out = os.path.join(State.out_root, vid)
    os.makedirs(out, exist_ok=True)
    log("start YouTube %s" % vid)
    cmd = ["yt-dlp", "--no-playlist", "--no-cookies", "--no-progress", "-f", "bestaudio[ext=m4a]/bestaudio",
           "-o", os.path.join(out, "audio.%(ext)s"),
           "--write-subs", "--write-auto-subs", "--sub-langs", args.sub_langs,
           "--sub-format", "srt/vtt/best", "--convert-subs", "srt", "--write-info-json", clean]
    r = run(cmd, timeout=1800)
    err = (r.stderr or "")[-400:]
    if r.returncode != 0:
        if re.search(r"resolve|Name or service|Network is unreachable|getaddrinfo|Temporary failure|"
                     r"Tunnel connection failed|ProxyError|Connection refused", err):
            State.count_failure = False
            raise Fail("no network in this environment; run the same command in a terminal on your computer. %s"
                       % redact(err.strip()[-150:]))
        raise Fail("yt-dlp failed (no automatic retry): %s" % redact(err.strip().replace("\n", " ")[-250:]))
    names = os.listdir(out)
    audio = next((os.path.join(out, n) for n in names
                  if n.startswith("audio.") and not n.endswith((".srt", ".vtt", ".json"))), None)
    if not audio:
        raise Fail("yt-dlp produced no audio file")
    info = {}
    ipp = next((os.path.join(out, n) for n in names if n.endswith(".info.json")), None)
    if ipp:
        with open(ipp, encoding="utf-8") as f:
            info = json.load(f)
        os.remove(ipp)
    ilang = (args.lang or info.get("language") or "").split("-")[0].lower()
    # Collect every caption as a candidate. transcribe() keeps the one in the transcript's language,
    # so captions survive even when YouTube reports no language, and auto-translated ones are dropped.
    sub_dir = os.path.join(out, "_subs")
    os.makedirs(sub_dir, exist_ok=True)
    found = {}
    for n in sorted(os.listdir(out)):
        if n.startswith(("transcript_", "platform_subtitle_")):
            continue
        if n.endswith(".srt"):
            code = n[:-4].split(".")[-1]
            dst = os.path.join(sub_dir, code + ".srt")
            os.replace(os.path.join(out, n), dst)
            found[code] = dst
        elif n.endswith(".vtt"):  # left over when conversion to .srt failed
            os.remove(os.path.join(out, n))
    # Order the candidates as in --sub-langs, so the user's order breaks ties (zh-Hant before zh-Hans, say).
    want = [c.strip() for c in args.sub_langs.split(",") if c.strip()]
    rank = {c: i for i, c in enumerate(want)}
    subs = {c: found[c] for c in sorted(found, key=lambda c: (rank.get(c, len(want)), c))}
    pr = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type", "-of", "json", audio])
    if pr.returncode != 0:
        raise Fail("ffprobe cannot read the audio; the file may be damaged")
    inf = json.loads(pr.stdout or "{}")
    dur = float((inf.get("format") or {}).get("duration") or 0)
    if not any(s.get("codec_type") == "audio" for s in inf.get("streams", [])) or dur <= 0:
        raise Fail("no audio track: no speech to transcribe")
    log("audio OK: %.0f s, caption candidates: %s" % (dur, ", ".join(sorted(subs)) or "none"))
    source = {"platform": "youtube", "video_id": vid, "title": info.get("title", ""),
              "author": info.get("uploader", ""), "link": clean,
              "description": (info.get("description") or "")[:5000], "tags": (info.get("tags") or [])[:10],
              "chapters": [str(c.get("title", "")).strip() for c in (info.get("chapters") or [])
                           if str(c.get("title", "")).strip()],
              "language": ilang or None}
    return source, out, audio, dur, subs


def main():
    ap = argparse.ArgumentParser(description="YouTube video -> Whisper transcript.")
    ap.add_argument("link", nargs="?", help="YouTube link")
    ap.add_argument("--reindex", action="store_true", help="rebuild index.md and exit")
    ap.add_argument("--analyze", metavar="WHISPER_JSON", help="report repeated segments in a Whisper .json and exit")
    ap.add_argument("--out-root", default=DEFAULT_OUT_ROOT)
    ap.add_argument("--model", default="small")
    ap.add_argument("--lang", default=None)
    ap.add_argument("--sub-langs", default="en,en-orig")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--keep-audio", action="store_true", help="keep the audio after a successful run")
    args = ap.parse_args()
    State.out_root = os.path.expanduser(args.out_root)

    if args.analyze:
        print(json.dumps(analyze_json(args.analyze), ensure_ascii=False))
        return
    if args.reindex:
        print("index.md rebuilt, %d videos" % reindex())
        return
    if not args.link:
        ap.print_help()
        sys.exit(2)

    log("script start")
    try:
        source, out, audio, dur, subs = download_youtube(args.link, args)
        transcribe(source, out, audio, dur, subs, args.model, args.keep_audio)
    except Fail as e:
        log("failed: %s" % e)
        if State.vid and State.count_failure:
            log_access(State.vid, "fail", str(e))
        notify("Failed: %s" % str(e)[:40])
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        log("unexpected error: %s: %s" % (type(e).__name__, e))
        if State.vid:  # recorded, but as "error", which the 24-hour limit does not count
            log_access(State.vid, "error", "%s: %s" % (type(e).__name__, e))
        notify("Unexpected error, see the log")
        sys.exit(1)


if __name__ == "__main__":
    main()
