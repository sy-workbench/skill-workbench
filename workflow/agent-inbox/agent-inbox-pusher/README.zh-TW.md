# agent-inbox-pusher

版本 1.3，最後更新 2026-11-12。屬於 [agent-inbox](../README.zh-TW.md)。

把目前 session 的討論存成 Notion Agent Inbox 裡的一條事項，讓另一個 agent（或換了裝置的你）之後能接手。也可以不經過 Notion，直接產生一段 prompt，貼進新的 session（模式 B）。它做什麼、要說哪些觸發詞、需求、設定、升級，以及在雲端或手機上執行，都寫在 [agent-inbox README](../README.zh-TW.md)。

## 補充

- 模式 A（寫進 Notion）：skill 會先給你看一份草稿，分成四段（Background / Problem / Resolution / Next Step），並附上 Type 和 Handover To。你確認後，它才會寫進 Notion。
- 模式 B（貼 prompt）：skill 會印出一個 code block，讓你貼進新的 session，不會寫入任何東西。

## 授權

MIT，見 repo 根目錄的 [LICENSE](../../../LICENSE)。
