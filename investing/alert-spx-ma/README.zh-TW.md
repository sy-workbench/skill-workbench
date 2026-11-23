# alert-spx-ma

[English](README.md) | 繁體中文 | [简体中文](README.zh-CN.md)

版本 1.0，最後更新 2026-11-23。

分批建立長期的指數部位，就得每隔幾天看一次線圖，判斷「現在」是不是好時機。這個 skill 幫你做這件事：指數回到 50 日均線附近時告訴你；另外有一個保底機制，如果市場一路漲、遲遲不回檔，一年中你自己選的幾個月份照樣買，不會一直空等。設成排程之後，「今天要不要看盤？」就變成一份簡短的報告。

它只回報，不會下單，內容也不構成投資建議：數字由你自己決定。

## 需求

- 一個 agent 可以用來查每日收盤價的工具。預設是 Interactive Brokers（IBKR）連接器，需要 IBKR 帳戶。其他能回傳你那檔標的每日收盤價的連接器或工具也可以。

另外有一個數字要你自己決定：門檻（見設定）。其他都有預設值。

## 設定

把這個 skill 資料夾複製到 agent 的 skills 目錄（位置依工具而定）。

接著把 `settings.example.md` 在同一個資料夾複製成 `settings.md` 並填寫。有一項必填：

- 門檻：離均線多近算回檔，用高於均線的百分比表示。填 N 就代表收盤價最多比均線高 N% 才算數。沒有預設值，沒填之前 skill 會停下來請你設定。

其餘是選填，都有預設值：

- 標的、證券類型、交易所：要看哪一檔。預設是 S&P 500 指數（`SPX`，類型 `IND`，在 `CBOE`）。要看 ETF（例如追蹤 S&P 500 的基金），填它的代號、類型 `STK` 和它的交易所。
- 均線天數：簡單移動平均的長度，單位是交易日。預設 `50`，想看別的均線就填其他天數。
- 保底月份：哪些月份照樣買，用月份數字、以逗號分隔。月份由你自己決定，skill 不提供建議值。預設關閉。
- 時區：判斷保底條件時「現在是幾月」用的時區，填 IANA 名稱，例如 `Europe/London`、`America/New_York`。預設用 agent 知道的你的當地時區，不知道時用 UTC，在月初或月底可能差一天。
- 價格來源：`IBKR`，或其他 agent 能用來查每日收盤價的工具名稱。

## 用法

問 `is SPX near the MA50?` 或 `is it time to buy?`。agent 會抓最新的每日收盤價、算出均線、檢查兩個條件，寫出像這樣的報告：

```
SPX MA50 entry check
- Date checked: 2026-11-14
- Latest close (2026-11-13): 6,812.40 (source: IBKR)
- 50-day average: 6,745.00
- Distance from the average: +1.00% (above)
Conditions:
- Pullback (within <your threshold>% of the average): met
- Fallback month (<your months>): not met
Result: Entry signal is on. Consider your next planned purchase.
```

（上面的數字是虛構的。）

想不用問就收到通知，在 agent 裡設一個排程任務，在交易日收盤後執行這個 skill。

## 補充

- 這個 skill 不保存任何檔案。每次執行都重新抓價格、自己算均線，沒有東西需要維護。
- 如果市場還沒收盤，最新那根 K 棒還不是收盤價。skill 會改用前一天的收盤價，並在報告中註明。
- 價格來源回傳的天數不夠時，skill 會停下來，不會用比較少的天數硬算，所以你看到的一定是真正的 N 日均線。
- 它不會改用新聞或記憶裡的價格。沒有可用的價格工具時，會直接告訴你。

## 升級到新版本

換掉 skill 資料夾時，你的 `settings.md` 可能會一起被刪掉。升級前先複製到其他地方，升級完再搬回來。

如果新版需要新的設定，`CHANGELOG.md` 會寫明。

## 在雲端或手機上執行

雲端排程和手機 app 常常只保存 `SKILL.md`，讀不到 `settings.md`。把 `settings.md` 的內容貼到 `SKILL.md` 最後面，標題用 `## Settings (pasted)`。升級會換掉 `SKILL.md`，所以每次升級後都要重貼。價格連接器在那個環境裡也要能用。

## 授權

MIT 授權，見 repo 根目錄的 [LICENSE](../../LICENSE)。
