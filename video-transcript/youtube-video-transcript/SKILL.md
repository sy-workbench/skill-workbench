---
name: "youtube-video-transcript"
version: "1.1"
updated: "2026-11-18"
description: "Turn a YouTube video into a transcript: Whisper does the transcription, and the video's own captions, if any, are kept only for comparison. Then fix names and terms the speech recognition got wrong. Use when the user pastes a YouTube link (youtube.com/watch, youtu.be, shorts, live) and asks for a transcript, especially when the video has no usable captions. One video at a time."
---

## Settings

Read `settings.md` in the same folder as this file, if it exists. Every value is optional: if the file is missing, or a value still has the form `<YOUR_...>`, use the default below. If `settings.md` cannot be read in your environment, use the block headed `## Settings (pasted)` at the end of this file, if the user added one.

| Setting | Default |
|---|---|
| Output folder | `~/video-transcripts` |
| Whisper model | `small` |
| Caption languages | `en,en-orig` |
| Who runs the script | `me` (the user runs it in a terminal) |
| Keep audio | `no` (the audio is deleted after a successful run) |

## Overview

The script `scripts/yt_transcript.py` (in the same folder as this file) downloads only the audio, captions and metadata with yt-dlp, then transcribes with Whisper. It does not open a browser, sign in or use cookies. Results go to one folder per video under the output folder, with an `index.md` that lists every video processed so far.

## Scope of use

This skill is for personal study notes on the user's own computer. A transcript is a copy of someone else's spoken content, so it is not for reposting or publishing another person's full transcript, or for commercial use. YouTube's Terms of Service restrict downloading content, and copyright rules differ between countries; the user checks what applies where they live. Do not tell the user whether a particular use is legal. If they ask, repeat this scope and suggest they check the rules themselves.

## How it is split

The work has two halves. Downloading is specific to YouTube. Transcribing and correcting are the same for any video source; see "Correcting names and terms" below.

## Input format

- One YouTube link: `youtube.com/watch?v=`, `youtu.be/`, `/shorts/`, `/live/`. Extra parameters such as `&t=` are ignored; the whole video is transcribed.
- Optional: a language code to force, for example `en`, `zh`, `ja`. By default the script uses the language YouTube reports, and Whisper detects it if there is none.
- A playlist link: only one video is processed. Ask which one first.
- Private, members-only, sign-in-only or age-restricted videos are not supported, because the script never signs in. Tell the user.

## Workflow

### Step 1: check whether it is already done

1. Take the 11-character video ID from the link.
2. Read `index.md` in the output folder, if it exists, and look for that ID in the "Video ID" column.
3. If it is there, answer from that video's folder and do not run again, unless the user asks for a fresh run. The audio is normally gone (it is deleted after a successful run); that is expected and does not mean the run is incomplete. A fresh run downloads the audio again.

### Step 2: run the script

The command (`<skill folder>` is the folder this file is in; add `--out-root`, `--model` and `--sub-langs` only when the settings differ from the defaults above; add `--keep-audio` only when **Keep audio** is `yes` or the user asks to keep the audio):

```
python3 "<skill folder>/scripts/yt_transcript.py" "<link>" [--out-root <folder>] [--model <name>] [--sub-langs <list>] [--lang <code>] [--keep-audio]
```

- If **Who runs the script** is `me`: give the user the command, with the real path and link filled in, and tell them where to paste it (a terminal on their computer). Say what they should see when it finishes: the last line is the output folder's path; on macOS a "Done" notification also appears. Wait for them to say it finished or paste the error.
- If it is `agent`: run it yourself, but only if you have a shell on the user's computer with network access and can let a command run for a long time (with `small`, Whisper takes roughly 0.4 times the video length, and up to twice that when it has to run again; `medium` and `large` are several times slower). Otherwise fall back to `me`.
- If it fails: do not retry, and do not change options to try again. Read the last lines of the output (or `/tmp/yt_transcript.log`) and tell the user what went wrong. Let the user decide the next step.

Limits built into the script: each video is downloaded once per run, with no automatic retry. A video that failed twice in 24 hours is refused; add `--force` only when the user explicitly asks to try again. Every attempt is recorded in `access_log.jsonl` in the output folder.

### Step 3: correct names and terms

Read `transcript_<lang>.txt` in the video's folder and follow "Correcting names and terms" below. Then run the script with `--reindex` (plus `--out-root` if you used it) so `index.md` shows the corrected file.

### Step 4: report

Tell the user where the files are, how many corrections you made, and how many suspect words you left alone for lack of evidence. Say that both the transcript and the captions are machine output; if captions exist, the script cannot tell whether they were written by a person or generated automatically, so they are only for comparison.

### Correcting names and terms

These rules work for any video source. The YouTube-specific part is only which reference sources exist.

Fix only two things: names (people, products, companies, ticker symbols, technical terms) and obvious sound-alike mistakes. For example, Whisper hears "Codex" as "CoreDesk".

Do not:
- rewrite sentences, polish wording or change punctuation style;
- convert between scripts (for example Traditional and Simplified Chinese) or change regional wording. Keep the characters as transcribed;
- change a suspect word without evidence. Leave it, and list it under "Not changed" in `corrections.md` with the reason.

Reference sources, strongest first:
1. The video's title, description, tags and chapter titles (in `source-metadata.md`; chapter titles often contain the names).
2. Captions uploaded by the creator.
3. Automatic captions (`platform_subtitle_<lang>.srt` may be either kind). They are also machine output with their own mistakes, so they only count as supporting evidence: a correction needs the transcript context or a source above to agree. A word that appears only in the captions needs a check against the title or the surrounding text.
4. No source, only your own knowledge: fix only when you are very sure (for example the standard spelling of a well-known company), and write "general knowledge" as the evidence. Never change numbers, ticker symbols or amounts on general knowledge alone.

Saving:
1. Save the corrected text as `transcript_<lang>_corrected.txt`. Never change the original `transcript_<lang>.txt` or `.srt`.
2. Write `corrections.md` in the same folder: one line naming the reference sources used, a table with the columns `Original | Corrected | Evidence`, then a "Not changed" list with reasons.

### Edge Cases

- `yt-dlp not found` (or `whisper`, `ffmpeg`, `ffprobe`): the user needs to install it; the README lists what to install.
- yt-dlp warns `No supported JavaScript runtime`, or YouTube downloads fail with HTTP 403: the user needs a JavaScript runtime such as Deno; the README lists it.
- `Whisper did not finish within ... seconds`: the time limit depends on the model. Suggest a smaller model; the user decides.
- What counts toward the two-failures-in-24-hours limit: only download failures that come from the video or YouTube. No network (including a blocked proxy), a missing tool, any Whisper problem, and unexpected errors in the script are logged but not counted.
- yt-dlp fails (HTTP 429, sign-in required, region lock, video removed): no retry. Report the last line of the error. YouTube changes often, and an old yt-dlp is a common cause, so suggest updating yt-dlp; the user decides whether to run again.
- "no network in this environment": common in agent sandboxes. It is not counted as a failure. Ask the user to run the command in their own terminal.
- Long videos: for anything over an hour, tell the user the expected time before running (roughly 0.4 times the length, up to twice that if a second run is needed).
- No speech, or only music: report "no speech to transcribe" instead of passing off noise as a transcript.
- Repeats remain after the second run: report the timestamps and let the user decide whether to accept the transcript.
- Language: an English video gives an English transcript. Nothing is translated.
- A run failed after the download: the audio stays in the video's folder, and the next run reuses it instead of downloading it again. It is deleted when a later run succeeds, unless **Keep audio** is `yes`.

## Output files

One folder per video, `<output folder>/<video id>/`:
- `source-metadata.md`: platform, title, author, link, duration, tags, chapter titles, description (up to 5,000 characters), transcription settings.
- `transcript_<lang>.txt` and `transcript_<lang>.srt`: the Whisper transcript (`<lang>` is the language code).
- `platform_subtitle_<code>.srt`: captions in the same language as the transcript, if any. When several exist, the exact language code is kept over regional variants and automatic `-orig` captions; remaining ties follow the order in **Caption languages**. Auto-translated captions are not kept.
- `audio.m4a` (or whichever audio format yt-dlp got): deleted after a successful run, unless **Keep audio** is `yes` (`--keep-audio`). After a failed run it stays, so the next run can reuse it.
- `transcript_<lang>_corrected.txt` and `corrections.md`: written in step 3.
- `meta.json`: platform, video ID, title, author, link, date processed, duration, language.

In the output folder itself: `index.md` (generated; do not edit by hand) and `access_log.jsonl`. Log file: `/tmp/yt_transcript.log`.

## Reference

- yt-dlp: https://github.com/yt-dlp/yt-dlp
- Whisper: https://github.com/openai/whisper
- Script usage: `python3 scripts/yt_transcript.py --help`.

## Dependencies

- On the computer that runs the script: Python 3.9 or later, yt-dlp, a JavaScript runtime for yt-dlp (Deno recommended), openai-whisper, ffmpeg and ffprobe.
- No browser, account, sign-in or cookies.
