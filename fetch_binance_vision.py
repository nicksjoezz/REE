import requests
import zipfile
import io
import pandas as pd
import os

def download_binance_data(symbol='BTCUSDT', timeframe='1m', year='2021', month='10'):
    url = f"https://data.binance.vision/data/spot/monthly/klines/{symbol}/{timeframe}/{symbol}-{timeframe}-{year}-{month}.zip"
    print(f"Downloading {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("binance_data")
        print(f"Extracted {year}-{month} data.")
        return True
    else:
        print(f"Failed to download {year}-{month}. Status: {response.status_code}")
        return False

def combine_data():
    all_files = [os.path.join("binance_data", f) for f in os.listdir("binance_data") if f.endswith(".csv")]
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, header=None)
        li.append(df)

    if not li:
        return None

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame = frame.iloc[:, :6]
    frame.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    frame['timestamp'] = pd.to_datetime(frame['timestamp'], unit='ms')
    frame = frame.sort_values('timestamp')
    return frame

if __name__ == "__main__":
    if not os.path.exists("binance_data"):
        os.makedirs("binance_data")

    # Download more high-volume periods (late 2021 bull run)
    for y in ['2021']:
        for m in ['10', '11', '12']:
            download_binance_data(year=y, month=m)

    # Download some 2024 months as well
    for m in ['01', '02', '03']:
        download_binance_data(year='2024', month=m)

    df = combine_data()
    if df is not None:
        df.to_csv('btc_1m_data.csv', index=False)
        print(f"Saved combined data to btc_1m_data.csv. Total rows: {len(df)}")
    else:
        print("No data to save.")
