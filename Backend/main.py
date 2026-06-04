from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class WaitTimeRequest(BaseModel):
    season: str
    time_of_day: str
    urgency_level: str
    nurse_ratio: float
    specialist_availability: str
    facility_size: int
    patient_satisfaction: int

class StaffRequest(BaseModel):
    week: int
    role: str
    service: str


# Load Model

model_path = os.path.join(
    os.path.dirname(__file__),
    "models",
    "bed_model.pkl"
)

columns_path = os.path.join(
    os.path.dirname(__file__),
    "models",
    "bed_columns.pkl"
)

model = joblib.load(model_path)
columns = joblib.load(columns_path)


waittime_model = joblib.load(
    "models/waittime_model.pkl"
)

waittime_columns = joblib.load(
    "models/waittime_columns.pkl"
)

staff_model = joblib.load(
    "models/staff_model.pkl"
)

staff_columns = joblib.load(
    "models/staff_columns.pkl"
)

# Home

@app.get("/")
def home():
    return {
        "message": "Smart Hospital Prediction API Running"
    }

# Bed Prediction

@app.post("/predict-bed")
def predict_bed(data: dict):

    age = data["age"]
    satisfaction = data["satisfaction"]
    service = data["service"]

    row = {}

    for col in columns:
        row[col] = 0

    if "age" in row:
        row["age"] = age

    if "satisfaction" in row:
        row["satisfaction"] = satisfaction

    service_column = f"service_{service}"

    if service_column in row:
        row[service_column] = 1

    input_df = pd.DataFrame([row])

    prediction = model.predict(input_df)[0]

    return {
        "predicted_length_of_stay": round(float(prediction), 2)
    }

@app.post("/predict-waittime")
def predict_waittime(data: WaitTimeRequest):

    input_data = {
        "Nurse-to-Patient Ratio": data.nurse_ratio,
        "Facility Size (Beds)": data.facility_size,
        "Patient Satisfaction": data.patient_satisfaction
    }

    for col in waittime_columns:

        if col.startswith("Season_"):
            input_data[col] = (
                1 if col == f"Season_{data.season}" else 0
            )

        elif col.startswith("Time of Day_"):
            input_data[col] = (
                1 if col == f"Time of Day_{data.time_of_day}" else 0
            )

        elif col.startswith("Urgency Level_"):
            input_data[col] = (
                1 if col == f"Urgency Level_{data.urgency_level}" else 0
            )

        elif col.startswith("Specialist Availability_"):
            input_data[col] = (
                1 if col == f"Specialist Availability_{data.specialist_availability}" else 0
            )

    import pandas as pd

    X = pd.DataFrame(
        [input_data]
    )

    X = X.reindex(
        columns=waittime_columns,
        fill_value=0
    )

    prediction = waittime_model.predict(X)[0]

    return {
        "predicted_wait_time": round(
            float(prediction),
            2
        )
    }

@app.post("/predict-staff")
def predict_staff(data: StaffRequest):

    row = {}

    for col in staff_columns:
        row[col] = 0

    if "week" in row:
        row["week"] = data.week

    role_col = f"role_{data.role}"

    if role_col in row:
        row[role_col] = 1

    service_col = f"service_{data.service}"

    if service_col in row:
        row[service_col] = 1

    X = pd.DataFrame([row])

    prediction = staff_model.predict(X)[0]

    return {
        "staff_available":
        "Yes" if prediction == 1 else "No"
    }

@app.post("/hospital-status")
def hospital_status(data: dict):

    stay = float(data["stay"])
    wait = float(data["wait"])
    staff = data["staff"]

    score = 100

    if stay > 10:
        score -= 20

    if wait > 60:
        score -= 30

    if staff == "No":
        score -= 40

    score = max(score, 0)

    # Capacity
    capacity = max(
        0,
        100 - (stay * 5)
    )

    # Status
    if score >= 80:
        status = "Normal"

    elif score >= 60:
        status = "Busy"

    elif score >= 40:
        status = "High Load"

    else:
        status = "Critical"

    # Risk Level

    if wait <= 20:
        risk = "Low"

    elif wait <= 40:
        risk = "Moderate"

    elif wait <= 60:
        risk = "High"

    else:
        risk = "Extreme"

    recommendations = []

    if wait > 60:
        recommendations.append(
            "ER overloaded. Redirect non-critical patients."
        )

    if staff == "No":
        recommendations.append(
            "Staff shortage detected. Assign backup staff."
        )

    if stay > 10:
        recommendations.append(
            "High bed occupancy expected."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Hospital operating normally."
        )

    return {
        "readiness_score": score,
        "capacity": round(capacity, 2),
        "hospital_status": status,
        "risk_level": risk,
        "recommendations": recommendations
    }
