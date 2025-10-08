import cudf


def load_df():
    df = cudf.read_csv("./datasets/*.csv")
    return df.to_pandas()