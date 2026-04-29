# 🚀 End-to-End FinTech Fraud Detection & AML Pipeline

## 📊 Project Overview
This project is an end-to-end data pipeline designed to detect financial fraud and Anti-Money Laundering (AML) activities. It bridges the gap between backend data engineering, predictive machine learning, and executive business intelligence. 

Instead of relying solely on traditional rule-based flagging, this project utilizes a Machine Learning model to identify hidden fraud patterns, ultimately securing **$417.02 Million** in simulated banking funds.

## 🛠️ Technology Stack
* **Data Engineering & Analysis:** PostgreSQL / Advanced SQL
* **Machine Learning:** Python (Pandas, Scikit-Learn, Imbalanced-Learn)
* **Business Intelligence:** Power BI

---

## 🏗️ Project Architecture & Phases

### Phase 1: Forensic Data Engineering (SQL)
To establish a baseline for fraud detection, I engineered advanced SQL queries to track the movement of illicit funds. 
* Utilized **Recursive CTEs** to trace multi-step money laundering chains across different accounts.
* Applied **Window Functions** to calculate rolling sums of fraudulent activity, helping to identify temporal distribution patterns of financial crimes.

### Phase 2: Predictive AI Modeling (Python)
Since financial fraud datasets are highly imbalanced (legitimate transactions vastly outnumber fraudulent ones), standard accuracy metrics are insufficient.
* Conducted Feature Engineering using **Pandas** (One-Hot Encoding transaction types, calculating balance errors).
* Handled extreme class imbalance utilizing **SMOTE** (Synthetic Minority Over-sampling Technique).
* Trained and evaluated a **Random Forest Classifier** to predict fraudulent transfers and cash-outs with high precision.

### Phase 3: Executive Dashboard (Power BI)
A model is only as valuable as its business impact. The predictions from the ML model were exported and visualized in Power BI to provide stakeholders with actionable insights.
* **Stakeholder-Driven KPIs:** Built a custom KPI card proving the AI engine successfully intercepted **$417.02M** in potential losses.
* **Root Cause Analysis:** Deployed an interactive **Decomposition Tree** to allow executives to dynamically drill down into the paths of actual vs. predicted fraud.
* **Transaction Breakdown:** Visualized the distribution of flagged transactions across transfer types to monitor false-positive rates.

---

## 📁 Repository Structure
\`\`\`text
├── 1_SQL_Data_Engineering/
│   ├── SQL_Data_Analyst_Project.pdf     # SQL Queries and AML Logic
├── 2_Machine_Learning/
│   ├── aml_model.py                     # Python ML script (SMOTE & Random Forest)
│   ├── requirements.txt                 # Project dependencies
├── 3_PowerBI_Dashboard/
│   ├── Enterprise_Fraud_Dashboard.pbix  # Interactive Power BI file
│   ├── Dashboard_Screenshot.png         # High-res image of the final dashboard
├── Data/
│   ├── fraud_predictions_for_powerbi.csv # Processed dataset with AI predictions
└── README.md
\`\`\`

## 💡 How to Run the Python Model
1. Clone this repository.
2. Install the required packages: `pip install -r requirements.txt`
3. Run the ML script: `python Machine_Learning/aml_model.py`
