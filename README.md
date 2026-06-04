# Smart Emergency Hospital Availability Prediction System

## Overview
This project is a Machine Learning-based hospital decision support system that predicts hospital resource availability and emergency readiness.

The original concept was to identify the best hospital using patient location and real-time hospital resource data. However, access to live hospital APIs, GPS services, bed occupancy systems, ICU status, ambulance tracking, and specialist availability is not publicly available.

Therefore, this project implements the concept within a single hospital environment and predicts critical operational factors using historical datasets.

---

## Features

### Bed Availability Prediction
Predicts the expected patient stay duration based on:
- Age
- Patient Satisfaction
- Service Type

Output:
- Predicted Length of Stay (Days)

### ER Wait Time Prediction
Predicts emergency room waiting time using:
- Nurse-to-Patient Ratio
- Facility Size
- Patient Satisfaction
- Season
- Time of Day
- Urgency Level
- Specialist Availability

Output:
- Predicted Wait Time (Minutes)

### Staff Availability Prediction
Predicts whether staff will be available based on:
- Week Number
- Staff Role
- Service Department

Output:
- Yes / No

### Emergency Readiness Analysis
Combines all prediction results to estimate:
- Emergency Readiness Score
- Capacity Percentage
- Hospital Status
- Risk Level
- Operational Recommendations

---

## Datasets Used

### Hospital Beds Dataset
Files:
- patients.csv
- services_weekly.csv

### ER Wait Time Dataset
Files:
- ER Wait Time Dataset.csv

### Staff Dataset
Files:
- staff.csv
- staff_schedule.csv

### COVID Capacity Dataset
Files:
- reported_hospital_capacity_admissions_facility-level_weekly_average_timeseries.csv

---

## Machine Learning Models

| Module | Algorithm |
|----------|----------|
| Bed Prediction | Random Forest Regressor |
| Wait Time Prediction | Random Forest Regressor |
| Staff Availability | Random Forest Classifier |

---

## Technology Stack

### Frontend
- ReactJS
- CSS

### Backend
- FastAPI
- Python

### Machine Learning
- Pandas
- NumPy
- Scikit-Learn
- Joblib

---

## Project Workflow

1. User enters hospital-related parameters.
2. Bed Prediction model estimates stay duration.
3. Wait Time model predicts ER waiting time.
4. Staff model predicts availability.
5. Smart Analysis Engine calculates:
   - Readiness Score
   - Capacity
   - Risk Level
   - Hospital Status
6. Recommendations are generated.

---

## Sample Output

- Predicted Stay: 6.58 Days
- Predicted Wait: 24.47 Minutes
- Staff Available: No

Generated Analysis:
- Emergency Readiness: 60%
- Capacity: 67.1%
- Hospital Status: Busy
- Risk Level: Moderate

Recommendation:
> Staff shortage detected. Assign backup staff.

---

## Future Enhancements

- GPS-based nearest hospital recommendation
- Real-time bed occupancy monitoring
- ICU availability tracking
- Ambulance management integration
- Multi-hospital comparison
- Live hospital dashboard
- Cloud deployment

---

## Author

**Varshini**  
B.E. Computer Science and Engineering  
Velammal Engineering College
