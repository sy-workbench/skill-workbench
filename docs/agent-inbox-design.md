# Design notes: the Agent Inbox

These notes explain why the three Agent Inbox skills (loader, pusher, screenshot-intake) are built the way they are. You do not need them to run the skills.

## The problem

When several agents (or several chat windows) each hold part of your context, work gets stuck at the edges: an idea from your phone never reaches the agent that could act on it, and a long discussion is lost when you start a new session.

## The idea

One shared Notion database acts as a mailbox. A writer skill leaves a short structured note. A reader skill picks it up in another session. The mailbox only announces that material exists. The follow-up work happens in the proper session.

```
 session A                      Notion Agent Inbox                 session B
 ---------                      ------------------                 ---------
 discussion --pusher (Mode A)--> entry: Pending  --loader-->  entry: Picked Up
                                                                      |
                                                              work happens here
                                                                      |
                                                 entry: Done / Dropped / Deferred
                                                 (Resolution written in the same update)

 discussion --pusher (Mode B)--> pasteable prompt in the chat (nothing is saved)

 screenshots in Drive --screenshot-intake--> entry: Pending  (original image moved to _archive)
```

## Decisions worth knowing

- **Four fixed sections.** Every entry has Background, Problem, Resolution, Next Step. A fixed shape makes entries quick to read and easy to compare. Resolution stays empty until something is really decided.
- **A view for listing, not SQL.** Listing active entries reads a saved Notion view. Query modes that run SQL can share a workspace-wide quota, which can run out when several agents work at once. A view avoids that. SQL is kept only as a fallback for looking up closed entries.
- **Pick up on read.** Loading an entry assigned to you sets it to Picked Up immediately, even if you do not act on it. That way the entry's status always says whether someone has seen it.
- **Assignment is the human's call.** An empty `Handover To` means "not assigned yet". Agents do not claim unassigned entries on their own.
- **Two modes in the writer.** Saving to Notion is heavy for a quick session switch. Mode B prints a prompt instead and keeps nothing. When a phrase could mean either, the skill asks once.
- **Redact before writing.** Entries live outside your machine, so sensitive figures are rewritten as relative terms or "see local file" before they are written.
- **Screenshots become entries, originals are archived.** The intake skill turns loose screenshots into entries and moves each original to `_archive` under a readable name, so the drop folder stays empty and an original can always be found again. Several shots of one post become one entry. Images it cannot read stay in place.
- **Your values live in `settings.md`.** Each skill ships `settings.example.md`. You copy it to `settings.md` and fill it in, and `SKILL.md` holds none of your values. An update can then replace `SKILL.md` without touching your settings. Environments that keep only `SKILL.md` get a pasted settings block instead.
