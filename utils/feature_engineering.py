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

def statistical(df):
    df['rolling_mean_5'] = df['Close'].rolling(5).mean()
    df['rolling_std_5'] = df['Close'].rolling(5).std()
    df['rolling_min_5'] = df['Close'].rolling(5).min()
    df['rolling_max_5'] = df['Close'].rolling(5).max()
    
    df['z_score_5'] = (df['Close'] - df['rolling_mean_5']) / df['rolling_std_5']
    df['price_position'] = (df['Close'] - df['rolling_min_5']) / (df['rolling_max_5'] - df['rolling_min_5'])

    df['volatility_5'] = df['Close'].rolling(5).std() / df['Close'].rolling(5).mean()
    df['volatility_10'] = df['Close'].rolling(10).std() / df['Close'].rolling(10).mean()
    
    return df

def lag_features(df):
    for lag in [3, 5, 10]:
        df[f'close_lag_{lag}'] = df['Close'].shift(lag)
        df[f'volume_lag_{lag}'] = df['Volume'].shift(lag)

    df['return_3'] = df['Close'].pct_change(3)
    df['return_5'] = df['Close'].pct_change(5)
    df['return_10'] = df['Close'].pct_change(19)
 
    df['return_volatility_5'] = df['return_1'].rolling(5).std()
    df['return_volatility_10'] = df['return_1'].rolling(10).std()
    
    return df



 