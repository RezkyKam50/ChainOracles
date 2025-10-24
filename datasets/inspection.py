import cudf, pandas as pd
import time

filename="BTC_REV_1.parquet"
df = cudf.read_parquet(filename)
print(len(df))
print(df.head(10))