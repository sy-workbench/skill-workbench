---
name: "agent-inbox-screenshot-intake"
version: "1.2"
updated: "2026-11-11"
description: "Turn loose screenshots in a Google Drive folder into Notion Agent Inbox entries: read each image, group multi-shot captures of the same post, route it to an agent, create the entry, rename the file and move it to an _archive folder. Use when the user says \"process screenshots\" or \"process the screenshot inbox\", or when run on a schedule."
---

## Settings

Before anything else, read `settings.md` in the same folder as this file. It holds the **Inbox folder ID**, **Archive folder ID**, **Data source ID**, **Time zone**, the **Routing table**, and optionally **Filename date patterns** and **Sensitive data** rules. If it does not exist, or any value in it still has the form `<YOUR_...>`, stop and tell the user to copy `settings.example.md` to `settings.md` and fill it in (README, Setup). Do not guess values. If `settings.md` cannot be read in your environment (for example a cloud or phone run that only stores this file), use the block headed `## Settings (pasted)` at the end of this file, if the user added one.

## Overview

Reads loose screenshots from the root of one Google Drive folder, understands each image, decides which agent should handle it, creates one entry in the Notion Agent Inbox, and moves the original image into `_archive` under a readable name. Several screenshots of the same post or document become a single entry. Images the skill cannot read stay where they are.

This file is self-contained: the routing, naming and privacy rules are all below, and it needs no local files, so it can run from a phone or a scheduled cloud session.

Companion skills: `agent-inbox-loader` (reads entries) and `agent-inbox-pusher` (writes entries from a discussion). The database schema is in `references/inbox-database.md`.

## Input format

- Trigger: the user says `process screenshots` or `process the screenshot inbox`, or a scheduled run. `read inbox` belongs to `agent-inbox-loader`, not this skill.
- Source: the **root** of the Drive folder named by **Inbox folder ID** in `settings.md`.
- Archive: the `_archive` folder named by **Archive folder ID** in `settings.md`.
- Target: the Notion Agent Inbox, the data source named by **Data source ID** in `settings.md`.
- Connectors needed: Google Drive and Notion.

### Routing and filename dates

The **Routing table** in `settings.md` says which agent should receive which kind of screenshot. Rules for using it:

- If the table is empty, or you cannot tell which row fits, leave `Handover To` empty. Never guess the closest match.
- If a row names an agent that is not an option in the database's `Handover To` property, leave `Handover To` empty and mention it in the run summary.

**Filename date patterns** in `settings.md` are used in step 8. If that entry is missing, use these defaults: `Screenshot_YYYYMMDD_...`, `IMG_YYYYMMDD_...`, `YYYY-MM-DD ...`.

## Workflow

If you can write files, keep a run log at `/tmp/screenshot_intake_YYYYMMDD.log` (otherwise put the same lines in the run summary), one line per event, format `[YYYY-MM-DD HH:MM:SS] message`. Log: start, the result for each image or group, errors, and a final summary.

1. **Scan the root folder.** Use `search_files` with `parentId = '<Inbox folder ID from settings.md>'` (optionally `mimeType contains 'image/'`). Only direct children. Follow `nextPageToken` until the list is complete.
2. **Filter.** Keep image files only (`image/*`). Skip every subfolder, including `_archive` and any folder you made yourself, because a subfolder means you already filed that material. Skip non-image files.
3. **Read each image.** Start with the file metadata's `contentSnippet` (Google's free OCR text).
   - If the snippet is enough to understand the image, use it.
   - If it is empty, very short, or the image is a chart or other non-text picture, download the image with `download_file_content` and read it with vision.
   - Decide this per image. The goal is to save tokens: plain-text screenshots rarely need vision.
4. **Group multi-shot captures.** Put screenshots of the same post or document into one group. Look at several signals together: same author or account and topic, page numbers (3/13, 2/4), capture times a few minutes apart, content that continues from one image to the next. If you are not sure, do not merge. A single image is a group of one.
5. **Route.** Use the Routing table in `settings.md`. Fill `Handover To` only when you are confident.
6. **Privacy check (before writing; this rule wins over completeness of the summary).** If an image shows exact financial amounts (balances, holdings, salary), account details, policy numbers, or identity document details, write the title and body in relative terms (percentages, ranges) or "see original image". Do not copy the exact figures. Also apply any rules under **Sensitive data** in `settings.md`.
7. **Create the Notion entry.** One entry per image or per group, in the data source above:
   - `Title`: a plain description of the content in 3 to 6 words. For a group, name the whole post and leave out page numbers.
   - `Type`: `Content` only when the image is clearly source material for writing something. Everything else is `Task`. If unsure, `Task`.
   - `Handover To`: from step 5, or empty.
   - `Status`: `Pending`.
   - `Source`: the original image's view URL. For a group, the first image's URL.
   - `Date`: the day this run happened.
   - Body: Background (the original link plus a one-sentence summary) and Next Step (a suggestion). Problem and Resolution can be left out for passively collected material.
   - For a group, also: list the number of images and every image link with its page number (for example `1/13 https://...`), and summarise the whole post, not just the first image.
   - Do not mention missing pages (for example "only 5/6 received"). People often keep only the pages they care about, so gaps are usually on purpose, and noting them makes the receiving agent ask needless questions. Do not put a single image's page number in the title or summary either.
8. **Rename and move.** For each image, one `update_file` call changes the title and the parent together:
   - Title: `YYYYMMDD_topic.ext`. Find the date in this order and note which source you used:
     1. A filename date pattern from `settings.md` (or the defaults above).
     2. The file's capture time, if the connector returns one (for example in image metadata).
     3. The Drive creation time.
     Convert timestamps to the **Time zone** in `settings.md` before taking the date. If you had to use source 2 or 3, add one line to the Notion entry saying so.
   - For a group, every image is renamed `YYYYMMDD_topic_NNofMM.ext` with the post's own page numbers (zero-pad when the total has two digits). Use the first image's date for the whole group. If pages are missing, keep the original page numbers; do not renumber.
   - A single image that is clearly one page of a multi-page post may carry that page number in its filename (for example `_5of6`), but not in the entry.
   - Parent: set to the **Archive folder ID** from `settings.md`.
   - The file ID does not change when a file moves, so the view URL stays valid and the `Source` link keeps working.
9. **Notify (optional).** If you have a way to notify the user, send one short message only when some entries need a manual assignment (for example "5 entries, 2 need assigning"). Stay silent when everything was routed. If you have no notification channel, put the same line in the run summary.
10. **Finish.** Log the number of images processed, groups formed, routing counts, entries left unassigned, and images left in the folder because they could not be read.

### Edge Cases

- **Empty folder:** stop. No entries, no notification.
- **Unreadable image (vision also fails):** do not rename, move, or create an entry. Leave it in the folder so the user can look at the original. Renaming it would bury it.
- **Unreadable image inside a group:** leave that image alone, process the rest as one entry, and say in the body which page was left in the folder because it could not be read. This is different from pages the user skipped on purpose, which are not mentioned.
- **Page numbers with gaps:** treat them as a deliberate selection. Process what is there; do not note the gap or ask about it.
- **Empty or tiny `contentSnippet`:** do not wait or retry. Dark-mode and low-contrast screenshots can stay empty indefinitely. Download the image and use vision.
- **Readable but unsure who should take it:** still rename, move and create the entry, with `Handover To` empty.
- **Unsure whether images belong together:** do not merge.
- **Safe to run twice:** processed images are gone from the root, so a repeated run only sees what is new. If a run was missed, the next one picks up everything that piled up.
- **Subfolders:** never open them.

## Output files

- Notion Agent Inbox: one entry per image or group.
- Google Drive: original images renamed and moved to `_archive`.
- Log: `/tmp/screenshot_intake_YYYYMMDD.log`.
- Notification: at most one message per run.

## Reference

- Database schema, status meanings and handling principles: `references/inbox-database.md`.

## Dependencies

- Google Drive connector with `search_files`, `get_file_metadata`, `download_file_content` and `update_file`.
- Notion connector.
- An Agent Inbox database with the properties in `references/inbox-database.md`, including `Source` (URL).
- An `_archive` subfolder inside the screenshot folder.
- A filled-in `settings.md`.
