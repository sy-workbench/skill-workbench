---
name: "agent-inbox-pusher"
version: "1.1"
updated: "2026-11-09"
description: "Push the current session's discussion into the Notion Agent Inbox, or print a pasteable handoff prompt for a new session. Notion mode: use when the user says \"push to inbox\", \"save to inbox\", or \"sync to inbox\". Paste mode: use when the user says \"provide a prompt\", \"handoff prompt\", or \"prompt for the new session\"; it prints a prompt in the conversation and writes nothing. Overlapping phrases such as \"handoff\", \"hand this off to [agent]\", \"new session\", \"switching devices\", \"let's talk later\": ask once which mode, do not guess."
---

## Setup (fill in once)

Replace the placeholder below with your own value (see README.md for how to find it). If a placeholder in the form `<YOUR_...>` still appears anywhere outside this table, stop and tell the user to finish Setup first. Do not guess values. Paste mode (Mode B) needs no Setup.

| Placeholder | What to put there |
|---|---|
| `<YOUR_AGENT_INBOX_DATA_SOURCE_ID>` | The database's data source ID, in the form `collection://...` |

## Overview

Captures the current session's **discussion** and writes it as one structured entry in the Notion **Agent Inbox**, the single shared handoff database for all agents. It can also print a pasteable handoff prompt instead.

Content ideas live in the same database with `Type = Content`. This skill is the only writer to the Agent Inbox. The database schema, status meanings, and roles are in `references/inbox-database.md`.

Companion skill: `agent-inbox-loader` (reads entries back).

### Two modes

- Mode A: write an entry into the Notion Agent Inbox. Use it for handoffs across agents or devices, when the content needs to be kept.
- Mode B: only print a pasteable prompt in the conversation. Use it when switching sessions. It is throwaway and writes nothing.

Steps 1 to 3 and the Edge Cases belong to Mode A. Mode B has its own workflow below.

### Scope

The Agent Inbox holds work that is still to be done: discussion summaries, topics not yet written, tasks to hand over. It does not hold finished deliverables. Every entry body uses four sections (Background / Problem / Resolution / Next Step).

## Input format

The user triggers with one of:

**Clearly Mode A (write to the Notion Agent Inbox)**

- `push to inbox` / `save to inbox` / `sync to inbox`

**Clearly Mode B (only print a pasteable prompt, write nothing)**

- `provide a prompt`
- `handoff prompt` / `prompt for the new session`

**Overlapping phrases: always ask once first**

- `handoff` / `hand this off to [agent]`
- `new session` / `switching sessions`
- `I'll continue on another device` / `let's talk about this later`

Ask: "Paste a prompt or write it to the Inbox?" Do not guess. If the user picks Mode A, put the named agent in `Handover To`. If the user picks Mode B, ignore the target agent, because the user pastes the prompt themselves.

No other input is required. Everything else comes from the session.

## Workflow: Mode A (write to Notion)

### Step 1: Summarize the session

Extract:

- **Title**: a topic name of 3 to 6 words, not a sentence. Example: "Broker connector evaluation"
- **Date**: today, YYYY-MM-DD
- **Background**: why this discussion started
- **Problem**: the core question and its constraints
- **Resolution**: what is already decided. Leave it empty if nothing has converged. Do not force it
- **Next Step**: what to do next

Before writing, run the sensitive data check below.

**Sensitive data rule (edit to fit your own needs):** if the summary contains asset amounts, holdings, salaries, or account or identity document details, rewrite them as relative terms (percentages, ranges) or "see local file". This rule wins over completeness of the summary.

### Step 2: Determine Type and Handover To (verification)

Both fields need a clear basis. Do not leave either empty to avoid deciding. An empty `Handover To` has its own meaning in the schema (not yet assigned), and using it for "I could not tell" would mix the two.

Decide each field separately:

| Situation | What to do |
|---|---|
| The user said it ("this is a content idea", "hand it to the writer") | Write it directly |
| The user did not say it, but the discussion points to exactly one answer | Write it, and state the basis when you report, so the user can overrule it at a glance |
| You cannot tell, or two or more answers are equally reasonable | Stop and ask. Do not guess and do not leave it empty |

Values:

- `Type`: `Task` (has a concrete action) or `Content` (a topic that could become an article, not started)
- `Handover To`: the role names defined in your setup. See "Roles" in `references/inbox-database.md`. Use the human's own option only for work nobody else can do (real orders, manual configuration, contacting people).

### Step 3: Write to Notion

Show the user what you are about to write, and write only after they confirm:

```
About to save to the Agent Inbox:
Title: [title]
Type: [Task / Content] (basis: ...)
Handover To: [role] (basis: ...)
[four-section summary]
```

After confirmation, create the page with `notion-create-pages`:

- Data source: `<YOUR_AGENT_INBOX_DATA_SOURCE_ID>`
- Properties: Title / Date / Type / Handover To / Status = `Pending`
- Page content:

```
## Background
[content]

## Problem
[content]

## Resolution
[content]

## Next Step
[content]
```

Then report:

```
Saved to the Agent Inbox: [Title] (Type: [x], Handover To: [y])
In [y]'s session, say "read inbox: [Title]" to pick it up.
```

### Edge Cases

- **The content is a finished deliverable**: do not use this skill. Tell the user the Inbox is for work still to be done.
- **The discussion has not converged**: leave Resolution empty, but write Next Step clearly: what comes next and where it is stuck.
- **One session covered several topics**: ask which one to push, or propose several entries. Do not put unrelated topics into one entry.
- **Updating an existing entry instead of adding one**: check for an entry on the same topic first. If there is one, update it with `notion-update-page`. Do not create a duplicate.
- **Handing over to another agent**: change `Handover To` and set `Status` back to `Pending`. A handover is an event, not a state. If the entry stays at `Picked Up`, nobody can tell who holds the ball.
- **The content does not match what the user said** (for example they said content idea, but it is really a to-do): decide `Type` from the content, and say in your report that you changed it so the user can overrule you.
- **Handover To cannot be inferred at all**: ask. Offer two or three candidates with reasons. Do not default to the human.

## Workflow: Mode B (pasteable prompt)

Writes nothing to Notion, saves no file, and needs no confirmation first. The prompt is printed in the conversation, and the user copies it into a new session.

### Step B1: Organize

Take from the current session:

- Topic (3 to 6 words) and date
- Background: why this work exists
- Decided (with reasons)
- Still under discussion (current leaning, where it is stuck)
- Key numbers and facts
- To-dos in priority order
- Relevant files: list only paths you are sure exist. Never write a path from impression
- First step: what the new session should do first

Anything you are unsure was decided goes under "still under discussion", not "decided". Omit a field entirely if it has no content. Leave out detours and failed attempts.

### Step B2: Sensitive data check

Same check as Step 1: rewrite asset amounts, holdings, salaries, and account or identity document details as relative terms or "see local file".

### Step B3: Output

Print one code block. Use the language of the current session:

```
[Handoff prompt] Topic / Date
Read this first and tell me your understanding. Start work only after I confirm.
Background:
Decided (with reasons):
Still under discussion (current leaning, where it is stuck):
Key numbers and facts:
To-dos (in priority order):
Relevant files:
First step:
```

After the code block add only one line: "Paste this into the new session. Nothing was saved anywhere."

### Mode B Edge Cases

- **Overlapping phrase**: handle as described under "Overlapping phrases" above. Ask once first.
- **The user chose switching devices or "later", and still wants a prompt**: remind them in one line that a pasted prompt does not travel between devices, then do what they chose.
- **The user later wants it in the Inbox**: reuse the same organized result and go through Mode A. Do not ask again.
- **The content is long**: keep decisions, to-dos, and the first step, and shrink the rest to one line each. Do not paste the whole discussion.

## Output files

Mode A: the entry is written into Notion, no local file. Mode B: no output file; the prompt exists only in the conversation.

## Reference

- Database schema, status meanings, handling principles, roles: `references/inbox-database.md`
- `Last Edited` is Notion's built-in last edited time and updates by itself. Never write it.
- Handover history is not recorded. If you ever need it, Notion's page history is still there.
- Companion skill: `agent-inbox-loader`

## Dependencies

- Notion MCP tools: `notion-create-pages`, `notion-update-page`, `notion-query-data-sources` (needed by Mode A only; Mode B needs no tools). Tool names may differ between Notion MCP versions.
