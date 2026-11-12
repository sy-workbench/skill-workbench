# agent-inbox-loader

Version 1.2. Last updated 2026-11-12. Part of [agent-inbox](../README.md).

Loads an entry from your Notion Agent Inbox into the current agent session, so you can continue work that was started somewhere else. What it does, which phrases to say, the requirements, setup, upgrading, and running in the cloud or on a phone are all in the [agent-inbox README](../README.md).

## Also good to know

- `read inbox: <title>` loads the entry with that title directly.
- Something like `let's continue the <topic> discussion` also works. The skill looks for a matching entry.
- After loading, the agent gives a short summary and waits. It does not start working until you confirm.

## Optional: check the Inbox automatically

This skill only loads content when you ask. If you want an automatic check, there are two ways.

**At the start of every session.** Add something like this to each agent's own instructions:

```
## Session start: Agent Inbox check
At the start of a session, query the Active view of the Agent Inbox.
List entries where Handover To is "<this agent's role>" and where Handover To is empty.
Show Title, Date, and Status only. Do not load full content unless I ask.
```

**On a schedule.** Set up a scheduled task to run the check at set times.

## License

MIT, see the [LICENSE](../../../LICENSE) at the repo root.
