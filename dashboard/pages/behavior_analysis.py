import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.visualization.charts import (
    apply_dark_theme, create_line_chart, create_bar_chart,
    create_donut_chart, create_box_plot, CYAN, PURPLE, MAGENTA, COLOR_PALETTE
)

def render(df_cleaned, df_features):
    st.markdown("<h2 style='color: #93C5FD; font-family: Inter, sans-serif;'>📊 Customer Behavior Analysis</h2>", unsafe_allow_html=True)

    if df_cleaned is None or df_cleaned.empty or df_features is None or df_features.empty:
        st.warning("Please load database data first.")
        return


    with st.expander("📖 Metric Glossary & Definitions"):
        st.markdown("""
        * **Repeat Purchase Rate**: The percentage of customers who have made more than 1 transaction. Calculated as: `(Repeat Customers / Total Customers) * 100`.
        * **Average Purchase Frequency**: The average number of unique orders placed per customer.
        * **Average Customer Spend**: The average monetary amount spent by a customer across all their lifetime transactions.
        * **Average Days Between Purchases**: The average interval in days between consecutive orders for repeat buyers. Calculated as: `(Tenure - Recency) / (Total Orders - 1)`.
        """)


    avg_frequency = df_features["Frequency"].mean() if "Frequency" in df_features.columns else 0.0
    avg_spend = df_features["Monetary"].mean() if "Monetary" in df_features.columns else 0.0
    repeat_rate = (df_features["Repeat_Customer_Flag"] == 1).mean() * 100 if "Repeat_Customer_Flag" in df_features.columns else 0.0
    avg_recency = df_features["Recency"].mean() if "Recency" in df_features.columns else 0.0


    st.markdown("<div class='section-header'>Behavioral KPIs Overview</div>", unsafe_allow_html=True)
    kcol1, kcol2, kcol3, kcol4, kcol5 = st.columns(5)

    def render_metric(col, title, value, sub_text, color, is_currency=False, is_percent=False):
        if is_currency:
            val_str = f"${value:,.2f}"
        elif is_percent:
            val_str = f"{value:.1f}%"
        elif isinstance(value, float):
            val_str = f"{value:.1f}"
        else:
            val_str = f"{value:,}"

        col.markdown(f"""
        <div class="card" style="border-top: 3px solid {color}; min-height: 120px;">
            <div class="card-title">{title}</div>
            <div class="card-value" style="color: {color}; font-size: 24px; margin-top: 5px;">{val_str}</div>
            <div class="card-sub">{sub_text}</div>
        </div>
        """, unsafe_allow_html=True)

    render_metric(kcol1, "Avg Orders / Customer", avg_frequency, "Average purchase frequency", CYAN)
    render_metric(kcol2, "Avg Spend / Customer", avg_spend, "Average monetary spend", PURPLE, is_currency=True)
    render_metric(kcol3, "Repeat Purchase Rate", repeat_rate, "Share of repeat buyers", "#A7F3D0", is_percent=True)
    render_metric(kcol4, "Avg Recency", avg_recency, "Avg days since last order", MAGENTA)
    render_metric(kcol5, "Total Transactions", len(df_cleaned), "Gross logs analyzed", "#93C5FD")

    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("<div class='section-header'>Purchase Patterns & Spending Distributions</div>", unsafe_allow_html=True)
    col_dist1, col_dist2 = st.columns(2)

    with col_dist1:

        freq_bins = [0, 1, 5, 10, np.inf]
        freq_labels = ["1 time", "2–5 times", "6–10 times", "10+ times"]
        df_features["FreqGroup"] = pd.cut(df_features["Frequency"], bins=freq_bins, labels=freq_labels)

        freq_dist = df_features["FreqGroup"].value_counts().reindex(freq_labels).reset_index()
        freq_dist.columns = ["Order Count Group", "Customers"]

        fig_freq = create_bar_chart(
            freq_dist, x="Order Count Group", y="Customers",
            title="Purchase Frequency Distribution",
            x_label="Number of Purchases", y_label="Customer Count",
            color_hex=CYAN
        )
        st.plotly_chart(fig_freq, use_container_width=True)

    with col_dist2:

        fig_spend = create_box_plot(
            df_features, x=None, y="Monetary",
            title="Customer Monetary Spending Distribution (Outlier Analysis)"
        )
        fig_spend.update_layout(yaxis_title="Total Customer Spend ($)")
        st.plotly_chart(fig_spend, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)


    col_rep1, col_rep2 = st.columns(2)

    with col_rep1:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-bottom: 15px;'>Repeat vs One-Time Customers</h4>", unsafe_allow_html=True)

        rep_counts = df_features["Repeat_Customer_Flag"].value_counts().reset_index()
        rep_counts.columns = ["Status", "Count"]
        rep_counts["Status"] = rep_counts["Status"].map({1: "Repeat Customer", 0: "One-Time Buyer"})

        rep_rev = df_features.groupby("Repeat_Customer_Flag")["Monetary"].sum().reset_index()
        rep_rev.columns = ["Status", "Spend"]
        rep_rev["Status"] = rep_rev["Status"].map({1: "Repeat Customer Spend", 0: "One-Time Buyer Spend"})

        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            fig_rep_count = create_donut_chart(rep_counts, names="Status", values="Count", title="Buyer Type Count Share")
            fig_rep_count.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=230)
            st.plotly_chart(fig_rep_count, use_container_width=True)

        with sub_col2:
            fig_rep_rev = create_donut_chart(rep_rev, names="Status", values="Spend", title="Revenue Contribution Share")
            fig_rep_rev.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=230)
            st.plotly_chart(fig_rep_rev, use_container_width=True)

    with col_rep2:

        if "Purchase Date" in df_cleaned.columns:
            df_cleaned["Purchase Date"] = pd.to_datetime(df_cleaned["Purchase Date"])
            df_cleaned["YearMonth"] = df_cleaned["Purchase Date"].dt.to_period("M").astype(str)
            mac_df = df_cleaned.groupby("YearMonth")["Customer ID"].nunique().reset_index()
            mac_df.columns = ["Month", "Active Customers"]

            if not mac_df.empty:
                fig_mac = create_line_chart(
                    mac_df, x="Month", y="Active Customers",
                    title="Monthly Active Customers (MAC) Trend",
                    x_label="Month", y_label="Unique Active Buyers",
                    color_hex=MAGENTA
                )
                fig_mac.update_layout(height=280)
                st.plotly_chart(fig_mac, use_container_width=True)
            else:
                st.warning("No monthly transaction history available.")
        else:
            st.warning("Missing 'Purchase Date' column for MAC trend.")

    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("<div class='section-header'>Category Preference & Behavioral Summary</div>", unsafe_allow_html=True)
    col_cat1, col_cat2 = st.columns([1.2, 1])

    with col_cat1:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-top:0;'>Category Preference Breakdown</h4>", unsafe_allow_html=True)
        tab_cust, tab_freq, tab_rev = st.tabs(["Customer Counts", "Purchase Volume", "Revenue contribution"])


        cat_stats = df_cleaned.groupby("Product Category").agg({
            "Customer ID": "nunique",
            "Transaction ID": "count",
            "Purchase Amount": "sum"
        }).rename(columns={
            "Customer ID": "Unique Customers",
            "Transaction ID": "Purchase Count",
            "Purchase Amount": "Total Revenue"
        }).reset_index()

        with tab_cust:
            fig_cc = create_bar_chart(
                cat_stats.sort_values(by="Unique Customers", ascending=True),
                x="Unique Customers", y="Product Category",
                title="Unique Customers per Product Category",
                x_label="Customer Count", y_label="Category", color_hex=PURPLE,
                horizontal=True
            )
            fig_cc.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10))
            st.plotly_chart(fig_cc, use_container_width=True)

        with tab_freq:
            fig_pc = create_bar_chart(
                cat_stats.sort_values(by="Purchase Count", ascending=True),
                x="Purchase Count", y="Product Category",
                title="Transaction Count per Product Category",
                x_label="Orders Count", y_label="Category", color_hex=CYAN,
                horizontal=True
            )
            fig_pc.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10))
            st.plotly_chart(fig_pc, use_container_width=True)

        with tab_rev:
            fig_rc = create_bar_chart(
                cat_stats.sort_values(by="Total Revenue", ascending=True),
                x="Total Revenue", y="Product Category",
                title="Total Gross Revenue per Product Category",
                x_label="Revenue ($)", y_label="Category", color_hex=MAGENTA,
                horizontal=True
            )
            fig_rc.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10))
            st.plotly_chart(fig_rc, use_container_width=True)

    with col_cat2:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-top:0;'>Cohort Behavioral Summary Matrix</h4>", unsafe_allow_html=True)


        total_cust_val = len(df_features)
        one_time_val = int((df_features["Repeat_Customer_Flag"] == 0).sum())
        repeat_val = int((df_features["Repeat_Customer_Flag"] == 1).sum())

        summary_data = {
            "Behavioral Metric": [
                "Average Orders per Customer",
                "Average Spend per Customer",
                "Repeat Customers Count",
                "Repeat Customer Share (%)",
                "One-Time Customers Count",
                "One-Time Customer Share (%)",
                "Average Days Since Last Purchase (Recency)"
            ],
            "Value": [
                f"{avg_frequency:.1f} orders",
                f"${avg_spend:,.2f}",
                f"{repeat_val:,} buyers",
                f"{repeat_rate:.1f}%",
                f"{one_time_val:,} buyers",
                f"{100.0 - repeat_rate:.1f}%",
                f"{avg_recency:.1f} days"
            ]
        }
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True, height=280)
