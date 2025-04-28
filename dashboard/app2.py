# dashboard/app.py

import streamlit as st
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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
            return "bot", float(timestamp), country
        else:
            return "human", float(timestamp), country
    except:
        return "unknown", None, None

# Preset Options
st.sidebar.header("🛠️ View Settings")
time_filter = st.sidebar.selectbox(
    "Select Traffic Time Window",
    ("In Last Hour", "Today", "Last 7 Days", "Last 30 Days")
)

# Time Filter Mapping
now = datetime.utcnow()
if time_filter == "In Last Hour":
    time_threshold = now - timedelta(hours=1)
elif time_filter == "Today":
    time_threshold = datetime(now.year, now.month, now.day)
elif time_filter == "Last 7 Days":
    time_threshold = now - timedelta(days=7)
elif time_filter == "Last 30 Days":
    time_threshold = now - timedelta(days=30)
else:
    time_threshold = datetime.min  # no filtering

# Live Placeholders
metrics_placeholder = st.empty()
chart_placeholder = st.empty()
table_placeholder = st.empty()

# Live loop
while True:
    logs = load_access_logs()
    blocked_ips = load_blocked_ips()

    bot_timestamps = []
    human_timestamps = []

    for log in logs:
        classification, timestamp, country = classify_log(log)
        if timestamp:
            dt = datetime.utcfromtimestamp(timestamp)
            if dt >= time_threshold:
                if classification == "bot":
                    bot_timestamps.append(dt)
                elif classification == "human":
                    human_timestamps.append(dt)

    total_traffic = len(bot_timestamps) + len(human_timestamps)
    total_bots = len(bot_timestamps)
    total_humans = len(human_timestamps)
    total_blocked_ips = len(blocked_ips)

    # Metrics
    with metrics_placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌐 Total Traffic Hits", total_traffic)
        col2.metric("🤖 Total Bot Hits", total_bots)
        col3.metric("🧑‍💻 Total Human Hits", total_humans)
        col4.metric("🚫 Blocked IPs", total_blocked_ips)

    # Bot Hits Line Chart
    with chart_placeholder.container():
        if bot_timestamps:
            df_bots = pd.DataFrame(bot_timestamps, columns=["timestamp"])
            df_bots["count"] = 1
            df_bots = df_bots.set_index("timestamp").resample('5min').sum().fillna(0).cumsum()

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df_bots.index, df_bots["count"], marker='o')
            ax.set_xlabel("Time")
            ax.set_ylabel("Cumulative Bot Hits")
            ax.set_title(f"🚀 Bot Hits Over Time ({time_filter})")
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.info("No bot hits detected in selected time window... 🚦")

    # Blocked IP Table
    with table_placeholder.container():
        st.subheader("📋 Blocked IP Addresses")
        if blocked_ips:
            df_blocked = pd.DataFrame(blocked_ips, columns=["Blocked IP Address"])
            st.dataframe(df_blocked, use_container_width=True)
        else:
            st.warning("⚡ No blocked IP addresses yet.")

    # Sleep and rerun
    time.sleep(5)
