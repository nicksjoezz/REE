# Volume Strategy Backtest Report

## Strategy Overview
This strategy aims to capture short-term price reactions (0.20% - 1.00%) on the BTCUSDT 1-minute timeframe by identifying volumetric spikes accompanied by price rejection wicks in low-volatility environments.

## Entry Conditions (Used in Backtest)
- **Volume**: > 500 BTC (Adjusted from 2000 BTC in PDF to capture trades in current market conditions).
- **Previous Volume**: < 1000 BTC.
- **Wick (Spike)**: > 0.05% rejection from high/low.
- **Opposite Wick**: < 0.03% (Minimal rejection from opposite side).
- **Body**: < 0.50% (To avoid high-momentum trend candles).
- **ATR (14)**: < 100 (To filter for low-volatility environments).

## Exit & Risk Management
- **Initial Stop Loss**: 0.45% from entry.
- **Position Sizing**: 2% of balance at risk per trade.
- **Move to Breakeven**: When profit reaches +0.30%.
- **Trailing Stop**: Tighter trailing stop activated after reaching breakeven.

## Historical Data
- **Period**: 6 months (Oct-Dec 2021 and Jan-Mar 2024).
- **Total Candles**: ~260,000 minutes.

## Backtest Results
Refer to `metrics.md` for the final statistics.
- **Initial Balance**: $1000
- **Final Balance**: $874.38
- **Win Rate**: 40.74% (11 wins, 16 losses)
- **Max Drawdown**: 16.36%

## Conclusion
The strategy shows potential in specific lateral market conditions but experienced a drawdown during the tested periods. The requirement for very high volume spikes (>2000 BTC) is rare in modern 1-minute BTCUSDT data, necessitating the slightly lower threshold used to gather a meaningful trade sample.
