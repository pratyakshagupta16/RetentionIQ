import streamlit as st
import pandas as pd
import numpy as np
import os


st.set_page_config(
    page_title="RetentionIQ - Customer Behavior Analytics & Segmentation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Main body background styling */
    .stApp {
        background-color: #0B1220;
        color: #F9FAFB;
        font-family: 'Inter', 'Roboto', sans-serif;
    }

    /* Top header styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #F9FAFB;
    }

    /* Global glassmorphic metric cards */
    .card {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        border-color: #93C5FD;
    }

    .card-title {
        font-size: 13px;
        text-transform: uppercase;
        color: #9CA3AF;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    .card-value {
        font-size: 28px;
        font-weight: 800;
        color: #93C5FD;
        margin-top: 8px;
        margin-bottom: 4px;
        text-shadow: 0 0 10px rgba(147, 197, 253, 0.15);
    }

    .card-sub {
        font-size: 12px;
        color: #9CA3AF;
    }

    .trend-pos {
        color: #A7F3D0;
        font-weight: bold;
    }

    .trend-neg {
        color: #FECDD3;
        font-weight: bold;
    }

    /* Section dividers headers */
    .section-header {
        font-size: 18px;
        font-weight: bold;
        color: #93C5FD;
        border-bottom: 2px solid #1F2937;
        padding-bottom: 6px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Style default Streamlit UI components slightly */
    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border-color: #1F2937 !important;
        color: #F9FAFB !important;
    }
    div[data-baseweb="select"] svg {
        color: #93C5FD !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #080C14 !important;
        border-right: 1px solid #1F2937 !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #9CA3AF !important;
    }
</style>
""", unsafe_allow_html=True)


from src.utils.data_generator import ensure_sample_data_exists, generate_synthetic_data
from src.preprocessing.pipeline import clean_and_preprocess_raw, engineer_customer_features


import dashboard.pages.executive_overview as page_executive
import dashboard.pages.behavior_analysis as page_behavior
import dashboard.pages.segmentation as page_segmentation
import dashboard.pages.customer_360 as page_360
import dashboard.pages.churn_prediction as page_churn
import dashboard.pages.product_analytics as page_product
import dashboard.pages.revenue_simulator as page_simulator

def initialize_platform_data():




    for path in ["data/raw", "data/processed", "models"]:
        os.makedirs(path, exist_ok=True)


    filepath = ensure_sample_data_exists()

    if "master_df" not in st.session_state:

        df_raw = pd.read_csv(filepath)
        from src.preprocessing.pipeline import rebuild_master_dataframe

        rebuild_master_dataframe(df_raw)


initialize_platform_data()


st.sidebar.markdown("""
<div style="text-align: center; padding: 15px 0;">
    <h1 style="color: #93C5FD; margin: 0; font-size: 24px; font-family: Inter; letter-spacing: -0.02em;">RetentionIQ</h1>
    <p style="color: #9CA3AF; margin: 5px 0 0 0; font-size: 9px; text-transform: uppercase; letter-spacing: 0.05em;">Customer Behavior & Segmentation</p>
</div>
<hr style="border-top: 1px solid #1F2937; margin: 10px 0 20px 0;" />
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 11px; text-transform: uppercase; font-weight: bold; color: #4B5563; margin-bottom: 5px;'>Navigation Dashboard</p>", unsafe_allow_html=True)

nav_options = [
    "🏠 Executive Overview",
    "📊 Customer Behavior Analysis",
    "👥 Customer Segmentation",
    "🎯 Customer 360°",
    "⚠️ Churn Prediction",
    "📦 Product Analytics",
    "📈 Revenue Simulator"
]

page_choice = st.sidebar.radio(
    label="Select dashboard tab:",
    options=nav_options,
    label_visibility="collapsed"
)

st.sidebar.markdown("<hr style='border-top: 1px solid #1F2937; margin: 30px 0 10px 0;' />", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="font-size: 11px; color: #4B5563; text-align: center;">
    RetentionIQ v1.2.0<br>
    © 2026 Analytics Dashboard Inc.
</div>
""", unsafe_allow_html=True)


if "prev_page" not in st.session_state:
    st.session_state["prev_page"] = page_choice
elif st.session_state["prev_page"] != page_choice:
    st.session_state["prev_page"] = page_choice
    from streamlit.components.v1 import html
    html("""
    <script>
        try {
            var mainContainer = window.parent.document.querySelector(".main");
            if (mainContainer) {
                mainContainer.scrollTop = 0;
            }
        } catch (e) {
            console.error(e);
        }
    </script>
    """, height=0, width=0)

raw_df = st.session_state.get("raw_df", None)
cleaned_df = st.session_state.get("cleaned_df", None)
features_df = st.session_state.get("master_df", None)
churn_results = st.session_state.get("churn_results", None)


if features_df is None or features_df.empty:
    st.error("Error: Centralized RetentionIQ Database ('master_df') could not be initialized.")
else:
    if page_choice == "🏠 Executive Overview":
        page_executive.render(cleaned_df, features_df)

    elif page_choice == "📊 Customer Behavior Analysis":
        page_behavior.render(cleaned_df, features_df)

    elif page_choice == "👥 Customer Segmentation":
        page_segmentation.render(features_df)

    elif page_choice == "🎯 Customer 360°":
        page_360.render(cleaned_df, features_df, churn_results)

    elif page_choice == "⚠️ Churn Prediction":
        page_churn.render(features_df)

    elif page_choice == "📦 Product Analytics":
        page_product.render(cleaned_df, features_df)

    elif page_choice == "📈 Revenue Simulator":
        page_simulator.render(cleaned_df, features_df)
