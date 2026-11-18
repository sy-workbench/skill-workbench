# md-to-html

English | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

Version 1.0. Last updated 2026-11-18.

I write notes in Markdown, often with an AI agent editing alongside me, but some of them are hard to read in the editor: a twelve-column comparison table gets squeezed until every cell wraps, and long notes have no way to fold sections away. This skill turns a `.md` file into a single HTML page that is easier to read. Wide tables scroll sideways with the header and first two columns fixed, Obsidian callouts become collapsible blocks, and the layout adapts to a phone.

The rule that makes it work with an agent: the `.md` is the only source. When you look at the page and say "fold this section" or "add a link to that heading", the agent edits the `.md` and regenerates the page. It never edits the HTML, so the two never drift apart.

## Requirements

- An agent that can run shell commands on the machine where your files are (for example a coding agent, or a desktop app with a terminal tool).
- Python 3 and the `markdown` package, installed for the same `python3` that runs the script, for example `python3 -m pip install --user markdown`. A Homebrew-managed Python may refuse this; a virtual environment works there. You can also ask your agent to install it.

There are no accounts or IDs to set up. With no `settings.md`, the skill uses the `default` theme and English as the page language.

## Setup

Copy this skill folder, including `scripts/` and `assets/`, into your agent's skills directory (the directory depends on your tool).

Optional: copy `settings.example.md` to `settings.md` in the same folder to change two defaults:

- Default theme: the theme used when you do not name one. Either a file name in `assets/themes/` without `.css` (for example `dark`), or the path to your own `.css` file.
- Page language: the language code written into the page, for example `zh-Hant` or `ja`. Browsers use it to pick fonts, and screen readers use it to pick a voice.

## Usage

Ask in your own words, for example "preview notes.md as HTML" or "turn this file into an HTML page". The agent runs the script and tells you where the HTML file is. Open it in a browser. After later changes, refresh the tab.

While looking at the page, you can ask for changes the same way: "fold the Background section", "make a jump link to Pricing", "use the dark theme". The agent puts them into the `.md`.

## Themes

The page layout is in `assets/base.css`. Colors and fonts are in small files under `assets/themes/`: this version ships with `default` (light) and `dark`. To make your own, copy `default.css` to a new name in the same folder and change the values. Your theme is then available by that name, with no change to the script. A theme file can also add its own CSS rules, which override the base layout.

## Good to know

- Everything is inlined into the HTML file, so you can open it offline or send it to someone as a single file.
- Generating a page overwrites the old HTML. Do not edit the HTML yourself; put your changes in the `.md`.
- Supported Obsidian syntax: `[[#Heading]]` and `[[#Heading|label]]` links within the same file, and callouts (`> [!note]- Title` starts folded, `+` or no sign starts open). Links to other files are not converted.
- YAML frontmatter at the top of the `.md` is left out of the page.
- Obsidian syntax inside code blocks or `inline code` is shown as written, so a note that explains the syntax displays correctly.
- Headings inside a callout have no anchor, so a jump link to them does not work.
- Every run writes a log to `/tmp/md_to_html.log`. Your agent can read it when something goes wrong.

## Upgrading to a new version

Replacing the skill folder can erase your `settings.md` and any themes you added to `assets/themes/`. Copy them to another place before you upgrade, and move them back afterwards.

If a new version needs a new setting, `CHANGELOG.md` says so.

## Running in the cloud or on a phone

The skill needs a shell to run the script, so it does not work in environments without one, such as most phone apps. In an environment that has a shell but keeps only `SKILL.md`, paste the contents of your `settings.md` at the end of `SKILL.md` under the heading `## Settings (pasted)`, and copy `scripts/` and `assets/` as well. Upgrading replaces `SKILL.md`, so paste the settings again after each upgrade.

## License

MIT, see the [LICENSE](../../LICENSE) at the repo root.
