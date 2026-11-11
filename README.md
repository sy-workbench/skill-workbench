# skill-workbench

These are the skills I use with my own AI agents, cleaned up so you can use them too. To start, pick a category below, open the README of a skill you like, and see what you need to prepare.

Traditional Chinese: [README.zh-TW.md](README.zh-TW.md)

## Categories

### workflow

When I discuss a topic with AI, I often switch between agents, sessions and devices (for example, phone and laptop). The skills in this category are small tools that make that switching more efficient.

For example, picking up a discussion in a different agent, or sending a phone screenshot to the agent that should handle it.

Browse them in [workflow/](workflow/).

I will add more categories as I clean up more skills. Design notes are in [docs/](docs/). They are only for reference and do not affect how you use the skills.

## How to use a skill

Every skill README lists what you need to prepare. If a skill is part of a group, the group README has it. In general, it comes down to two steps:

1. Copy the skill folder into the folder where you keep your skills.
2. Copy `settings.example.md` to `settings.md` and fill in your own values. If you miss one, the skill stops and tells you which when it runs.

`SKILL.md` has no placeholders to replace, so you can overwrite it when a new version comes out, unless you have changed it yourself.

Some environments, such as scheduled cloud runs and phone apps, cannot read `settings.md`. There, paste your settings at the end of `SKILL.md`. The README explains how. Overwriting `SKILL.md` on update erases what you pasted, so paste it again.

## Versions

Each skill has its own version and its own `CHANGELOG.md`, which records what changed in each version. A small fix raises the number after the dot. A major change in behavior raises the number before it. Each skill README shows the current version and the date it was last updated.

## License and notes

MIT, see [LICENSE](LICENSE). This is my personal project and is not affiliated with any company.
