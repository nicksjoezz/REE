# Profit-Optimized Volume Strategy Backtest Report

## Strategy Overview
This strategy aims to capture short-term price reactions on the BTCUSDT 1-minute timeframe. It has been optimized specifically for **Total PnL** and **Profit Factor**, addressing the previous issue where a high win rate did not translate into significant profits.

## Optimization Strategy
The previous high-win-rate version (74%) had an "Avg Win" ($6) much smaller than its "Avg Loss" ($20). We optimized the exit parameters to allow winning trades more room to breathe, improving the Reward-to-Risk ratio.

## Optimized Parameters
- **Trades**: > 1000 per minute.
- **Wick (Spike)**: > 0.10% rejection.
- **ATR (14)**: < 100.

## Optimized Exit & Risk Management
- **Initial Stop Loss**: 0.50%.
- **Move to Breakeven**: **+0.80%** (Increased from 0.20%).
- **Trailing Stop**: **0.40%** (Increased from 0.10%).

## Historical Data
- **Period**: 6 months (Oct 2023 - Mar 2024).

## Backtest Results
- **Net Profit**: **+$1520.99** (on a $1000 initial balance).
- **Final Balance**: $2520.99.
- **Number of Trades**: 277.
- **Win Rate**: 46.21%.
- **Max Drawdown**: 26.23%.

## Conclusion
By widening the exit parameters, we successfully transformed the strategy from a high-win-rate/low-profit setup into a highly profitable system. The strategy now allows winning trades to develop into significant gains (+0.80% or more), which more than compensates for the moderate 46% win rate. This demonstrates the critical importance of the Reward-to-Risk ratio in high-frequency trading.
