import requests
import zipfile
import io
import pandas as pd
import os

def download_binance_data(symbol='BTCUSDT', timeframe='1m', year='2024', month='01'):
    url = f"https://data.binance.vision/data/spot/monthly/klines/{symbol}/{timeframe}/{symbol}-{timeframe}-{year}-{month}.zip"
    print(f"Downloading {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall("binance_data")
            print(f"Extracted {year}-{month} data.")
            return True
        else:
            print(f"Failed to download {year}-{month}. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {year}-{month}: {e}")
        return False

def combine_data():
    if not os.path.exists("binance_data"):
        return None

    all_files = [os.path.join("binance_data", f) for f in os.listdir("binance_data") if f.endswith(".csv")]
    li = []
    for filename in all_files:
        try:
            df = pd.read_csv(filename, header=None)
            li.append(df)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    if not li:
        return None

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades', 'taker_base', 'taker_quote', 'ignore']
    frame['timestamp'] = pd.to_datetime(frame['timestamp'], unit='ms')
    frame = frame.sort_values('timestamp')
    return frame

if __name__ == "__main__":
    if not os.path.exists("binance_data"):
        os.makedirs("binance_data")

    # Fetch 6 months of data: Late 2023 to early 2024
    for y, months in [('2023', ['10', '11', '12']), ('2024', ['01', '02', '03'])]:
        for m in months:
            download_binance_data(year=y, month=m)

    df = combine_data()
    if df is not None:
        df.to_csv('btc_1m_data.csv', index=False)
        print(f"Saved combined data to btc_1m_data.csv. Total rows: {len(df)}")
    else:
        print("No data to save.")
