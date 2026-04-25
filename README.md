# 🚀 AI Expense Auditor Agent

An AI-powered full-stack application that automates corporate expense auditing, detects fraud, and enforces policy compliance using intelligent pipelines and real-time analytics.

---

## 📌 Overview

The AI Expense Auditor Agent streamlines the process of auditing expense data by combining:

- 📊 Data processing & validation  
- ⚙️ Rule-based compliance checks  
- 🤖 AI-driven anomaly detection  
- 📈 Insightful dashboards  

It transforms raw CSV expense data into a comprehensive audit report with actionable insights.

---

## 🧠 Key Features

### 🔍 Automated Expense Auditing
- Upload CSV files with transaction data
- Automatically cleans, standardizes, and processes data

### 🚨 Fraud & Anomaly Detection
- Detects unusual spending patterns
- Identifies duplicate or suspicious transactions
- Flags risky vendor usage

### 📏 Policy Compliance Enforcement
- Budget threshold violations
- Frequency-based violations
- Missing documentation detection

### 📊 Interactive Dashboard
- Executive summary
- Risk scoring
- Spending trends
- Category distribution
- Top spenders

### 🤖 AI Insights (Llama-based)
- Natural language summaries
- Financial recommendations
- Cost optimization suggestions

---

## 🏗️ System Architecture
Frontend (Flutter)
↓
FastAPI Backend (/api/full-audit)
↓
Full Audit Pipeline
↓
[Phase 1] Data Preparation
[Phase 2] Rule Engine
[Phase 3] Financial Auditor AI
[Phase 4] Report Generation
↓
JSON Response → Dashboard UI


---

## ⚙️ Tech Stack

### 🎨 Frontend
- Flutter (Dart)
- Glassmorphism UI
- Custom widgets (GlassContainer)
- Animated loading screens

### 🧩 Backend
- Python
- FastAPI
- Pandas / NumPy

### 🤖 AI / Intelligence Layer
- Statistical analysis (variance, distributions)
- Rule-based engine
- Local LLM integration (Llama 3 via Ollama)

---

## 🔄 Workflow Explained

### 1️⃣ User Interaction
- Upload CSV file
- View animated processing screen
- Receive dashboard-based audit report

---

### 2️⃣ Data Preparation
Handled by **DataPrepAgentOrchestrator**:
- Column mapping (dynamic schema detection)
- Data cleaning (missing values, formatting)
- Feature enrichment:
  - Spending level classification
  - Behavioral tagging

---

### 3️⃣ Rule-Based Compliance Engine
Detects:
- 💸 High-value transactions (> threshold)
- 🔁 Duplicate entries
- 📅 High-frequency submissions
- 📝 Missing descriptions

---

### 4️⃣ Financial Auditor Engine
Core intelligence layer:
- Risk scoring (Low / Medium / High)
- Anomaly detection (statistical deviations)
- Fraud signal correlation
- Vendor & employee behavior analysis

---

### 5️⃣ Output Generation
Returns structured JSON:
- Executive summary
- Risk insights
- Violations breakdown
- Visualization-ready data

---

## 📊 Example Insights Generated

- “Employee spending spiked 2σ above normal behavior”
- “Category ‘Travel’ contributes to 45% of expenses”
- “Frequent transactions with high-risk vendor detected”
- “Potential savings: Negotiate bulk vendor contracts”

---

## 🚀 API Endpoint

### `POST /api/full-audit`

**Input:**
- CSV file (multipart/form-data)

**Output:**
- JSON audit report

---

## 🖥️ UI Highlights

- 🌙 Dark theme with glassmorphism
- 📊 Real-time charts & analytics
- ⚡ Smooth transitions and animations
- 🧠 AI chat interface (future/extended feature)

---

## 🧪 Future Improvements

- 🔗 PDF report generation
- 💬 Chat with audit report (RAG-based AI)
- 📡 Real-time expense monitoring
- 🔐 Role-based access control
- 📱 Mobile-first optimizations

---

## 📦 Installation & Setup

### Backend (FastAPI)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend (Flutter)
flutter pub get
flutter run

🧠 Why This Project?

This system demonstrates:

Agentic AI workflows
Real-world financial auditing logic
Integration of LLMs into structured pipelines
Full-stack production-ready architecture
🤝 Contributing

Contributions are welcome!
Feel free to fork, open issues, and submit PRs.
