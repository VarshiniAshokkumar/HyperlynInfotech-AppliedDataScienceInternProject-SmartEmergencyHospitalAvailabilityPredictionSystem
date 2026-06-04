import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [age, setAge] = useState("");
  const [satisfaction, setSatisfaction] = useState("");
  const [service, setService] = useState("emergency");

  const [ratio, setRatio] = useState("");
  const [facility, setFacility] = useState("");
  const [patientSat, setPatientSat] = useState("");

  const [week, setWeek] = useState("");
  const [role, setRole] = useState("doctor");
  const [staffService, setStaffService] = useState("emergency");

  const [dashboard, setDashboard] = useState(null);

  async function runPredictions() {
    try {
      const bedRes = await axios.post(
        "http://127.0.0.1:8000/predict-bed",
        {
          age: Number(age),
          satisfaction: Number(satisfaction),
          service,
        }
      );

      const stay =
        bedRes.data.predicted_length_of_stay;

      const waitRes = await axios.post(
        "http://127.0.0.1:8000/predict-waittime",
        {
          season: "Summer",
          time_of_day: "Morning",
          urgency_level: "High",
          nurse_ratio: Number(ratio),
          specialist_availability: "Available",
          facility_size: Number(facility),
          patient_satisfaction: Number(patientSat),
        }
      );

      const wait =
        waitRes.data.predicted_wait_time;

      const staffRes = await axios.post(
        "http://127.0.0.1:8000/predict-staff",
        {
          week: Number(week),
          role,
          service: staffService,
        }
      );

      const staff =
        staffRes.data.staff_available;

      const statusRes = await axios.post(
        "http://127.0.0.1:8000/hospital-status",
        {
          stay,
          wait,
          staff,
        }
      );

      setDashboard({
        stay,
        wait,
        staff,
        ...statusRes.data,
      });

    } catch (error) {
      alert("Backend API Error");
      console.log(error);
    }
  }

  const getStatusColor = () => {
    if (!dashboard) return "";

    if (dashboard.hospital_status === "Normal")
      return "#d4edda";

    if (dashboard.hospital_status === "Busy")
      return "#fff3cd";

    return "#f8d7da";
  };

  return (
    <div className="container">

      <div className="header">
        <h1>
          🏥 Smart Emergency Hospital Availability Prediction System
        </h1>
        <p>
          AI Powered Hospital Resource Analytics Dashboard
        </p>
      </div>

      <div className="grid">

        <div className="card">
          <h2>🛏 Bed Prediction</h2>

          <input
            type="number"
            placeholder="Patient Age"
            onChange={(e) =>
              setAge(e.target.value)
            }
          />

          <input
            type="number"
            placeholder="Satisfaction Score"
            onChange={(e) =>
              setSatisfaction(e.target.value)
            }
          />

          <select
            onChange={(e) =>
              setService(e.target.value)
            }
          >
            <option value="emergency">
              Emergency
            </option>
            <option value="ICU">
              ICU
            </option>
            <option value="surgery">
              Surgery
            </option>
            <option value="general_medicine">
              General Medicine
            </option>
          </select>
        </div>

        <div className="card">
          <h2>⏱ ER Wait Prediction</h2>

          <input
            type="number"
            placeholder="Nurse Ratio"
            onChange={(e) =>
              setRatio(e.target.value)
            }
          />

          <input
            type="number"
            placeholder="Facility Size"
            onChange={(e) =>
              setFacility(e.target.value)
            }
          />

          <input
            type="number"
            placeholder="Patient Satisfaction"
            onChange={(e) =>
              setPatientSat(e.target.value)
            }
          />
        </div>

        <div className="card">
          <h2>👨‍⚕️ Staff Prediction</h2>

          <input
            type="number"
            placeholder="Week Number"
            onChange={(e) =>
              setWeek(e.target.value)
            }
          />

          <select
            onChange={(e) =>
              setRole(e.target.value)
            }
          >
            <option value="doctor">
              Doctor
            </option>
            <option value="nurse">
              Nurse
            </option>
          </select>

          <select
            onChange={(e) =>
              setStaffService(e.target.value)
            }
          >
            <option value="emergency">
              Emergency
            </option>
            <option value="ICU">
              ICU
            </option>
            <option value="surgery">
              Surgery
            </option>
          </select>
        </div>
      </div>

      <button
        className="predict-btn"
        onClick={runPredictions}
      >
        🚀 Run Smart Analysis
      </button>

      {dashboard && (
        <>
          <div className="results-grid">

            <div className="result-card">
              <h3>📊 Emergency Readiness</h3>
              <h1>
                {dashboard.readiness_score}%
              </h1>

              <div className="progress">
                <div
                  className="fill"
                  style={{
                    width:
                      dashboard.readiness_score +
                      "%",
                  }}
                />
              </div>
            </div>

            <div className="result-card">
              <h3>🏥 Capacity</h3>
              <h1>
                {dashboard.capacity}%
              </h1>
            </div>

            <div
              className="result-card"
              style={{
                background:
                  getStatusColor(),
              }}
            >
              <h3>🚨 Hospital Status</h3>
              <h1>
                {
                  dashboard.hospital_status
                }
              </h1>
            </div>

            <div className="result-card">
              <h3>⚠ Risk Level</h3>
              <h1>
                {dashboard.risk_level}
              </h1>
            </div>

          </div>

          <div className="results-grid">

            <div className="result-card">
              <h3>🛏 Predicted Stay</h3>
              <h1>
                {dashboard.stay} Days
              </h1>
            </div>

            <div className="result-card">
              <h3>⏱ Predicted Wait</h3>
              <h1>
                {dashboard.wait} Min
              </h1>
            </div>

            <div className="result-card">
              <h3>👨‍⚕️ Staff Available</h3>
              <h1>
                {dashboard.staff}
              </h1>
            </div>

          </div>

          <div className="recommendation">
            <h2>
              📋 Recommendations
            </h2>

            <ul>
              {dashboard.recommendations.map(
                (item, index) => (
                  <li key={index}>
                    {item}
                  </li>
                )
              )}
            </ul>
          </div>

          <div className="footer-card">
            <h3>
              Machine Learning Models Used
            </h3>

            <p>
              ✅ Random Forest - Bed
              Prediction
            </p>

            <p>
              ✅ Random Forest - ER Wait
              Prediction
            </p>

            <p>
              ✅ Random Forest - Staff
              Availability Prediction
            </p>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
