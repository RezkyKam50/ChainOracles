from xgboost import XGBRegressor
import cupy as cp, cudf, pickle, joblib
from sklearn.metrics import root_mean_squared_error
from cuml.preprocessing import RobustScaler
from cuml.metrics import (
    r2_score, 
    mean_absolute_error
)


def load_df():
    df = cudf.read_csv("./datasets/*.csv")
    return df


def preprocess(df):
    df = df.sort_values('Timestamp').reset_index(drop=True)
    df['Open_next'] = df['Open'].shift(-1)
    df = df.iloc[:-1]

    df['minute'] = (df['Timestamp'] // 60) % 60
    df['hour'] = (df['Timestamp'] // 3600) % 24
    df['dayofweek'] = cudf.to_datetime(df['Timestamp'], unit='s').dt.dayofweek


    df['hour_sin'] = cp.sin(2 * cp.pi * df['hour'] / 24)
    df['hour_cos'] = cp.cos(2 * cp.pi * df['hour'] / 24)
    df['minute_sin'] = cp.sin(2 * cp.pi * df['minute'] / 60)
    df['minute_cos'] = cp.cos(2 * cp.pi * df['minute'] / 60)
    df['dayofweek_sin'] = cp.sin(2 * cp.pi * df['dayofweek'] / 7)
    df['dayofweek_cos'] = cp.cos(2 * cp.pi * df['dayofweek'] / 7)

    return df
# These are the training data columns
# Timestamp    float64 <- this is in Unix Time Epoch
# Open         float64
# High         float64
# Low          float64
# Close        float64
# Volume       float64


df = preprocess(load_df())
X = df.drop(columns=['Open_next', 'Timestamp'])
y = df['Open_next']

 
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

 
model = XGBRegressor(
    random_state=42,
    tree_method="hist",
    device="cuda"
)

model.fit(X_train_gpu, y_train_gpu)
 
y_pred_gpu = model.predict(X_test_gpu)
 
y_pred_cpu = cp.asnumpy(y_pred_gpu)
y_test_cpu = cp.asnumpy(y_test_gpu)

r2 = r2_score(y_test_cpu, y_pred_cpu)
rmse = root_mean_squared_error(y_test_cpu, y_pred_cpu)
mae = mean_absolute_error(y_test_cpu, y_pred_cpu)

print("R² score:", r2)
print("RMSE score:", rmse)
print("MAE score:", mae)


'''
R² score: 0.4932951610173718
RMSE score: 22350.178787597404
MAE score: 13073.122637284132
'''