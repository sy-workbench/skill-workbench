# skill-workbench

[English](README.md) | 繁體中文 | [简体中文](README.zh-CN.md)

這裡放的是我給自己的 AI agents 使用的 skills。已經整理過了可以直接拿去使用。
先從下面點進你有興趣的分類/類別，裡面是相關的 skills，照它 README 裡的說明準備就可以了。

## 分類/類別

### workflow

為了討論一個主題，我常同時在不同專案、sessions 或是裝置 (e.g. 手機和電腦) 之間切換。這一類 skills 是我在這類場景下，為了提高效率而使用的小工具。

例如：把談到一半的討論，換到另一個 agent 繼續；或是把手機上的截圖，交給該處理它的 agent。

從 [agent-inbox](workflow/agent-inbox/README.zh-TW.md) 開始看。

### tools

背後有一支 script 的小工具。

[md-to-html](tools/md-to-html/README.zh-TW.md) 把 Markdown 筆記轉成比較好讀的 HTML：寬表可以左右捲動，段落可以收合，手機上也好看。`.md` 一直是唯一的來源，所以你可以看著網頁，繼續請 agent 修改。

### video-transcript

[youtube-video-transcript](video-transcript/youtube-video-transcript/README.zh-TW.md) 在你自己的電腦上用 Whisper 把 YouTube 影片轉成逐字稿，再修正語音辨識聽錯的專有名詞。下載和轉錄是分開的兩半，要支援其他影片網站，不用動到其他部分。

### investing

[alert-spx-ma20](investing/alert-spx-ma20/README.zh-TW.md) 檢查 S&P 500 是否回到 20 日均線附近，設了保底月份的話，也不會一直空等。它只回報，不會下單。

之後整理好更多 skills，我會再加上新的分類/類別。設計說明放在 [docs/](docs/)，不影響 skills 的使用，純粹記錄性質。如果你同時用好幾個 agent，[one skill folder, two agents](docs/claude-codex-skill-sync.md)（英文）記錄了我怎麼讓同一套 skills 在 Claude 和 Codex 都能用。

## 怎麼用

每個 skill 的 README 都會列出需要準備的東西（同一組的 skills，說明放在這一組的 README），大致上都是這兩步：

1. 把 skill 的資料夾複製到你放 skills 的資料夾。
2. 把 `settings.example.md` 複製一份，改名成 `settings.md`，填上你自己的設定。如果 skill 需要的值漏填了，被調用時會停下來告訴你缺哪一項。有些 skill 每一項都有預設值，只要填你想改的就好，也可以完全不填。

`SKILL.md` 沒有任何 placeholder 需要替換，所以出新版本時，可以直接覆蓋檔案，除非你自己後續進行了調整。

有些環境（例如雲端排程、手機 app）讀不到 `settings.md`。這時要把設定貼在 `SKILL.md` 的最後面，README 裡有說明貼法。更新時覆蓋 `SKILL.md` 會把貼的設定蓋掉，所以要重貼一次。

## 版本

每個 skill 有自己的版本號，也有自己的 `CHANGELOG.md`，裡面記錄每個版本改了什麼。小修正，版本號小數位加1。主要行為有改變，前面的數字加 1。每個 skill README 會說明當前的版本和最後更新日期。

## 授權與聲明

MIT 授權，見 [LICENSE](LICENSE)。這是我的個人專案，與任何公司無關。
