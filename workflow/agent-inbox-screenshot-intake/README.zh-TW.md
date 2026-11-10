# agent-inbox-screenshot-intake

版本 1.1，最後同步 2026-11-10。屬於 [skill-workbench](../../README.zh-TW.md)。非官方作品，與 Anthropic 無關。

在手機上看到值得留的東西，截個圖，然後就忘了。這個 skill 專門清這堆圖。它會讀 Google Drive 某個資料夾裡的鬆散截圖，判斷每張在講什麼，在 Notion Agent Inbox 建一筆條目，分派給該處理的 agent，再把原圖用看得懂的名字搬進 `_archive`。同一篇貼文分成好幾張截的，會合成一筆。

它和 [agent-inbox-loader](../agent-inbox-loader/README.zh-TW.md)、[agent-inbox-pusher](../agent-inbox-pusher/README.zh-TW.md) 共用同一個 Notion 資料庫。

## 需求

- 能載入 skill（含 `SKILL.md` 的資料夾）、並且開啟 Google Drive 與 Notion MCP 連接器的 agent。我是用 Claude 建置與測試，其他讀 `SKILL.md` 的 agent 可能也能用，但沒有測過。
- 一個可以建立資料庫的 Notion 工作區。
- 一個用來放截圖的 Google Drive 資料夾。

## 設定

以下每步只需做一次。

1. 建立 Agent Inbox 資料庫。照 [loader README](../agent-inbox-loader/README.zh-TW.md) 設定的第 1 到 3 步做。已經做過就跳過。
2. 在那個資料庫再加一個欄位：`Source`，類型是 URL。這個 skill 會把原圖的連結寫在這裡。
3. 在 Google Drive 建一個放截圖的資料夾，例如「Screenshot Inbox」。
4. 在裡面建一個名稱叫 `_archive` 的子資料夾。處理完的圖會搬到這裡，主資料夾才不會越堆越多，需要時也找得回原圖。
5. 取得兩個資料夾的 ID。在 Drive 打開資料夾，看網址列，`/folders/` 後面那串就是 ID。
6. 請你的 agent 說：「用 Notion 工具讀這個資料庫，告訴我它的 data source ID。」應該會得到一串以 `collection://` 開頭的文字。
7. 把這個 skill 資料夾複製到你的 agent 的 skills 目錄，目錄位置依工具而定。
8. 在 skill 資料夾裡，把 `settings.example.md` 複製成 `settings.md`，填入必填的值：第 5 步的兩個資料夾 ID、第 6 步的 data source ID、你的時區。不要直接改 example 檔。要確認沒有漏填，在 skill 資料夾執行 `grep -n '<YOUR_' settings.md`，應該什麼都不會印出來。
9. 在 `settings.md` 把分派表改成你自己的 agent，名稱必須和 `Handover To` 欄位的選項一致。如果你的手機截圖檔名格式不同，也改一下檔名日期樣式；有自己的敏感資料規則，加在 Sensitive data 底下。
10. 用一張無關緊要的截圖測試：丟進資料夾，對 agent 說「process the screenshot inbox」。應該會看到 Notion 多一筆條目，圖片已經在 `_archive`，名稱也改了。這個 skill 的觸發詞是英文，中文說法通常也能觸發，但沒有測過；想固定用中文，可以在 `SKILL.md` 的 description 加上你的說法。

## 用法

- 請 agent 處理截圖 inbox，它會處理資料夾根目錄的所有圖，然後回報做了什麼。
- 想定時執行，就在你的 agent 工具設一個排程任務，送出同樣的請求。排程要能跑的前提是，你的工具允許 Drive 與 Notion 連接器在沒人看著時運作，而且排程通常讀不到 `settings.md`，請看下面「在雲端或手機上執行」。

## 注意事項

- 截圖可能含有隱私資訊。寫入 Notion 前，這個 skill 會把精確的金額、帳戶資訊、證件資訊改寫成相對描述，但請在 `settings.md` 的 Sensitive data 加上符合你自己定義的規則。
- 讀不懂的圖會留在資料夾，讓你自己看。
- 日期優先取自檔名。如果你的連接器也能回傳拍攝時間，次選用拍攝時間，再來是 Drive 建立時間。連接器是否回傳拍攝時間，目前沒有驗證過。
- 重複執行是安全的，處理完的圖已經離開資料夾。

## 更新

把新版檔案複製到原本的 skill 資料夾上覆蓋。不要先刪掉資料夾，否則你的 `settings.md` 也會一起消失。`SKILL.md` 與 `settings.example.md` 可以直接覆蓋。新版如果需要新的設定，`CHANGELOG.md` 會註明，skill 也會停下來告訴你缺哪一項。

## 在雲端或手機上執行

有些環境（雲端排程、手機 app）只存 `SKILL.md`，讀不到 `settings.md`。這種情況，把填好的 `settings.md` 內容貼到 `SKILL.md` 最後面，標題用 `## Settings (pasted)`。skill 讀不到檔案時會改用這一段。更新會換掉 `SKILL.md`，所以更新後要重貼一次。

## 檔案

| 檔案 | 用途 |
|---|---|
| `settings.example.md` | 要你填的值。複製成 `settings.md` 再填 |
| `SKILL.md` | skill 本體，含分派表 |
| `references/inbox-database.md` | 資料庫欄位、狀態定義、處理原則、角色說明（英文） |
| `CHANGELOG.md` | 版本紀錄（英文） |
| `README.md` | 英文 README |

## 授權

MIT，見 repo 根目錄的 [LICENSE](../../LICENSE)。
