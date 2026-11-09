# Placeholders

Every value you must fill in before a skill works. Each skill stops and tells you if one is still empty.

| Placeholder | File | Line | What to put there |
|---|---|---|---|
| `<YOUR_ACTIVE_VIEW_URL>` | `workflow/agent-inbox-loader/SKILL.md` | 43 | URL of the Notion view that shows Pending and Picked Up entries, sorted by Date descending (loader README, Setup steps 4 and 5) |
| `<YOUR_AGENT_INBOX_DATA_SOURCE_ID>` | `workflow/agent-inbox-loader/SKILL.md` | 57 | Data source ID of your Agent Inbox database, in the form `collection://...` (loader README Setup step 6, pusher README Setup step 4) |
| `<YOUR_AGENT_INBOX_DATA_SOURCE_ID>` | `workflow/agent-inbox-pusher/SKILL.md` | 106 | Data source ID of your Agent Inbox database, in the form `collection://...` (loader README Setup step 6, pusher README Setup step 4) |

## Check for leftovers

Run this from the repo root. It should print nothing once you have filled everything in:

```
grep -rn '<YOUR_[A-Z_]*>' --include=SKILL.md . | grep -v '^./PLACEHOLDERS.md' | grep -v '| `<YOUR_'
```

The Setup table at the top of each `SKILL.md` lists the placeholders by name on purpose. That table can stay.
