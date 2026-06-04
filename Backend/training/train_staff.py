import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset

df = pd.read_csv(
    "../datasets/hospital_beds/staff_schedule.csv"
)

# Features

X = df[
    [
        "week",
        "role",
        "service"
    ]
]

# Target

y = df["present"]

# One Hot Encoding

X = pd.get_dummies(
    X,
    columns=[
        "role",
        "service"
    ]
)

# Save columns

joblib.dump(
    X.columns,
    "models/staff_columns.pkl"
)

# Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# Accuracy

pred = model.predict(X_test)

acc = accuracy_score(
    y_test,
    pred
)

print(
    "Staff Availability Accuracy:",
    acc
)

# Save model

joblib.dump(
    model,
    "models/staff_model.pkl"
)

print("Staff Model Saved")