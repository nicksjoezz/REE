# Volume Strategy Backtest Report

## Strategy Overview
This strategy aims to capture short-term price reactions on the BTCUSDT 1-minute timeframe by identifying spikes in number of trades accompanied by price rejection wicks.

## Strategy Variations Tested

### Option 1: Profit-Optimized (Dynamic Exit)
Uses dynamic targets (0.80% breakeven trigger, 0.40% trailing stop).
- **Net Profit**: +$1520.99
- **Number of Trades**: 277
- **Win Rate**: 46.21%

### Option 2: 15-Candle Fixed Exit
Exits exactly at the close of the 15th candle after entry.
- **Net Profit**: +$169.24
- **Number of Trades**: 342
- **Win Rate**: 53.80%

## Historical Data
- **Period**: 6 months (Oct 2023 - Mar 2024).
- **Total Candles**: 263,520 minutes.

## Conclusion
The **Profit-Optimized Dynamic Exit** (Option 1) significantly outperforms the fixed time-based exit (Option 2) in terms of total PnL, although Option 2 maintains a higher win rate. The dynamic exit allows the strategy to capture larger trend extensions following the initial volume spike.
