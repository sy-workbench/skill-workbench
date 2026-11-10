# skill-workbench

我自己多 agent 工作流裡用的 skill，整理成別人也能拿去用的版本。每個 skill 是一個資料夾，裡面有 AI agent 能載入的 `SKILL.md`，以及說明設定方式的 README。

這是個人作品，非官方，與 Anthropic 無關，也未經其背書或贊助。「Claude」是 Anthropic 的商標。

English: [README.md](README.md)

## Skill 清單

| Skill | 分類 | 版本 | 做什麼 |
|---|---|---|---|
| [agent-inbox-loader](workflow/agent-inbox-loader/README.zh-TW.md) | workflow | 1.1 | 把共用 Notion「Agent Inbox」的一筆條目讀進目前 session，接續在別處開始的工作 |
| [agent-inbox-pusher](workflow/agent-inbox-pusher/README.zh-TW.md) | workflow | 1.2 | 把目前討論存成 Agent Inbox 條目，或印出一段可貼進新 session 的交接 prompt |
| [agent-inbox-screenshot-intake](workflow/agent-inbox-screenshot-intake/README.zh-TW.md) | workflow | 1.1 | 把 Google Drive 資料夾裡的鬆散截圖變成 Notion Agent Inbox 條目，合併連拍、分派給 agent，並把原圖歸檔 |

之後整理好的 skill 會依分類陸續加進來。

## 目錄結構

```
skill-workbench/
  README.md            英文索引
  README.zh-TW.md      繁體中文索引
  LICENSE              MIT
  PLACEHOLDERS.md      所有要你自己填的設定，以及位置
  docs/                設計說明（執行 skill 不需要）
  workflow/            處理 agent 與 session 之間交棒的 skill
    <skill 名稱>/
      SKILL.md         skill 本體
      settings.example.md  要你填的值（複製成 settings.md）
      README.md        設定與用法（英文）
      README.zh-TW.md  設定與用法（繁體中文）
      CHANGELOG.md     版本紀錄
      references/      skill 會讀的輔助檔
```

每個 skill 資料夾都自成一體，只複製一個資料夾就能用。共用的參考檔刻意在每個 skill 各放一份，這樣不需要另外安裝其他東西。

## 怎麼用

1. 打開該 skill 的 README，照「設定」一節做。
2. 把 skill 資料夾複製到你的 agent 的 skills 目錄。
3. 在 skill 資料夾裡把 `settings.example.md` 複製成 `settings.md` 再填。有沒填的，skill 會停下來提醒你。你不需要改 `SKILL.md`，所以更新時可以直接覆蓋。

## 版本

每個 skill 有自己的版本（major.minor）和自己的 `CHANGELOG.md`。小修正升小數，行為有大改升整數。各 skill 的 README 會標明版本和最後同步日期。

## 授權

MIT，見 [LICENSE](LICENSE)。
