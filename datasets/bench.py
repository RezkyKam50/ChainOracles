import cudf
import pandas as pd
import time

filename = "btcusd_1-min_data.csv"

# Benchmark cuDF
start = time.time()
df_cudf = cudf.read_csv(filename)
end = time.time()
print(f"cuDF: {end - start:.4f} seconds, rows: {len(df_cudf)}")
print(df_cudf.head(10))

# Benchmark pandas
start = time.time()
df_pd = pd.read_csv(filename)
end = time.time()
print(f"pandas: {end - start:.4f} seconds, rows: {len(df_pd)}")
print(df_pd.head(10))
