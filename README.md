# 💸 Real-Time Financial Dashboard with LLM Integration

This is a smart financial analytics backend that simulates real-time bank transactions, categorizes them using an LLM, detects anomalies, and generates insightful weekly summaries and forecasts. Built with **FastAPI**, **SQLite**, **Kafka**, and **LLMs**

---

## 🚀 Features

- 🔁 Real-time Kafka transaction stream
- 🧠 LLM-powered transaction categorization
- ⚠️ Anomaly detection using Z-score + LLM
- 📊 Weekly summary generation with insights
- 📅 Smart budget forecasting
- 🔗 Simulated “Connect Bank” flow with OAuth-like experience
- 💬 Terminal CLI UX for commands like `summary`, `analyze`, etc.
- 🧽 LLM-based cleaning of cryptic transaction descriptions

---

## 📦 Tech Stack

- **Backend:** FastAPI, SQLAlchemy
- **Database:** SQLite (dev) → upgradable to PostgreSQL
- **Stream:** Kafka (for real-time simulation)
- **LLM:** Gemini
- **Language:** Python 3.11+

---


