import time
import pandas as pd
import cudf
import glob
import os
from feature_engineering import intermediate, cyclical_encoding, lag_features

def load_df(lib):
    revision = 1
    parquet_path = f"./datasets/BTC_REV_{revision}.parquet"
    if os.path.exists(parquet_path):
        df = lib.read_parquet(parquet_path)
    else:
        files = glob.glob("./datasets/*.csv")
        df_list = [lib.read_csv(f) for f in files]
        df = lib.concat(df_list, ignore_index=True)
        df.to_parquet(parquet_path)
    return df, revision

def preprocess_sort(df):
    df = df.sort_values('Timestamp').reset_index(drop=True)
    df['Open_next'] = df['Open'].shift(-1)
    return df.iloc[:-1]

def feature_engineering(df):
    df = intermediate(df)
    df = cyclical_encoding(df)
    df = lag_features(df)
    return df.dropna().astype({c: 'float32' for c in df.columns if c != 'Timestamp'})

def feature_engineering(df):
    df = intermediate(df)
    df = cyclical_encoding(df)
    df = lag_features(df)
    df = df.dropna()
    if isinstance(df, pd.DataFrame):
        df = df.astype({c: 'float32' for c in df.columns if c != 'Timestamp'})
    return df

def prepare_xy(df):
    df = preprocess_sort(df)
    df = feature_engineering(df)
    X = df.drop(columns=['Open_next', 'Timestamp'])
    y = df['Open_next']
    return X, y

def benchmark_function(func, name, *args):
    start = time.time()
    result = func(*args)
    elapsed = time.time() - start
    print(f"{name}: {elapsed:.4f} seconds")
    return result, elapsed

def main():

    result_pandas, pandas_load = benchmark_function(load_df, "Pandas load_df", pd)
    result_cudf, cudf_load = benchmark_function(load_df, "cuDF load_df", cudf)

    df_pandas, _ = result_pandas
    df_cudf, _ = result_cudf

    print(f"\nDataset shape - Pandas: {df_pandas.shape}, cuDF: {df_cudf.shape}")

    df_pandas_sorted, pandas_sort = benchmark_function(preprocess_sort, "Pandas preprocess_sort", df_pandas.copy())
    df_cudf_sorted, cudf_sort = benchmark_function(preprocess_sort, "cuDF preprocess_sort", df_cudf.copy())

    df_pandas_fe, pandas_fe = benchmark_function(feature_engineering, "Pandas feature_engineering", df_pandas_sorted.copy())
    df_cudf_fe, cudf_fe = benchmark_function(feature_engineering, "cuDF feature_engineering", df_cudf_sorted.copy())

    print("\nSummary: ")
    print(f"{'Operation':<25} {'Pandas (s)':<12} {'cuDF (s)':<12} {'Speedup':<10}")
    print("-" * 60)
    print(f"{'Data Loading':<25} {pandas_load:<12.4f} {cudf_load:<12.4f} {pandas_load/cudf_load if cudf_load>0 else 'N/A':<10}")
    print(f"{'Preprocessing Sort':<25} {pandas_sort:<12.4f} {cudf_sort:<12.4f} {pandas_sort/cudf_sort if cudf_sort>0 else 'N/A':<10}")
    print(f"{'Feature Engineering':<25} {pandas_fe:<12.4f} {cudf_fe:<12.4f} {pandas_fe/cudf_fe if cudf_fe>0 else 'N/A':<10}")


if __name__ == "__main__":
    main()
