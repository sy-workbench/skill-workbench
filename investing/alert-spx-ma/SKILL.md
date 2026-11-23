---
name: "alert-spx-ma"
version: "1.1"
updated: "2026-11-24"
description: "Check whether the S&P 500 index (SPX), or another symbol you set, has pulled back to near its moving average (50-day by default), then write a short entry-signal report. Use when run on a schedule, or when the user asks things like \"is SPX near the MA50?\", \"is it time to buy?\", or \"how far is SPX from its moving average?\"."
---

## Settings

Read `settings.md` in the same folder as this file. **Threshold** is required and has no default: if the file is missing, or **Threshold** is empty or still has the form `<YOUR_...>`, stop and ask the user to set it in `settings.md` (or the pasted block below). Never assume a value. Every other value is optional: if it is missing or still has the form `<YOUR_...>`, use the default below. If `settings.md` cannot be read in your environment (for example a scheduled cloud run that only stores this file), use the block headed `## Settings (pasted)` at the end of this file, if the user added one.

| Setting | Default |
|---|---|
| Symbol | `SPX` |
| Security type | `IND` (index) |
| Exchange | `CBOE` |
| Moving average days | `50` |
| Threshold | none, required (percent above the average) |
| Price source | `IBKR` (the Interactive Brokers connector) |

## Overview

A simple rule for adding to a long-term index position: buy on a pullback.

- **Pullback condition:** the latest close is no more than **Threshold** percent above its **Moving average days** simple moving average.

When the condition is met, the entry signal is on. The skill only reports; it never places orders and does not decide how much to buy.

The skill keeps no files or state. Every run fetches fresh prices and computes the average itself.

## Input format

- Trigger: a scheduled run, or the user asking about the signal.
- Optional in the question: a different symbol for this run. Use it for this run only; do not change `settings.md`.
- Needed: a tool that returns daily closing prices, named by **Price source**.

## Workflow

### Step 1: get daily closes

Fetch at least **Moving average days** + 2 daily bars, regular trading hours only.

With the Interactive Brokers connector (**Price source** `IBKR`):
1. `search_contracts` with the **Symbol** as the query. It cannot filter by type, so pick the row whose exchange matches **Exchange** and whose listed sections include **Security type**. Use its contract ID.
2. `get_price_history` with that contract ID, the **Exchange** and **Security type**, `step` = `ONE_DAY`, `step_count` = **Moving average days** + 2, `outside_rth` = false.

With any other source: use the equivalent call that returns daily closes for the same symbol. If no tool you have can return daily closes, stop and tell the user which kind of tool is missing. Do not estimate prices from news or memory.

### Step 2: pick the close and compute the average

1. If the last bar is dated today (in the exchange's own time zone) and the exchange has not reached its regular closing time yet (for `SPX` on `CBOE`, 16:00 America/New_York; for another exchange, use its own regular close), the bar is still moving. Drop it and use the previous bar as the latest close, and say so in the report.
2. The latest close and its date come from the last complete bar.
3. The moving average is the simple average of the last **Moving average days** complete closes, ending with that bar.
4. Distance = (close / average - 1) x 100, rounded to two decimals.

### Step 3: check the condition

- Pullback condition: close <= average x (1 + **Threshold** / 100).

### Step 4: write the report

Always write the report, whether or not the condition is met:

---

**{Symbol} MA{days} entry check**

- Date checked: YYYY-MM-DD
- Latest close (YYYY-MM-DD): X,XXX.XX (source: {Price source})
- {days}-day average: X,XXX.XX
- Distance from the average: +X.XX% (above) or -X.XX% (below)

**Condition:**
- Pullback (within {Threshold}% of the average): met / not met

**Result:**
- If it is met: Entry signal is on. Consider your next planned purchase.
- If it is not met: No signal yet. The close needs to fall about X.XX% to reach the threshold.

---

"About X.XX%" is the drop needed from the latest close to reach average x (1 + Threshold / 100).

### Edge Cases

- Fewer than **Moving average days** complete bars, after dropping a still-moving bar (a new listing, or a data gap): stop and report how many complete bars came back, instead of averaging fewer days.
- The latest complete bar is more than 5 calendar days old (a long holiday, or a stale feed): still report, but add a line saying how old the data is.
- `search_contracts` returns several matches: pick the one on **Exchange** whose sections include **Security type**. If none fits, list the candidates and ask the user.
- The connector needs a sign-in or returns an error: report the error and stop. Do not switch to another source on your own unless the user has set one.
- The user asks whether they *should* buy: the report states the conditions, not advice. Say the decision is theirs.

## Output files

None. The report is the reply. If a scheduled run must notify the user, that is set up in the scheduler, not here.

## Reference

- Simple moving average: the mean of the last N closing prices.
- Interactive Brokers connector tools used: `search_contracts`, `get_price_history`.

## Dependencies

- A connector or tool that returns daily closing prices. The default is the Interactive Brokers connector, which needs an IBKR account.
