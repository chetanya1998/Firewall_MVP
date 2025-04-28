import time
import pandas as pd
import joblib
import os
from firewall.actions import block_ip

MODEL_PATH = "model/model.pkl"
LOG_FILE = "logs/access.log"

SEEN_LINES = set()

model = joblib.load(MODEL_PATH)

def parse_log_line(line):
    parts = line.strip().split("|")
    if len(parts) < 4:
        return None
    timestamp, ip, user_agent, path = parts
    return {"ip": ip.strip(), "user_agent": user_agent.strip(), "path": path.strip()}

def engineer_features(df):
    ip_counts = df.groupby('ip').size().rename('request_count')
    unique_paths = df.groupby('ip')['path'].nunique().rename('unique_paths')
    features = pd.concat([ip_counts, unique_paths], axis=1).fillna(0)
    return features.reset_index()

def main():
    print("🚀 Monitor Started...")
    while True:
        if not os.path.exists(LOG_FILE):
            print("⚠️ No access.log found. Waiting...")
            time.sleep(5)
            continue

        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        new_lines = [line for line in lines if line not in SEEN_LINES]
        SEEN_LINES.update(new_lines)

        records = [parse_log_line(line) for line in new_lines if parse_log_line(line)]

        if records:
            df = pd.DataFrame(records)
            features = engineer_features(df)
            X = features[['request_count', 'unique_paths']]

            print(f"Current Features for Prediction:\n{X}")

            preds = model.predict(X)
            print(f"Model Predictions: {preds}")

            anomalies = features[preds == -1]

            if anomalies.empty:
                print("⚠️ No anomalies detected... (model too strict?)")
                # FOR DEBUGGING: block dummy IP
                print("⚡ Blocking dummy IP for testing...")
                block_ip("123.123.123.123")  # add dummy for dashboard to test
            else:
                for ip in anomalies['ip']:
                    block_ip(ip)

        time.sleep(5)

if __name__ == "__main__":
    main()
