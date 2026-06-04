import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Load dataset
df = pd.read_csv(
    "../datasets/er_wait_time/ER Wait Time Dataset.csv"
)

# Select useful columns
df = df[
    [
        "Season",
        "Time of Day",
        "Urgency Level",
        "Nurse-to-Patient Ratio",
        "Specialist Availability",
        "Facility Size (Beds)",
        "Patient Satisfaction",
        "Total Wait Time (min)"
    ]
]

# One-hot encoding
df = pd.get_dummies(
    df,
    columns=[
        "Season",
        "Time of Day",
        "Urgency Level",
        "Specialist Availability"
    ]
)

# Features and Target
X = df.drop(
    "Total Wait Time (min)",
    axis=1
)

y = df["Total Wait Time (min)"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# Evaluate
predictions = model.predict(X_test)

score = r2_score(
    y_test,
    predictions
)

print("Wait Time Model Accuracy:", score)

# Save model
joblib.dump(
    model,
    "models/waittime_model.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "models/waittime_columns.pkl"
)

print("Wait Time Model Saved")