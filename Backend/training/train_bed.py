import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os


# Load Dataset

file_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "datasets",
    "hospital_beds",
    "patients.csv"
)

df = pd.read_csv(file_path)


# Data Preprocessing

df["arrival_date"] = pd.to_datetime(df["arrival_date"])
df["departure_date"] = pd.to_datetime(df["departure_date"])

# Length of stay

df["length_of_stay"] = (
    df["departure_date"] - df["arrival_date"]
).dt.days

# Convert service category

df = pd.get_dummies(
    df,
    columns=["service"],
    drop_first=True
)


X = df.drop(
    columns=[
        "patient_id",
        "name",
        "arrival_date",
        "departure_date",
        "length_of_stay"
    ]
)

y = df["length_of_stay"]


# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

score = model.score(X_test, y_test)

print("Model Accuracy (R2):", score)

# Save Model

models_dir = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models"
)

os.makedirs(models_dir, exist_ok=True)

joblib.dump(
    model,
    os.path.join(models_dir, "bed_model.pkl")
)

joblib.dump(
    X.columns.tolist(),
    os.path.join(models_dir, "bed_columns.pkl")
)

print("Model Saved Successfully")
