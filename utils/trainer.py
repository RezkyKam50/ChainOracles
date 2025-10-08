from xgboost import XGBRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
import cupy as cp, cudf, pickle, joblib
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error


def load_df():
    df = cudf.read_csv("./datasets/*.csv")
    return df

df = load_df()
 
X = df.drop(columns=['Open'])
y = df['Open']
 
X_train, X_test, y_train, y_test = train_test_split(
    X.to_pandas(), y.to_pandas(), train_size=0.8, random_state=42
)
 
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
 
X_train_gpu = cp.array(X_train_scaled)
X_test_gpu = cp.array(X_test_scaled)
y_train_gpu = cp.array(y_train.values)
y_test_gpu = cp.array(y_test.values)
 
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




"""
R² score: 0.9999289862013638
RMSE score: 242.77401451684483
MAE score: 99.36013877457599
"""