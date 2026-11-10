# Settings for agent-inbox-screenshot-intake

How to use this file: copy it, rename the copy to `settings.md` (same folder), and fill in the copy. Do not edit this example, so that updating the skill can replace it safely. To find each value, see the README, section "Setup". If your environment cannot read extra files, see the README, section "Running in the cloud or on a phone".

## Required

Inbox folder ID: <YOUR_INBOX_FOLDER_ID>
Archive folder ID: <YOUR_ARCHIVE_FOLDER_ID>
Data source ID: <YOUR_AGENT_INBOX_DATA_SOURCE_ID>
Time zone: <YOUR_TIMEZONE>

## Routing table

Which agent gets which kind of screenshot. The rows below are examples only. Replace them with your own agents. The first column must match an option of the `Handover To` property. Leave the table empty if you do not want routing; every entry will then have an empty `Handover To`.

| Handover To | Takes screenshots about |
|---|---|
| Research Assistant | Tech news, papers, product reviews |
| Trip Assistant | Travel articles, flight deals, places to visit |
| Me | Things only I can act on, such as orders and bills |

## Filename date patterns (optional)

Tried in order; the first match gives the screenshot date. Delete this section to use the defaults.

| Pattern | Example filename | Date |
|---|---|---|
| `Screenshot_YYYYMMDD_...` | `Screenshot_20260908_141500.png` | 2026-09-08 |
| `IMG_YYYYMMDD_...` | `IMG_20260908_141500.jpg` | 2026-09-08 |
| `YYYY-MM-DD ...` | `2026-09-08 at 14.15.00.png` | 2026-09-08 |

## Sensitive data (optional)

Extra rules for what must not be copied into Notion. The skill already rewrites exact financial amounts, account details, policy numbers and identity document details into relative terms. Add your own, one per line. Delete this section if you have none.

- 
