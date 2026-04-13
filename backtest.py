import pandas as pd
import numpy as np

def calculate_atr(df, n=14):
    df = df.copy()
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(n).mean()
    return atr

def backtest(data_file='btc_1m_data.csv'):
    try:
        df = pd.read_csv(data_file)
    except FileNotFoundError:
        print(f"Error: {data_file} not found.")
        return [], 0, 0, 0

    df['atr'] = calculate_atr(df, 14)
    df['body_perc'] = (df['close'] - df['open']) / df['open'] * 100
    df['spike_up'] = (df['high'] - np.maximum(df['open'], df['close'])) / df['open'] * 100
    df['spike_down'] = (df['low'] - np.minimum(df['open'], df['close'])) / df['open'] * 100

    # OPTIMIZED Strategy Parameters
    VOLUME_THRESHOLD = 1000
    PREV_VOLUME_THRESHOLD = 1000
    SPIKE_THRESHOLD = 0.12
    OPPOSITE_SPIKE_THRESHOLD = 0.05
    BODY_LIMIT = 0.50
    ATR_THRESHOLD = 80

    STOP_LOSS_PERC = 0.0060 # 0.60%
    BREAKEVEN_PERC = 0.0020 # 0.20%
    TRAILING_PERC = 0.0010  # 0.10%

    # Signal on Candle N-1, Entry on Candle N (Open)
    df['long_signal'] = (
        (df['spike_down'] < -SPIKE_THRESHOLD) &
        (df['spike_up'] < OPPOSITE_SPIKE_THRESHOLD) &
        (df['body_perc'] > -BODY_LIMIT) &
        (df['trades'] > VOLUME_THRESHOLD) &
        (df['trades'].shift(1) < PREV_VOLUME_THRESHOLD) &
        (df['atr'] < ATR_THRESHOLD)
    )

    df['short_signal'] = (
        (df['spike_up'] > SPIKE_THRESHOLD) &
        (df['spike_down'] > -OPPOSITE_SPIKE_THRESHOLD) &
        (df['body_perc'] < BODY_LIMIT) &
        (df['trades'] > VOLUME_THRESHOLD) &
        (df['trades'].shift(1) < PREV_VOLUME_THRESHOLD) &
        (df['atr'] < ATR_THRESHOLD)
    )

    initial_balance = 1000
    balance = initial_balance
    risk_per_trade = 0.02
    trades = []
    in_position = False
    peak_balance = balance
    max_drawdown = 0

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i-1]

        peak_balance = max(peak_balance, balance)
        max_drawdown = max(max_drawdown, (peak_balance - balance) / peak_balance if peak_balance > 0 else 0)

        if not in_position:
            if prev_row['long_signal'] or prev_row['short_signal']:
                in_position = True
                position_type = 'long' if prev_row['long_signal'] else 'short'
                entry_price = row['open']
                stop_loss = entry_price * (1 - STOP_LOSS_PERC if position_type == 'long' else 1 + STOP_LOSS_PERC)
                breakeven_reached = False
                qty = (balance * risk_per_trade) / abs(entry_price - stop_loss)
        else:
            exit_pnl = 0
            exited = False
            if position_type == 'long':
                if row['low'] <= stop_loss:
                    exit_pnl = (stop_loss - entry_price) * qty
                    exited = True
                elif not breakeven_reached and (row['high'] - entry_price) / entry_price >= BREAKEVEN_PERC:
                    breakeven_reached, stop_loss = True, entry_price
                elif breakeven_reached:
                    new_sl = row['high'] * (1 - TRAILING_PERC)
                    if new_sl > stop_loss: stop_loss = new_sl
                    if row['low'] <= stop_loss:
                        exit_pnl = (stop_loss - entry_price) * qty
                        exited = True
            else:
                if row['high'] >= stop_loss:
                    exit_pnl = (entry_price - stop_loss) * qty
                    exited = True
                elif not breakeven_reached and (entry_price - row['low']) / entry_price >= BREAKEVEN_PERC:
                    breakeven_reached, stop_loss = True, entry_price
                elif breakeven_reached:
                    new_sl = row['low'] * (1 + TRAILING_PERC)
                    if new_sl < stop_loss: stop_loss = new_sl
                    if row['high'] >= stop_loss:
                        exit_pnl = (entry_price - stop_loss) * qty
                        exited = True

            if exited:
                balance += exit_pnl
                trades.append(exit_pnl)
                in_position = False

    return trades, balance, max_drawdown, initial_balance

def run():
    trades, final_balance, max_drawdown, initial_balance = backtest()
    wins = [p for p in trades if p > 0]
    wr = len(wins) / len(trades) * 100 if trades else 0

    output = f"""# Optimized Backtest Metrics
- **Initial Balance**: ${initial_balance}
- **Final Balance**: ${final_balance:.2f}
- **Total PnL**: ${final_balance - initial_balance:.2f}
- **Number of Trades**: {len(trades)}
- **Wins**: {len(wins)}
- **Losses**: {len(trades) - len(wins)}
- **Win Rate**: {wr:.2f}%
- **Max Drawdown**: {max_drawdown*100:.2f}%
"""
    with open('metrics.md', 'w') as f:
        f.write(output)
    print("Done")

if __name__ == "__main__":
    run()
