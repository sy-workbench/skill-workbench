# alert-spx-ma

English | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

Version 1.0. Last updated 2026-11-23.

Building a long-term index position in batches means asking, every few days, whether "now" is a good time, and checking the chart to find out. This skill does the checking. It says when the index has pulled back to near its 50-day moving average, and it has a fallback: if the market keeps rising and never pulls back, you still buy in a few months of the year that you choose, instead of waiting forever. Run on a schedule, it turns "should I look at the chart today?" into a short report.

It only reports. It never places orders, and nothing in it is investment advice: the numbers are yours to choose.

## Requirements

- A tool your agent can use to get daily closing prices. By default this is the Interactive Brokers (IBKR) connector, which needs an IBKR account. Any other connector or tool that returns daily closes for your symbol works too.

You also need to choose one number yourself, the threshold (see Setup). Everything else has a default.

## Setup

Copy this skill folder into your agent's skills directory (the directory depends on your tool).

Then copy `settings.example.md` to `settings.md` in the same folder and fill it in. One value is required:

- Threshold: how close to the average counts as a pullback, as a percentage above it. If you set N, the close has to be at most N% above the average to count. There is no default; the skill stops and asks until you set it.

The rest are optional and have defaults:

- Symbol, security type and exchange: what to watch. The default is the S&P 500 index (`SPX`, type `IND`, on `CBOE`). For an ETF such as an S&P 500 fund, use its ticker, type `STK` and its exchange.
- Moving average days: the length of the simple moving average, in trading days. Default `50`; set another number to watch a different average.
- Fallback months: the months in which you buy anyway, written as month numbers separated by commas. Pick your own; the skill has no suggested months. Off by default.
- Time zone: used to decide which month it is for the fallback condition, as an IANA name such as `America/New_York` or `Europe/London`. By default the agent uses your local time zone if it knows it, otherwise UTC, which can be a day off at the start or end of a month.
- Price source: `IBKR`, or the name of another tool your agent can use for daily closes.

## Usage

Ask "is SPX near the MA50?" or "is it time to buy?". The agent fetches the latest daily closes, computes the average, checks both conditions and writes a report like this:

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

(The numbers above are made up.)

To be told without asking, set up a scheduled task in your agent that runs the skill after the market closes on trading days.

## Good to know

- The skill keeps no files. Each run fetches fresh prices and computes the average itself, so there is nothing to maintain.
- If the market is still open, the latest bar is not a close yet. The skill uses the previous day's close and says so.
- If the price source returns too few days, the skill stops instead of averaging fewer days, so the number you see is always a real N-day average.
- It never falls back to prices from news or memory. If no price tool is available, it says so.

## Upgrading to a new version

Replacing the skill folder can erase your `settings.md`. Copy it to another place before you upgrade, and move it back afterwards.

If a new version needs a new setting, `CHANGELOG.md` says so.

## Running in the cloud or on a phone

Scheduled cloud runs and phone apps often keep only `SKILL.md` and cannot read `settings.md`. Paste the contents of your `settings.md` at the end of `SKILL.md` under the heading `## Settings (pasted)`. Upgrading replaces `SKILL.md`, so paste the settings again after each upgrade. The price connector also has to be available in that environment.

## License

MIT, see the [LICENSE](../../LICENSE) at the repo root.
