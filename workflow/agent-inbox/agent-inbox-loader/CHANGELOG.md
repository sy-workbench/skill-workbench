# Changelog

## 1.2 (2026-11-11)
- Initial public release.
- Reads one entry from a Notion Agent Inbox into the session, lists active entries in two groups (mine and unassigned), and sets Status to Picked Up when you load an entry assigned to you.
- Uses a Notion view to list active entries, so routine listing does not depend on SQL queries.
- Your own values live in `settings.md` (copied from `settings.example.md`), so `SKILL.md` can be replaced on update.
- Triggered by `read inbox` or `read notion inbox`.
- With no title, if exactly one entry is assigned to you, it is loaded directly; unassigned entries are still listed.
