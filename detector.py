import csv
from datetime import datetime, timezone

INPUT_FILE = "logins.csv"
OUTPUT_FILE = "flagged.csv"
SUMMARY_FILE = "summary.txt"

FAIL_STREAK_THRESHOLD = 5
SUCCESS_WINDOW_MINUTES = 30

def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)

def severity_from_score(score: int) -> str:
    if score >= 100:
        return "HIGH"
    if score >= 60:
        return "MEDIUM"
    return "LOW"

known_locations = {}
fail_streak = {}
streak_reached_time = {}

flagged_rows = []

with open(INPUT_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ts = parse_ts(row["timestamp"])
        user = row["user"]
        location = row["location"]
        result = row["result"].lower().strip()

        if user not in known_locations:
            known_locations[user] = set()
        if user not in fail_streak:
            fail_streak[user] = 0
        if user not in streak_reached_time:
            streak_reached_time[user] = None

        reasons = []
        score = 0

        # New location (after baseline exists)
        if len(known_locations[user]) > 0 and location not in known_locations[user]:
            reasons.append("new_location")
            score += 40

        # Always learn location
        known_locations[user].add(location)

        # Fail/success logic
        if result == "failure":
            fail_streak[user] += 1

            if fail_streak[user] == FAIL_STREAK_THRESHOLD:
                streak_reached_time[user] = ts
                reasons.append("brute_force_streak")
                score += 60

        elif result == "success":
            if streak_reached_time[user] is not None:
                minutes_since = (ts - streak_reached_time[user]).total_seconds() / 60.0
                if 0 <= minutes_since <= SUCCESS_WINDOW_MINUTES:
                    reasons.append("success_after_fail_streak")
                    score += 80

            fail_streak[user] = 0
            streak_reached_time[user] = None

        if reasons:
            row["risk_score"] = score
            row["severity"] = severity_from_score(score)
            row["reasons"] = ",".join(reasons)
            flagged_rows.append(row)

# Sort alerts by risk score (highest first), then newest first
flagged_rows.sort(key=lambda r: (r["risk_score"], r["timestamp"]), reverse=True)

# Write flagged.csv
fieldnames = ["timestamp", "user", "location", "result", "risk_score", "severity", "reasons"]
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in flagged_rows:
        r_out = dict(r)
        r_out["risk_score"] = str(r_out["risk_score"])  # csv needs strings
        writer.writerow(r_out)

# Write summary.txt
with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
    f.write("Login Anomaly Detector Summary\n")
    f.write("=============================\n\n")
    f.write(f"Total alerts: {len(flagged_rows)}\n")
    f.write(f"Fail streak threshold: {FAIL_STREAK_THRESHOLD}\n")
    f.write(f"Success-after-streak window (min): {SUCCESS_WINDOW_MINUTES}\n\n")

    highs = [r for r in flagged_rows if r["severity"] == "HIGH"]
    meds  = [r for r in flagged_rows if r["severity"] == "MEDIUM"]
    lows  = [r for r in flagged_rows if r["severity"] == "LOW"]

    f.write(f"HIGH: {len(highs)} | MEDIUM: {len(meds)} | LOW: {len(lows)}\n\n")
    f.write("Top alerts:\n")

    for i, r in enumerate(flagged_rows[:3], start=1):
        f.write(f"{i}. [{r['severity']}] user={r['user']} location={r['location']} result={r['result']} ")
        f.write(f"score={r['risk_score']} reasons={r['reasons']}\n")

print(f"Done. Wrote {len(flagged_rows)} alerts to {OUTPUT_FILE} and summary to {SUMMARY_FILE}")
