# agent-inbox-screenshot-intake

版本 1.2，最後更新 2026-11-11。屬於 [agent-inbox](../README.zh-TW.md) 的附加 skill。

常常在手機上看到想要等等處理的內容或東西，截個圖，然後就忘了。這個 skill 是負責處理這些截圖的，它會讀 Google Drive（或是其他你慣用的）某個資料夾裡零散的截圖，判斷每張在講什麼，在 Notion Agent Inbox 建一條事項，分派給該處理的 agent，再把原圖重新命名成易懂的檔名，搬進 `_archive`。同一篇貼文分成好幾張截圖的，也會合成一條事項。

這些事項會寫進和核心 skill 同一個資料庫。要讀取和處理它們，用 [agent-inbox-loader](../agent-inbox-loader/README.zh-TW.md)。

## 需求

- 安裝好這個 skill，並設定好兩個連接器：Notion MCP，以及存放截圖資料夾的那個儲存空間對應的 MCP（例如 Google Drive MCP）。
- [agent-inbox README](../README.zh-TW.md#設定) 裡說明的 Agent Inbox 資料庫，並多加一個欄位：`Source`，類型是 URL。這個 skill 會把原圖的連結寫在這裡。
- 儲存空間裡一個放截圖的資料夾，裡面再建一個叫 `_archive` 的子資料夾。處理完的圖片會搬到這裡，主資料夾不會越堆越多，也隨時找得到原圖。

## 設定

把這個 skill 資料夾複製到 agent 的 skills 目錄（位置依工具而定）。再到 skill 資料夾裡，把 `settings.example.md` 複製成 `settings.md`，填入下面這些。不要直接改 example 檔。

必填：

- 放截圖的資料夾 ID，以及它底下 `_archive` 子資料夾的 ID。在 Google Drive 打開資料夾，網址列 `/folders/` 後面那一串就是 ID。
- Agent Inbox 資料庫的 data source ID，和核心 skill 用的是同一個。
- 你的時區。

分派表：哪一類截圖交給哪個 agent。把範例列換成你自己的 agent，名稱要和 `Handover To` 的選項一致。不想分派的話，把表格留空。

選填：

- 檔名日期格式：你的手機命名截圖的方式和檔案裡的範例不同時才需要改。
- 敏感資料規則：加上你不想被複製進 Notion 的內容。

## 用法

說 `process screenshots` 或 `process the screenshot inbox`。skill 會處理資料夾最上層的每一張圖，做完回報結果。

想先試試，丟一張無關緊要的截圖進資料夾再執行。應該會在 Notion 看到一條新事項，圖片也已經在 `_archive` 裡，檔名是新的。

想定時執行，就設定一個排程任務。

## 補充

- 截圖可能含有私人資訊。skill 在寫進 Notion 之前，會把確切的金額、帳戶資料和證件資料改寫成相對的說法。你覺得敏感的內容，請自己加在 `settings.md` 的 Sensitive data 底下。
- 讀不了的圖片會留在資料夾裡，讓你自己看。
- 日期先看檔名。連接器如果有回傳拍攝時間，其次用拍攝時間，最後才用 Drive 的建立時間。連接器會不會回傳拍攝時間，目前還沒驗證過。
- 重複執行不會有問題，因為處理完的圖片已經離開資料夾。

## 升級，以及在雲端或手機上執行

這兩件事和核心 skill 的做法一樣，請看 [agent-inbox README](../README.zh-TW.md) 的「[升級到新版本](../README.zh-TW.md#升級到新版本)」與「[在雲端或手機上執行](../README.zh-TW.md#在雲端或手機上執行)」。

## 授權

MIT，見 repo 根目錄的 [LICENSE](../../../LICENSE)。
