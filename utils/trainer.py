from xgboost import XGBRegressor
import cupy as cp, cudf, pickle, joblib
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
    df = cudf.read_csv("./datasets/*.csv")
    return df

def preprocess_sort(df):

    df = df.sort_values('Timestamp').reset_index(drop=True)
    df['Open_next'] = df['Open'].shift(-1)
    df = df.iloc[:-1]

    return df

def feature_engineering(df):

    df = intermediate(df)
    df = cyclical_encoding(df)

    return df.dropna().astype({col: 'float32' for col in df.columns if col != 'Timestamp'})

df = load_df()
df = preprocess_sort(df)
df = feature_engineering(df)
print(df.dtypes)

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
    n_estimators=1000,
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

"""
R² score: 0.5489589169846156
RMSE score: 21086.841144893515
MAE score: 12211.506633945908

"""