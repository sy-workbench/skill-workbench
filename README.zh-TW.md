# skill-workbench

這裡放的是我給自己的 AI agents 使用的 skills。已經整理過了可以直接拿去使用。
先從下面點進你有興趣的分類/類別，裡面是相關的 skills，照它 README 裡的說明準備就可以了。

English: [README.md](README.md)

## 分類/類別

### workflow

為了討論一個主題，我常同時在不同專案、sessions 或是裝置 (e.g. 手機和電腦) 之間切換。這一類 skills 是我在這類場景下，為了提高效率而使用的小工具。

例如：把談到一半的討論，換到另一個 agent 繼續；或是把手機上的截圖，交給該處理它的 agent。

資料夾在 [workflow/](workflow/)。

之後整理好更多 skills，我會再加上新的分類/類別。設計說明放在 [docs/](docs/)，不影響 skills 的使用，純粹記錄性質。

## 怎麼用

每個 skill 的 README 都會列出需要準備的東西（同一組的 skills，說明放在這一組的 README），大致上都是這兩步：

1. 把 skill 的資料夾複製到你放 skills 的資料夾。
2. 把 `settings.example.md` 複製一份，改名成 `settings.md`，填上你自己的設定。如果有漏填，被調用時 skill 會停下來告訴你缺哪一項。

`SKILL.md` 沒有任何 placeholder 需要替換，所以出新版本時，可以直接覆蓋檔案，除非你自己後續進行了調整。

有些環境（例如雲端排程、手機 app）讀不到 `settings.md`。這時要把設定貼在 `SKILL.md` 的最後面，README 裡有說明貼法。更新時覆蓋 `SKILL.md` 會把貼的設定蓋掉，所以要重貼一次。

## 版本

每個 skill 有自己的版本號，也有自己的 `CHANGELOG.md`，裡面記錄每個版本改了什麼。小修正，版本號小數位加1。主要行為有改變，前面的數字加 1。每個 skill README 會說明當前的版本和最後更新日期。

## 授權與聲明

MIT 授權，見 [LICENSE](LICENSE)。這是我的個人專案，與任何公司無關。
