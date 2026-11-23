# skill-workbench

English | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

These are the skills I use with my own AI agents, cleaned up so you can use them too. To start, pick a category below, open the README of a skill you like, and see what you need to prepare.

## Categories

### workflow

When I discuss a topic with AI, I often switch between agents, sessions and devices (for example, phone and laptop). The skills in this category are small tools that make that switching more efficient.

For example, picking up a discussion in a different agent, or sending a phone screenshot to the agent that should handle it.

Start with [agent-inbox](workflow/agent-inbox/README.md).

### tools

Small utilities with a script behind them.

[md-to-html](tools/md-to-html/README.md) turns a Markdown note into an HTML page that is easier to read: wide tables scroll sideways, sections fold away, and it works on a phone. The `.md` stays the only source, so you can keep asking your agent for changes while looking at the page.

### video-transcript

[youtube-video-transcript](video-transcript/youtube-video-transcript/README.md) turns a YouTube video into a transcript with Whisper on your own computer, then fixes the names and terms speech recognition gets wrong. The download and the transcription are separate halves, so other video sites can be added without touching the rest.

### investing

[alert-spx-ma](investing/alert-spx-ma/README.md) checks whether the S&P 500 has pulled back to near its 50-day moving average (you can set another length), and, if you set fallback months, never waits forever. It only reports; it never trades.

I will add more categories as I clean up more skills. Design notes are in [docs/](docs/). They are only for reference and do not affect how you use the skills. If you use more than one agent, [one skill folder, two agents](docs/claude-codex-skill-sync.md) describes how I keep the same skills working in Claude and Codex.

## How to use a skill

Every skill README lists what you need to prepare. If a skill is part of a group, the group README has it. In general, it comes down to two steps:

1. Copy the skill folder into the folder where you keep your skills.
2. Copy `settings.example.md` to `settings.md` and fill in your own values. If a skill needs a value you left empty, it stops and tells you which when it runs. Some skills have defaults for everything, so you only fill in what you want to change, or nothing at all.

`SKILL.md` has no placeholders to replace, so you can overwrite it when a new version comes out, unless you have changed it yourself.

Some environments, such as scheduled cloud runs and phone apps, cannot read `settings.md`. There, paste your settings at the end of `SKILL.md`. The README explains how. Overwriting `SKILL.md` on update erases what you pasted, so paste it again.

## Versions

Each skill has its own version and its own `CHANGELOG.md`, which records what changed in each version. A small fix raises the number after the dot. A major change in behavior raises the number before it. Each skill README shows the current version and the date it was last updated.

## License and notes

MIT, see [LICENSE](LICENSE). This is my personal project and is not affiliated with any company.
