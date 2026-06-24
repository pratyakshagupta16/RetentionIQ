import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import streamlit as st

REQUIRED_COLUMNS = [
    "Customer ID", "Age", "Gender", "City", "State",
    "Transaction ID", "Purchase Date", "Product Name",
    "Product Category", "Quantity", "Purchase Amount"
]

OPTIONAL_COLUMNS = [
    "Website Visits", "Email Opens", "Customer Satisfaction Score"
]

def validate_dataset_schema(df):




    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return len(missing) == 0, missing

def evaluate_data_quality(df):




    total_rows = len(df)
    if total_rows == 0:
        return {}


    missing_counts = df.isnull().sum().to_dict()
    missing_pct = {k: (v / total_rows) * 100 for k, v in missing_counts.items()}


    duplicate_count = df.duplicated().sum()
    duplicate_pct = (duplicate_count / total_rows) * 100


    outliers = {}
    for col in ["Quantity", "Purchase Amount"]:
        if col in df.columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            outliers[col] = {
                "count": int(outlier_count),
                "pct": float((outlier_count / total_rows) * 100),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound)
            }



    missing_penalty = min(30, sum(missing_pct.values()) / len(df.columns) * 2)
    duplicate_penalty = min(20, duplicate_pct * 2)
    outlier_penalty = min(10, sum([item["pct"] for item in outliers.values()]) * 0.5)

    quality_score = max(0, min(100, 100 - (missing_penalty + duplicate_penalty + outlier_penalty)))


    dtype_dict = df.dtypes.astype(str).to_dict()

    return {
        "total_rows": total_rows,
        "missing_counts": missing_counts,
        "missing_pct": missing_pct,
        "duplicate_count": int(duplicate_count),
        "duplicate_pct": float(duplicate_pct),
        "outliers": outliers,
        "quality_score": round(quality_score, 1),
        "data_types": dtype_dict
    }

@st.cache_data
def clean_and_preprocess_raw(df, handle_missing="fill_median", remove_duplicates=True):



    df_clean = df.copy()


    if remove_duplicates:
        df_clean = df_clean.drop_duplicates()


    if "Purchase Date" in df_clean.columns:
        df_clean["Purchase Date"] = pd.to_datetime(df_clean["Purchase Date"])


    for col in ["Quantity", "Purchase Amount", "Age"]:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")


    for col in OPTIONAL_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")


    for col in df_clean.columns:
        if df_clean[col].isnull().sum() > 0:
            if df_clean[col].dtype in [np.float64, np.int64]:
                if handle_missing == "fill_median":
                    df_clean[col] = df_clean[col].fillna(df_clean[col].median())
                elif handle_missing == "fill_mean":
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
                elif handle_missing == "drop":
                    df_clean = df_clean.dropna(subset=[col])
            else:
                if handle_missing == "drop":
                    df_clean = df_clean.dropna(subset=[col])
                else:
                    df_clean[col] = df_clean[col].fillna("Unknown")

    return df_clean

@st.cache_data
def engineer_customer_features(df_cleaned):





    ref_date = df_cleaned["Purchase Date"].max()


    customer_agg = df_cleaned.groupby("Customer ID").agg({
        "Purchase Date": [
            lambda x: (ref_date - x.max()).days,
            lambda x: (ref_date - x.min()).days,
            "min",
            "max"
        ],
        "Transaction ID": "nunique",
        "Purchase Amount": ["sum", "mean"],
        "Quantity": "sum",
        "Age": "first",
        "Gender": "first",
        "City": "first",
        "State": "first"
    })


    customer_agg.columns = [
        "Recency", "Tenure", "First Purchase Date", "Last Purchase Date",
        "Frequency", "Monetary", "Average Spend", "Total Quantity",
        "Age", "Gender", "City", "State"
    ]
    customer_agg = customer_agg.reset_index()


    bins = [0, 25, 35, 50, 65, 120]
    labels = ["18-25", "26-35", "36-50", "51-65", "66+"]
    customer_agg["Age Group"] = pd.cut(customer_agg["Age"], bins=bins, labels=labels)


    for col in OPTIONAL_COLUMNS:
        if col in df_cleaned.columns:

            cust_val = df_cleaned.groupby("Customer ID")[col].mean().reset_index()
            customer_agg = pd.merge(customer_agg, cust_val, on="Customer ID", how="left")


    category_pivot = df_cleaned.pivot_table(
        index="Customer ID",
        columns="Product Category",
        values="Purchase Amount",
        aggfunc="sum",
        fill_value=0
    ).reset_index()


    for col in category_pivot.columns:
        if col != "Customer ID":
            category_pivot.rename(columns={col: f"Spend Category {col}"}, inplace=True)

    customer_agg = pd.merge(customer_agg, category_pivot, on="Customer ID", how="left")


    cat_qty_pivot = df_cleaned.pivot_table(
        index="Customer ID",
        columns="Product Category",
        values="Quantity",
        aggfunc="sum",
        fill_value=0
    )
    if not cat_qty_pivot.empty:
        customer_agg["Favorite Category"] = cat_qty_pivot.idxmax(axis=1).values
    else:
        customer_agg["Favorite Category"] = "None"



    customer_agg["Churned"] = (customer_agg["Recency"] > 90).astype(int)

    return customer_agg

def get_scaled_features(df_features, feature_cols, scaler_type="standard"):



    data_to_scale = df_features[feature_cols].copy()


    data_to_scale = data_to_scale.fillna(0)

    if scaler_type == "standard":
        scaler = StandardScaler()
    else:
        scaler = MinMaxScaler()

    scaled_data = scaler.fit_transform(data_to_scale)
    return scaled_data, scaler

def rebuild_master_dataframe(raw_df, n_clusters=None):






    cleaned_df = clean_and_preprocess_raw(raw_df)


    features_df = engineer_customer_features(cleaned_df)


    from src.segmentation.rfm import perform_rfm_segmentation
    rfm_df = features_df[["Customer ID", "Recency", "Frequency", "Monetary", "Last Purchase Date"]].copy()
    segmented_df, label_mapping = perform_rfm_segmentation(rfm_df)


    features_df = pd.merge(
        features_df,
        segmented_df[["Customer ID", "Segment"]],
        on="Customer ID",
        how="left"
    )


    from src.churn.models import prepare_churn_dataset, train_and_compare_models
    X, y, feature_names = prepare_churn_dataset(features_df)
    churn_results = train_and_compare_models(features_df, X, y)
    best_churn_model = churn_results["best_model"]


    predictions_df = churn_results["predictions"]


    cols_to_drop = ["Churn_Probability", "Churn_Risk", "Predicted_Churn"]
    features_df = features_df.drop(columns=[c for c in cols_to_drop if c in features_df.columns])

    features_df = pd.merge(
        features_df,
        predictions_df[["Customer ID", "Churn_Probability", "Churn_Risk", "Predicted_Churn"]],
        on="Customer ID",
        how="left"
    )


    features_df["Total_Orders"] = features_df["Frequency"]
    features_df["Average_Order_Value"] = features_df["Average Spend"]
    features_df["Total_Spend"] = features_df["Monetary"]
    features_df["Repeat_Customer_Flag"] = (features_df["Frequency"] > 1).astype(int)
    features_df["Average_Days_Between_Purchases"] = np.where(
        features_df["Frequency"] > 1,
        (features_df["Tenure"] - features_df["Recency"]) / (features_df["Frequency"] - 1),
        0.0
    )


    master_cols = [
        "Customer ID", "Age", "Gender", "Last Purchase Date", "Recency", "Frequency",
        "Monetary", "Segment", "Total_Orders", "Average_Order_Value",
        "Total_Spend", "Repeat_Customer_Flag", "Favorite Category", "Churn_Probability",
        "Predicted_Churn", "Churn_Risk", "Average_Days_Between_Purchases"
    ]
    master_customer_df = features_df[master_cols].copy()


    st.session_state["raw_df"] = raw_df
    st.session_state["cleaned_df"] = cleaned_df
    st.session_state["master_df"] = master_customer_df
    st.session_state["segmentation_results"] = label_mapping
    st.session_state["churn_results"] = churn_results
    st.session_state["churn_model_results"] = churn_results
    st.session_state["churn_model"] = best_churn_model


    unused_keys = ["clv_model_results", "clv_model", "segmentation_model", "predictions_df", "features_df"]
    for k in unused_keys:
        if k in st.session_state:
            del st.session_state[k]

    return master_customer_df
