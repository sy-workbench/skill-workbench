---
name: "agent-inbox-loader"
version: "1.2"
updated: "2026-11-12"
description: "Load a Notion Agent Inbox entry's full content into the current session. Use when the user says \"read inbox\" or \"read notion inbox\", or names a specific inbox entry they want to pick up. Also trigger when the user says something like \"let's continue the [topic] discussion\" and the context likely lives in the Agent Inbox. If no title is given, list entries assigned to this agent plus unassigned ones and ask which one; if exactly one is assigned to this agent, load it directly."
---

## Settings

Before anything else, read `settings.md` in the same folder as this file. It holds the **Active view URL** and the **Data source ID**. If it does not exist, or any value in it still has the form `<YOUR_...>`, stop. Tell the user which values are missing, and that they go in `settings.md` (a copy of `settings.example.md`, which says what each value is). Do not guess values. If `settings.md` cannot be read in your environment (for example a cloud or phone run that only stores this file), use the block headed `## Settings (pasted)` at the end of this file, if the user added one.

Each agent also needs a role name that matches one option of the `Handover To` property. Define it in that agent's own instructions, not in this file or in settings.

## Overview

Reads a single entry from the Notion **Agent Inbox** and loads its full content into the current session, so you can continue work that was started elsewhere (a phone chat, another agent's session, or an earlier session of your own).

The Agent Inbox is one shared handoff database for all agents. Content ideas live in the same database with `Type = Content`. The database schema and the handling principles are in `references/inbox-database.md`.

Listing candidates and showing summaries are read-only. Loading the full content of an entry assigned to you sets `Status = Picked Up` (see Step 3).

Companion skill: `agent-inbox-pusher` (writes entries).

## Input format

The user triggers with one of:

- A phrase only: `read inbox` / `read notion inbox`
- A phrase plus a title: `read inbox: Weekly planning rework`
- An implicit reference: `let's continue the connector discussion`

No other input is required.

## Workflow

### Step 1: Resolve the entry

Active view URL: the **Active view URL** in `settings.md`

This view (Status is Pending or Picked Up, sorted by Date descending) is the single source for "what is active". Query it in **view mode**:

`notion-query-data-sources` with `{"mode":"view","view_url":"<Active view URL>","page_size":100}`. If `has_more` is true, pass `next_cursor` as `start_cursor`.

Why view mode and not SQL: SQL and rows mode may share a workspace-wide query quota, and it can run out when several agents process the Inbox at the same time. View mode did not count against it in our setup. Do not switch routine listing back to SQL.

The view returns every agent's active entries, so filter client-side by `Handover To`. Entries with an empty Date still appear.

**If a title (or partial title) is given**, look for it in the view result first (substring match on Title). A single match goes to Step 2. Multiple matches: list them and ask. Zero matches: the entry may already be closed, so fall back to one SQL query:

```sql
SELECT url, Title, Type, "Handover To", Status, "date:Date:start" AS d
FROM "<Data source ID from settings.md>"
WHERE Title LIKE '%<keyword>%';
```

Zero matches there: fall through to the listing below, but always list and ask. Do not apply the "exactly one entry: load it directly" rule, because the user named a different entry. Multiple matches there: list them with Date and Status, and ask which one.

**If no title is given**, split the view result into two groups:

1. Mine: `Handover To` equals your own role name (Pending or Picked Up, i.e. waiting for you to handle)
2. Unassigned: `Handover To` is empty and Status = Pending

Then:

- Mine has exactly one entry: load it directly (go to Step 2, which sets Picked Up). Do not ask first. In the same reply, list Unassigned with Title / Date / Status, if there are any.
- Mine has two or more: list both groups with Title / Date / Status only, newest first, and ask which one to handle first.
- Mine is empty: list Unassigned (if any) and ask. Loading an unassigned entry does not claim it (see Step 3).

Do not expand any page content when listing. Do not silently truncate the list. If a group is long, report the count rather than dropping the oldest entries.

SQL alias rule (applies to any SQL that selects the date column): write `"date:Date:start" AS d`. Without an alias, rows whose Date is empty can be silently dropped from the result.

### Step 2: Load the entry

Use `notion-fetch` on the page URL. Read the whole page body into context, then give the user a short orientation (roughly 5 lines), not a full reproduction:

- What this entry is and where it got stuck
- What is already decided
- What is left in Next Step
- Whether the content may be out of date (compare Date with Last Edited)

Then ask what to do next. Do not start executing the Next Step without confirmation.

### Step 3: Status handling

- Listing candidates or showing summaries: do not change `Status`.
- Loading the full content of an entry whose `Handover To` is you: set `Status = Picked Up` right away, whether or not you go on to act on it.
- `Handover To` empty: do not claim it on your own initiative. Assignment is the human's call. Only when the human explicitly asks you to handle it, set `Handover To` to your own role name and `Status = Picked Up` in the same update.
- Entry assigned to another agent: do not claim or change it.
- When the action is finished, close the entry following the handling principles in `references/inbox-database.md`: set Done / Dropped / Deferred and write Resolution in the same update.

### Edge Cases

- **Title matches nothing**: do not guess. Fall back to the no-title listing above. List and ask even if exactly one entry is assigned to you; do not load it directly.
- **Multiple matches**: list them with Date and Status, ask which one.
- **Entry is already Done / Dropped / Deferred**: load it, but say so up front. The user may be looking at a stale reference.
- **Entry contradicts the current project state**: flag the conflict rather than silently following the entry. Inbox content is a snapshot from when it was written.
- **Financial or personal figures in the page**: they were redacted at write time (see "Sensitive data" in `references/inbox-database.md`). Do not try to reconstruct them; ask the user to point at the local file if the numbers matter.
- **Both groups empty**: say so in one line and move on.
- **You cannot find your own role name** in your instructions: ask the user which `Handover To` option is yours. Do not guess, and do not list or load anything until you know.

## Output files

None. This skill only loads context into the session.

## Reference

- Database schema, status meanings, handling principles, roles: `references/inbox-database.md`
- `Last Edited` is Notion's built-in last edited time. Use it to judge how long an entry has been sitting.
- An automatic check at the start of a session is not part of this skill. If you want one, put it in each agent's own instructions (README.md has an example). This skill loads full content only when the user asks.
- Companion skill: `agent-inbox-pusher`

## Dependencies

- Notion MCP tools: `notion-query-data-sources`, `notion-fetch`, `notion-update-page` (set Picked Up when you read an entry assigned to you, and set the final status with Resolution when you close it). Tool names may differ between Notion MCP versions.
