# 设计说明：一份 skill 文件夹，两个 agent 共用

[English](claude-codex-skill-sync.md) | [繁體中文](claude-codex-skill-sync.zh-TW.md) | 简体中文

这份说明记录我怎么让同一套 skills 在 Claude Cowork 和 Codex 两个 agent 里都能用，而不用手动维护两份。要使用这个 repo 的 skills 不需要看这份，它是我希望一开始就这样做的做法。

最后更新：2026-11-26。

## 问题

我大部分讨论用 Cowork，部分写程序的工作用 Codex。很多 skills 两边都用得到。我从一开始就不想两边各放一份，因为每次修正都要改两次。我希望一边调整时，另一边也能自动同步，所以在写第一个 skill 之前，就先和两边的 AI 讨论出一套做法。

这件事比复制文件麻烦，有两个原因：

- 两个 agent 读 skills 的地方不一样。Codex 读我电脑上的 skill 文件夹。Cowork 把 skills 存在我云端的账号里，看不到我电脑上的文件。
- 不是每个 skill 都要放两边。有些只在某一个项目里才有意义。

## 想法

每个 skill 在我自己的电脑上只留一份正本。每个 agent 不是直接读这份正本，就是从它取得副本。所有改动都从正本开始。

```
 正本：~/skills/<name>/SKILL.md          （我唯一会编辑的一份）
   |
   |-- Codex：   ~/.agents/skills/<name>  -> 指向正本的 symlink，改了立刻生效
   |
   '-- Cowork：  账号层级的 skill         -> 每次改完要再提交一次
```

正本就是一般文件夹，一个 skill 一个文件夹，里面放 `SKILL.md`。App 安装时需要的 zip 文件只是备份，不当正本。

Claude Code 在这里和 Codex 一样。它读本机文件夹里的 skills（个人层级放在 `~/.claude/skills/<name>/SKILL.md`），也会跟着 symlink 读到目标文件夹，所以不需要重新提交。

## 要设置的四个地方

1. **正本文件夹。** 一个 skill 一个文件夹，里面放 `SKILL.md`。
2. **规范文档。** 放在你的笔记或知识库里，写给 agent 照着做的文档。我把它叫作 agent wiki 页。它的 `description` 写“新增、修改、删除 skill 之前先读”，agent 就是靠这句找到它。模板在下面。
3. **两个 agent 共用的偏好设置。** 让每个新 session 一开始先看一遍规范文档和 skills。
4. **只给 Codex 的偏好设置。** 让 Codex 把缺少的共用 skill 接起来。

这两段偏好设置，是让整套做法不用我每次开口要求的关键。Agent 要有东西告诉它规范文档存在，才会照着做。扫描只读每份文件的 `name` 和 `description`，成本很低。

### 两个 agent 共用的偏好设置

```
每个新 session 的第一个输入，先扫描两个地方：规范文档文件夹和 skills 文件夹。
只读每份文件的 name 与 description，不读全文。描述命中当下任务才读全文。
判断不出来是否命中时，先问我。
```

### 只给 Codex 的偏好设置

```
每个新 session 的第一个输入，先扫描共用 skill 文件夹（<skills-master>），
和 Codex 自己的 skills 文件夹（<codex-skills-dir>）比对。缺的就创建指向正本的
symlink，已存在的不覆盖。只汇报添加或异常的项目。遵守当前的权限与审批机制；
无法写入时，汇报未完成的项目与原因。
```

`~/.agents/skills` 是目前 Codex 文档里的用户层级位置；旧版 Codex 用的是 `~/.codex/skills`。如果链接好的 skill 没出现，请查你那个版本的文档。

### 规范文档

```
---
name: skill-sync-rules
description: 添加、修改、删除 skill 之前先读。说明正本放哪里、各 agent 怎么接到正本、
  改动怎么记版本。
---

# Skill 同步规范

## 1. 先判断是哪一种 skill
- 共用 skill：跨项目或跨 agent 使用。正本放在共用 skills 文件夹。需要同步，
  依第 2 到 4 节处理。
- 项目 skill：只有一个项目使用。正本放在该项目自己的 skills 文件夹。读本机
  文件夹的 agent 直接从那里读。把 skills 存在云端的 agent 仍然要提交一次。

## 2. 添加共用 skill
顺序不能反：先建正本，再接各 agent。
1. 创建 <skills-master>/<name>/SKILL.md，含 version 与 updated 字段，
   并创建 CHANGELOG.md，从 1.0 开始。
2. Codex：创建 <codex-skills-dir>/<name>，连到正本（symlink）。
3. Cowork：以新 skill 提交。

## 3. 修改共用 skill
1. 只改正本。升版本、更新日期，并在 CHANGELOG.md 加一行。
2. Codex：不用做任何事，链接已经指向正本。
3. Cowork：重新提交这次的改动。改完时提醒我：“这支 skill 的 Cowork 版需要
   重新提交”，否则 Cowork 会停在旧版。

## 4. 删除共用 skill
1. 移除 Codex 的链接。
2. 从 Cowork 账号移除这支 skill。
3. 删除正本。

## 禁止
- 通过 Codex 的链接编辑，或直接编辑云端那份。
- 另外手动维护共用 skill 清单。文件夹本身就是清单。
```

Cowork 在被要求提交 skill 时，会跳出一张审核卡片让我同意。这就是第 3 节那个手动步骤。

## 每次改动都要记版本

没有版本，就无法回答“哪一份是最新的”。每个 skill 都有：

- `SKILL.md` frontmatter 里的 `version` 与 `updated` 字段。版本号用 `major.minor`：小修正升小数（1.0 到 1.1），行为上的实质改变升整数（1.x 到 2.0）。不改变任何行为的错字修正不需要升版。
- `SKILL.md` 旁边的 `CHANGELOG.md`，最新版本放最上面：版本、日期、改了什么、为什么。通常一行就够，大改动可以写几行。它不放在 `SKILL.md` 里，agent 每次加载 skill 时就不用花 token 读历史。

有些 App 保存 skill 时只保留名称和说明，所以云端那份可能不会留下 `version` 字段。这也是为什么要以正本和它的 changelog 为准，云端那份拿来对照正本，而不是反过来。

## 项目指令也是同样的做法

Agent 也会读项目层级的指令文件，而且它们找的文件名不一样：Claude Code 读 `CLAUDE.md`，Codex 读 `AGENTS.md`。我只留一份文件，在项目文件夹里把另一个名称连到它：

```
ln -s CLAUDE.md AGENTS.md
```

这样两个 agent 读到的就是同一份指令。需要不同行为的地方，文件里明确写出来（例如“如果你是 Codex，用这个名称”），而不是让两份文件悄悄变得不一样。

## 我遵守的规则

- 先建正本，再接各 agent。只存在云端的 skill 没有正本可以连，本机的 agent 会漏掉它。
- 只改正本。通过链接编辑虽然行得通，但很容易搞不清楚改的是哪个文件。永远不要直接编辑云端那份：下次上传会覆盖它，它的改动也不会回到正本。（我曾经在云端那份发现正本没有的修正，只好手动搬回来。）
- 不另外维护共用 skill 清单。文件夹就是清单：扫描它、读每个 `description`，永远是最新的，手写的清单会过期。
- 要删除共用 skill：先删链接，再从云端账号移除，最后删正本。

## 这个做法没有解决的事

- Cowork 仍然需要一个手动步骤。规范文档会让 agent 提醒我，但提交我还是要自己同意。如果哪天有工具能把账号层级的 skills 从本机文件夹同步出去，这会是第一个要自动化的地方。
- 每个 agent 不一样的设置（路径、名称）还是要小心。这个 repo 的 skills 把这些值放在独立的 `settings.md`，所以 `SKILL.md` 在每个地方都可以完全一样。
