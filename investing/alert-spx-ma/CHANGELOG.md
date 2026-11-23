# Changelog

## 1.1 (2026-11-24)
- Removed the fallback months condition and the time zone setting, which was only used for it. The skill now checks one condition: the pullback. If your `settings.md` still has `Fallback months` or `Time zone` lines, they are ignored and you can delete them.

## 1.0 (2026-11-23)
- Initial public release.
- Checks two entry conditions for a long-term index position: the latest close is within a set percentage of its simple moving average (pullback), or the current month is one of your fallback months (buy anyway).
- The moving average is 50 days by default; any length can be set in `settings.md`.
- Fetches daily closes and computes the average on every run, so it keeps no files or state.
- Uses the Interactive Brokers connector by default; any tool that returns daily closes can replace it.
- Drops a still-moving bar when the market is open, and stops instead of averaging when too few bars come back.
- Symbol, average length, threshold, fallback months, time zone and price source live in `settings.md`. Threshold is required and has no default; everything else is optional. Fallback months have no suggested values; you choose them.
- Reports only. It never places orders.
