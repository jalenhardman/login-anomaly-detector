# Login Anomaly Detection Project

## Overview
This project is a simple anomaly detection tool built in Python to identify suspicious login activity in security logs. It analyzes login behavior using baseline patterns and flags unusual events based on location, IP address, and login time.

## Objective
The goal of this project is to simulate how a security analyst might detect suspicious login behavior by comparing normal user activity against unusual events.

## Tools Used
- Python
- Pandas

## Detection Logic
The script uses the following rules:
- Flags logins from locations that differ from the user's most common location
- Flags logins from IP addresses that differ from the user's most common IP
- Flags logins that occur during unusual hours, defined as before 6:00 AM or after 10:00 PM
- Assigns a risk score based on how many anomaly conditions are triggered

## Risk Scoring
- 0 = Normal
- 1 = Suspicious
- 2 or 3 = High Risk

## Files
- `data/logins.csv` → sample login dataset
- `anomaly_detector.py` → Python script for detection logic
- `output/flagged_logins.csv` → output file with flagged results

## Outcome
This project demonstrates basic threat detection concepts by identifying suspicious login attempts through behavior analysis. It shows foundational skills in log analysis, Python scripting, and security-focused thinking.

## What I Learned
Through this project, I strengthened my understanding of:
- security log analysis
- anomaly detection concepts
- behavioral baselining
- Python data processing with pandas