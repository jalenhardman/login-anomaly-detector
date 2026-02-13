# 🔐 Login Anomaly Detector (Python)

Simulates real-world SOC detection by identifying anomalous login behavior and potential account compromise.
A lightweight cybersecurity tool that analyzes login activity from log files and detects suspicious behavior using rule-based anomaly detection and risk scoring.

---

## 🧠 Overview

This project simulates how security systems (SIEM/SOC tools) monitor login activity to identify potential threats such as brute force attacks and unusual login behavior.

The script processes login events, applies detection logic, and generates structured alert reports.

---

## 🚨 Detection Capabilities

The system identifies:

### 1. New Location Anomaly

Flags when a user logs in from a location that has not been previously observed (after establishing a baseline).

### 2. Brute Force Attack Detection

Detects multiple consecutive failed login attempts (default: 5 failures in a row).

### 3. Success After Failed Attempts (High Risk)

Flags a successful login that occurs shortly after a brute force streak (within 30 minutes).

---

## 📊 Risk Scoring & Severity

Each flagged event is assigned a **risk score** and **severity level**:

| Condition                 | Score |
| ------------------------- | ----: |
| New location              |   +40 |
| Brute force streak        |   +60 |
| Success after fail streak |   +80 |

### Severity Levels

* **LOW**: < 60
* **MEDIUM**: 60–99
* **HIGH**: 100+

---

## 📁 Project Structure

```
login-anomaly-detector/
│
├── detector.py        # Main detection script
├── logins.csv         # Input log file
├── flagged.csv        # Output: flagged suspicious events
├── summary.txt        # Output: summary report
└── README.md          # Project documentation
```

---

## ⚙️ How It Works

1. Reads login data from `logins.csv`
2. Tracks user behavior (locations, login attempts)
3. Applies detection rules:

   * Identifies anomalies
   * Detects brute force patterns
   * Correlates suspicious sequences
4. Assigns risk scores and severity levels
5. Outputs results into:

   * `flagged.csv`
   * `summary.txt`

---

## ▶️ How to Run

Make sure you have Python installed.

```bash
python3 detector.py
```

---

## 📤 Output Files

### flagged.csv

Contains all flagged login events with:

* timestamp
* user
* location
* result
* risk_score
* severity
* reasons

### summary.txt

Provides:

* total number of alerts
* severity breakdown
* top flagged events

---

## 🧪 Real-World Detection Scenario

A user experiences:

* Multiple failed login attempts (possible brute force)
* Followed by a successful login
* From a new geographic location

The system flags this as a **HIGH severity event** due to correlated suspicious behavior.

---

## 🎯 Skills Demonstrated

* Python scripting
* Log analysis
* Cybersecurity detection logic
* Behavioral analysis
* Risk scoring systems
* Threat pattern recognition

---

## 🚀 Future Improvements

* Add IP-based detection
* Implement impossible travel logic (geo-distance/time)
* Integrate with real-time log streams
* Add machine learning-based anomaly detection
* Build a web dashboard for visualization

---

## 📌 Author

Built as part of a cybersecurity portfolio project focused on practical, hands-on detection engineering.
