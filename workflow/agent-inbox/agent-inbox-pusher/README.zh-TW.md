# agent-inbox-pusher

版本 1.2，最後同步 2026-11-10。屬於 [skill-workbench](../../README.zh-TW.md)。非官方作品，與 Anthropic 無關。

把目前 session 的討論整理成一筆結構化條目，存進 Notion「Agent Inbox」，讓另一個 agent（或換了裝置的你）之後能接手。也可以不經過 Notion，直接印出一段可貼進新 session 的交接 prompt。

搭配的 skill 是 [agent-inbox-loader](../agent-inbox-loader/README.zh-TW.md)，負責把條目讀回來。

## 兩種模式

| 模式 | 你說 | 結果 |
|---|---|---|
| A：寫進 Notion | `push to inbox`、`save to inbox`、`sync to inbox` | 先給你看四段草稿（Background / Problem / Resolution / Next Step）與 Type、Handover To，你確認後才寫進 Notion |
| B：可貼 prompt | `provide a prompt`、`handoff prompt`、`prompt for the new session` | 印出一個 code block，貼到新 session 即可，不寫任何東西 |

兩種模式都可能用到的說法（例如「handoff」、「new session」），skill 會先問一句：「貼 prompt 還是寫進 Inbox？」

模式 B 不需要任何設定，模式 A 需要下面的設定。

## 需求

- 能載入 skill（含 `SKILL.md` 的資料夾）、並且開啟 Notion MCP 連接器的 agent。我是用 Claude 建置與測試，其他讀 `SKILL.md` 的 agent 可能也能用，但沒有測過。
- 一個可以建立資料庫的 Notion 工作區。

## 設定

以下每步只需做一次。

1. 在 Notion 建立一個資料庫，名稱叫「Agent Inbox」。
2. 照 `references/inbox-database.md` 加上欄位：Title、Date、Type、Handover To、Status、Last Edited。
3. 在 `Handover To` 欄位加入你每個 agent 角色的選項，再多加一個給你自己的選項。
4. 請你的 agent 說：「用 Notion 工具讀這個資料庫，告訴我它的 data source ID。」應該會得到一串以 `collection://` 開頭的文字。
5. 把這個 skill 資料夾複製到你的 agent 的 skills 目錄，目錄位置依工具而定。
6. 在 skill 資料夾裡，把 `settings.example.md` 複製成 `settings.md`，填入第 4 步的 data source ID。有自己的敏感資料規則，加在 Sensitive data 底下。不要直接改 example 檔。要確認沒有漏填，在 skill 資料夾執行 `grep -n '<YOUR_' settings.md`，應該什麼都不會印出來。
7. 在每個 agent 自己的指令檔寫明它的角色名稱，必須和 `Handover To` 的某個選項一致。

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
