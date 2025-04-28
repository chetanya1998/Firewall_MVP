# dashboard/app.py

import streamlit as st
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Page Config
st.set_page_config(page_title="🚦 Smart Traffic Firewall Dashboard", layout="wide")
st.title("🚦 Smart Traffic Firewall Dashboard")

# Paths
ACCESS_LOG = "logs/access.log"
BLOCKED_IPS_LOG = "logs/blocked_ips.log"

# Helper functions
def load_access_logs():
    if not os.path.exists(ACCESS_LOG):
        return []
    with open(ACCESS_LOG, "r") as f:
        logs = [line.strip() for line in f if line.strip()]
    return logs

def load_blocked_ips():
    if not os.path.exists(BLOCKED_IPS_LOG):
        return []
    with open(BLOCKED_IPS_LOG, "r") as f:
        ips = [line.strip() for line in f if line.strip()]
    return ips

def classify_log(log_line):
    """Simple classifier based on user-agent."""
    try:
        parts = log_line.split("|")
        timestamp, ip, country, user_agent, path = [x.strip() for x in parts]
        if any(bot_indicator in user_agent.lower() for bot_indicator in ["scrapy", "curl", "python-urllib", "bot", "crawler"]):
            return "bot", timestamp, country
        else:
            return "human", timestamp, country
    except:
        return "unknown", None, None

# Realtime placeholders
metrics_placeholder = st.empty()
chart_placeholder = st.empty()
table_placeholder = st.empty()

# Live loop
while True:
    # Load logs
    logs = load_access_logs()
    blocked_ips = load_blocked_ips()

    # Classify traffic
    bot_timestamps = []
    human_timestamps = []

    for log in logs:
        classification, timestamp, country = classify_log(log)
        if timestamp:
            dt = datetime.fromtimestamp(float(timestamp))
            if classification == "bot":
                bot_timestamps.append(dt)
            elif classification == "human":
                human_timestamps.append(dt)

    # Calculate counts
    total_traffic = len(logs)
    total_bots = len(bot_timestamps)
    total_humans = len(human_timestamps)
    total_blocked_ips = len(blocked_ips)

    # Update Metrics
    with metrics_placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌐 Total Traffic Hits", total_traffic)
        col2.metric("🤖 Total Bot Hits", total_bots)
        col3.metric("🧑‍💻 Total Human Hits", total_humans)
        col4.metric("🚫 Blocked IPs", total_blocked_ips)

    # Update Bot Hits Line Chart
    with chart_placeholder.container():
        if bot_timestamps:
            df_bots = pd.DataFrame(bot_timestamps, columns=["timestamp"])
            df_bots["count"] = 1
            df_bots = df_bots.set_index("timestamp").resample('5s').sum().fillna(0).cumsum()

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df_bots.index, df_bots["count"], marker='o')
            ax.set_xlabel("Time")
            ax.set_ylabel("Cumulative Bot Hits")
            ax.set_title("🚀 Bot Hits Over Time (every 5s)")
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.info("No bot hits detected yet... 🚦")

    # Update Blocked IPs Table
    with table_placeholder.container():
        st.subheader("📋 Blocked IP Addresses")
        if blocked_ips:
            df_blocked = pd.DataFrame(blocked_ips, columns=["Blocked IP Address"])
            st.dataframe(df_blocked, use_container_width=True)
        else:
            st.warning("⚡ No blocked IP addresses yet.")

    # Sleep for 5 seconds and rerun loop (but page remains open)
    time.sleep(5)
