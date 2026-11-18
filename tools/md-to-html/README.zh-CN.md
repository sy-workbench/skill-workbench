# md-to-html

[English](README.md) | [繁體中文](README.zh-TW.md) | 简体中文

版本 1.0，最后更新 2026-11-18。

我习惯用 Markdown 写笔记，常常是 AI agent 跟我一起改。但有些笔记在编辑器里很难读：十几列的比较表被挤到每格都在换行，长笔记也没办法把段落收起来。这个 skill 会把 `.md` 转成一页比较好读的 HTML：宽表可以左右滚动，表头和前两列固定不动；Obsidian 的 callout 变成折叠区块；手机上看排版也会自动调整。

和 agent 一起用的关键是一条规则：`.md` 是唯一的来源。你看着网页说“这段收起来”、“加一个跳到那个标题的链接”，agent 会去改 `.md`，再重新生成网页，不会直接改 HTML，两边就不会对不上。

## 需求

- 一个能在你文件所在的电脑上运行指令的 agent（例如 coding agent，或有终端工具的桌面 app）。
- Python 3 和 `markdown` 包，要装在运行 script 的同一个 `python3` 底下，例如 `python3 -m pip install --user markdown`。Homebrew 管理的 Python 可能会拒绝，这时改用虚拟环境（venv）。也可以请 agent 帮你装。

不需要任何账号或 ID。没有 `settings.md` 时，skill 用 `default` 主题，网页语言设为英文。

## 设置

把整个 skill 文件夹（含 `scripts/` 和 `assets/`）复制到 agent 的 skills 目录（位置依工具而定）。

可选：把 `settings.example.md` 在同一个文件夹复制成 `settings.md`，可以改两个默认值：

- 默认主题：没指定主题时用哪一个。可以是 `assets/themes/` 里的文件名（不含 `.css`，例如 `dark`），或是你自己的 `.css` 文件路径。
- 网页语言：写进网页的语言代码，例如 `zh-Hant`、`ja`。浏览器靠它挑字体，屏幕阅读器靠它选语音。

## 用法

用你自己的话说就可以，例如“把 notes.md 转成 HTML 给我看”。agent 会运行 script，告诉你 HTML 文件在哪里，用浏览器打开就好。之后内容有改，刷新标签页就看得到。

看着网页时，也可以直接提要求：“Background 那段收起来”、“加一个跳到 Pricing 的链接”、“换成深色主题”。agent 会把这些写进 `.md`。

## 主题

排版在 `assets/base.css`，颜色和字体放在 `assets/themes/` 底下的小文件，这一版附 `default`（浅色）和 `dark`（深色）。想做自己的主题，把 `default.css` 在同一个文件夹复制成新文件名，改里面的值，就能用那个名字指定，不用改 script。主题文件也可以加自己的 CSS 规则，会覆盖基本排版。

## 补充

- 所有东西都内嵌在 HTML 文件里，离线也能打开，也能单独传给别人。
- 每次生成网页都会覆盖旧的 HTML。不要自己改 HTML，要改就改 `.md`。
- 支持的 Obsidian 语法：同一个文件内的 `[[#标题]]`、`[[#标题|显示文字]]` 链接，以及 callout（`> [!note]- 标题` 默认收起，`+` 或不加符号默认展开）。连到其他文件的链接不会转换。
- `.md` 开头的 YAML frontmatter 不会出现在网页上。
- 代码块或 `行内代码` 里的 Obsidian 语法会照原样显示，所以解说语法的笔记也能正确呈现。
- callout 里的标题没有锚点，跳到这些标题的链接不会动。
- 每次运行都会写 log 到 `/tmp/md_to_html.log`，出问题时 agent 可以自己看。

## 升级到新版本

换掉 skill 文件夹时，你的 `settings.md` 和自己加进 `assets/themes/` 的主题可能会一起被删掉。升级前先复制到其他地方，升级完再搬回来。

如果新版需要新的设置，`CHANGELOG.md` 会写明。

## 在云端或手机上运行

这个 skill 要靠终端运行 script，所以在没有终端的环境（例如大部分手机 app）不能用。如果环境有终端、但只保存 `SKILL.md`，把 `settings.md` 的内容贴到 `SKILL.md` 最后面，标题用 `## Settings (pasted)`，`scripts/` 和 `assets/` 也要一起放进去。升级会换掉 `SKILL.md`，所以每次升级后都要重贴。

## 授权

MIT 授权，见 repo 根目录的 [LICENSE](../../LICENSE)。
