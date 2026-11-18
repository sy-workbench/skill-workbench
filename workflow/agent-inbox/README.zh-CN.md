# agent-inbox

[English](README.md) | [繁體中文](README.zh-TW.md) | 简体中文

agent-inbox-pusher 和 agent-inbox-loader 是一组工具可以搭配使用。这两个 skills 的目的是让我可以快速的把工作从一个 agent 或 session 交接给另一个。做法是通过在 Notion 里创建的一个 Agent Inbox 的数据库：agent-inbox-pusher 负责把讨论按照规定格式存进去，agent-inbox-loader 负责读取交接内容。

agent-inbox-pusher 还有另一种用法，叫模式 B：不经过 Notion，直接生成一段 prompt，让你可以快速复制粘贴进新的 session 接着讨论或执行。模式 B 不需要数据库，也不用安装 agent-inbox-loader。

想用 Notion 的方式的话，要先准备好数据库和几项设置，需要的东西写在下面的“设置”。只用模式 B 的话，安装 agent-inbox-pusher 就好，不需要任何设置。

## 这一组有哪些 skills

| Skill | 做什么 |
|---|---|
| [agent-inbox-pusher](agent-inbox-pusher/README.zh-CN.md) | 把目前的讨论存成 Agent Inbox 里的一条事项，或生成一段 prompt，让你贴进新的 session |
| [agent-inbox-loader](agent-inbox-loader/README.zh-CN.md) | 列出 Agent Inbox 里等待这个 agent 处理的事项，读入其中一条（只有一条指派给它时会直接读入），并标记成已接手 |

## 怎么搭配

1. 在旧的 session 里，对 agent 说 `push to inbox`。它会把讨论存成一条事项，并记下这条要交给哪个 agent。
2. 到新的 session 或另一个 agent，说 `read inbox`。它会看这两种事项：指派给它的，以及还没有指派对象的。
3. 如果指派给它的刚好只有一条，它会直接读入，并标记成已接手，再给你一段简短摘要。有好几条事项的话，它会列出清单，问你要先处理哪一条。
4. 还没有指派的事项也会列出来，但 agent 不会自己认领，你开口它才会接。
5. 读完之后，agent 会等你点头才开始动手。

触发动作的关键词：

| 动作 | 说这句 | 哪个 skill |
|---|---|---|
| 把讨论存进 Notion | `push to inbox` / `save to inbox` / `sync to inbox` | agent-inbox-pusher |
| 生成一段 prompt，贴进新的 session（模式 B） | `provide a prompt` / `handoff prompt` / `prompt for the new session` | agent-inbox-pusher |
| 读取等这个 agent 处理的事项 | `read inbox` / `read notion inbox` | agent-inbox-loader |

像 `handoff`、`new session`、`let's talk later` 这类说法，两种模式都说得通，pusher 会先问一次：要生成 prompt，还是存进 Inbox。

## 需求

- 安装好 skill（含 `SKILL.md` 的文件夹），以及设置好 Notion MCP，也就是让 agent 能读写 Notion 的功能。
- 一个可以创建数据库的 Notion 工作区。

## 设置

**只想用模式 B**：把 `agent-inbox-pusher` 文件夹复制到你的 agent 的 skills 目录，目录位置依工具而定。之后在任何对话里说 `provide a prompt` 就能用。不需要 Notion，也不用设置。

**要连 Notion**：把你要用的 skill 文件夹复制到 agent 的 skills 目录（位置依工具而定），再准备好下面这些东西。怎么准备都可以，也可以请你的 agent 执行。

pusher 和 loader 两个 skill 都需要用到的：

- 一个叫“Agent Inbox”的 Notion 数据库，字段参照 [`inbox-database.md`](agent-inbox-pusher/references/inbox-database.md)。
- 在数据库 `Handover To` 字段里，替每个 agent 角色添加一个选项（例如 `Writer`、`Researcher`），可以考虑再加一个给你自己（依你工作习惯决定）。
- 数据库的 data source ID，是一串以 `collection://` 开头的文字。

只有 agent-inbox-loader 需要用到的：

- 一个叫“Active”的数据库视图：筛选 Status 是 Pending 或 Picked Up，依 Date 由新到旧排序。
- 这个视图的网址，里面含有 `?v=`。

每个 agent 都需要用到的：

- 在它自己的指令文件写明角色名称，例如“你在 Agent Inbox 的角色名称是 Writer”。名称要和 `Handover To` 的某个选项完全一致。

最后，在每个 skill 文件夹里，把 `settings.example.md` 复制成 `settings.md`，填入上面的值。不要直接改 example 文件。

## 附加 skill (Add-ons)

这里列出其他可选用搭配的 skill（目前只有一个）。这些 skill 会把事项写进和核心 skill 同一个 Agent Inbox 数据库，让 agent 可以调用 loader 去读取和处理。

| 附加 skill | 多了什么功能 | 还需要什么 |
|---|---|---|
| [agent-inbox-screenshot-intake](agent-inbox-screenshot-intake/README.zh-CN.md) | 把你丢进 Google Drive 文件夹的截屏，变成 Agent Inbox 里的事项，并交给适合处理的 agent | Google Drive，以及数据库里多一个 `Source` 字段 |

## 升级到新版本

换掉 skill 文件夹时，你的 `settings.md` 可能会一起被删掉。升级前先把它复制到其他地方，升级完再搬回来。

如果新版需要新的设置，`CHANGELOG.md` 会写明，skill 也会停下来，告诉你缺哪一项。

## 在云端或手机上运行

有些环境，例如云端定时任务和手机 app，只会保存 `SKILL.md`，读不到 `settings.md`。这种情况下，把填好的 `settings.md` 内容贴到 `SKILL.md` 的最后面，标题用 `## Settings (pasted)`。每个 skill 各贴自己的。skill 找不到文件时，会改读这一段。

升级会换掉 `SKILL.md`，所以每次升级后都要重贴一次。

## 授权

MIT，见 repo 根目录的 [LICENSE](../../LICENSE)。
