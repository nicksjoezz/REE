# Volume Strategy Backtest Report

## Strategy Overview
This strategy aims to capture short-term price reactions (0.20% - 1.00%) on the BTCUSDT 1-minute timeframe by identifying spikes in number of trades accompanied by price rejection wicks in low-volatility environments.

## Entry Conditions (Used in Backtest)
- **Trades**: > 500 per minute.
- **Previous Trades**: < 1000 per minute.
- **Wick (Spike)**: > 0.10% rejection from high/low.
- **Opposite Wick**: < 0.05% (Minimal rejection from opposite side).
- **Body**: < 0.50% (To avoid high-momentum trend candles).
- **ATR (14)**: < 100 (To filter for low-volatility environments).

## Exit & Risk Management
- **Initial Stop Loss**: 0.45% from entry.
- **Position Sizing**: 2% of balance at risk per trade ($20 risk initially).
- **Move to Breakeven**: When profit reaches +0.30%.
- **Trailing Stop**: 0.1% trailing activated after reaching breakeven.

## Historical Data
- **Period**: 6 months (Oct 2023 - Mar 2024).
- **Total Candles**: 263,520 minutes.

## Backtest Results
Refer to `metrics.md` for the final statistics.
- **Initial Balance**: $1000
- **Final Balance**: $803.35
- **Number of Trades**: 331
- **Win Rate**: 58.31% (193 wins, 138 losses)
- **Max Drawdown**: 35.19%

## Conclusion
The strategy generates a high trade frequency (~55 trades per month) during the tested 6-month period. While the win rate is relatively high (58.31%), the risk-reward ratio and drawdown suggest that the strategy's performance is sensitive to the 0.1% trailing stop. The number of trades (331) aligns with the expectation of a high-frequency reversal strategy.
