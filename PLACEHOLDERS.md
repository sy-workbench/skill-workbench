# Settings you fill in

Every value you must fill in before a skill works. Each skill keeps them in its own `settings.example.md`. Copy that file to `settings.md` in the same folder and fill in the copy; the skill reads `settings.md` and stops if a value is still missing. `SKILL.md` contains no values of yours, so an update can replace it.

| Placeholder | File (copy it to `settings.md`) | Line | What to put there |
|---|---|---|---|
| `<YOUR_ACTIVE_VIEW_URL>` | `workflow/agent-inbox-loader/settings.example.md` | 5 | URL of the Notion view that shows Pending and Picked Up entries, sorted by Date descending (loader README, Setup steps 4 and 5) |
| `<YOUR_AGENT_INBOX_DATA_SOURCE_ID>` | `workflow/agent-inbox-loader/settings.example.md` | 6 | Data source ID of your Agent Inbox database, in the form `collection://...` (loader README, Setup step 6) |
| `<YOUR_AGENT_INBOX_DATA_SOURCE_ID>` | `workflow/agent-inbox-pusher/settings.example.md` | 5 | Same data source ID, in the form `collection://...` (pusher README, Setup step 4) |
| `<YOUR_INBOX_FOLDER_ID>` | `workflow/agent-inbox-screenshot-intake/settings.example.md` | 7 | ID of the Google Drive folder where you drop screenshots (intake README, Setup steps 3 and 5) |
| `<YOUR_ARCHIVE_FOLDER_ID>` | `workflow/agent-inbox-screenshot-intake/settings.example.md` | 8 | ID of the `_archive` subfolder inside it (intake README, Setup steps 4 and 5) |
| `<YOUR_AGENT_INBOX_DATA_SOURCE_ID>` | `workflow/agent-inbox-screenshot-intake/settings.example.md` | 9 | Same data source ID, in the form `collection://...` (intake README, Setup step 6) |
| `<YOUR_TIMEZONE>` | `workflow/agent-inbox-screenshot-intake/settings.example.md` | 10 | Your IANA time zone, for example `Europe/London` |

Some `settings.example.md` files also have sections without placeholders: the intake skill's routing table and filename date patterns, and an optional Sensitive data section in the pusher and intake skills. Edit them to fit your setup. The routing table rows are examples only.

## Check for leftovers

Run this from the repo root after filling in. It should print nothing:

```
grep -rn '<YOUR_[A-Z_]*>' --include=settings.md .
```
