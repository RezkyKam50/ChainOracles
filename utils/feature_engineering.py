import cupy as cp, pandas as pd, numpy as np, cudf


# Timestamp, Open, Close, High, Low 
# Target (y) : Open

def intermediate(df):
    df['price_change'] = df['Close'] - df['Open']
    df['price_return'] = (df['Close'] - df['Open']) / df['Open']
    df['volume_price_ratio'] = df['Volume'] / (df['Close'] * 1000)   
    df['volatility'] = df['High'] / df['Low'] - 1

    return df 

def cyclical_encoding(df):
    df['minute'] = (df['Timestamp'] // 60) % 60
    df['hour'] = (df['Timestamp'] // 3600) % 24
    df['dayofweek'] = cudf.to_datetime(df['Timestamp'], unit='s').dt.dayofweek
    df['hour_sin'] = cp.sin(2 * cp.pi * df['hour'] / 24)
    df['hour_cos'] = cp.cos(2 * cp.pi * df['hour'] / 24)
    df['minute_sin'] = cp.sin(2 * cp.pi * df['minute'] / 60)
    df['minute_cos'] = cp.cos(2 * cp.pi * df['minute'] / 60)
    df['dayofweek_sin'] = cp.sin(2 * cp.pi * df['dayofweek'] / 7)
    df['dayofweek_cos'] = cp.cos(2 * cp.pi * df['dayofweek'] / 7)
    df['price_range'] = df['High'] - df['Low']
    df['typical_price'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['price_momentum'] = df['Close'] - df['Open']

    return df 




 