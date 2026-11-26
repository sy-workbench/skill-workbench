# skill-workbench

[English](README.md) | [繁體中文](README.zh-TW.md) | 简体中文

这里放的是我给自己的 AI agents 使用的 skills。已经整理过了可以直接拿去使用。
先从下面点进你有兴趣的分类/类别，里面是相关的 skills，照它 README 里的说明准备就可以了。

## 分类/类别

### workflow

为了讨论一个主题，我常同时在不同项目、sessions 或是设备 (e.g. 手机和电脑) 之间切换。这一类 skills 是我在这类场景下，为了提高效率而使用的小工具。

例如：把谈到一半的讨论，换到另一个 agent 继续；或是把手机上的截屏，交给该处理它的 agent。

从 [agent-inbox](workflow/agent-inbox/README.zh-CN.md) 开始看。

### tools

背后有一个 script 的小工具。

[md-to-html](tools/md-to-html/README.zh-CN.md) 把 Markdown 笔记转成比较好读的 HTML：宽表可以左右滚动，段落可以折叠，手机上也好看。`.md` 一直是唯一的来源，所以你可以看着网页，继续请 agent 修改。

### video-transcript

[youtube-video-transcript](video-transcript/youtube-video-transcript/README.zh-CN.md) 在你自己的电脑上用 Whisper 把 YouTube 视频转成文字稿，再修正语音识别听错的专有名词。下载和转录是分开的两半，要支持其他视频网站，不用动到其他部分。

### investing

[alert-spx-ma](investing/alert-spx-ma/README.zh-CN.md) 检查 S&P 500 是否回到 50 日均线附近（天数可自定义）。它只汇报，不会下单。

之后整理好更多 skills，我会再加上新的分类/类别。设计说明放在 [docs/](docs/)，不影响 skills 的使用，纯粹记录性质。如果你同时用好几个 agent，[一份 skill 文件夹，两个 agent 共用](docs/claude-codex-skill-sync.zh-CN.md)记录了我怎么让同一套 skills 在 Claude Cowork 和 Codex 都能用。

## 怎么用

每个 skill 的 README 都会列出需要准备的东西（同一组的 skills，说明放在这一组的 README），大致上都是这两步：

1. 把 skill 的文件夹复制到你放 skills 的文件夹。
2. 把 `settings.example.md` 复制一份，改名成 `settings.md`，填上你自己的设置。如果 skill 需要的值漏填了，被调用时会停下来告诉你缺哪一项。有些 skill 每一项都有默认值，只要填你想改的就好，也可以完全不填。

`SKILL.md` 没有任何 placeholder 需要替换，所以出新版本时，可以直接覆盖文件，除非你自己后续进行了调整。

有些环境（例如云端定时任务、手机 app）读不到 `settings.md`。这时要把设置贴在 `SKILL.md` 的最后面，README 里有说明贴法。更新时覆盖 `SKILL.md` 会把贴的设置覆盖掉，所以要重贴一次。

## 版本

每个 skill 有自己的版本号，也有自己的 `CHANGELOG.md`，里面记录每个版本改了什么。小修正，版本号小数位加 1。主要行为有改变，前面的数字加 1。每个 skill README 会说明当前的版本和最后更新日期。

## 授权与声明

MIT 授权，见 [LICENSE](LICENSE)。这是我的个人项目，与任何公司无关。
