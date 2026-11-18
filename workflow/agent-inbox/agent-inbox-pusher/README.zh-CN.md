# agent-inbox-pusher

[English](README.md) | [繁體中文](README.zh-TW.md) | 简体中文

版本 1.3，最后更新 2026-11-12。属于 [agent-inbox](../README.zh-CN.md)。

把目前 session 的讨论存成 Notion Agent Inbox 里的一条事项，让另一个 agent（或换了设备的你）之后能接手。也可以不经过 Notion，直接生成一段 prompt，贴进新的 session（模式 B）。它做什么、要说哪些触发词、需求、设置、升级，以及在云端或手机上运行，都写在 [agent-inbox README](../README.zh-CN.md)。

## 补充

- 模式 A（写进 Notion）：skill 会先给你看一份草稿，分成四段（Background / Problem / Resolution / Next Step），并附上 Type 和 Handover To。你确认后，它才会写进 Notion。
- 模式 B（贴 prompt）：skill 会印出一个 code block，让你贴进新的 session，不会写入任何东西。

## 授权

MIT，见 repo 根目录的 [LICENSE](../../../LICENSE)。
