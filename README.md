# skill-workbench

Agent skills from my own multi-agent setup, cleaned up so you can reuse them. Each skill is a folder with a `SKILL.md` that an AI agent can load, plus a README that explains setup.

This is an unofficial personal project. It is not affiliated with, endorsed by, or sponsored by Anthropic. "Claude" is a trademark of Anthropic.

Traditional Chinese: [README.zh-TW.md](README.zh-TW.md)

## Skills

| Skill | Category | Version | What it does |
|---|---|---|---|
| [agent-inbox-loader](workflow/agent-inbox-loader/README.md) | workflow | 1.0 | Loads one entry from a shared Notion "Agent Inbox" into the current session, so you can continue work started elsewhere |
| [agent-inbox-pusher](workflow/agent-inbox-pusher/README.md) | workflow | 1.1 | Saves the current discussion as an Agent Inbox entry, or prints a pasteable handoff prompt for a new session |

More skills will be added by category as they are cleaned up.

## Layout

```
skill-workbench/
  README.md            this index
  README.zh-TW.md      Traditional Chinese index
  LICENSE              MIT
  PLACEHOLDERS.md      every value you must fill in, and where
  docs/                design notes (not needed to run a skill)
  workflow/            skills about moving work between agents and sessions
    <skill-name>/
      SKILL.md         the skill
      README.md        setup and usage
      README.zh-TW.md  Traditional Chinese README
      CHANGELOG.md     version history
      references/      supporting files the skill reads
```

Each skill folder is self-contained. Copy one folder and it works on its own. Shared reference files are duplicated on purpose, so you never need to install anything else.

## How to use a skill

1. Open the skill's README and follow its Setup section.
2. Copy the skill folder into your agent's skills directory.
3. Fill in the placeholders in `SKILL.md`. If one is left empty, the skill stops and tells you.

## Versions

Every skill has its own version (major.minor) and its own `CHANGELOG.md`. A small fix bumps the minor number. A change in behavior bumps the major number. The README of each skill shows the version and the date it was last synced.

## License

MIT. See [LICENSE](LICENSE).
