# Volume Strategy Summary

## Overview
A high-frequency trading strategy for BTCUSDT on the 1-minute timeframe, focusing on volume spikes and candle wicks (rejections) in low-volatility environments.

## Timeframe
- 1 Minute (1m)

## Indicators
- **Volume**: BTC Volume per candle.
- **ATR (14)**: Used as a volatility filter.
- **Wicks (Spikes)**: Percentage of the high/low relative to the candle body.

## Entry Conditions

### Long Entry (at the open of the candle following the signal candle)
- **Signal Candle Criteria**:
  - `Lower Wick > 0.10%` (rejection from below)
  - `Upper Wick < 0.05%` (minimal rejection from above)
  - `Body > -0.50%` (not a massive red candle)
  - `Volume > 2000 BTC`
  - `Previous Volume < 1000 BTC`
  - `ATR(14) < 50-100` (Low volatility environment)

### Short Entry (at the open of the candle following the signal candle)
- **Signal Candle Criteria**:
  - `Upper Wick > 0.10%` (rejection from above)
  - `Lower Wick < 0.05%` (minimal rejection from below)
  - `Body < 0.50%` (not a massive green candle)
  - `Volume > 2000 BTC`
  - `Previous Volume < 1000 BTC`
  - `ATR(14) < 50-100`

## Exit Conditions & Risk Management
- **Initial Stop Loss**: 0.40% - 0.50% from entry price.
- **Move to Breakeven**: When price reaches +0.30% profit.
- **Trailing Stop**: Activated when price reaches +0.30%. (In the PDF, it mentions trailing above/below previous highs/lows or using a fixed tick offset).
- **Position Sizing**: 2% of balance per trade (as per user request).

## Filters
- **ATR Filter**: Avoid entries when ATR is too high (above 50-100).
- **Volume Filter**: Entry only on high volume relative to the previous candle.
- **Directionality**: Performs best when price lateralizes or breaks a previous low/high without a strong trend.
