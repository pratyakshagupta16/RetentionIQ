import unittest
import pandas as pd
import numpy as np
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.data_generator import generate_synthetic_data
from src.preprocessing.pipeline import clean_and_preprocess_raw, engineer_customer_features, validate_dataset_schema, rebuild_master_dataframe
from src.segmentation.rfm import perform_rfm_segmentation
from src.churn.models import prepare_churn_dataset, train_and_compare_models

class TestAnalyticsPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.df_raw = generate_synthetic_data(num_customers=50, num_transactions=200, random_seed=42)

    def test_schema_validation(self):
        is_valid, missing = validate_dataset_schema(self.df_raw)
        self.assertTrue(is_valid, f"Schema invalid. Missing: {missing}")

    def test_preprocessing(self):
        df_clean = clean_and_preprocess_raw(self.df_raw)
        self.assertFalse(df_clean.empty)
        self.assertEqual(df_clean.isnull().sum().sum(), 0, "Cleaned dataset should not contain NaNs")

        df_features = engineer_customer_features(df_clean)
        self.assertFalse(df_features.empty)
        self.assertIn("Recency", df_features.columns)
        self.assertIn("Frequency", df_features.columns)
        self.assertIn("Monetary", df_features.columns)
        self.assertIn("Churned", df_features.columns)

    def test_segmentation(self):
        df_clean = clean_and_preprocess_raw(self.df_raw)
        df_features = engineer_customer_features(df_clean)

        rfm_df = df_features[["Customer ID", "Recency", "Frequency", "Monetary", "Last Purchase Date"]].copy()
        df_segmented, label_mapping = perform_rfm_segmentation(rfm_df)

        self.assertIn("Segment", df_segmented.columns)
        self.assertTrue(df_segmented["Segment"].isin(["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Lost Customers"]).all())

    def test_churn_prediction(self):
        df_clean = clean_and_preprocess_raw(self.df_raw)
        df_features = engineer_customer_features(df_clean)


        rfm_df = df_features[["Customer ID", "Recency", "Frequency", "Monetary", "Last Purchase Date"]].copy()
        df_segmented, _ = perform_rfm_segmentation(rfm_df)
        df_features_updated = pd.merge(df_features, df_segmented[["Customer ID", "Segment"]], on="Customer ID")

        X, y, feature_names = prepare_churn_dataset(df_features_updated)
        self.assertFalse("Recency" in X.columns, "Leakage protection: Recency should be excluded from Churn classification features")
        self.assertFalse("Last Purchase Date" in X.columns)

        results = train_and_compare_models(df_features_updated, X, y)
        self.assertIn(results["best_model_name"], ["Logistic Regression", "Random Forest", "XGBoost"])
        self.assertIsNotNone(results["best_model"])


        required_keys = ["best_model", "accuracy", "predictions", "feature_importance", "classification_report", "confusion_matrix"]
        for key in required_keys:
            self.assertIn(key, results, f"Standardized churn result is missing key: {key}")


        predictions_df = results["predictions"]
        required_pred_cols = ["Customer ID", "Churn_Probability", "Predicted_Churn", "Churn_Risk"]
        for col in required_pred_cols:
            self.assertIn(col, predictions_df.columns, f"Predictions dataframe is missing column: {col}")

    def test_rebuild_master_dataframe(self):

        import streamlit as st
        if "raw_df" not in st.session_state:
            st.session_state["raw_df"] = self.df_raw

        master_df = rebuild_master_dataframe(self.df_raw)
        self.assertFalse(master_df.empty)


        required_master_cols = [
            "Customer ID", "Age", "Gender", "Last Purchase Date", "Recency", "Frequency",
            "Monetary", "Segment", "Total_Orders", "Average_Order_Value",
            "Total_Spend", "Repeat_Customer_Flag", "Favorite Category", "Churn_Probability",
            "Predicted_Churn", "Churn_Risk", "Average_Days_Between_Purchases"
        ]
        for col in required_master_cols:
            self.assertIn(col, master_df.columns, f"Unified master database is missing column: {col}")

if __name__ == "__main__":
    unittest.main()
