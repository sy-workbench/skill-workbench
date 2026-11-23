# alert-spx-ma

[English](README.md) | [繁體中文](README.zh-TW.md) | 简体中文

版本 1.0，最后更新 2026-11-23。

分批建立长期的指数仓位，就得每隔几天看一次走势图，判断“现在”是不是好时机。这个 skill 帮你做这件事：指数回到 50 日均线附近时告诉你；另外有一个保底机制，如果市场一路涨、迟迟不回调，一年中你自己选的几个月份照样买，不会一直空等。设成定时任务之后，“今天要不要看盘？”就变成一份简短的报告。

它只汇报，不会下单，内容也不构成投资建议：数字由你自己决定。

## 需求

- 一个 agent 可以用来查每日收盘价的工具。默认是 Interactive Brokers（IBKR）连接器，需要 IBKR 账户。其他能返回你那只标的每日收盘价的连接器或工具也可以。

另外有一个数字要你自己决定：阈值（见设置）。其他都有默认值。

## 设置

把这个 skill 文件夹复制到 agent 的 skills 目录（位置依工具而定）。

接着把 `settings.example.md` 在同一个文件夹复制成 `settings.md` 并填写。有一项必填：

- 阈值：离均线多近算回调，用高于均线的百分比表示。填 N 就代表收盘价最多比均线高 N% 才算数。没有默认值，没填之前 skill 会停下来请你设置。

其余是可选，都有默认值：

- 标的、证券类型、交易所：要看哪一只。默认是 S&P 500 指数（`SPX`，类型 `IND`，在 `CBOE`）。要看 ETF（例如追踪 S&P 500 的基金），填它的代码、类型 `STK` 和它的交易所。
- 均线天数：简单移动平均的长度，单位是交易日。默认 `50`，想看别的均线就填其他天数。
- 保底月份：哪些月份照样买，用月份数字、以逗号分隔。月份由你自己决定，skill 不提供建议值。默认关闭。
- 时区：判断保底条件时“现在是几月”用的时区，填 IANA 名称，例如 `Europe/London`、`America/New_York`。默认用 agent 知道的你的当地时区，不知道时用 UTC，在月初或月底可能差一天。
- 价格来源：`IBKR`，或其他 agent 能用来查每日收盘价的工具名称。

## 用法

问 `is SPX near the MA50?` 或 `is it time to buy?`。agent 会抓最新的每日收盘价、算出均线、检查两个条件，写出像这样的报告：

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

（上面的数字是虚构的。）

想不用问就收到通知，在 agent 里设一个定时任务，在交易日收盘后运行这个 skill。

## 补充

- 这个 skill 不保存任何文件。每次运行都重新抓价格、自己算均线，没有东西需要维护。
- 如果市场还没收盘，最新那根 K 线还不是收盘价。skill 会改用前一天的收盘价，并在报告中注明。
- 价格来源返回的天数不够时，skill 会停下来，不会用比较少的天数硬算，所以你看到的一定是真正的 N 日均线。
- 它不会改用新闻或记忆里的价格。没有可用的价格工具时，会直接告诉你。

## 升级到新版本

换掉 skill 文件夹时，你的 `settings.md` 可能会一起被删掉。升级前先复制到其他地方，升级完再搬回来。

如果新版需要新的设置，`CHANGELOG.md` 会写明。

## 在云端或手机上运行

云端定时任务和手机 app 常常只保存 `SKILL.md`，读不到 `settings.md`。把 `settings.md` 的内容贴到 `SKILL.md` 最后面，标题用 `## Settings (pasted)`。升级会换掉 `SKILL.md`，所以每次升级后都要重贴。价格连接器在那个环境里也要能用。

## 授权

MIT 授权，见 repo 根目录的 [LICENSE](../../LICENSE)。
