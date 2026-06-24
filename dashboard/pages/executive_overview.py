import streamlit as st
import pandas as pd
import numpy as np
from src.visualization.charts import (
    create_line_chart, create_bar_chart, create_donut_chart,
    CYAN, PURPLE, MAGENTA, SEGMENT_COLORS
)

def render(df_cleaned, df_features):
    st.markdown("<h2 style='color: #93C5FD; font-family: Inter, sans-serif;'>🏠 Executive Overview</h2>", unsafe_allow_html=True)


    if df_cleaned is None or df_cleaned.empty or df_features is None or df_features.empty:
        st.warning("No customer data available to render the Executive Overview. Please load or upload data first.")
        return


    st.markdown("""
    <div style="background-color: #111827; padding: 15px; border-radius: 8px; border: 1px solid #1F2937; margin-bottom: 20px;">
        <h4 style="color: #93C5FD; margin-top: 0; font-family: Inter, sans-serif; font-size: 15px;">ℹ️ About RetentionIQ</h4>
        <p style="color: #9CA3AF; font-size: 13px; line-height: 1.5; margin-bottom: 0;">
            <b>RetentionIQ</b> is an interactive customer behavior analytics and segmentation platform designed for e-commerce businesses. It analyzes transaction logs to study customer purchase behavior, segment customers using RFM analysis, identify customers at risk of churn, track product preferences, and estimate the financial impact of successful retention strategies. Use the navigation sidebar to explore different analytical views.
        </p>
    </div>
    """, unsafe_allow_html=True)


    total_revenue = df_cleaned["Purchase Amount"].sum() if "Purchase Amount" in df_cleaned.columns else 0.0
    total_customers = df_features["Customer ID"].nunique() if "Customer ID" in df_features.columns else 0


    if "Predicted_Churn" in df_features.columns:
        active_customers = df_features[df_features["Predicted_Churn"] == "No"]["Customer ID"].nunique()
        inactive_customers = df_features[df_features["Predicted_Churn"] == "Yes"]["Customer ID"].nunique()
    else:
        active_customers = total_customers
        inactive_customers = 0


    if "Transaction ID" in df_cleaned.columns and "Purchase Amount" in df_cleaned.columns:
        aov = df_cleaned.groupby("Transaction ID")["Purchase Amount"].sum().mean()
    else:
        aov = 0.0


    repeat_rate = (df_features["Repeat_Customer_Flag"] == 1).mean() * 100 if "Repeat_Customer_Flag" in df_features.columns else 0.0
    avg_freq = df_features["Frequency"].mean() if "Frequency" in df_features.columns else 0.0
    avg_spend = df_features["Monetary"].mean() if "Monetary" in df_features.columns else 0.0

    if "Average_Days_Between_Purchases" in df_features.columns and "Repeat_Customer_Flag" in df_features.columns:
        repeat_customers_df = df_features[df_features["Repeat_Customer_Flag"] == 1]
        avg_days_between = repeat_customers_df["Average_Days_Between_Purchases"].mean() if not repeat_customers_df.empty else 0.0
    else:
        avg_days_between = 0.0


    def render_kpi_card(col, title, value, sub_text, color_hex=CYAN, is_currency=False, is_percent=False, force_million=False):
        if is_currency:
            if force_million and value >= 1000000:
                val_str = f"${value/1000000:.2f}M"
            else:
                val_str = f"${value:,.2f}"
        elif is_percent:
            val_str = f"{value:.1f}%"
        elif isinstance(value, float):
            val_str = f"{value:.1f}"
        else:
            val_str = f"{value:,}"

        col.markdown(f"""
        <div class="card" style="border-top: 3px solid {color_hex}; min-height: 120px;">
            <div class="card-title">{title}</div>
            <div class="card-value" style="color: {color_hex}; font-size: 24px; margin-top: 5px;">{val_str}</div>
            <div class="card-sub">{sub_text}</div>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("<div class='section-header'>Key Performance Indicators</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    render_kpi_card(col1, "Total Revenue", total_revenue, "Historical Gross Sales", CYAN, is_currency=True, force_million=True)
    render_kpi_card(col2, "Total Customers", total_customers, "Unique Buyers Database", PURPLE)
    render_kpi_card(col3, "Active Customers", active_customers, "Predicted Non-Churners", "#A7F3D0")
    render_kpi_card(col4, "Avg Order Value", aov, "Average ticket size", MAGENTA, is_currency=True)

    col5, col6, col7, col8 = st.columns(4)
    render_kpi_card(col5, "Repeat Purchase Rate", repeat_rate, "Share of repeat buyers", "#93C5FD", is_percent=True)
    render_kpi_card(col6, "Avg Purchase Frequency", avg_freq, "Avg orders per customer", "#FED7AA")
    render_kpi_card(col7, "Avg Customer Spend", avg_spend, "Avg customer lifetime spend", "#A7F3D0", is_currency=True)
    render_kpi_card(col8, "Avg Days Between Purchases", avg_days_between, "Days between orders", "#FECDD3")

    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("<div class='section-header'>Sales Trend & Behavioral Splits</div>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)


    if "Purchase Date" in df_cleaned.columns and "Purchase Amount" in df_cleaned.columns:
        df_cleaned["Purchase Date"] = pd.to_datetime(df_cleaned["Purchase Date"])
        df_cleaned["YearMonth"] = df_cleaned["Purchase Date"].dt.to_period("M").astype(str)
        monthly_sales = df_cleaned.groupby("YearMonth")["Purchase Amount"].sum().reset_index()

        if not monthly_sales.empty:
            fig_sales = create_line_chart(
                monthly_sales,
                x="YearMonth",
                y="Purchase Amount",
                title="Monthly Revenue Trend",
                x_label="Month",
                y_label="Revenue ($)",
                color_hex=CYAN
            )
            chart_col1.plotly_chart(fig_sales, use_container_width=True)
        else:
            chart_col1.warning("No sales transactions available to plot Monthly Revenue Trend.")
    else:
        chart_col1.warning("Missing required columns for MoM Revenue Trend.")


    if "Repeat_Customer_Flag" in df_features.columns:
        repeat_counts = df_features["Repeat_Customer_Flag"].value_counts().reset_index()
        repeat_counts.columns = ["Customer Type", "Count"]
        repeat_counts["Customer Type"] = repeat_counts["Customer Type"].map({1: "Repeat Customer", 0: "One-Time Buyer"})

        fig_repeat = create_donut_chart(
            repeat_counts,
            names="Customer Type",
            values="Count",
            title="Repeat vs One-Time Buyers Count"
        )
        chart_col2.plotly_chart(fig_repeat, use_container_width=True)
    else:
        chart_col2.warning("Missing Repeat Customer Flag for comparison chart.")

    st.markdown("<br>", unsafe_allow_html=True)

    chart_col3, chart_col4 = st.columns(2)


    if "Segment" in df_features.columns and "Monetary" in df_features.columns:
        seg_rev = df_features.groupby("Segment")["Monetary"].sum().reset_index()
        if not seg_rev.empty:
            fig_seg_rev = create_donut_chart(
                seg_rev,
                names="Segment",
                values="Monetary",
                title="Revenue by Customer Segment",
                color_map=SEGMENT_COLORS
            )
            chart_col3.plotly_chart(fig_seg_rev, use_container_width=True)
        else:
            chart_col3.warning("No segments available to plot revenue contribution.")
    else:
        chart_col3.info("Segment metadata missing.")


    if "Product Category" in df_cleaned.columns and "Purchase Amount" in df_cleaned.columns:
        cat_rev = df_cleaned.groupby("Product Category")["Purchase Amount"].sum().reset_index().sort_values(by="Purchase Amount", ascending=False).head(5)
        if not cat_rev.empty:
            fig_cat = create_bar_chart(
                cat_rev,
                x="Purchase Amount",
                y="Product Category",
                title="Top 5 Product Categories by Revenue",
                x_label="Revenue ($)",
                y_label="Category",
                color_hex=MAGENTA,
                horizontal=True
            )
            fig_cat.update_layout(yaxis=dict(autorange="reversed"))
            chart_col4.plotly_chart(fig_cat, use_container_width=True)
        else:
            chart_col4.warning("No category transaction records available.")
    else:
        chart_col4.warning("Missing columns for Category Revenue Chart.")


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Key Behavioral Insights</div>", unsafe_allow_html=True)


    repeat_rev_pct = 0.0
    champs_count_pct = 0.0
    champs_rev_pct = 0.0
    high_risk_pct = 0.0
    top_cat_name = "N/A"

    if total_revenue > 0:
        rep_spend = df_features[df_features["Repeat_Customer_Flag"] == 1]["Monetary"].sum()
        repeat_rev_pct = (rep_spend / total_revenue) * 100

        champs_df = df_features[df_features["Segment"] == "Champions"]
        champs_count_pct = (len(champs_df) / total_customers) * 100 if total_customers > 0 else 0.0
        champs_rev_pct = (champs_df["Monetary"].sum() / total_revenue) * 100

    if total_customers > 0 and "Churn_Risk" in df_features.columns:
        high_risk_count = len(df_features[df_features["Churn_Risk"] == "High Risk"])
        high_risk_pct = (high_risk_count / total_customers) * 100

    if "Product Category" in df_cleaned.columns and "Purchase Amount" in df_cleaned.columns:
        cat_agg = df_cleaned.groupby("Product Category")["Purchase Amount"].sum()
        if not cat_agg.empty:
            top_cat_name = cat_agg.idxmax()

    st.markdown(f"""
    <div style="background-color: #111827; padding: 20px; border-radius: 10px; border: 1px solid #1F2937;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px;">
            <div>
                <b style="color: #93C5FD; font-size: 14px;">🔄 Repeat Buyer Contribution:</b>
                <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                    Repeat shoppers represent <b>{repeat_rate:.1f}%</b> of the buyer base but drive <b>{repeat_rev_pct:.1f}%</b> of gross sales, emphasizing the value of loyalty.
                </p>
            </div>
            <div>
                <b style="color: #A7F3D0; font-size: 14px;">🏆 Champions Leverage:</b>
                <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                    Champions account for just <b>{champs_count_pct:.1f}%</b> of all customers, but contribute <b>{champs_rev_pct:.1f}%</b> of total revenue.
                </p>
            </div>
            <div>
                <b style="color: #DDD6FE; font-size: 14px;">📦 Top Revenue Category:</b>
                <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                    <b>{top_cat_name}</b> is the leading product category, representing the highest spend contribution across historical sales logs.
                </p>
            </div>
            <div>
                <b style="color: #FECDD3; font-size: 14px;">⚠️ High Churn Risk Base:</b>
                <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                    Approximately <b>{high_risk_pct:.1f}%</b> of the customer database is classified as High Risk of churn, representing potential revenue leakage.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
