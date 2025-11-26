import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
data = pd.read_csv("energydata_complete.csv")

# Feature (input) and target (output)
X = data[["T1"]].values
y = data["T1"].shift(-1).fillna(method="ffill").values

# 80/20 Train-Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
model = RandomForestRegressor(n_estimators=50)
model.fit(X_train, y_train)

# Evaluate the model
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

print("MAE (Model Error):", mae)

# Save the model
joblib.dump(model, "temp_model.pkl")

print("Model trained and saved.")
