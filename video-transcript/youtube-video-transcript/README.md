# youtube-video-transcript

English | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

Version 1.0. Last updated 2026-11-18.

I learn a lot from videos, but I want to search, quote and take notes from them, and many videos have no captions or only rough automatic ones. This skill turns a YouTube video into a text transcript. It downloads only the audio, transcribes it with Whisper on your own computer, keeps the video's own captions next to it for comparison, and then has your agent fix the names and terms that speech recognition tends to get wrong (a product called "Codex" coming out as "CoreDesk", for example).

If a video already has good captions and a captions tool gets you what you need, that is quicker. This skill is for when it does not.

## Requirements

On the computer that runs the transcription:

- Python 3.9 or later.
- yt-dlp, to download the audio and captions.
- A JavaScript runtime for yt-dlp, which YouTube downloads now need. Deno is the one yt-dlp recommends.
- openai-whisper, which does the transcription locally. The first run downloads the model.
- ffmpeg, which includes ffprobe, for Whisper to read the audio.

On macOS with Homebrew, for example: `brew install yt-dlp deno ffmpeg pipx`, then `pipx install openai-whisper`. A plain `pip install` may be refused by a Homebrew-managed Python, which is why the example uses pipx. You can also ask your agent to check and install these.

No account, sign-in or cookies are needed. Private, members-only and age-restricted videos are therefore not supported.

## Setup

Copy this skill folder, including `scripts/`, into your agent's skills directory (the directory depends on your tool).

Optional: copy `settings.example.md` to `settings.md` in the same folder to change the defaults:

- Output folder: where transcripts go, one subfolder per video. Default `~/video-transcripts`.
- Whisper model: `small` is the default and a good balance. `medium` or `large` are more accurate and much slower.
- Caption languages: which caption languages to ask YouTube for, comma separated. Default `en,en-orig`. Add the codes of the languages you watch, for example `en,en-orig,ja,zh-Hant`. Only captions in the video's own language are kept.
- Who runs the script: `me` (default) means the agent gives you a command to paste into a terminal. `agent` means the agent runs it, which only works if it has a shell on your computer, network access, and can wait a long time.

## Usage

Paste a YouTube link and ask for a transcript. With the default setting, the agent gives you one command to run in a terminal. When it finishes, tell the agent, and it reads the result, corrects names and terms, and tells you where the files are.

Each video gets a folder with the original transcript, the corrected one, a `corrections.md` table of what changed and why, the captions if there were any, and the audio. Ask about the same video again later and the agent answers from that folder instead of downloading it again.

Rough timing with the `small` model: about 0.4 times the video length. If Whisper gets stuck repeating one line, the script runs it again with a different setting, which can almost double the time. Larger models are several times slower; the script's time limit grows with the model, and a run that hits it is not counted as a failed download.

## How it handles different platforms

The script is split into two halves on purpose:

- **Download** is specific to each platform. For YouTube, one yt-dlp call returns the audio, the captions and the metadata (title, description, tags).
- **Transcribe and correct** does not care where the video came from. It takes an audio file plus a small description of the source (platform, ID, title, author, link, description, tags, language) and does the rest: Whisper, the second run when it repeats itself, the output files and the index.

The correction rules in `SKILL.md` follow the same split. What to fix, what never to change, and how strong each kind of evidence is are the same everywhere. The only platform-specific part is which reference sources exist: on YouTube that is the title, description, tags, chapter titles and captions.

To support another site, write a download function that produces that audio file and source description, and pass them to `transcribe()` in `scripts/yt_transcript.py`. The output folder, the index and the correction steps stay the same, so all your transcripts live in one place whatever their source.

## Good to know

- The script never retries on its own. If a download fails, it stops and says why, and a video that failed twice in 24 hours is refused until you explicitly ask again. This avoids hammering YouTube, which can lead to temporary blocks.
- yt-dlp needs updating from time to time, because YouTube changes often. An old yt-dlp is the most common reason downloads fail.
- Both the transcript and the captions are machine output. The correction step only changes names and obvious sound-alike mistakes, and lists anything it was unsure about instead of guessing.
- Nothing is translated: an English video gives an English transcript.
- Every run writes a log to `/tmp/yt_transcript.log`.

## Upgrading to a new version

Replacing the skill folder can erase your `settings.md`. Copy it to another place before you upgrade, and move it back afterwards. Your transcripts live in the output folder, outside the skill, so they are not affected.

If a new version needs a new setting, `CHANGELOG.md` says so.

## Running in the cloud or on a phone

The transcription runs on a computer with the tools above installed, so it cannot run inside a phone app or most cloud sandboxes, which usually have no network access for downloads either. From a phone, you can still ask for the command and run it later on your computer. In an environment that keeps only `SKILL.md`, paste your `settings.md` at the end of `SKILL.md` under the heading `## Settings (pasted)`, and paste it again after each upgrade.

## License

MIT, see the [LICENSE](../../LICENSE) at the repo root.
