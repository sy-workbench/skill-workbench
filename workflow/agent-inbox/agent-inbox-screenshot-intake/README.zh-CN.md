# agent-inbox-screenshot-intake

[English](README.md) | [繁體中文](README.zh-TW.md) | 简体中文

版本 1.2，最后更新 2026-11-12。属于 [agent-inbox](../README.zh-CN.md) 的附加 skill。

常常在手机上看到想要等等处理的内容或东西，截个图，然后就忘了。这个 skill 是负责处理这些截屏的，它会读 Google Drive 某个文件夹里零散的截屏，判断每张在讲什么，在 Notion Agent Inbox 建一条事项，分派给该处理的 agent，再把原图重命名成易懂的文件名，搬进 `_archive`。同一篇帖子分成好几张截屏的，也会合成一条事项。

这些事项会写进和核心 skill 同一个数据库。要读取和处理它们，用 [agent-inbox-loader](../agent-inbox-loader/README.zh-CN.md)。

## 需求

- 安装好这个 skill，并设置好两个连接器：Notion MCP 与 Google Drive MCP。
- [agent-inbox README](../README.zh-CN.md#设置) 里说明的 Agent Inbox 数据库，并多加一个字段：`Source`，类型是 URL。这个 skill 会把原图的链接写在这里。
- Google Drive 里一个放截屏的文件夹，里面再建一个叫 `_archive` 的子文件夹。处理完的图片会搬到这里，主文件夹不会越堆越多，也随时找得到原图。

## 设置

把这个 skill 文件夹复制到 agent 的 skills 目录（位置依工具而定）。再到 skill 文件夹里，把 `settings.example.md` 复制成 `settings.md`，填入下面这些。不要直接改 example 文件。

必填：

- 放截屏的文件夹 ID，以及它底下 `_archive` 子文件夹的 ID。在 Google Drive 打开文件夹，地址栏 `/folders/` 后面那一串就是 ID。
- Agent Inbox 数据库的 data source ID，和核心 skill 用的是同一个。
- 你的时区。

分派表：哪一类截屏交给哪个 agent。把示例列换成你自己的 agent，名称要和 `Handover To` 的选项一致。不想分派的话，把表格留空。

可选：

- 文件名日期格式：你的手机命名截屏的方式和文件里的示例不同时才需要改。
- 敏感数据规则：加上你不想被复制进 Notion 的内容。

## 用法

说 `process screenshots` 或 `process the screenshot inbox`。skill 会处理文件夹最上层的每一张图，做完汇报结果。

想先试试，丢一张无关紧要的截屏进文件夹再运行。应该会在 Notion 看到一条新事项，图片也已经在 `_archive` 里，文件名是新的。

想定时运行，就设置一个定时任务。

## 补充

- 截屏可能含有私人信息。skill 在写进 Notion 之前，会把确切的金额、账户信息和证件信息改写成相对的说法。你觉得敏感的内容，请自己加在 `settings.md` 的 Sensitive data 底下。
- 读不了的图片会留在文件夹里，让你自己看。
- 新文件名的日期取自原文件名；原文件名没有日期时，改用 Drive 的创建时间。
- 重复运行不会有问题，因为处理完的图片已经离开文件夹。

## 升级，以及在云端或手机上运行

这两件事和核心 skill 的做法一样，请看 [agent-inbox README](../README.zh-CN.md) 的“[升级到新版本](../README.zh-CN.md#升级到新版本)”与“[在云端或手机上运行](../README.zh-CN.md#在云端或手机上运行)”。

## 授权

MIT，见 repo 根目录的 [LICENSE](../../../LICENSE)。
