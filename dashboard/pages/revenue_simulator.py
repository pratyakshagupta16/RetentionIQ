import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.visualization.charts import apply_dark_theme, CARD_COLOR, CYAN, PURPLE

def render(df_cleaned, df_features):
    st.markdown("<h2 style='color: #93C5FD; font-family: Inter, sans-serif;'>📈 Revenue Retention Simulator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Estimate the business and financial impact of retaining at-risk customers and preventing churn.</p>", unsafe_allow_html=True)

    if df_cleaned is None or df_cleaned.empty or df_features is None or df_features.empty:
        st.warning("Please load database data first.")
        return


    with st.expander("📖 Simulator Overview & Assumptions"):
        st.markdown("""
        This simulator estimates the financial impact of successful retention campaigns that prevent at-risk customers from churning.

        **How it works:**
        * **Reduce Churn Rate (%)**: Slider representing the share of predicted churned customers you expect to successfully retain.
        * **Customers Retained**: Calculated as `Predicted Churn Customers * Churn Reduction Pct`.
        * **Revenue Saved**: Calculated as `Retained Customers * Avg Churn Customer Spend`.
        * **Projected Revenue**: Calculated as `Baseline Revenue + Revenue Saved`.
        """)


    current_revenue = df_cleaned["Purchase Amount"].sum()
    total_customers = df_features["Customer ID"].nunique()


    if "Predicted_Churn" in df_features.columns:
        churned_customers = df_features[df_features["Predicted_Churn"] == "Yes"]["Customer ID"].nunique()
        churned_revenue = df_features[df_features["Predicted_Churn"] == "Yes"]["Monetary"].sum()
    else:
        churned_customers = int(total_customers * 0.2)
        churned_revenue = current_revenue * 0.15

    avg_churned_spend = churned_revenue / churned_customers if churned_customers > 0 else 0.0


    st.markdown("<div class='section-header'>What-If Simulation Scenario</div>", unsafe_allow_html=True)

    col_ctrl1, col_ctrl2 = st.columns([1, 1.5])

    with col_ctrl1:
        reduce_churn_pct = st.slider(
            "Reduce Churn Rate by (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=5.0,
            help="Simulate converting predicted churned customers back into active buyers."
        ) / 100.0

        st.markdown(f"""
        <div style="background-color: #111827; padding: 15px; border-radius: 8px; border: 1px solid #1F2937; margin-top: 15px; font-size:13px; color:#9CA3AF;">
            <b style="color: #93C5FD;">📊 Simulation Assumptions:</b><br>
            • Predicted Churn Base: <b>{churned_customers:,}</b> customers<br>
            • Churn Revenue Contribution: <b>${churned_revenue:,.2f}</b><br>
            • Average Churned Customer Spend: <b>${avg_churned_spend:,.2f}</b>
        </div>
        """, unsafe_allow_html=True)


    retained_customers = int(churned_customers * reduce_churn_pct)
    revenue_saved = retained_customers * avg_churned_spend
    projected_revenue = current_revenue + revenue_saved

    revenue_growth_pct = (revenue_saved / current_revenue * 100) if current_revenue > 0 else 0.0

    with col_ctrl2:

        sim_col1, sim_col2 = st.columns(2)

        sim_col1.markdown(f"""
        <div class="card" style="border-top:3px solid {PURPLE}; min-height: 125px;">
            <div class="card-title">Customers Retained</div>
            <div class="card-value" style="color:{PURPLE}; font-size: 26px; margin-top: 5px;">{retained_customers:,}</div>
            <div class="card-sub">Saved customer accounts</div>
        </div>
        """, unsafe_allow_html=True)

        sim_col2.markdown(f"""
        <div class="card" style="border-top:3px solid #10B981; min-height: 125px;">
            <div class="card-title">Revenue Saved / Gained</div>
            <div class="card-value" style="color:#10B981; font-size: 26px; margin-top: 5px;">+${revenue_saved:,.2f}</div>
            <div class="card-sub">Growth rate: <b>+{revenue_growth_pct:.2f}%</b></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card" style="border-top:3px solid {CYAN}; min-height: 110px;">
            <div class="card-title">Total Projected Revenue</div>
            <div class="card-value" style="color:{CYAN}; font-size: 28px; margin-top: 5px;">${projected_revenue:,.2f}</div>
            <div class="card-sub">Baseline spend + simulated saved spend</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("<div class='section-header'>Retained Revenue Forecast</div>", unsafe_allow_html=True)

    fig_sim = go.Figure()

    fig_sim.add_trace(go.Bar(
        x=["Current Status", "Simulated Target"],
        y=[current_revenue, projected_revenue],
        marker_color=[PURPLE, CYAN],
        width=0.4,
        text=[f"${current_revenue:,.2f}", f"${projected_revenue:,.2f}"],
        textposition="auto"
    ))

    fig_sim.update_layout(
        title="Revenue Comparison: Baseline vs Retained Projection",
        yaxis_title="Revenue ($)",
        showlegend=False
    )
    apply_dark_theme(fig_sim)
    st.plotly_chart(fig_sim, use_container_width=True)
