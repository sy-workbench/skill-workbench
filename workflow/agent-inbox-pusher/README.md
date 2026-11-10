# agent-inbox-pusher

Version 1.2. Last synced 2026-11-10. Part of [skill-workbench](../../README.md). Unofficial, not affiliated with Anthropic.

Saves the current session's discussion as a structured entry in a Notion "Agent Inbox", so another agent (or you, on another device) can pick it up later. It can also skip Notion and print a pasteable handoff prompt for a new session.

Its companion is [agent-inbox-loader](../agent-inbox-loader/README.md), which reads entries back.

## Two modes

| Mode | Say this | What happens |
|---|---|---|
| A: Notion | `push to inbox`, `save to inbox`, `sync to inbox` | Shows a four-section draft (Background / Problem / Resolution / Next Step) with Type and Handover To, then writes it to Notion after you confirm |
| B: Paste | `provide a prompt`, `handoff prompt`, `prompt for the new session` | Prints one code block you can paste into a new session. Writes nothing |

Phrases that fit both modes, such as "handoff" or "new session", make the skill ask once: "Paste a prompt or write it to the Inbox?"

Mode B needs no setup. Mode A needs the Setup below.

## Requirements

- An agent that can load skills (a folder with a `SKILL.md`) and has the Notion MCP connector enabled. This was built and tested with Claude. Other agents that read `SKILL.md` folders may work, but that is untested.
- A Notion workspace where you can create a database.

## Setup

Do each step once.

1. In Notion, create a database named "Agent Inbox".
2. Add the properties listed in `references/inbox-database.md` (Title, Date, Type, Handover To, Status, Last Edited).
3. In the `Handover To` property, add one option per agent role you use. Add one more option for yourself.
4. Ask your agent: "Fetch this database with the Notion tool and tell me its data source ID." You should get a string that starts with `collection://`.
5. Copy this skill folder into your agent's skills directory. The directory depends on your tool.
6. In the skill folder, copy `settings.example.md` to `settings.md` and fill in the data source ID from step 4. Add your own sensitive-data rules under Sensitive data if you have any. Do not edit the example file. `PLACEHOLDERS.md` at the repo root lists every setting.
7. In each agent's own instructions, state its role name. It must match one option of `Handover To`.

## Updating

Copy the new files over your existing skill folder. Do not delete the folder first, or your `settings.md` goes with it. `SKILL.md` and `settings.example.md` are safe to overwrite. If a new version needs a new setting, `CHANGELOG.md` says so, and the skill stops and names the missing one.

## Running in the cloud or on a phone

Some environments (scheduled cloud runs, phone apps) store only `SKILL.md` and cannot read `settings.md`. There, paste the contents of your filled-in `settings.md` at the end of `SKILL.md` under the heading `## Settings (pasted)`. The skill uses that block when it cannot read the file. An update replaces `SKILL.md`, so paste again after updating.

## Files

| File | Purpose |
|---|---|
| `settings.example.md` | The values you fill in. Copy it to `settings.md` |
| `SKILL.md` | The skill itself |
| `references/inbox-database.md` | Database schema, status meanings, handling principles, roles |
| `CHANGELOG.md` | Version history |
| `README.zh-TW.md` | Traditional Chinese README |

## License

MIT, see the [LICENSE](../../LICENSE) at the repo root.
