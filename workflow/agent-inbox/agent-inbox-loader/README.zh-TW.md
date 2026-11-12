# agent-inbox-loader

版本 1.2，最後更新 2026-11-12。屬於 [agent-inbox](../README.zh-TW.md)。

把 Notion Agent Inbox 裡的一條事項讀進目前的 agent session，讓你接著做在別處開始的工作。它做什麼、要說哪些觸發詞、需求、設定、升級，以及在雲端或手機上執行，都寫在 [agent-inbox README](../README.zh-TW.md)。

## 補充

- `read inbox: <標題>`：直接讀那個標題的事項。
- 說「`let's continue the <topic> discussion`」也可以，skill 會去找對應的事項。
- 讀入後，agent 會先給你一段簡短摘要，然後等你。你確認之前它不會開始動手。

## 選用：自動檢查 Inbox

這個 skill 只有在你開口時才讀內容。想要自動檢查的話，有兩種做法。

**每次開 session 時檢查**：在每個 agent 自己的指令檔加上類似這段：

```
## Session 開場：Agent Inbox 檢查
開場時查詢 Agent Inbox 的 Active 檢視。
列出 Handover To 是「<這個 agent 的角色名稱>」的事項，以及 Handover To 是空的事項。
只顯示 Title、Date、Status。我沒要求就不要讀完整內容。
```

**定時檢查**：設定一個排程任務定時去處理。

## 授權

MIT，見 repo 根目錄的 [LICENSE](../../../LICENSE)。
