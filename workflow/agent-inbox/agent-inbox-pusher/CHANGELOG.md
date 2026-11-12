# Changelog

## 1.3 (2026-11-12)
- Initial public release.
- Two modes. Mode A writes a four-section entry (Background / Problem / Resolution / Next Step) into a Notion Agent Inbox, after showing the draft and getting confirmation. Mode B prints a pasteable handoff prompt in the conversation and writes nothing.
- Phrases that could mean either mode (for example "handoff") make the skill ask once which mode to use instead of guessing.
- Type and Handover To must each have a stated basis. If it cannot tell the Type, it asks. If it cannot tell who should take the entry, it leaves Handover To empty.
- Your own values live in `settings.md` (copied from `settings.example.md`), so `SKILL.md` can be replaced on update. Mode B needs no settings.
- After writing, the report tells you to say `read inbox: [Title]` in the receiving session.
