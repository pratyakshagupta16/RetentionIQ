import streamlit as st
import pandas as pd
import numpy as np
from src.visualization.charts import (
    create_bar_chart, create_donut_chart,
    CYAN, PURPLE, MAGENTA, COLOR_PALETTE, SEGMENT_COLORS
)

def render(df_features):
    st.markdown("<h2 style='color: #93C5FD; font-family: Inter, sans-serif;'>👥 Customer Segmentation</h2>", unsafe_allow_html=True)

    if df_features is None or df_features.empty:
        st.warning("Please load database data first.")
        return

    df_features_updated = df_features.copy()


    with st.expander("📖 Segmentation & RFM Glossary"):
        st.markdown("""
        * **Recency (R)**: Days since the customer's last purchase. Lower recency indicates more active shoppers.
        * **Frequency (F)**: Total number of orders placed. Higher frequency indicates stronger brand loyalty.
        * **Monetary (M)**: Total monetary spend. Identifies high-value customers.

        **Segment Descriptions:**
        * 🟢 **Champions**: Bought recently, buy frequently, and spend the most. Reward them with VIP events, early access, and loyalty perks.
        * 🔵 **Loyal Customers**: Purchase regularly with good spend. Focus on upselling and cross-selling related product categories.
        * 🟡 **Potential Loyalists**: Recent buyers who spent average amounts. Nurture with targeted email campaigns.
        * 🟠 **At Risk**: High-spending, frequent buyers in the past, but haven't purchased in a while. Send win-back offers.
        * 🔴 **Lost Customers**: Lowest scores across Recency, Frequency, and Monetary. Reactivate via low-cost email campaigns.
        """)


    st.markdown("<div class='section-header'>Segment Distributions & Business Impact</div>", unsafe_allow_html=True)

    col_vis1, col_vis2 = st.columns(2)

    with col_vis1:

        seg_dist = df_features_updated["Segment"].value_counts().reset_index()
        seg_dist.columns = ["Segment", "Customers"]
        fig_dist = create_donut_chart(seg_dist, names="Segment", values="Customers", title="Customer Share by Segment", color_map=SEGMENT_COLORS)
        st.plotly_chart(fig_dist, use_container_width=True)

    with col_vis2:

        seg_rev = df_features_updated.groupby("Segment")["Monetary"].sum().reset_index().sort_values(by="Monetary", ascending=False)
        fig_rev = create_bar_chart(
            seg_rev, x="Segment", y="Monetary",
            title="Revenue Contribution by Customer Segment",
            x_label="Segment", y_label="Total Revenue ($)",
            color_map=SEGMENT_COLORS
        )
        st.plotly_chart(fig_rev, use_container_width=True)


    st.markdown("<br><div class='section-header'>Behavioral Metric Averages by Segment</div>", unsafe_allow_html=True)

    seg_averages = df_features_updated.groupby("Segment").agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean"
    }).reset_index()


    segment_order = ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Lost Customers"]
    seg_averages["order"] = seg_averages["Segment"].apply(lambda x: segment_order.index(x) if x in segment_order else 99)
    seg_averages = seg_averages.sort_values("order").drop(columns=["order"])

    c_r, c_f, c_m = st.columns(3)

    with c_r:
        fig_r = create_bar_chart(
            seg_averages, x="Segment", y="Recency",
            title="Average Recency by Segment (Lower is Better)",
            x_label="", y_label="Average Recency (Days)", color_map=SEGMENT_COLORS
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with c_f:
        fig_f = create_bar_chart(
            seg_averages, x="Segment", y="Frequency",
            title="Average Frequency by Segment (Higher is Better)",
            x_label="", y_label="Average Frequency (Orders)", color_map=SEGMENT_COLORS
        )
        st.plotly_chart(fig_f, use_container_width=True)

    with c_m:
        fig_m = create_bar_chart(
            seg_averages, x="Segment", y="Monetary",
            title="Average Spend (Monetary) by Segment",
            x_label="", y_label="Average Spend ($)", color_map=SEGMENT_COLORS
        )
        st.plotly_chart(fig_m, use_container_width=True)


    st.markdown("<br><div class='section-header'>Segment Profiles & Analytics Matrix</div>", unsafe_allow_html=True)

    col_prof1, col_prof2 = st.columns([1.5, 1])

    with col_prof1:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-bottom: 10px;'>RFM Behavioral Scorecard</h4>", unsafe_allow_html=True)


        total_rev_all = df_features_updated["Monetary"].sum()

        cohort_table = df_features_updated.groupby("Segment").agg({
            "Customer ID": "count",
            "Recency": "mean",
            "Frequency": "mean",
            "Monetary": ["mean", "sum"]
        })


        cohort_table.columns = ["Customer Count", "Avg Recency", "Avg Frequency", "Avg Monetary", "Total Spend"]
        cohort_table = cohort_table.reset_index()


        cohort_table["Revenue Contribution"] = cohort_table["Total Spend"].map(lambda x: f"${x:,.2f}")
        cohort_table["Revenue Share (%)"] = ((cohort_table["Total Spend"] / total_rev_all) * 100).round(1).astype(str) + "%"


        cohort_table["Avg Recency"] = cohort_table["Avg Recency"].round(1)
        cohort_table["Avg Frequency"] = cohort_table["Avg Frequency"].round(1)
        cohort_table["Avg Monetary"] = cohort_table["Avg Monetary"].round(2)


        cohort_table["order"] = cohort_table["Segment"].apply(lambda x: segment_order.index(x) if x in segment_order else 99)
        cohort_table = cohort_table.sort_values("order").drop(columns=["order", "Total Spend"])

        st.dataframe(cohort_table, use_container_width=True, hide_index=True)

    with col_prof2:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-bottom: 10px;'>Cohort Definitions & Actions</h4>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 13px; color: #9CA3AF; line-height: 1.6;">
            • <b style="color: #A7F3D0;">Champions:</b> VIP loyalty perks, early product releases, and exclusive referral programs.<br>
            • <b style="color: #93C5FD;">Loyal Customers:</b> Multi-category cross-selling and automated lifecycle updates.<br>
            • <b style="color: #DDD6FE;">Potential Loyalists:</b> Welcome discount bundles and onboarding email nurture flows.<br>
            • <b style="color: #FED7AA;">At Risk:</b> Time-sensitive high-value win-back vouchers and customer surveys.<br>
            • <b style="color: #FECDD3;">Lost Customers:</b> Low-cost quarterly reactivation mailers and feedback collection.
        </div>
        """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Key Segmentation Insights</div>", unsafe_allow_html=True)

    loyal_spend_pct = 0.0
    champs_rec = 0.0
    lost_rec = 0.0
    risk_freq = 0.0
    champs_freq = 0.0

    if total_rev_all > 0:
        loyal_spend = df_features_updated[df_features_updated["Segment"] == "Loyal Customers"]["Monetary"].sum()
        loyal_spend_pct = (loyal_spend / total_rev_all) * 100

    champs_sub = df_features_updated[df_features_updated["Segment"] == "Champions"]
    lost_sub = df_features_updated[df_features_updated["Segment"] == "Lost Customers"]
    risk_sub = df_features_updated[df_features_updated["Segment"] == "At Risk"]

    champs_rec = champs_sub["Recency"].mean() if not champs_sub.empty else 0.0
    lost_rec = lost_sub["Recency"].mean() if not lost_sub.empty else 0.0
    risk_freq = risk_sub["Frequency"].mean() if not risk_sub.empty else 0.0
    champs_freq = champs_sub["Frequency"].mean() if not champs_sub.empty else 0.0

    st.markdown(f"""
    <div style="background-color: #111827; padding: 20px; border-radius: 10px; border: 1px solid #1F2937;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px;">
            <div>
                <b style="color: #93C5FD; font-size: 14px;">🔵 Loyal Buyers Revenue Contribution:</b>
                <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                    Loyal Customers drive <b>{loyal_spend_pct:.1f}%</b> of total revenue, representing a primary revenue-generating core.
                </p>
            </div>
            <div>
                <b style="color: #A7F3D0; font-size: 14px;">⏱️ Champions Recency Advantage:</b>
                <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                    Champions have an average recency of <b>{champs_rec:.1f} days</b> compared to <b>{lost_rec:.1f} days</b> for Lost Customers, indicating a major activity gap.
                </p>
            </div>
            <div>
                <b style="color: #FED7AA; font-size: 14px;">📉 Frequency Gaps in At-Risk:</b>
                <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                    At Risk customers average only <b>{risk_freq:.1f} orders</b> compared to <b>{champs_freq:.1f} orders</b> for Champions, highlighting opportunities for win-back campaigns.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
