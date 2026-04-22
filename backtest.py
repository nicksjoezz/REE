import pandas as pd
import numpy as np
import os

def calculate_atr(df, n=14):
    df = df.copy()
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(n).mean()
    return atr

def prepare_data(data_file='btc_1m_data.csv'):
    if not os.path.exists(data_file):
        return None
    df = pd.read_csv(data_file)
    df['atr'] = calculate_atr(df, 14)
    df['body_perc'] = (df['close'] - df['open']) / df['open'] * 100
    df['spike_up'] = (df['high'] - np.maximum(df['open'], df['close'])) / df['open'] * 100
    df['spike_down'] = (df['low'] - np.minimum(df['open'], df['close'])) / df['open'] * 100

    # Strategy Parameters (Consistent across versions)
    VOLUME_THRESHOLD = 1000
    PREV_VOLUME_THRESHOLD = 1000
    SPIKE_THRESHOLD = 0.10
    OPPOSITE_SPIKE_THRESHOLD = 0.05
    BODY_LIMIT = 0.50
    ATR_THRESHOLD = 100

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
    return df

def backtest_dynamic(df):
    balance = 1000
    risk_per_trade = 0.02
    trades = []
    in_pos = False
    peak = balance
    mdd = 0

    STOP_LOSS_PERC = 0.0050
    BREAKEVEN_PERC = 0.0080
    TRAILING_PERC = 0.0040

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i-1]
        peak = max(peak, balance)
        mdd = max(mdd, (peak - balance) / peak if peak > 0 else 0)

        if not in_pos:
            if prev['long_signal'] or prev['short_signal']:
                in_pos = True
                p_type = 'long' if prev['long_signal'] else 'short'
                entry = row['open']
                sl = entry * (1 - STOP_LOSS_PERC if p_type == 'long' else 1 + STOP_LOSS_PERC)
                be_reached = False
                qty = (balance * risk_per_trade) / abs(entry - sl)
        else:
            pnl = 0
            exit_now = False
            if p_type == 'long':
                if row['low'] <= sl:
                    pnl = (sl - entry) * qty
                    exit_now = True
                elif not be_reached and (row['high'] - entry) / entry >= BREAKEVEN_PERC:
                    be_reached, sl = True, entry
                elif be_reached:
                    new_sl = row['high'] * (1 - TRAILING_PERC)
                    if new_sl > sl: sl = new_sl
                    if row['low'] <= sl:
                        pnl = (sl - entry) * qty
                        exit_now = True
            else:
                if row['high'] >= sl:
                    pnl = (entry - sl) * qty
                    exit_now = True
                elif not be_reached and (entry - row['low']) / entry >= BREAKEVEN_PERC:
                    be_reached, sl = True, entry
                elif be_reached:
                    new_sl = row['low'] * (1 + TRAILING_PERC)
                    if new_sl < sl: sl = new_sl
                    if row['high'] >= sl:
                        pnl = (entry - sl) * qty
                        exit_now = True

            if exit_now:
                balance += pnl
                trades.append(pnl)
                in_pos = False
    return trades, balance, mdd

def backtest_15_candles(df):
    balance = 1000
    risk_per_trade = 0.02
    trades = []

    STOP_LOSS_PERC = 0.01 # 1% safety SL

    opens = df['open'].values
    closes = df['close'].values
    lows = df['low'].values
    highs = df['high'].values
    long_signals = df['long_signal'].values
    short_signals = df['short_signal'].values

    for i in range(1, len(df) - 15):
        if long_signals[i-1]:
            entry = opens[i]
            sl = entry * (1 - STOP_LOSS_PERC)
            qty = (balance * risk_per_trade) / (entry - sl)
            pnl = 0
            hit_sl = False
            for j in range(i, i + 15):
                if lows[j] <= sl:
                    pnl = (sl - entry) * qty
                    hit_sl = True
                    break
            if not hit_sl:
                pnl = (closes[i+14] - entry) * qty
            balance += pnl
            trades.append(pnl)
        elif short_signals[i-1]:
            entry = opens[i]
            sl = entry * (1 + STOP_LOSS_PERC)
            qty = (balance * risk_per_trade) / (sl - entry)
            pnl = 0
            hit_sl = False
            for j in range(i, i + 15):
                if highs[j] >= sl:
                    pnl = (entry - sl) * qty
                    hit_sl = True
                    break
            if not hit_sl:
                pnl = (entry - closes[i+14]) * qty
            balance += pnl
            trades.append(pnl)
    return trades, balance

def run():
    df = prepare_data()
    if df is None:
        return

    # Run Profit-Optimized Dynamic Backtest
    t_dyn, b_dyn, m_dyn = backtest_dynamic(df)
    w_dyn = len([p for p in t_dyn if p > 0])
    l_dyn = len(t_dyn) - w_dyn

    with open('metrics.md', 'w') as f:
        f.write(f"# Profit-Optimized Backtest Metrics\n")
        f.write(f"- **Final Balance**: ${b_dyn:.2f}\n")
        f.write(f"- **Number of Trades**: {len(t_dyn)}\n")
        f.write(f"- **Wins**: {w_dyn}\n")
        f.write(f"- **Losses**: {l_dyn}\n")
        f.write(f"- **Win Rate**: {w_dyn/len(t_dyn)*100 if t_dyn else 0:.2f}%\n")
        f.write(f"- **Max Drawdown**: {m_dyn*100:.2f}%\n")

    # Run 15-Candle Fixed Exit Backtest
    t_15, b_15 = backtest_15_candles(df)
    w_15 = len([p for p in t_15 if p > 0])
    l_15 = len(t_15) - w_15

    with open('options.md', 'w') as f:
        f.write(f"# 15-Candle Exit Backtest Metrics\n")
        f.write(f"- **Final Balance**: ${b_15:.2f}\n")
        f.write(f"- **Number of Trades**: {len(t_15)}\n")
        f.write(f"- **Wins**: {w_15}\n")
        f.write(f"- **Losses**: {l_15}\n")
        f.write(f"- **Win Rate**: {w_15/len(t_15)*100 if t_15 else 0:.2f}%\n")

if __name__ == "__main__":
    run()
