# agent-inbox

agent-inbox-pusher 和 agent-inbox-loader 是一組工具可以搭配使用。這兩個 skills 的目的是讓我可以快速的把工作從一個 agent 或 session 交接給另一個。做法是透過在 Notion 裡創建的一個 Agent Inbox 的資料庫：agent-inbox-pusher 負責把討論按照規定格式存進去，agent-inbox-loader 負責讀取交接內容。

agent-inbox-pusher 還有另一種用法，叫模式 B：不經過 Notion，直接產生一段 prompt，讓你可以快速複製貼上進新的 session 接著討論或執行。模式 B 不需要資料庫，也不用安裝 agent-inbox-loader。

想用 Notion 的方式的話，要先準備好資料庫和幾項設定，需要的東西寫在下面的「設定」。只用模式 B 的話，安裝 agent-inbox-pusher 就好，不需要任何設定。

## 這一組有哪些 skills

| Skill | 做什麼 |
|---|---|
| [agent-inbox-pusher](agent-inbox-pusher/README.zh-TW.md) | 把目前的討論存成 Agent Inbox 裡的一條事項，或產生一段 prompt，讓你貼進新的 session |
| [agent-inbox-loader](agent-inbox-loader/README.zh-TW.md) | 列出 Agent Inbox 裡等待這個 agent 處理的事項，讀入其中一條（只有一條指派給它時會直接讀入），並標記成已接手 |

## 怎麼搭配

1. 在舊的 session 裡，對 agent 說 `push to inbox`。它會把討論存成一條事項，並記下這條要交給哪個 agent。
2. 到新的 session 或另一個 agent，說 `read inbox`。它會看這兩種事項：指派給它的，以及還沒有指派對象的。
3. 如果指派給它的剛好只有一條，它會直接讀入，並標記成已接手，再給你一段簡短摘要。有好幾條事項的話，它會列出清單，問你要先處理哪一條。
4. 還沒有指派的事項也會列出來，但 agent 不會自己認領，你開口它才會接。
5. 讀完之後，agent 會等你點頭才開始動手。

觸發動作的關鍵詞：

| 動作 | 說這句 | 哪個 skill |
|---|---|---|
| 把討論存進 Notion | `push to inbox` / `save to inbox` / `sync to inbox` | agent-inbox-pusher |
| 產生一段 prompt，貼進新的 session（模式 B） | `provide a prompt` / `handoff prompt` / `prompt for the new session` | agent-inbox-pusher |
| 讀取等這個 agent 處理的事項 | `read inbox` / `read notion inbox` | agent-inbox-loader |

像 `handoff`、`new session`、`let's talk about this later` 這類說法，兩種模式都說得通，pusher 會先問一次：要產生 prompt，還是存進 Inbox。

## 需求

- 安裝好 skill（含 `SKILL.md` 的資料夾），以及設定好 Notion MCP，也就是讓 agent 能讀寫 Notion 的功能。
- 一個可以建立資料庫的 Notion 工作區。

## 設定

**只想用模式 B**：把 `agent-inbox-pusher` 資料夾複製到你的 agent 的 skills 目錄，目錄位置依工具而定。之後在任何對話裡說 `provide a prompt` 就能用。不需要 Notion，也不用設定。

**要連 Notion**：把你要用的 skill 資料夾複製到 agent 的 skills 目錄（位置依工具而定），再準備好下面這些東西。怎麼準備都可以，也可以請你的 agent 執行。

pusher 和 loader 兩個 skill 都需要用到的：

- 一個叫「Agent Inbox」的 Notion 資料庫，欄位參照 [`inbox-database.md`](agent-inbox-pusher/references/inbox-database.md)。
- 在資料庫 `Handover To` 欄位裡，替每個 agent 角色新增一個選項（例如 `Writer`、`Researcher`），可以考慮再加一個給你自己（依你工作習慣決定）。
- 資料庫的 data source ID，是一串以 `collection://` 開頭的文字。

只有 agent-inbox-loader 需要用到的：

- 一個叫「Active」的資料庫檢視：篩選 Status 是 Pending 或 Picked Up，依 Date 由新到舊排序。
- 這個檢視的網址，裡面含有 `?v=`。

每個 agent 都需要用到的：

- 在它自己的指令檔寫明角色名稱，例如「你在 Agent Inbox 的角色名稱是 Writer」。名稱要和 `Handover To` 的某個選項完全一致。

最後，在每個 skill 資料夾裡，把 `settings.example.md` 複製成 `settings.md`，填入上面的值。不要直接改 example 檔。

## 附加 skill (Add-ons)

這裡列出其他可選用搭配的 skill（目前只有一個）。這些 skill 會把事項寫進和核心 skill 同一個 Agent Inbox 資料庫，讓 agent 可以調用 loader 去讀取和處理。

| 附加 skill | 多了什麼功能 | 還需要什麼 |
|---|---|---|
| [agent-inbox-screenshot-intake](agent-inbox-screenshot-intake/README.zh-TW.md) | 把你丟進 Google Drive 資料夾的截圖，變成 Agent Inbox 裡的事項，並交給適合處理的 agent | Google Drive，以及資料庫裡多一個 `Source` 欄位 |

## 升級到新版本

換掉 skill 資料夾時，你的 `settings.md` 可能會一起被刪掉。升級前先把它複製到其他地方，升級完再搬回來。

如果新版需要新的設定，`CHANGELOG.md` 會寫明，skill 也會停下來，告訴你缺哪一項。

## 在雲端或手機上執行

有些環境，例如雲端排程和手機 app，只會保存 `SKILL.md`，讀不到 `settings.md`。這種情況下，把填好的 `settings.md` 內容貼到 `SKILL.md` 的最後面，標題用 `## Settings (pasted)`。每個 skill 各貼自己的。skill 找不到檔案時，會改讀這一段。

升級會換掉 `SKILL.md`，所以每次升級後都要重貼一次。

## 授權

MIT，見 repo 根目錄的 [LICENSE](../../LICENSE)。
