# RetentionIQ — Customer Behavior Analytics & Segmentation Dashboard

An interactive, business-focused customer behavior analytics and segment intelligence platform built with **Streamlit**, **Scikit-learn**, **XGBoost**, and **Plotly**.

**RetentionIQ** transforms raw e-commerce transaction logs into actionable customer profiles, RFM segments, predictive churn risk evaluations, product categories affinity graphs, and financial retention what-if simulation models.

---

## 🚀 Key Modules & Capabilities

1. **🏠 Executive Overview**: Dynamic KPI cards displaying Total Revenue, Unique Customer Count, Active Customer projections, Repeat Purchase rates, and average ticket sizes alongside monthly sales trends.
2. **📊 Customer Behavior Analysis**: Analyzes purchase frequency distribution bins, lifetime customer monetary spend outliers, repeat vs. one-time buyer shares, and Monthly Active Customer (MAC) trends.
3. **👥 Customer Segmentation**: Performs RFM (Recency, Frequency, Monetary) analytics, grouping the database into Champions, Loyal Customers, Potential Loyalists, At Risk, and Lost segments. Renders share metrics and actionable segment cohort scorecards.
4. **🎯 Customer 360° Profile**: Select or search customers by ID to inspect transactional ledger history, individual customer spending trends over time, and segment status indicators.
5. **⚠️ Churn Prediction**: Supporting predictive customer risk analytics comparing classifier models (Logistic Regression, Random Forest, XGBoost) alongside global feature importance drivers.
6. **📦 Product Analytics**: Details category revenue contribution treemaps, volume-sold logs, and cross-cohort product category affinity layouts.
7. **📈 Revenue Retention Simulator**: Simulates retention scenarios to forecast customer win-back gains, revenue saved, and financial growth percentages.

---

## 📂 Project Architecture

```text
RetentionIQ/
│
├── src/                      # Core backend pipeline modules
│   ├── preprocessing/
│   │   └── pipeline.py       # Data cleaning and feature engineering pipeline
│   ├── segmentation/
│   │   └── rfm.py            # RFM analysis logic
│   ├── churn/
│   │   └── models.py         # ML model definitions and training logic
│   ├── utils/
│   │   └── data_generator.py # Synthetic data creator with correlations
│   └── visualization/
│       └── charts.py         # Global Plotly styling wrappers and palettes
│
├── dashboard/
│   ├── pages/                # Page controllers for dashboard tabs
│   │   ├── executive_overview.py
│   │   ├── behavior_analysis.py
│   │   ├── segmentation.py
│   │   ├── customer_360.py
│   │   ├── churn_prediction.py
│   │   ├── product_analytics.py
│   │   └── revenue_simulator.py
│   └── components.py
│
├── tests/                    # Pipeline validation suites
│   └── test_pipelines.py
│
├── app.py                    # Main controller and style entrypoint
├── requirements.txt          # Library dependencies list
└── README.md
```

---

## 🛠 Setup & Run Instructions

### 1. Prerequisites
Ensure you have Python 3.9 - 3.12 installed on your machine.

### 2. Environment Setup
Install the project dependencies:
```bash
# Install packages
pip install -r requirements.txt
```

### 3. Run the Dashboard
Run the Streamlit application:
```bash
streamlit run app.py
```
The application will launch in your default browser at `http://localhost:8501`.

*Note: On startup, the dashboard automatically generates a synthetic demo dataset with e-commerce transactions and fits all machine learning models so it is fully populated and viewable immediately.*
