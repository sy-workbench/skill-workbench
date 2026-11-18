# agent-inbox-loader

[English](README.md) | [繁體中文](README.zh-TW.md) | 简体中文

版本 1.2，最后更新 2026-11-12。属于 [agent-inbox](../README.zh-CN.md)。

把 Notion Agent Inbox 里的一条事项读进目前的 agent session，让你接着做在别处开始的工作。它做什么、要说哪些触发词、需求、设置、升级，以及在云端或手机上运行，都写在 [agent-inbox README](../README.zh-CN.md)。

## 补充

- `read inbox: <标题>`：直接读那个标题的事项。
- 说“`let's continue the <topic> discussion`”也可以，skill 会去找对应的事项。
- 读入后，agent 会先给你一段简短摘要，然后等你。你确认之前它不会开始动手。

## 选用：自动检查 Inbox

这个 skill 只有在你开口时才读内容。想要自动检查的话，有两种做法。

**每次开 session 时检查**：在每个 agent 自己的指令文件加上类似这段：

```
## Session 开场：Agent Inbox 检查
开场时查找 Agent Inbox 的 Active 视图。
列出 Handover To 是“<这个 agent 的角色名称>”的事项，以及 Handover To 是空的事项。
只显示 Title、Date、Status。我没要求就不要读完整内容。
```

**定时检查**：设置一个定时任务定时去处理。

## 授权

MIT，见 repo 根目录的 [LICENSE](../../../LICENSE)。
