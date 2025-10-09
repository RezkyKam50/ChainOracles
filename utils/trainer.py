from xgboost import XGBRegressor
import cupy as cp, cudf, pickle, joblib, glob, os
from sklearn.metrics import root_mean_squared_error
from cuml.preprocessing import (
    RobustScaler, 
    MinMaxScaler
)
from cuml.metrics import (
    r2_score, 
    mean_absolute_error,
    mean_squared_error
)
from feature_engineering import (
    intermediate,
    cyclical_encoding
)


def load_df():
    revision = 1
    parquet_path = f"./datasets/BTC_REV_{revision}.parquet"
    if os.path.exists(parquet_path):
        df = cudf.read_parquet(parquet_path)
    else:
        csv_files = glob.glob("./datasets/*.csv")
        df = cudf.concat([cudf.read_csv(f) for f in csv_files], ignore_index=True)
        df.to_parquet(parquet_path)

    return df, revision

def preprocess_sort(df):
    df = df.sort_values('Timestamp').reset_index(drop=True)
    df['Open_next'] = df['Open'].shift(-1)
    df = df.iloc[:-1]

    return df

def feature_engineering(df):
    df = intermediate(df)
    df = cyclical_encoding(df)

    # reduce precision from f64 to f32 for compute efficiency (XGB & RAPIDS doesn't support f16 yet)
    return df.dropna().astype({col: 'float32' for col in df.columns if col != 'Timestamp'})

def prepare_xy(df):
    df = load_df()
    df = preprocess_sort(df)
    df = feature_engineering(df)
    print(df.dtypes)
    X = df.drop(columns=['Open_next', 'Timestamp'])
    y = df['Open_next']

    return X, y

def trainsplit(X, y, df):
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    
    X_train_gpu = X_train_scaled.to_cupy()
    X_test_gpu = X_test_scaled.to_cupy()
    y_train_gpu = y_train.to_cupy()
    y_test_gpu = y_test.to_cupy()

    return X_train_gpu, X_test_gpu, y_train_gpu, y_test_gpu


if __name__ == "__main__":

    df, revision                                        = load_df()
    X, y                                                = prepare_xy(df)
    X_train_gpu, X_test_gpu, y_train_gpu, y_test_gpu    = trainsplit(X, y, df)
 

    # Initialize XGBoost classifier
    num_estimators_per_batch = 150
    model = XGBRegressor(
        n_estimators=num_estimators_per_batch,
        max_depth=14,
        learning_rate=0.09,
        subsample=0.8,
        colsample_bytree=0.8,
        colsample_bylevel=0.8,
        gamma=0.1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        tree_method="hist",
        device="cuda",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_gpu, y_train_gpu)

    # Train model in batches of rounds
    num_batches = 20
    for i in range(num_batches):
        model.fit(X_train_gpu, y_train_gpu, xgb_model=model.get_booster())

        # Make predictions on train and test data
        y_train_pred = model.predict(X_train_gpu)
        y_pred_gpu = model.predict(X_test_gpu)

        y_pred_cpu = cp.asnumpy(y_pred_gpu)
        y_test_cpu = cp.asnumpy(y_test_gpu)

        r2 = r2_score(y_test_cpu, y_pred_cpu)
        rmse = root_mean_squared_error(y_test_cpu, y_pred_cpu)
        mae = mean_absolute_error(y_test_cpu, y_pred_cpu)
        mse = mean_squared_error(y_test_cpu, y_pred_cpu)

        print("R² score:", r2)
        print("RMSE score:", rmse)
        print("MAE score:", mae)
        print("MSE score:", mse)

    model.save_model(f"./models/XGB_REV_{revision}.json")

    """
    R² score: 0.5489589169846156
    RMSE score: 21086.841144893515
    MAE score: 12211.506633945908

    """





    # model = XGBRegressor(
    #     n_estimators=1000,
    #     max_depth=14,
    #     learning_rate=0.09,
    #     subsample=0.8,
    #     colsample_bytree=0.8,
    #     colsample_bylevel=0.8,
    #     gamma=0.1,
    #     reg_alpha=0.1,
    #     reg_lambda=1.0,
    #     tree_method="hist",
    #     device="cuda",
    #     random_state=42,
    #     n_jobs=-1
    # )

    # model.fit(X_train_gpu, y_train_gpu)
    
    # y_pred_gpu = model.predict(X_test_gpu)
    
    # y_pred_cpu = cp.asnumpy(y_pred_gpu)
    # y_test_cpu = cp.asnumpy(y_test_gpu)

    # r2 = r2_score(y_test_cpu, y_pred_cpu)
    # rmse = root_mean_squared_error(y_test_cpu, y_pred_cpu)
    # mae = mean_absolute_error(y_test_cpu, y_pred_cpu)
    # mse = mean_squared_error(y_test_cpu, y_pred_cpu)

    # print("R² score:", r2)
    # print("RMSE score:", rmse)
    # print("MAE score:", mae)
    # print("MSE score:", mse)
