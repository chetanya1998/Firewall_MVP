# firewall/monitor.py

import time
import pandas as pd
import joblib
import os
from firewall.actions import block_ip

# Configurations
MODEL_NAME = "IsolationForest"  # Options: IsolationForest, OneClassSVM, LocalOutlierFactor
MODEL_PATH = f"model/{MODEL_NAME}_model.pkl"
SCALER_PATH = f"model/{MODEL_NAME}_scaler.pkl"
LOG_FILE = "logs/access.log"

SEEN_LINES = set()

# Load model and scaler
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print(f"✅ Loaded {MODEL_NAME} model and scaler successfully!")
except Exception as e:
    print(f"❌ Error loading model or scaler: {e}")
    exit(1)

def parse_log_line(line):
    """Parse a line from access.log."""
    parts = line.strip().split("|")
    if len(parts) < 5:
        return None
    timestamp, ip, country, user_agent, path = [x.strip() for x in parts]
    return {
        "ip": ip,
        "country": country,
        "user_agent": user_agent,
        "path": path
    }

def engineer_features(df):
    """Feature engineering to match training phase."""
    ip_counts = df.groupby('ip').size().rename('request_count')
    unique_paths = df.groupby('ip')['path'].nunique().rename('unique_paths')
    unique_countries = df.groupby('ip')['country'].nunique().rename('unique_countries')

    features = pd.concat([ip_counts, unique_paths, unique_countries], axis=1).fillna(0)
    return features.reset_index()

def monitor_traffic():
    """Continuously monitor traffic and block detected bots."""
    print("🚀 Smart Traffic Monitor Started... Monitoring logs in real-time...")
    while True:
        if not os.path.exists(LOG_FILE):
            print("⚠️ No access.log file found yet. Waiting...")
            time.sleep(5)
            continue

        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        # Find new lines
        new_lines = [line for line in lines if line not in SEEN_LINES]
        SEEN_LINES.update(new_lines)

        # Parse lines
        records = [parse_log_line(line) for line in new_lines if parse_log_line(line)]

        if records:
            df = pd.DataFrame(records)

            features = engineer_features(df)
            if features.empty:
                time.sleep(5)
                continue

            X = features[['request_count', 'unique_paths', 'unique_countries']]
            X_scaled = scaler.transform(X)

            preds = model.predict(X_scaled)

            anomalies = features[preds == -1]

            if not anomalies.empty:
                print(f"🚨 {len(anomalies)} bot(s) detected!")

                for ip in anomalies['ip']:
                    block_ip(ip)

        time.sleep(5)

if __name__ == "__main__":
    monitor_traffic()
