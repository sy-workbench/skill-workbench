# Changelog

## 1.2 (2026-11-11)
- Initial public release.
- Reads loose screenshots from the root of a Google Drive folder, understands each one (Google's OCR text first, vision only when needed), and creates one Notion Agent Inbox entry per image.
- Groups screenshots of the same post or document into a single entry, with page numbers.
- Routes each entry with a routing table you edit. Leaves `Handover To` empty when it is not sure.
- Renames the original to `YYYYMMDD_topic.ext` and moves it to an `_archive` folder. Unreadable images stay where they are.
- Finds the screenshot date from the filename, then the Drive creation time, and notes in the entry when it had to fall back.
- Your own values, the routing table, date patterns and extra sensitive-data rules live in `settings.md` (copied from `settings.example.md`), so `SKILL.md` can be replaced on update.
- Triggered by `process screenshots` or `process the screenshot inbox`. `read inbox` is left to agent-inbox-loader, so the two never overlap.
- Missing pages in a multi-shot post are treated as a deliberate selection and not mentioned. Only pages left behind because they could not be read are noted.
