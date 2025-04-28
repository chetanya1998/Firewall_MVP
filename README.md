# 🚦 Smart Traffic Firewall: Real-Time Bot Detection and Traffic Analytics

A real-time, machine learning-powered smart firewall system that detects and blocks malicious bot traffic while providing deep insights into global traffic patterns through a live dashboard.

---

## 🧠 Project Overview

Smart Traffic Firewall is designed to:

- Detect suspicious traffic (bots, crawlers, scrapers) using machine learning
- Block malicious IPs automatically
- Monitor traffic in real-time via a beautiful Streamlit dashboard
- Visualize bot attacks over time and by geography
- Handle scalable traffic simulation for development/testing

---

## 🛠️ Technical Architecture

- **Backend Server**: Flask app that logs all incoming HTTP requests.
- **Traffic Simulator**: Sends realistic global traffic (human + bot) to the server.
- **Monitoring Agent**: Continuously analyzes access logs, predicts anomalies, and blocks malicious IPs.
- **Machine Learning Models**:
  - Isolation Forest
  - One-Class SVM
  - Local Outlier Factor
- **Dashboard**: Streamlit app providing live analytics (metrics, graphs, tables).
- **Storage**: Logs and blocked IPs are stored in the `logs/` directory.

---

## ⚙️ Core Features

| Feature | Description |
|:--------|:------------|
| 🌍 Global Traffic Simulation | Dynamic IPs and country-based traffic |
| 🛡️ Real-Time Bot Detection | ML models detect anomalies live |
| 🚫 Smart IP Blocking | Blocked IPs are logged and not re-blocked |
| 📈 Live Metrics & Graphs | See traffic trends, bot attacks over time |
| 🌐 Country-wise Analysis | Pie charts for geographic traffic distribution |
| 🔥 No Page Reload | Only internal components refresh every few seconds |

---

## 🎯 Business / Product Manager Perspective

From a **Product Manager** view:

- **Industry Problems Solved**:
  - AdTech: Click fraud detection
  - E-commerce: Scraper bots stealing product prices
  - SaaS: Account abuse by bots
  - EdTech: Automated login attacks
  - News Websites: Heavy scrapers reducing performance

- **Product Value Proposition**:
  - Proactively protects platforms against bot-based threats
  - Provides leadership teams live, actionable traffic analytics
  - Enables faster response times with real-time dashboards
  - Highly modular design — easy to plug into existing systems

- **Differentiators**:
  - Lightweight ML models (can deploy on-premise easily)
  - Full transparency (you see why an IP was blocked)
  - Easy to extend to cloud (AWS, Azure, GCP ready)

---

## 🏢 Industry Use Cases

| Industry | Use Case |
|:---------|:---------|
| AdTech | Click fraud prevention (fake ad clicks) |
| FinTech | Secure login systems (bot login attacks) |
| E-commerce | Prevent price scraping and stock scraping |
| EdTech | Stop mass data extraction from content libraries |
| SaaS | Stop account enumeration and credential stuffing attacks |

---

## 🏗️ Folder Structure

```plaintext
.
├── server/                # Flask server to log incoming traffic
│    └── app.py
├── simulator/             # Traffic simulator (realistic bot/human traffic)
│    └── Traffic_Simulator.py
├── firewall/              # Monitor + Actions (blockers)
│    ├── monitor.py
│    └── actions.py
├── model/                 # ML model training and saving
│    └── train_model.py
├── dashboard/             # Real-time visualization dashboard
│    └── app.py
├── logs/                  # Dynamic traffic and blocked IPs logs
│    ├── access.log
│    └── blocked_ips.log
├── README.md               # 📄 (You are reading it!)
