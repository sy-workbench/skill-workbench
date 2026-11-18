# Design notes: one skill folder, two agents

These notes describe how I keep the same skills working in two agents, Claude and Codex, without maintaining two copies by hand. Nothing here is needed to use the skills in this repo. It is the setup I wish I had started with.

Last updated 2026-11-18.

## The problem

I use Claude for most discussions and Codex for some coding work. Many of my skills are useful in both. At first each agent had its own copy, and the copies drifted: I fixed a bug in one, forgot the other, and a week later could not tell which version was right.

Two things make this harder than copying files:

- The agents read skills from different places. Codex reads skill folders from my computer. The Claude app keeps skills in my account in the cloud, so it never sees my local files.
- Not every skill belongs everywhere. Some only make sense inside one project.

## The idea

Keep exactly one master copy of every skill on my own computer. Every agent either reads that copy directly or gets a copy pushed from it. Changes always start at the master.

```
 master: ~/skills/<name>/SKILL.md          (the only copy I edit)
   |
   |-- Codex:      ~/.agents/skills/<name>  -> symlink to the master, picks up changes at once
   |
   '-- Claude app: account-level skill      -> re-uploaded by hand after each change
```

The master is plain folders, one per skill, each with a `SKILL.md`. Zip files that an app needs for installation are only backups, never the master.

## Step 1: decide where a skill lives

Ask one question: is this skill only used by one project?

| Kind | Test | Where the master lives | Needs syncing? |
|---|---|---|---|
| Shared skill | Used across projects or agents | One shared skills folder | Yes, follow the steps below |
| Project skill | Only one project uses it | That project's own `skills/` folder | Not for agents that read local folders: they read it from the project folder. An agent that keeps skills in the cloud still needs it uploaded, the same as Step 2 |

Most of the trouble comes from shared skills, so the rest of these notes are about them.

## Step 2: connect each agent to the master

**Agents that read local folders** (Codex, and coding agents in general): link the skill folder instead of copying it.

```
ln -s ~/skills/<name> ~/.agents/skills/<name>
```

Codex follows the link, so an edit to the master takes effect in the next session with nothing else to do. `~/.agents/skills` is the user-level location in the current Codex documentation; older Codex versions used `~/.codex/skills`. Check your version's documentation if a linked skill does not show up.

**Agents that keep skills in the cloud** (the Claude app): there is no link to make. After changing the master, upload or save the skill again in the app. This step is easy to forget, so I treat "the cloud copy needs updating" as part of finishing any change, not as a later chore.

## Step 3: version every change

Without versions, "which copy is current?" has no answer. Every skill gets:

- `version` and `updated` fields in the `SKILL.md` frontmatter. The version is `major.minor`: a small fix raises the minor number (1.0 to 1.1), a real change in behavior raises the major number (1.x to 2.0). A typo fix that changes nothing needs no new version.
- A `CHANGELOG.md` next to `SKILL.md`, with the newest version at the top: version, date, what changed, why. One line is often enough; a bigger change can take a few. It stays out of `SKILL.md`, so the agent does not spend tokens reading history every time the skill loads.

Some apps keep only the name and description when you save a skill, so the `version` field may not survive in the cloud copy. That is one more reason the master and its changelog are the reference, and the cloud copy is checked against them, not the other way round.

## Step 4: the same idea for project instructions

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

- The cloud copy still needs a manual step. If a tool ever offers a way to sync account skills from a local folder, this becomes the first thing to automate.
- Settings that differ per agent (paths, names) still need care. The skills in this repo keep those values in a separate `settings.md`, so `SKILL.md` can be identical everywhere.
