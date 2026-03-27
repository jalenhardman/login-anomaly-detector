import pandas as pd
import os

# Load the login data
file_path = "data/logins.csv"
df = pd.read_csv(file_path)

# Remove duplicate rows just in case
df = df.drop_duplicates()

# Clean up text fields
df["location"] = df["location"].astype(str).str.strip()
df["ip_address"] = df["ip_address"].astype(str).str.strip()
df["time"] = df["time"].astype(str).str.strip()

# Find the normal baseline behavior
baseline_location = df["location"].mode()[0]
baseline_ip = df["ip_address"].mode()[0]

# Function to flag unusual login times
def is_weird_time(time_str):
    try:
        hour = int(time_str.split(":")[0])
        return hour < 6 or hour > 22
    except (ValueError, IndexError):
        return True

# Flag anomalies
df["location_anomaly"] = df["location"].apply(
    lambda x: "YES" if x != baseline_location else "NO"
)

df["ip_anomaly"] = df["ip_address"].apply(
    lambda x: "YES" if x != baseline_ip else "NO"
)

df["weird_time"] = df["time"].apply(
    lambda x: "YES" if is_weird_time(x) else "NO"
)

# Calculate a simple risk score
def calculate_risk_score(row):
    score = 0

    if row["location_anomaly"] == "YES":
        score += 1
    if row["ip_anomaly"] == "YES":
        score += 1
    if row["weird_time"] == "YES":
        score += 1

    return score

df["risk_score"] = df.apply(calculate_risk_score, axis=1)

# Label the risk level
def label_risk(score):
    if score == 0:
        return "Normal"
    elif score == 1:
        return "Suspicious"
    else:
        return "High Risk"

df["risk_level"] = df["risk_score"].apply(label_risk)

# Make sure output folder exists
os.makedirs("output", exist_ok=True)

# Save the flagged results
output_path = "output/flagged_logins.csv"
df.to_csv(output_path, index=False)

# Print results
print("Baseline Location:", baseline_location)
print("Baseline IP:", baseline_ip)
print("\nFlagged Login Results:\n")
print(df)

print("\nSummary:")
print(df["risk_level"].value_counts())
print(f"\nResults saved to: {output_path}")