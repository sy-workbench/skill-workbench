# agent-inbox-screenshot-intake

Version 1.1. Last synced 2026-11-10. Part of [skill-workbench](../../README.md). Unofficial, not affiliated with Anthropic.

You see something worth keeping on your phone, take a screenshot, and forget about it. This skill empties that pile. It reads each loose screenshot in one Google Drive folder, works out what it is, creates an entry in your Notion Agent Inbox, routes it to the agent that should deal with it, and moves the original into an `_archive` folder under a readable name. Screenshots of the same post taken as several shots become one entry.

It works with [agent-inbox-loader](../agent-inbox-loader/README.md) and [agent-inbox-pusher](../agent-inbox-pusher/README.md), which share the same Notion database.

## Requirements

- An agent that can load skills (a folder with a `SKILL.md`) and has the Google Drive and Notion MCP connectors enabled. Built and tested with Claude. Other agents that read `SKILL.md` folders may work, but that is untested.
- A Notion workspace where you can create a database.
- A Google Drive folder that you drop screenshots into.

## Setup

Do each step once.

1. Create the Agent Inbox database. Follow steps 1 to 3 of the [loader README](../agent-inbox-loader/README.md#setup). If you already did this, skip it.
2. Add one more property to that database: `Source`, type URL. This skill writes the original image's link there.
3. In Google Drive, create a folder for your screenshots, for example "Screenshot Inbox".
4. Inside it, create a subfolder named `_archive`. Processed images are moved here, so the main folder does not fill up and you can always find an original again.
5. Get both folder IDs. Open each folder in Drive and look at the address bar: the ID is the text after `/folders/`.
6. Ask your agent: "Fetch this database with the Notion tool and tell me its data source ID." You should get a string that starts with `collection://`.
7. Copy this skill folder into your agent's skills directory. The directory depends on your tool.
8. In the skill folder, copy `settings.example.md` to `settings.md` and fill in the required values: the two folder IDs from step 5, the data source ID from step 6, and your time zone. Do not edit the example file. To check that nothing is left empty, run `grep -n '<YOUR_' settings.md` in the skill folder. It should print nothing.
9. In `settings.md`, edit the routing table so it names your own agents. The names must match options of the `Handover To` property. Edit the filename date patterns if your phone names screenshots differently, and add your own rules under Sensitive data if you have any.
10. Test with one harmless screenshot: drop it in the folder and ask "process the screenshot inbox". You should see a new Notion entry, and the image should now be in `_archive` with a new name.

## Usage

- Ask your agent to process the screenshot inbox. It handles everything in the folder's root and then reports what it did.
- To run it on a schedule, set up a scheduled task in your agent tool that sends the same request. Scheduled runs only work if your tool lets the Drive and Notion connectors run unattended, and they usually cannot read `settings.md`, so see "Running in the cloud or on a phone" below.

## Good to know

- Screenshots can contain private information. The skill rewrites exact financial amounts, account details and identity document details into relative terms before it writes to Notion, but add your own rules under Sensitive data in `settings.md` to match what you consider sensitive.
- Images it cannot read stay in the folder so you can look at them yourself.
- The date comes from the filename first. If your connector also returns a capture time it is used next, then the Drive creation time. Whether your connector returns a capture time has not been verified.
- Running it twice is safe. Processed images have already left the folder.

## Updating

Copy the new files over your existing skill folder. Do not delete the folder first, or your `settings.md` goes with it. `SKILL.md` and `settings.example.md` are safe to overwrite. If a new version needs a new setting, `CHANGELOG.md` says so, and the skill stops and names the missing one.

## Running in the cloud or on a phone

Some environments (scheduled cloud runs, phone apps) store only `SKILL.md` and cannot read `settings.md`. There, paste the contents of your filled-in `settings.md` at the end of `SKILL.md` under the heading `## Settings (pasted)`. The skill uses that block when it cannot read the file. An update replaces `SKILL.md`, so paste again after updating.

## Files

| File | Purpose |
|---|---|
| `settings.example.md` | The values you fill in. Copy it to `settings.md` |
| `SKILL.md` | The skill itself, including the routing table |
| `references/inbox-database.md` | Database schema, status meanings, handling principles, roles |
| `CHANGELOG.md` | Version history |
| `README.zh-TW.md` | Traditional Chinese README |

## License

MIT, see the [LICENSE](../../LICENSE) at the repo root.
