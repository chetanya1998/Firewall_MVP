# model/train_model.py

import pandas as pd
import joblib
import os
import time
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

LOG_FILE = "logs/access.log"
MODEL_DIR = "model/"

# Ensure model folder exists
os.makedirs(MODEL_DIR, exist_ok=True)

def load_logs():
    """Load and parse the access logs."""
    if not os.path.exists(LOG_FILE):
        raise FileNotFoundError(f"⚠️ Log file not found at {LOG_FILE}")
    
    df = pd.read_csv(
        LOG_FILE,
        delimiter="|",
        names=["timestamp", "ip", "country", "user_agent", "path"],
        skipinitialspace=True
    )
    return df

def engineer_features(df):
    """Feature engineering for model training."""
    df['timestamp'] = df['timestamp'].astype(float)
    df['minute'] = df['timestamp'].apply(lambda x: time.gmtime(x).tm_min)

    # Group by IP
    ip_counts = df.groupby('ip').size().rename('request_count')
    unique_paths = df.groupby('ip')['path'].nunique().rename('unique_paths')
    country_counts = df.groupby('ip')['country'].nunique().rename('unique_countries')

    # Merge features
    features = pd.concat([ip_counts, unique_paths, country_counts], axis=1).fillna(0)
    return features.reset_index()

def train_models(features):
    """Train multiple models and return them."""
    X = features[['request_count', 'unique_paths', 'unique_countries']]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Models to train
    models = {
        "IsolationForest": IsolationForest(contamination=0.05, random_state=42),
        "OneClassSVM": OneClassSVM(kernel='rbf', gamma='scale', nu=0.05),
        "LocalOutlierFactor": LocalOutlierFactor(novelty=True, contamination=0.05, n_neighbors=20)
    }

    trained_models = {}
    for name, model in models.items():
        model.fit(X_scaled)
        trained_models[name] = (model, scaler)
        print(f"✅ {name} trained successfully!")

    return trained_models

def save_models(trained_models):
    """Save all models and scalers."""
    for name, (model, scaler) in trained_models.items():
        model_path = os.path.join(MODEL_DIR, f"{name}_model.pkl")
        scaler_path = os.path.join(MODEL_DIR, f"{name}_scaler.pkl")
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        print(f"📦 Saved {name} model and scaler.")

def main():
    print("🚀 Starting Training Process...")

    logs_df = load_logs()

    if logs_df.empty:
        print("⚠️ Log file is empty. Please generate traffic first.")
        return

    features_df = engineer_features(logs_df)
    trained_models = train_models(features_df)
    save_models(trained_models)

    print("🏁 All models trained and saved!")

if __name__ == "__main__":
    main()
