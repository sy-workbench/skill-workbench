# Design notes: one skill folder, two agents

[English](claude-codex-skill-sync.md) | [繁體中文](claude-codex-skill-sync.zh-TW.md) | [简体中文](claude-codex-skill-sync.zh-CN.md)

These notes describe how I keep the same skills working in two agents, Claude Cowork and Codex, without maintaining two copies by hand. Nothing here is needed to use the skills in this repo. It is the setup I wish I had started with.

Last updated 2026-11-26.

## The problem

I use Cowork for most discussions and Codex for some coding work. Many of my skills are useful in both. From the start I did not want a copy in each place, because then every fix has to be made twice. I wanted a change on one side to reach the other side by itself, so I worked out a setup with both agents before I wrote the first skill.

Two things make this harder than copying files:

- The agents read skills from different places. Codex reads skill folders from my computer. Cowork keeps skills in my account in the cloud, so it never sees my local files.
- Not every skill belongs everywhere. Some only make sense inside one project.

## The idea

Keep exactly one master copy of every skill on my own computer. Every agent either reads that copy directly or gets a copy pushed from it. Changes always start at the master.

```
 master: ~/skills/<name>/SKILL.md          (the only copy I edit)
   |
   |-- Codex:   ~/.agents/skills/<name>  -> symlink to the master, picks up changes at once
   |
   '-- Cowork:  account-level skill      -> submitted again after each change
```

The master is plain folders, one per skill, each with a `SKILL.md`. Zip files that an app needs for installation are only backups, never the master.

Claude Code works like Codex here. It reads skills from a local folder (`~/.claude/skills/<name>/SKILL.md` for personal skills) and follows a symlink to the target folder, so it needs no resubmitting.

## What to set up: four places

1. **The master folder.** One folder per skill, each with a `SKILL.md`.
2. **A rules doc.** A document, kept in your notes or knowledge base, that is written for the agent to follow. I call mine an agent wiki page. Its `description` says "read before adding, changing or removing any skill", which is how an agent finds it. A template is below.
3. **A user preference for both agents.** It makes every new session start by looking at the rules doc and the skills.
4. **A user preference for Codex only.** It makes Codex connect any shared skill it is missing.

The two preferences are what make this work without me asking each time. An agent only follows a rules doc if something tells it the doc exists. Scanning reads just the `name` and `description` of each file, so it stays cheap.

### The preference for both agents

```
At the first message of every new session, scan two places: the rules folder
and the skills folder. Read only the name and description of each file, not
the full text. Read a file in full only when its description matches the
current task. If you cannot tell whether one matches, ask me.
```

### The preference for Codex only

```
At the first message of every new session, scan the shared skills folder
(<skills-master>) and compare it with Codex's own skills folder
(<codex-skills-dir>). If a skill is missing there, create a symlink to the
master. If something already exists there, leave it alone. Report only what
was added or looks wrong. Follow the current permission rules; if you cannot
write there, report what is unfinished and why.
```

`~/.agents/skills` is the user-level location in the current Codex documentation; older Codex versions used `~/.codex/skills`. Check your version's documentation if a linked skill does not show up.

### The rules doc

```
---
name: skill-sync-rules
description: Read before adding, changing or removing any skill. Says where
  the master lives, how each agent connects to it, and how to version a change.
---

# Skill sync rules

## 1. Decide the kind of skill
- Shared skill: used across projects or agents. The master lives in the
  shared skills folder. It needs syncing, so follow sections 2 to 4.
- Project skill: used by one project only. The master lives in that
  project's own skills folder. Agents that read local folders read it from
  there. An agent that keeps skills in the cloud still needs it submitted.

## 2. Add a shared skill
Order matters: create the master first, then connect the agents.
1. Create <skills-master>/<name>/SKILL.md with version and updated fields,
   and a CHANGELOG.md that starts at 1.0.
2. Codex: link <codex-skills-dir>/<name> to the master (symlink).
3. Cowork: submit it as a new skill.

## 3. Change a shared skill
1. Edit the master only. Raise the version, update the date, and add a line
   to CHANGELOG.md.
2. Codex: nothing to do, the link already points to the master.
3. Cowork: submit the change again. When you finish a change, remind me:
   "the Cowork copy of this skill needs to be submitted again". Otherwise
   Cowork stays on the old version.

## 4. Remove a shared skill
1. Remove the Codex link.
2. Remove the skill from the Cowork account.
3. Delete the master.

## Never
- Edit through the Codex link, or edit the cloud copy.
- Keep a hand-written list of shared skills. The folder is the list.
```

When Cowork is asked to submit a skill, it shows a review card that I approve. That is the manual step in section 3.

## Version every change

Without versions, "which copy is current?" has no answer. Every skill gets:

- `version` and `updated` fields in the `SKILL.md` frontmatter. The version is `major.minor`: a small fix raises the minor number (1.0 to 1.1), a real change in behavior raises the major number (1.x to 2.0). A typo fix that changes nothing needs no new version.
- A `CHANGELOG.md` next to `SKILL.md`, with the newest version at the top: version, date, what changed, why. One line is often enough; a bigger change can take a few. It stays out of `SKILL.md`, so the agent does not spend tokens reading history every time the skill loads.

Some apps keep only the name and description when you save a skill, so the `version` field may not survive in the cloud copy. That is one more reason the master and its changelog are the reference, and the cloud copy is checked against them, not the other way round.

## The same idea for project instructions

Agents also read a project-level instruction file, and they look for different names: Claude Code reads `CLAUDE.md`, Codex reads `AGENTS.md`. I keep one file and link the other name to it, inside the project folder:

```
ln -s CLAUDE.md AGENTS.md
```

Both agents now read the same instructions. Where they need different behavior, the file says so explicitly (for example, "if you are Codex, use this name"), instead of the two files quietly diverging.

## Rules I follow

- Create the master first, then connect the agents. A skill that exists only in the cloud has no master to link to, and the local agents miss it.
- Edit the master only. Editing through the link works, but it is easy to lose track of which file you changed. Never edit the cloud copy directly: the next upload overwrites it, and its changes never reach the master. (I once found fixes in a cloud copy that the master never had, and had to copy them back by hand.)
- Do not keep a list of shared skills. The folder is the list: scanning it and reading each `description` is always current, and a hand-kept list goes stale.
- To remove a shared skill: delete the links, remove it from the cloud account, then delete the master.

## What this does not solve

- Cowork still needs a manual step. The rules doc makes the agent remind me, but I still approve the submission myself. If a tool ever offers a way to sync account skills from a local folder, this becomes the first thing to automate.
- Settings that differ per agent (paths, names) still need care. The skills in this repo keep those values in a separate `settings.md`, so `SKILL.md` can be identical everywhere.
