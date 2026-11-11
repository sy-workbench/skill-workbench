# agent-inbox

agent-inbox-pusher and agent-inbox-loader are a set of tools that work together. Their purpose is to let you quickly hand work over from one agent or session to another. The handover goes through a database called Agent Inbox, which you create in Notion: agent-inbox-pusher saves a discussion into it in a fixed format, and agent-inbox-loader reads the handover back.

agent-inbox-pusher has another way to work, called Mode B. It skips Notion and prints a prompt that you can quickly copy and paste into a new session, to continue the discussion or carry out the work. Mode B needs no database and no agent-inbox-loader.

To use the Notion way, you need to prepare the database and a few settings first. They are listed under "Setup" below. If you only want Mode B, install agent-inbox-pusher and you are done. It needs no settings.

## Skills in this set

| Skill | What it does |
|---|---|
| [agent-inbox-pusher](agent-inbox-pusher/README.md) | Saves the current discussion as an entry in the Agent Inbox, or prints a handoff prompt that you paste into a new session |
| [agent-inbox-loader](agent-inbox-loader/README.md) | Lists the entries in the Agent Inbox waiting for this agent, loads one (right away if only one is assigned to it), and marks it as picked up |

## How they work together

1. In the old session, tell the agent `push to inbox`. It saves the discussion as an entry and records which agent it is for.
2. In the new session, or in another agent, say `read inbox`. The agent looks at two kinds of entries: the ones assigned to it, and the ones nobody has been assigned yet.
3. If exactly one entry is assigned to it, the agent loads that entry right away, marks it as picked up, and gives you a short summary. If there are several, it lists them and asks which to handle first.
4. Unassigned entries are listed too, but the agent does not take them on its own. It claims one only when you ask.
5. After loading, the agent waits for your go-ahead before it starts working.

Trigger phrases:

| To do this | Say | Skill |
|---|---|---|
| Save the discussion to Notion | `push to inbox` / `save to inbox` / `sync to inbox` | agent-inbox-pusher |
| Get a prompt to paste into a new session (Mode B) | `provide a prompt` / `handoff prompt` / `prompt for the new session` | agent-inbox-pusher |
| Read what is waiting for this agent | `read inbox` / `read notion inbox` | agent-inbox-loader |

Vague phrases such as `handoff`, `new session` or `let's talk about this later` fit both modes, so the pusher asks once: paste a prompt, or write it to the Inbox.

## Requirements

- The skills installed (each one is a folder with a `SKILL.md`), and the Notion MCP connector set up, which lets the agent read and write Notion.
- A Notion workspace where you can create a database.

## Setup

**Only want Mode B?** Copy the `agent-inbox-pusher` folder into your agent's skills directory. The directory depends on your tool. After that, say `provide a prompt` in any session. It needs no Notion and no settings.

**Want to use Notion?** Copy the skill folders you want into your agent's skills directory (the directory depends on your tool), then prepare the items below. You can prepare them any way you like, including asking your agent to do it.

Both skills need:

- A Notion database named "Agent Inbox", with the properties listed in [`inbox-database.md`](agent-inbox-pusher/references/inbox-database.md).
- In the `Handover To` property, one option for each agent role you use (for example `Writer` or `Researcher`). You can also add one for yourself, depending on how you work.
- The database's data source ID, a string that starts with `collection://`.

Only agent-inbox-loader needs:

- A database view named "Active", filtered to Status is Pending or Picked Up, and sorted by Date with the newest first.
- That view's URL, which contains `?v=`.

Every agent needs:

- Its role name in its own instructions, for example "Your Agent Inbox role name is Writer". The name must match one `Handover To` option exactly.

Last, in each skill folder, copy `settings.example.md` to `settings.md` and fill in the values above. Do not edit the example file directly.

## Add-ons

These are optional skills that work with the core ones (there is only one for now). They write entries to the same Agent Inbox database as the core skills, so an agent can use the loader to read and handle what they add.

| Add-on | What it adds | What else it needs |
|---|---|---|
| [agent-inbox-screenshot-intake](agent-inbox-screenshot-intake/README.md) | Turns the screenshots you drop into a Google Drive folder into Agent Inbox entries, and routes each one to the agent that should handle it | Google Drive, and one extra `Source` property in the database |

## Upgrading to a new version

Replacing the skill folder can erase your `settings.md`. Copy it to another place before you upgrade, and move it back afterwards.

If a new version needs a new setting, `CHANGELOG.md` says so. The skill also stops and tells you which setting is missing.

## Running in the cloud or on a phone

Some environments, such as scheduled cloud runs and phone apps, keep only `SKILL.md` and cannot read `settings.md`. In that case, paste the contents of your filled-in `settings.md` at the end of `SKILL.md`, under the heading `## Settings (pasted)`. Do this for each skill. The skill reads that block when it cannot find the file.

Upgrading replaces `SKILL.md`, so paste the settings again after each upgrade.

## License

MIT, see the [LICENSE](../../LICENSE) at the repo root.
