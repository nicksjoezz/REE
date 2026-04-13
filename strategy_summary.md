# Profit-Optimized Volume Strategy Summary

## Overview
A high-frequency trading strategy for BTCUSDT on the 1-minute timeframe, optimized for **Total PnL** and **Profit Factor**. It identifies trade-volume spikes and candle wicks (rejections) while allowing profitable trades to run further using wider exit parameters.

## Timeframe
- 1 Minute (1m)

## Indicators
- **Trades**: Number of trades per 1-minute candle.
- **ATR (14)**: Used as a volatility filter.
- **Wicks (Spikes)**: Percentage of the high/low relative to the candle body.

## Entry Conditions (Signal candle N-1, Entry at open of candle N)

### Long Entry
- **Signal Candle Criteria**:
  - `Lower Wick > 0.10%` (rejection from below)
  - `Upper Wick < 0.05%` (minimal rejection from above)
  - `Body > -0.50%` (avoid massive red candles)
  - `Number of Trades > 1000`
  - `Previous Trades < 1000`
  - `ATR(14) < 100`

### Short Entry
- **Signal Candle Criteria**:
  - `Upper Wick > 0.10%` (rejection from above)
  - `Lower Wick < 0.05%` (minimal rejection from below)
  - `Body < 0.50%` (avoid massive green candles)
  - `Number of Trades > 1000`
  - `Previous Trades < 1000`
  - `ATR(14) < 100`

## Exit Conditions & Risk Management
- **Initial Stop Loss**: **0.50%** from entry price.
- **Move to Breakeven**: When price reaches **+0.80%** profit (Wider trigger to allow for volatility).
- **Trailing Stop**: **0.40%** trailing offset (Wider trail to capture larger moves).
- **Position Sizing**: 2% of balance at risk per trade ($20 risk initially).
