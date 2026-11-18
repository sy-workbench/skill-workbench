# Settings for youtube-video-transcript

How to use this file: copy it, rename the copy to `settings.md` (same folder), and fill in the copy. Do not edit this example, so that updating the skill can replace it safely. This skill's README in the skill-workbench repo explains each value.

Everything here is optional. Delete a line, or leave it as it is, to use the default.

Folder for the transcripts, one subfolder per video (default `~/video-transcripts`):
Output folder: <YOUR_OUTPUT_FOLDER>

Whisper model, for example `small`, `medium`, `large` (default `small`):
Whisper model: <YOUR_WHISPER_MODEL>

Caption languages to ask YouTube for, comma separated (default `en,en-orig`):
Caption languages: <YOUR_CAPTION_LANGUAGES>

Who runs the script: `me` (the agent gives you the command) or `agent` (the agent runs it itself) (default `me`):
Who runs the script: <YOUR_RUN_MODE>

Keep the downloaded audio after a successful run: `yes` or `no` (default `no`, the audio is deleted once the transcript is written):
Keep audio: <YOUR_KEEP_AUDIO>
