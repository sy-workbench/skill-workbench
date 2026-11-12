# Agent Inbox database reference

This file describes the Notion database that `agent-inbox-loader`, `agent-inbox-pusher` and `agent-inbox-screenshot-intake` read and write. Each skill ships an identical copy so each one works on its own.

## What the Agent Inbox is

One shared Notion database where agents and the human leave work for each other: a discussion summary, an unfinished task, a topic worth writing about later. It is a notification channel, not a workspace. Follow-up work happens in the relevant agent session, not in the entry.

## Properties

| Property | Type | Values |
|---|---|---|
| Title | Title | A topic name of 3 to 6 words, not a sentence |
| Date | Date | The day the entry was written (YYYY-MM-DD) |
| Type | Select | `Task` (has a concrete action) or `Content` (a topic that could become an article, not started) |
| Handover To | Select | One option per agent role in your setup. Empty means unassigned |
| Status | Status | `Pending`, `Picked Up`, `Done`, `Dropped`, `Deferred` |
| Source | URL | Optional. A link to the original material. Only `agent-inbox-screenshot-intake` writes it (the original image's link) |
| Last Edited | Last edited time | Built in. The skills never write it |

Status groups: To-do = Pending. In progress = Picked Up. Complete = Done, Dropped, Deferred.

## Entry body

Every entry has the same four sections. Entries that `agent-inbox-screenshot-intake` creates from screenshots may leave out Problem and Resolution:

```
## Background
Why this started.

## Problem
The core question and its constraints.

## Resolution
What is already decided. Leave empty if nothing is settled. Do not force it.

## Next Step
What happens next, and where it is stuck.
```

## Status meaning

- Pending: the responsible agent has not read it yet (this includes unassigned entries).
- Picked Up: the responsible agent has read it. Set this as soon as you load an entry assigned to you, whatever you do next.
- Done / Dropped / Deferred: the action named in the entry is finished, or follow-up continues in another session, or the idea was dropped, or it was shelved on purpose (Deferred).
- Pending and Picked Up both show up every time someone says "read inbox".

## Handling principles (the floor for every agent)

- Reading an entry assigned to you means setting Picked Up right away, even if you do not act on it.
- When the action is finished, set the final status and write Resolution in the same update. Resolution is one line: where the result went, or what is blocking it. Do not put sensitive details in it.
- Postponing: keep Picked Up and write "Later: when and what" in Resolution. Needing the human's decision: write "Waiting on human: what the question is" and ask in the same turn.
- If no workflow defines "the action", agree one with the human. If there is none, fall back to this: merge the content into an existing file, then close the entry.
- Prefer merging into existing files. Ask before creating a new file.
- Project-specific procedures belong in each agent's own instructions or skills. This list is only the shared floor.

## Roles

`Handover To` holds one role per agent. Use the names your agents already have, and keep the list of roles and what each one owns in one place that all agents share (for example a shared instructions file). The skills deliberately keep no copy of that list, so renaming a role means editing one place.

Suggested conventions:

- Keep one option for the human (for example `Me`) for work only the human can do: placing real orders, manual configuration, contacting other people.
- Assigning is the human's call. If you cannot tell who should take an entry, leave `Handover To` empty. Do not guess the closest match.
- An empty `Handover To` means "not yet assigned". `agent-inbox-loader` lists unassigned entries, so the human can assign them when reading the Inbox.

## Edge cases

- Unsure who should take it: leave it empty and let the human assign it.
- A topic spans two agents: write two entries, each with its own `Handover To`. Do not write one entry and make the receiver split it.
- Nobody picks an entry up: it stays `Pending`. A periodic review (by you or a designated agent) should surface it. The agent that wrote it does not chase.
- A discussion has not converged: it can still be written. Leave Resolution empty, and write Next Step clearly: what comes next and where it is stuck.

## Sensitive data

Entries live in Notion, outside your local machine. Before writing, rewrite sensitive details into relative terms (percentages, ranges) or "see local file": asset amounts, holdings, salaries, account or identity document details. This rule wins over completeness of the summary. To add your own rules, use the Sensitive data section of each skill's `settings.md`, not this file: an update replaces this file.
