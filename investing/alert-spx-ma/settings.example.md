# Settings for alert-spx-ma

How to use this file: copy it, rename the copy to `settings.md` (same folder), and fill in the copy. Do not edit this example, so that updating the skill can replace it safely. This skill's README in the skill-workbench repo explains each value.

**Threshold** (under "The rule") is required: the skill stops until you fill it in. Everything else is optional; delete a line, or leave it as it is, to use the default.

## What to watch

Symbol to watch (default `SPX`, the S&P 500 index):
Symbol: <YOUR_SYMBOL>

Security type, as your price source names it (default `IND` for an index; an ETF or stock is usually `STK`):
Security type: <YOUR_SECURITY_TYPE>

Exchange the symbol trades on (default `CBOE`):
Exchange: <YOUR_EXCHANGE>

## The rule

Length of the simple moving average, in trading days (default `50`):
Moving average days: <YOUR_MA_DAYS>

Required. How close to the average counts as a pullback, in percent above it (no default; choose your own):
Threshold: <YOUR_THRESHOLD_PERCENT>

Months in which to buy anyway, as month numbers separated by commas (default: none, which turns this condition off):
Fallback months: <YOUR_FALLBACK_MONTHS>

Time zone used to decide the current month, as an IANA name such as `America/New_York` (default: your local time zone if the agent knows it, otherwise UTC):
Time zone: <YOUR_TIME_ZONE>

## Data

Where daily closes come from: `IBKR` for the Interactive Brokers connector, or the name of another connector or tool your agent has (default `IBKR`):
Price source: <YOUR_PRICE_SOURCE>
