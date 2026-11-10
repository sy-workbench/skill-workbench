# agent-inbox-loader

Version 1.1. Last synced 2026-11-10. Part of [skill-workbench](../../README.md). Unofficial, not affiliated with Anthropic.

Loads one entry from a Notion "Agent Inbox" into your current agent session, so you can continue work that was started on a phone, in another agent's session, or earlier. It lists what is waiting for you, loads the one you pick, and marks it as picked up.

Its companion is [agent-inbox-pusher](../agent-inbox-pusher/README.md), which writes entries.

## Requirements

- An agent that can load skills (a folder with a `SKILL.md`) and has the Notion MCP connector enabled. This was built and tested with Claude. Other agents that read `SKILL.md` folders may work, but that is untested.
- A Notion workspace where you can create a database.

## Setup

Do each step once.

1. In Notion, create a database named "Agent Inbox".
2. Add the properties listed in `references/inbox-database.md` (Title, Date, Type, Handover To, Status, Last Edited).
3. In the `Handover To` property, add one option per agent role you use. Add one more option for yourself.
4. Create a database view named "Active". Filter: Status is Pending or Picked Up. Sort: Date, descending.
5. Open the "Active" view, open the view's menu, and choose "Copy link to view". You should have a URL that contains `?v=`.
6. Ask your agent: "Fetch this database with the Notion tool and tell me its data source ID." You should get a string that starts with `collection://`.
7. Copy this skill folder into your agent's skills directory. The directory depends on your tool.
8. In the skill folder, copy `settings.example.md` to `settings.md` and fill in the two values: the Active view URL from step 5 and the data source ID from step 6. Do not edit the example file. To check that nothing is left empty, run `grep -n '<YOUR_' settings.md` in the skill folder. It should print nothing.
9. In each agent's own instructions, state its role name. It must match one option of `Handover To`.

## Usage

- `read inbox`: lists active entries in two groups (assigned to you, and unassigned) and asks which one to load.
- `read inbox: <title>`: loads that entry directly.
- `let's continue the <topic> discussion`: the skill looks for a matching entry.

After loading, the agent gives a five-line orientation and waits for you. It does not start working until you confirm.

## Optional: check the Inbox at the start of every session

This skill only loads content when you ask. If you want an automatic check, add something like this to each agent's own instructions:

```
## Session start: Agent Inbox check
At the start of a session, query the Active view of the Agent Inbox.
List entries where Handover To is "<this agent's role>" and where Handover To is empty.
Show Title, Date, and Status only. Do not load full content unless I ask.
```

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
