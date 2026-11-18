# Changelog

## 1.0 (2026-11-18)
- Initial public release.
- One yt-dlp call downloads only the audio, captions and metadata. No browser, sign-in or cookies.
- Whisper transcribes the audio. If it repeats one segment three or more times in a row, it runs again with `condition_on_previous_text False` and keeps the better run.
- Keeps one caption file for comparison, in the transcript's language: the exact language code first, automatic `-orig` captions last, then the order of your caption languages. Auto-translated captions are dropped. Works even when YouTube does not report the video's language.
- `source-metadata.md` includes the chapter titles and up to 5,000 characters of the description, as evidence for name corrections.
- Writes one folder per video plus an `index.md`, so a video that was already done is answered from disk instead of downloaded again.
- Stops on the first failure with no automatic retry, and refuses a video that failed twice in 24 hours unless `--force` is given. Local problems (no network or a blocked proxy, a missing tool, any Whisper problem, an unexpected script error) do not count against the video.
- Whisper's time limit grows with the model, so `medium` and `large` are not cut off.
- Rules for correcting names and terms are part of the skill: what to fix, what never to change, and which reference sources count as evidence.
- Optional `settings.md` for the output folder, Whisper model, caption languages, and whether you or the agent runs the script.
