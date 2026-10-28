# Enterprise Decision Intelligence Platform

An end-to-end analytical decision intelligence platform transforming 15,000+ multi-dimensional enterprise transactions into automated prescriptive business interventions. Built using a high-performance **DuckDB** star schema, **Python/Scikit-learn** machine learning models, **Power BI**, and **Tableau**.

---

## 🏗 Platform Architecture

---

## 🌟 Key Highlights & Capabilities

### 1. Data Engineering & Dimensional Modeling (DuckDB)
- Engineered a dimensional star schema (`Fact_Transactions`, `Dim_Customer`, `Dim_Product`, `Dim_Date`) from multi-dimensional transactional records.
- Standardized surrogate keys across all dimensions to ensure fast analytical aggregation and eliminate join redundancy.

### 2. Machine Learning & Prescriptive Engine (Python)
- **RFM Customer Segmentation**: Segmented customer accounts using K-Means clustering into four operational tiers:
  - `Tier 1: Champions`
  - `Tier 2: High Potential`
  - `Tier 3: At-Risk Frequenters`
  - `Tier 4: Low-Engagement`
- **Predictive Churn Risk**: Trained a Random Forest classifier evaluating purchase recency, transaction frequency, and discount dependency to output account-level churn probability scores.
- **Rule-Based Decision Logic**: Generated automated strategic recommendations (e.g., *Executive Sponsor Intervention*, *Volume Rebate Restructure*, *Re-engagement Discount*).

### 3. Operational What-If Cockpit (Power BI)
- Built an operational cockpit tracking `Total Revenue`, `Total Margin`, `Margin %`, and `At Risk Revenue`.
- Implemented dynamic What-If parameter sliders to model pricing elasticity impacts ($\pm 20\%$) across customer tiers in real time.

### 4. Exploratory Deep-Dive (Tableau)
- Visualized global profit distribution across North America, EMEA, APAC, and LATAM markets.
- Built a multi-tier continuous cohort churn decay curve tracking long-term attrition trajectories.

---

## 🛠 Tech Stack

| Category | Tools & Technologies |
| :--- | :--- |
| **Languages** | Python 3.10+, SQL |
| **Libraries** | Pandas, NumPy, Scikit-learn, Scipy |
| **Database / Warehousing** | DuckDB |
| **Business Intelligence** | Microsoft Power BI, Tableau Desktop Public Edition |
| **Version Control** | Git, GitHub |

---

## 📂 Project Structure

```text
decision_intelligence_platform/
├── data/
│   ├── raw/
│   │   └── raw_transactions.csv
│   ├── processed/
│   │   ├── Fact_Transactions.csv
│   │   ├── Dim_Customer.csv
│   │   ├── Dim_Product.csv
│   │   ├── Dim_Date.csv
│   │   └── Fact_Customer_Insights.csv
│   └── enterprise_warehouse.duckdb
├── sql/
│   └── 01_star_schema.sql
├── python/
│   ├── generate_raw_data.py
│   ├── build_warehouse.py
│   └── decision_engine.py
├── bi_artifacts/
│   ├── enterprise_decision_cockpit.pbix
│   └── executive_deepdive.twbx
├── requirements.txt
├── .gitignore
└── README.md