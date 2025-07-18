# Real-Time Financial Dashboard with LLM Integration

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

## 📝 Backend Project Roadmap

### Phase 1: Core System – ✅ Completed

- [x] 🗄️ Create SQLite DB with tables: transactions, users  
- [x] ⚙️ Build FastAPI backend: /transactions, /suspicious-transactions  
- [x] 🧠 Add Gemini-based LLM categorization and suspicious detection  
- [x] 🖥️ Create a test HTML frontend to validate backend functionality  
- [x] 📊 Add filters: bank, category  
- [x] 🔄 Add toggle for suspicious/all transactions  
- [x] 📈 Add summary stats and chart  
- [x] 🌊 Create stream simulator for new transactions  

### Phase 2: Real-time Intelligence + UX Polish – ⏳ In Progress

- [x] ➡️ Integrate Kafka producer in simulator  
- [x] ⬅️ Create Kafka consumer to listen for messages  
- [x] ⚡ Show suspicious txns live using WebSocket  
- [x] 🗺️ Prevent frontend duplication using txnMap  
- [ ] 🔬 Add Z-score based anomaly detection  
- [ ] 🗄️ Store anomalies in anomalies table  
- [ ] 🛣️ Create /anomalies route in API  
- [ ] ✨ Show anomalies in frontend (icon/highlight or separate tab)  
- [ ] 🤖 Add LLM reasoning for anomalies (optional enrichment)  
- [ ] 📅 Weekly summary: LLM-generated insights (spending, savings)  
- [ ] 🔮 Forecast spending for next week with LLM (basic ML or prompt)  
- [ ] 🧹 Clean up description using LLM (e.g., "AMZ*TRN" → "Amazon India")  
- [ ] 💰 (New) Personalized Budgeting (Allow users to set budgets by category, track progress, and receive alerts)  
- [ ] 🔁 (New) Subscription Management (Automatically identify and list recurring subscription payments)  
- [ ] 🧐 (New) Spending Pattern Recognition (Use clustering to identify user spending habits)  
- [ ] ⚡ (New) API & LLM Caching with Redis (Implement Redis to cache frequent database queries and LLM results for performance)  

### Phase 3: User Simulation – 🚧 Not Started

- [ ] 👥 Simulate multi-user: create dummy accounts  
- [ ] 🏦 Mock "Connect Bank" using OAuth screen (fake login)  
- [ ] 📥 Load per-user data (e.g., user_id with token)  
- [ ] 🔗 Optional: Integrate Mockaroo / Plaid sample feed  
- [ ] 🖱️ (New) Interactive Charts (Allow clicking on chart segments to filter the transaction table)  
- [ ] 🔍 (New) Full-Text Search (Add a search bar and API to find transactions by description)  
- [ ] 📄 (New) Data Export (Create an endpoint to download transactions as a CSV file)  

### Phase 4: Streaming Infra – ✅ Completed Early

- [x] 👍 Kafka producer setup  
- [x] 👍 Kafka consumer setup  
- [x] 👍 Background consumer in FastAPI using lifespan  
- [x] 👍 WebSocket broadcasting to frontend  

### Phase 5: Terminal Tools – 🚧 Not Started

- [ ] ⌨️ CLI tool to query: summary, anomalies, forecast  
- [ ] 🎨 Pretty terminal UX with `rich` or `textual`  

### Phase 6: Deployment and Production Readiness – 🚧 Not Started

- [ ] 🐳 Dockerize backend  
- [ ] 🐳 Dockerize frontend  
- [ ] 🐳 Docker Compose setup for Kafka + backend + frontend + Redis  
- [ ] 🚀 Deployment (Render / Railway / Vercel / localhost)  
- [ ] 🔑 Use `.env` for config and secrets  
- [ ] 🧪 (New) Automated Testing (Write unit and integration tests for the backend)  
- [ ] 🗃️ (New) Database Migrations (Integrate Alembic to manage schema changes without data loss)  
- [ ] 🔄 (New) CI/CD Pipeline (Set up GitHub Actions to run tests automatically)  
- [ ] ⚙️ (New) Robust Task Queue (Upgrade from BackgroundTasks to a Celery/RQ and Redis-based queue for background ETL jobs)  
- [ ] 🚫 (New) API Rate Limiting (Use Redis to protect login and other sensitive endpoints from abuse)  

---

## 🧩 Backend Workflow

![design](/pictures/Screenshot%202025-07-16%20at%209.46.38 PM.png)

---
