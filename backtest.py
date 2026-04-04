import pandas as pd
import numpy as np

def calculate_atr(df, n=14):
    """
    Calculates the Average True Range (ATR) indicator.
    """
    df = df.copy()
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(n).mean()
    return atr

def backtest(data_file='btc_1m_data.csv'):
    """
    Runs a backtest on the provided 1m historical data.
    Strategy follows the flowchart in the PDF: Volume spikes + price rejection wicks.
    """
    try:
        df = pd.read_csv(data_file)
    except FileNotFoundError:
        print(f"Error: {data_file} not found. Please run fetch_binance_vision.py first.")
        return [], 0, 0, 0

    # Calculate indicators
    df['atr'] = calculate_atr(df, 14)
    df['body_perc'] = (df['close'] - df['open']) / df['open'] * 100
    df['spike_up'] = (df['high'] - np.maximum(df['open'], df['close'])) / df['open'] * 100
    df['spike_down'] = (df['low'] - np.minimum(df['open'], df['close'])) / df['open'] * 100

    # PDF Strategy Parameters (Adjusted thresholds based on current market data to capture trades)
    # The PDF specifies > 2000 BTC volume, but mentioned lowering thresholds for backtesting.
    VOLUME_THRESHOLD = 500
    PREV_VOLUME_THRESHOLD = 1000
    SPIKE_THRESHOLD = 0.05
    OPPOSITE_SPIKE_THRESHOLD = 0.03
    BODY_LIMIT = 0.50
    ATR_THRESHOLD = 100

    # Entry conditions
    # Long signal (rejection from below)
    df['long_signal'] = (
        (df['spike_down'] < -SPIKE_THRESHOLD) &
        (df['spike_up'] < OPPOSITE_SPIKE_THRESHOLD) &
        (df['body_perc'] > -BODY_LIMIT) &
        (df['volume'] > VOLUME_THRESHOLD) &
        (df['volume'].shift(1) < PREV_VOLUME_THRESHOLD) &
        (df['atr'] < ATR_THRESHOLD)
    )

    # Short signal (rejection from above)
    df['short_signal'] = (
        (df['spike_up'] > SPIKE_THRESHOLD) &
        (df['spike_down'] > -OPPOSITE_SPIKE_THRESHOLD) &
        (df['body_perc'] < BODY_LIMIT) &
        (df['volume'] > VOLUME_THRESHOLD) &
        (df['volume'].shift(1) < PREV_VOLUME_THRESHOLD) &
        (df['atr'] < ATR_THRESHOLD)
    )

    # Backtest setup
    initial_balance = 1000
    balance = initial_balance
    risk_per_trade = 0.02 # 2% risk of balance
    trades = []

    in_position = False
    position_type = None
    entry_price = 0
    stop_loss = 0
    breakeven_reached = False
    qty = 0

    peak_balance = initial_balance
    max_drawdown = 0

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i-1]

        # Update Peak and Drawdown
        if balance > peak_balance:
            peak_balance = balance
        drawdown = (peak_balance - balance) / peak_balance if peak_balance > 0 else 0
        if drawdown > max_drawdown:
            max_drawdown = drawdown

        if not in_position:
            # Enter at the open of the candle after the signal
            if prev_row['long_signal']:
                in_position = True
                position_type = 'long'
                entry_price = row['open']
                stop_loss = entry_price * (1 - 0.0045) # 0.45% SL
                breakeven_reached = False
                # Position sizing based on 2% risk
                risk_amount = balance * risk_per_trade
                qty = risk_amount / (entry_price - stop_loss) if (entry_price - stop_loss) != 0 else 0
                if qty == 0: in_position = False

            elif prev_row['short_signal']:
                in_position = True
                position_type = 'short'
                entry_price = row['open']
                stop_loss = entry_price * (1 + 0.0045) # 0.45% SL
                breakeven_reached = False
                risk_amount = balance * risk_per_trade
                qty = risk_amount / (stop_loss - entry_price) if (stop_loss - entry_price) != 0 else 0
                if qty == 0: in_position = False

        else:
            # Manage position
            if position_type == 'long':
                # Check initial stop loss
                if row['low'] <= stop_loss:
                    pnl = (stop_loss - entry_price) * qty
                    balance += pnl
                    trades.append({'type': 'long', 'pnl': pnl})
                    in_position = False
                # Breakeven condition (+0.30% profit reached)
                elif not breakeven_reached and (row['high'] - entry_price) / entry_price >= 0.0030:
                    breakeven_reached = True
                    stop_loss = entry_price
                # Trailing stop after breakeven
                elif breakeven_reached:
                    new_sl = row['high'] * (1 - 0.0010) # 0.1% trailing from high
                    if new_sl > stop_loss:
                        stop_loss = new_sl
                    if row['low'] <= stop_loss:
                        pnl = (stop_loss - entry_price) * qty
                        balance += pnl
                        trades.append({'type': 'long', 'pnl': pnl})
                        in_position = False

            elif position_type == 'short':
                # Check initial stop loss
                if row['high'] >= stop_loss:
                    pnl = (entry_price - stop_loss) * qty
                    balance += pnl
                    trades.append({'type': 'short', 'pnl': pnl})
                    in_position = False
                # Breakeven condition
                elif not breakeven_reached and (entry_price - row['low']) / entry_price >= 0.0030:
                    breakeven_reached = True
                    stop_loss = entry_price
                # Trailing stop
                elif breakeven_reached:
                    new_sl = row['low'] * (1 + 0.0010)
                    if new_sl < stop_loss:
                        stop_loss = new_sl
                    if row['high'] >= stop_loss:
                        pnl = (entry_price - stop_loss) * qty
                        balance += pnl
                        trades.append({'type': 'short', 'pnl': pnl})
                        in_position = False

    return trades, balance, max_drawdown, initial_balance

def run():
    trades, final_balance, max_drawdown, initial_balance = backtest()

    if not trades and final_balance == 0:
         return

    trades_df = pd.DataFrame(trades)
    win_rate = len(trades_df[trades_df['pnl'] > 0]) / len(trades_df) * 100 if not trades_df.empty else 0
    total_pnl = final_balance - initial_balance

    report = []
    report.append("# Backtest Metrics")
    report.append(f"- **Initial Balance**: ${initial_balance}")
    report.append(f"- **Final Balance**: ${final_balance:.2f}")
    report.append(f"- **Total PnL**: ${total_pnl:.2f}")
    report.append(f"- **Number of Trades**: {len(trades_df)}")
    if not trades_df.empty:
        report.append(f"- **Wins**: {len(trades_df[trades_df['pnl'] > 0])}")
        report.append(f"- **Losses**: {len(trades_df[trades_df['pnl'] <= 0])}")
        report.append(f"- **Win Rate**: {win_rate:.2f}%")
        report.append(f"- **Max Drawdown**: {max_drawdown*100:.2f}%")
    else:
        report.append("- **No trades were executed with the specified parameters.**")

    with open('metrics.md', 'w') as f:
        f.write("\n".join(report))

    print("Backtest complete. Metrics updated in metrics.md")

if __name__ == "__main__":
    run()
