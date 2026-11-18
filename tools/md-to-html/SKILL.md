---
name: "md-to-html"
version: "1.0"
updated: "2026-11-18"
description: "Turn a Markdown file into a styled, self-contained HTML preview, and keep the .md as the only source when the user asks for changes while looking at the HTML. Use when the user asks to view, preview or convert a .md file as HTML, or, while looking at a generated HTML page, asks to change its content, make a section collapsible, or add a jump link to a heading."
---

## Settings

Read `settings.md` in the same folder as this file, if it exists. Every value in it is optional, so if it is missing, or a value still has the form `<YOUR_...>`, use the default for that value and carry on. If `settings.md` cannot be read in your environment, use the block headed `## Settings (pasted)` at the end of this file, if the user added one.

| Setting | Default |
|---|---|
| Default theme | `default` |
| Page language | `en` |

## Overview

The `.md` file is the only source. The HTML is a throwaway preview that the script regenerates; nobody edits it by hand. This is what lets the user keep writing in their Markdown editor (Obsidian works well) while reading the result in a browser, where wide tables scroll sideways and long notes fold away.

The script is `scripts/md_to_html.py`, in the same folder as this file. Themes are CSS files in `assets/themes/`.

## Input format

- A path to a `.md` file. If the user names a file without a path, find it first; if several files match, ask which one.
- Optional: a theme name (one of the files in `assets/themes/`, without `.css`) or a path to the user's own `.css` file.
- Optional: an output path. Default: next to the `.md`, same name, `.html`.

## Workflow

1. Run the script. `<skill folder>` is the folder this file is in.
   ```
   python3 "<skill folder>/scripts/md_to_html.py" "<path to .md>" [--theme <name or .css path>] [--out <path>] [--lang <code>]
   ```
   Pass `--theme` and `--lang` only when the user asked for something other than the settings, or the settings differ from the script's defaults (`default`, `en`).
2. The last line of output is the path of the HTML file. Tell the user where it is and that refreshing the browser tab shows the new version.
3. When the user asks for a change while looking at the HTML, edit the `.md`, then run step 1 again. Never edit the `.html`: the next run would overwrite the change, and the source and the preview would no longer match.

How to turn common requests into Markdown:

| The user asks | Write this in the .md |
|---|---|
| Fold this section (closed by default) | Make it a callout: first line `> [!note]- Title`, then every line of the section starting with `> ` |
| Fold it, but open by default | The same, with `+`: `> [!note]+ Title`. No sign at all (`> [!note] Title`) also starts open |
| A link that jumps to a heading | `[[#Heading]]`, or `[[#Heading\|shorter label]]`. The text after `#` must match the heading exactly |
| Change colors or fonts | Pick another theme with `--theme`, or copy `assets/themes/default.css` to a new file in the same folder and change the values. Do not add per-file CSS to the page |

What the script does on every run: removes YAML frontmatter, converts the two Obsidian syntaxes above, makes wide tables scroll sideways with the header row and first two columns fixed, adapts the layout to phones, and adds a back-to-top button.

### Edge Cases

- `python-markdown is not installed` in the output: the package must be installed for the same `python3` that runs the script. Tell the user to run `python3 -m pip install --user markdown` (or install it yourself if your environment allows), then run again. If pip refuses with `externally-managed-environment` (common with Homebrew's Python), suggest a virtual environment and running the script with that environment's `python3`.
- `cannot write ...`: the output folder does not exist or is not writable. Check the `--out` path; create the folder only if the user wants it.
- `cannot read ... as UTF-8 text`: the file is not UTF-8 text. Tell the user; do not convert the file's encoding without asking.
- Obsidian syntax inside code (a fenced block, or `inline code`) is shown as written on purpose, so notes that explain the syntax display correctly.
- A link to a heading that sits inside a callout does not jump, because those headings get no anchor. Suggest moving the heading out of the callout or linking to the heading above it.
- Markdown in a callout title (bold, code) is shown as plain text.
- `theme not found`: the message lists the available themes. Ask the user which one, or use `default`.
- A heading link does not jump: the text in `[[#...]]` does not match the heading exactly (punctuation and brackets count). Fix the link text, not the heading, unless the user wants the heading changed.
- The user pastes or edits HTML and asks to keep it: explain that the next run overwrites it, and offer to put the change into the `.md` instead.
- The user wants several files linked together or extra page features: these are not built in. Say so, and offer to add them to the `.md` as ordinary links or sections.
- Running in an environment without a shell (some phone or cloud runs): the script cannot run there. Say so; do not hand-write the HTML as a substitute.

## Output files

- The `.html` file, at the output path. CSS and the small page script are inlined, so the file works offline and can be sent on its own.
- Log: `/tmp/md_to_html.log`, one line per step, formatted `[YYYY-MM-DD HH:MM:SS] message`. Read it first when something goes wrong.

## Reference

- python-markdown: https://python-markdown.github.io/
- Theme variables: the comments at the top of `assets/base.css` and `assets/themes/default.css`.

## Dependencies

- Python 3 and the `markdown` package, installed for the same `python3` (`python3 -m pip install --user markdown`).
- A shell the agent can run commands in.
