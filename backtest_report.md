# Optimized Volume Strategy Backtest Report

## Strategy Overview
This strategy aims to capture short-term price reactions on the BTCUSDT 1-minute timeframe. It has been optimized using a grid search to maximize win rate and minimize drawdown by identifying higher-confidence rejection signals.

## Optimized Parameters
- **Trades**: > 1000 per minute.
- **Previous Trades**: < 1000 per minute.
- **Wick (Spike)**: > 0.12% rejection.
- **Opposite Wick**: < 0.05%.
- **ATR (14)**: < 80.

## Optimized Exit & Risk Management
- **Initial Stop Loss**: 0.60% (Increased from 0.45% to allow for more breathing room).
- **Move to Breakeven**: When profit reaches +0.20%.
- **Trailing Stop**: 0.1% trailing.

## Historical Data
- **Period**: 6 months (Oct 2023 - Mar 2024).

## Optimized Backtest Results
- **Win Rate**: 74.69% (121 wins, 41 losses).
- **Number of Trades**: 162.
- **Max Drawdown**: 11.88%.

## Conclusion
The optimized parameters significantly improved the strategy's stability and win rate. By raising the trade count and spike thresholds, we filtered out weaker signals, leading to more reliable reversal captures. The increased stop-loss distance (0.60%) combined with an earlier breakeven trigger (0.20%) proved effective in protecting capital while capturing the 0.30%+ reactions common to this setup.
