import pandas as pd
import numpy as np

def _get_library_module(df):
    if hasattr(df, 'to_pandas'):   
        import cudf
        import cupy as cp
        return cudf, cp
    else:
        return pd, np

def intermediate(df):
    lib, math_lib = _get_library_module(df)
    
    df['price_change'] = df['Close'] - df['Open']
    df['price_return'] = (df['Close'] - df['Open']) / df['Open']
    df['volume_price_ratio'] = df['Volume'] / (df['Close'] * 1000)   
    df['volatility'] = df['High'] / df['Low'] - 1
    return df 

def cyclical_encoding(df):
    lib, math_lib = _get_library_module(df)
    
    df['minute'] = (df['Timestamp'] // 60) % 60
    df['hour'] = (df['Timestamp'] // 3600) % 24
     
    if lib.__name__ == 'cudf':
        df['dayofweek'] = lib.to_datetime(df['Timestamp'], unit='s').dt.dayofweek
    else:
        df['dayofweek'] = pd.to_datetime(df['Timestamp'], unit='s').dt.dayofweek
     
    df['hour_sin'] = math_lib.sin(2 * math_lib.pi * df['hour'] / 24)
    df['hour_cos'] = math_lib.cos(2 * math_lib.pi * df['hour'] / 24)
    df['minute_sin'] = math_lib.sin(2 * math_lib.pi * df['minute'] / 60)
    df['minute_cos'] = math_lib.cos(2 * math_lib.pi * df['minute'] / 60)
    df['dayofweek_sin'] = math_lib.sin(2 * math_lib.pi * df['dayofweek'] / 7)
    df['dayofweek_cos'] = math_lib.cos(2 * math_lib.pi * df['dayofweek'] / 7)
    
    df['price_range'] = df['High'] - df['Low']
    df['typical_price'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['price_momentum'] = df['Close'] - df['Open']
    return df 

def lag_features(df, lags=[1, 2, 3, 5, 10]):
    for lag in lags:
        df[f'close_lag_{lag}'] = df['Close'].shift(lag)
        df[f'volume_lag_{lag}'] = df['Volume'].shift(lag)
        df[f'high_lag_{lag}'] = df['High'].shift(lag)
        df[f'low_lag_{lag}'] = df['Low'].shift(lag)
    return df