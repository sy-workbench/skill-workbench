# agent-inbox-loader

版本 1.1，最後同步 2026-11-10。屬於 [skill-workbench](../../README.zh-TW.md)。非官方作品，與 Anthropic 無關。

把 Notion「Agent Inbox」裡的一筆條目讀進目前的 agent session，讓你接續在手機、別的 agent 或之前的 session 開始的工作。它會列出等你處理的條目，讀入你選的那一筆，並標成已讀。

搭配的 skill 是 [agent-inbox-pusher](../agent-inbox-pusher/README.zh-TW.md)，負責寫入條目。

## 需求

- 能載入 skill（含 `SKILL.md` 的資料夾）、並且開啟 Notion MCP 連接器的 agent。我是用 Claude 建置與測試，其他讀 `SKILL.md` 的 agent 可能也能用，但沒有測過。
- 一個可以建立資料庫的 Notion 工作區。

## 設定

以下每步只需做一次。

1. 在 Notion 建立一個資料庫，名稱叫「Agent Inbox」。
2. 照 `references/inbox-database.md` 加上欄位：Title、Date、Type、Handover To、Status、Last Edited。
3. 在 `Handover To` 欄位加入你每個 agent 角色的選項，再多加一個給你自己的選項。
4. 建立一個名稱叫「Active」的資料庫檢視。篩選：Status 是 Pending 或 Picked Up。排序：Date 由新到舊。
5. 打開「Active」檢視，點檢視旁的選單，選「Copy link to view」。應該會得到一個含有 `?v=` 的網址。
6. 請你的 agent 說：「用 Notion 工具讀這個資料庫，告訴我它的 data source ID。」應該會得到一串以 `collection://` 開頭的文字。
7. 把這個 skill 資料夾複製到你的 agent 的 skills 目錄，目錄位置依工具而定。
8. 在 skill 資料夾裡，把 `settings.example.md` 複製成 `settings.md`，填入兩個值：第 5 步的 Active 檢視網址、第 6 步的 data source ID。不要直接改 example 檔。要確認沒有漏填，在 skill 資料夾執行 `grep -n '<YOUR_' settings.md`，應該什麼都不會印出來。
9. 在每個 agent 自己的指令檔寫明它的角色名稱，必須和 `Handover To` 的某個選項一致。

## 用法

- `read inbox`：分兩組列出進行中的條目（指派給你的、尚未指派的），問你要讀哪一筆。
- `read inbox: <標題>`：直接讀那一筆。
- `let's continue the <topic> discussion`：skill 會找對應的條目。

觸發詞是英文。中文說法通常也能觸發，但沒有測過。

讀入後，agent 會用大約五行說明這筆的狀況，然後等你。你確認之前它不會動手。

## 選用：每次開 session 自動檢查

這個 skill 只在你開口時才讀內容。想要自動檢查的話，可以在各 agent 自己的指令檔加上類似這段：

```
## Session 開場：Agent Inbox 檢查
開場時查詢 Agent Inbox 的 Active 檢視。
列出 Handover To 是「<這個 agent 的角色>」的條目，以及 Handover To 為空的條目。
只顯示 Title、Date、Status。我沒要求就不要讀完整內容。
```

## 更新

把新版檔案複製到原本的 skill 資料夾上覆蓋。不要先刪掉資料夾，否則你的 `settings.md` 也會一起消失。`SKILL.md` 與 `settings.example.md` 可以直接覆蓋。新版如果需要新的設定，`CHANGELOG.md` 會註明，skill 也會停下來告訴你缺哪一項。

## 在雲端或手機上執行

有些環境（雲端排程、手機 app）只存 `SKILL.md`，讀不到 `settings.md`。這種情況，把填好的 `settings.md` 內容貼到 `SKILL.md` 最後面，標題用 `## Settings (pasted)`。skill 讀不到檔案時會改用這一段。更新會換掉 `SKILL.md`，所以更新後要重貼一次。

## 檔案

| 檔案 | 用途 |
|---|---|
| `settings.example.md` | 要你填的值。複製成 `settings.md` 再填 |
| `SKILL.md` | skill 本體 |
| `references/inbox-database.md` | 資料庫欄位、狀態定義、處理原則、角色說明（英文） |
| `CHANGELOG.md` | 版本紀錄（英文） |
| `README.md` | 英文 README |

## 授權

MIT，見 repo 根目錄的 [LICENSE](../../LICENSE)。
