# 📊 RetentionIQ

### Customer Behavior Analytics, RFM Segmentation & Churn Intelligence Dashboard
<img width="1897" height="645" alt="image" src="https://github.com/user-attachments/assets/9f84f2d7-0a30-4229-8871-cb15bce3949e" />
<img width="1918" height="911" alt="image" src="https://github.com/user-attachments/assets/5dd01356-4160-4dc0-a372-cc4abf187162" />
<img width="1897" height="898" alt="image" src="https://github.com/user-attachments/assets/11233e14-0e1a-4138-8ca8-b3e4a3886b2f" />
<img width="1910" height="874" alt="image" src="https://github.com/user-attachments/assets/7bf9d3ad-67dc-4d6b-bc28-2fbc008aba09" />
<img width="1909" height="876" alt="image" src="https://github.com/user-attachments/assets/bab81101-2552-4af1-ae4b-c36b5574ca18" />
<img width="1919" height="857" alt="image" src="https://github.com/user-attachments/assets/5c84e8a4-2f33-42b9-b539-201be7062d75" />
<img width="1919" height="872" alt="image" src="https://github.com/user-attachments/assets/18a1790b-7baa-45db-a46c-efc1699c6630" />
<img width="1919" height="796" alt="image" src="https://github.com/user-attachments/assets/94fb34b2-ac6e-49b3-bcad-b55665b64516" />






**[🔗 View Live Dashboard](https://retentioniq-odxzwnbcfgbphjjukpqq9e.streamlit.app/)**

---

## 🧠 What is RetentionIQ?

**RetentionIQ** turns raw e-commerce transaction logs into a full **customer intelligence system** — answering the questions that matter most to a growth or retention team: *who are our best customers, who's about to leave, and what's it worth to keep them?*

Instead of being a one-off churn model or a static chart dump, RetentionIQ combines **behavioral analytics, RFM segmentation, machine learning churn prediction, product affinity analysis, and a revenue-impact simulator** into one cohesive, interactive Streamlit dashboard.

> Built as an end-to-end portfolio project demonstrating the full analytics lifecycle: **raw data → engineered features → segmentation & ML → business storytelling.**

---

## 🎯 Problem It Solves

E-commerce teams usually have transaction data sitting in a database — but no easy way to translate that into decisions. RetentionIQ closes that gap by answering:

| Business Question | Module |
|---|---|
| Who are our most valuable customers? | RFM Segmentation |
| What % of buyers are repeat vs one-time? | Behavior Analysis |
| Which segments drive the most revenue? | Executive Overview |
| Which customers are about to churn? | Churn Prediction |
| What do different customer groups prefer to buy? | Product Analytics |
| What's the ROI of improving retention by 5–10%? | Revenue Retention Simulator |

---

## ✨ Dashboard Modules

### 1️⃣ Executive Overview
High-level KPI snapshot — Total Revenue, Active Customers, AOV, Repeat Purchase Rate, Purchase Frequency, Monthly Revenue Trend, and Revenue Contribution by Segment.

### 2️⃣ Customer Behavior Analysis
A behavior-first view of *how* customers actually buy: purchase frequency distributions, spend distributions, repeat-vs-one-time splits, Monthly Active Customer trends, and category preference breakdowns.

### 3️⃣ Customer Segmentation (RFM)
Classic **Recency, Frequency, Monetary** scoring assigns every customer into business-friendly cohorts:
- 🏆 Champions
- 💎 Loyal Customers
- 🌱 Potential Loyalists
- ⚠️ At Risk
- ❌ Lost Customers

Includes segment scorecards, revenue share by segment, and average R/F/M by segment.

### 4️⃣ Customer 360° Profile
A searchable drill-down into any single customer: total spend, order history, AOV, last purchase date, segment, churn risk, favorite category, and spending trend over time.

### 5️⃣ Churn Prediction
Three classification models trained and compared head-to-head:
- Logistic Regression
- Random Forest
- XGBoost

Outputs churn probability scores, a high-risk customer watchlist, risk distribution charts, and global feature importance to explain *why* customers churn.

### 6️⃣ Product Analytics
Category and product-level performance through a customer-behavior lens — revenue contribution by category, top products, and segment-level category affinity.

### 7️⃣ Revenue Retention Simulator
A what-if tool: adjust assumed churn reduction and instantly see projected retained customers and revenue saved — connecting analytics directly to business decision-making.

---

## 🏗️ Architecture

```text
RetentionIQ/
│
├── src/
│   ├── preprocessing/
│   │   └── pipeline.py            # Cleaning, feature engineering, master dataframe
│   ├── segmentation/
│   │   └── rfm.py                 # RFM scoring + segment assignment logic
│   ├── churn/
│   │   └── models.py              # Model training, evaluation, predictions
│   ├── utils/
│   │   └── data_generator.py      # Synthetic e-commerce dataset generator
│   └── visualization/
│       └── charts.py              # Global Plotly theme, palettes, chart helpers
│
├── dashboard/
│   ├── pages/
│   │   ├── executive_overview.py
│   │   ├── behavior_analysis.py
│   │   ├── segmentation.py
│   │   ├── customer_360.py
│   │   ├── churn_prediction.py
│   │   ├── product_analytics.py
│   │   └── revenue_simulator.py
│   └── components.py
│
├── tests/
│   └── test_pipelines.py
│
├── app.py
├── requirements.txt
└── README.md
```

A **single shared feature pipeline** feeds every page, so all modules — segmentation, churn, behavior analysis — read from one consistent customer dataset instead of recalculating metrics independently.

---

## ⚙️ Feature Engineering

Every customer record is enriched with:

`Total Orders` · `Total Spend` · `AOV` · `Last Purchase Date` · `Recency` · `Frequency` · `Monetary` · `Repeat Customer Flag` · `Avg. Days Between Purchases` · `Favorite Category` · `Segment` · `Churn Probability`

---

## 🧪 Machine Learning

| Component | Approach |
|---|---|
| **Segmentation** | Unsupervised RFM scoring → 5 interpretable business cohorts |
| **Churn Prediction** | Supervised classification — Logistic Regression, Random Forest, XGBoost, compared on performance and feature importance |
| **Churn Features** | Recency, Frequency, Monetary, Total Orders, AOV, repeat-behavior signals |

---

## 📊 Tech Stack

**Core:** Python · Pandas · NumPy

**ML:** Scikit-learn · XGBoost

**Visualization:** Plotly · Streamlit

**Testing:** Python `unittest`

---

## 🎨 Design Highlights

This was built to look and feel like a real analytics product, not a notebook with charts bolted on:

- Dark, premium dashboard theme with a muted pastel segment palette
- Scroll-to-top reset on page navigation
- Built-in metric glossary for non-technical stakeholders
- "About This Dashboard" onboarding section
- Recruiter-friendly **Key Insights** callouts on each page
- Consistent currency/percentage formatting throughout

---

## 🚀 Live Demo

**[👉 Try RetentionIQ here](https://retentioniq-odxzwnbcfgbphjjukpqq9e.streamlit.app/)**

No setup needed — the app ships with a **synthetic e-commerce data generator**, so all modules (segmentation, churn models, simulator) populate automatically on load.

---

## 🛠️ Run It Locally

```bash
# 1. Clone the repo
git clone <your-repo-link>
cd RetentionIQ

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## ✅ Testing

```bash
python -m unittest discover -s tests
```

Validates preprocessing/feature-engineering outputs, master dataframe integrity, and RFM segment assignment logic.

---

## 💼 Why This Project Matters

RetentionIQ demonstrates the full analytics pipeline a real data team would build:

**Raw transactional data → engineered customer features → segmentation & ML → interactive business storytelling.**

It brings together data analysis, feature engineering, customer segmentation, machine learning, and dashboard design — all oriented around answering questions a growth/retention stakeholder would actually ask.

---

## 🔮 Future Enhancements

- [ ] CSV upload for real business datasets
- [ ] Cohort retention analysis
- [ ] Customer Lifetime Value (CLV) prediction
- [ ] Exportable management summary reports (PDF)
- [ ] Multi-user authentication
- [ ] Cloud deployment improvements & caching for scale

---

## 👩‍💻 Author

**Pratyaksha Gupta**
Integrated M.Tech, Computer Science & Engineering — Data Analytics & AI

*Data Analyst | Business Intelligence Enthusiast*

---

<p align="center">⭐ If you found this project useful or interesting, consider starring the repo!</p>
