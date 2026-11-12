# agent-inbox-screenshot-intake

Version 1.2. Last updated 2026-11-11. An add-on to [agent-inbox](../README.md).

You often see something on your phone that you want to deal with later, take a screenshot, and then forget about it. This skill handles those screenshots. It reads the loose screenshots in a Google Drive folder, works out what each one is about, creates an entry in your Notion Agent Inbox, assigns it to the agent that should handle it, then renames the original image to an easy-to-read name and moves it into `_archive`. If several screenshots belong to the same post, they become one entry.

These entries go into the same database as the core skills. To read and handle them, use [agent-inbox-loader](../agent-inbox-loader/README.md).

## Requirements

- The skill installed, and two connectors set up: the Notion MCP and the Google Drive MCP.
- The Agent Inbox database described in the [agent-inbox README](../README.md#setup), with one extra property: `Source`, type URL. This skill writes the link to the original image there.
- A Google Drive folder for the screenshots, with a subfolder named `_archive` inside it. Processed images are moved there, so the main folder stays clear and you can always find an original again.

## Setup

Copy this skill folder into your agent's skills directory (the directory depends on your tool). Then, in the skill folder, copy `settings.example.md` to `settings.md` and fill in the items below. Do not edit the example file directly.

Required:

- The ID of your screenshot folder, and the ID of its `_archive` subfolder. In Google Drive, open each folder and look at the address bar: the ID is the text after `/folders/`.
- The data source ID of your Agent Inbox database. It is the same one you use for the core skills.
- Your time zone.

Routing table: which agent gets which kind of screenshot. Replace the example rows with your own agents. The names must match options of the `Handover To` property. Leave the table empty if you do not want routing.

Optional:

- Filename date patterns, if your phone names screenshots differently from the examples in the file.
- Your own rules under Sensitive data, for what must not be copied into Notion.

## Usage

Say `process screenshots` or `process the screenshot inbox`. The skill handles every image at the top level of the folder, then reports what it did.

To test it, drop one harmless screenshot in the folder and run it. You should see a new entry in Notion, and the image should now be in `_archive` with a new name.

To run it on a schedule, set up a scheduled task.

## Good to know

- Screenshots can contain private information. Before writing to Notion, the skill rewrites exact financial amounts, account details and identity document details into relative terms. Add your own rules under Sensitive data in `settings.md` to match what you consider sensitive.
- Images it cannot read stay in the folder, so you can look at them yourself.
- The date in the new filename comes from the original filename. If there is none, the Drive creation time is used.
- Running it twice is safe, because processed images have already left the folder.

## Upgrading, and running in the cloud or on a phone

These work the same as for the core skills. See [Upgrading to a new version](../README.md#upgrading-to-a-new-version) and [Running in the cloud or on a phone](../README.md#running-in-the-cloud-or-on-a-phone) in the agent-inbox README.

## License

MIT, see the [LICENSE](../../../LICENSE) at the repo root.
