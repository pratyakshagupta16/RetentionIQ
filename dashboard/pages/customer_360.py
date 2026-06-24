import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.visualization.charts import apply_dark_theme, create_line_chart, CARD_COLOR, CYAN, PURPLE, MAGENTA, COLOR_PALETTE, SEGMENT_COLORS

def render(df_cleaned, df_features, churn_results):
    st.markdown("<h2 style='color: #93C5FD; font-family: Inter, sans-serif;'>🎯 Customer 360° Profile</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Drill down into individual customer purchase history, behavior patterns, and segment preferences.</p>", unsafe_allow_html=True)

    if df_cleaned is None or df_cleaned.empty or df_features is None or df_features.empty:
        st.warning("Please load database data first.")
        return


    cust_list = df_features["Customer ID"].unique()

    st.markdown("<div class='section-header'>Search Customer Profile</div>", unsafe_allow_html=True)
    col_sel1, col_sel2 = st.columns([1, 2])

    search_query = col_sel1.text_input("Search Customer ID (e.g., CUST-0001)", value="CUST-0001")

    if search_query in cust_list:
        selected_cust_id = search_query
    else:
        selected_cust_id = col_sel2.selectbox("Or select from list", cust_list)

    st.markdown(f"<h3>Viewing Profile: <span style='color:#93C5FD;'>{selected_cust_id}</span></h3>", unsafe_allow_html=True)


    cust_feat = df_features[df_features["Customer ID"] == selected_cust_id].iloc[0]
    cust_txns = df_cleaned[df_cleaned["Customer ID"] == selected_cust_id].sort_values(by="Purchase Date")


    p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns(5)


    seg_label = cust_feat.get('Segment', 'Unassigned')
    seg_color = SEGMENT_COLORS.get(seg_label, PURPLE)
    p_col1.markdown(f"""
    <div class="card" style="height: 120px; border-top: 3px solid {seg_color};">
        <div class="card-title">Behavioral Segment</div>
        <div class="card-value" style="font-size:20px; color:{seg_color}; margin-top:8px;">{seg_label}</div>
    </div>
    """, unsafe_allow_html=True)


    p_col2.markdown(f"""
    <div class="card" style="height: 120px; border-top: 3px solid {CYAN};">
        <div class="card-title">Total Spend</div>
        <div class="card-value" style="font-size:22px; color:{CYAN}; margin-top:8px;">${cust_feat.get('Total_Spend', 0.0):,.2f}</div>
    </div>
    """, unsafe_allow_html=True)


    p_col3.markdown(f"""
    <div class="card" style="height: 120px; border-top: 3px solid #A7F3D0;">
        <div class="card-title">Number of Orders</div>
        <div class="card-value" style="font-size:22px; color:#A7F3D0; margin-top:8px;">{int(cust_feat.get('Total_Orders', 0))}</div>
    </div>
    """, unsafe_allow_html=True)


    p_col4.markdown(f"""
    <div class="card" style="height: 120px; border-top: 3px solid {MAGENTA};">
        <div class="card-title">Average Order Value</div>
        <div class="card-value" style="font-size:22px; color:{MAGENTA}; margin-top:8px;">${cust_feat.get('Average_Order_Value', 0.0):,.2f}</div>
    </div>
    """, unsafe_allow_html=True)


    risk_label = cust_feat.get('Churn_Risk', 'Low Risk')
    risk_color = "#A7F3D0"
    if risk_label == "High Risk":
        risk_color = "#FECDD3"
    elif risk_label == "Medium Risk":
        risk_color = "#FED7AA"

    p_col5.markdown(f"""
    <div class="card" style="height: 120px; border-top: 3px solid {risk_color};">
        <div class="card-title">Churn Risk (Predicted)</div>
        <div class="card-value" style="font-size:22px; color:{risk_color}; margin-top:8px;">{risk_label}</div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    det_col1, det_col2, det_col3, det_col4 = st.columns(4)


    last_date = cust_feat.get("Last Purchase Date", "N/A")
    if isinstance(last_date, str):
        try:
            last_date = pd.to_datetime(last_date).strftime("%B %d, %Y")
        except:
            pass
    elif hasattr(last_date, "strftime"):
        last_date = last_date.strftime("%B %d, %Y")

    det_col1.metric("Customer ID", selected_cust_id)
    det_col2.metric("Last Purchase Date", str(last_date))
    det_col3.metric("Favorite Product Category", str(cust_feat.get("Favorite Category", "None")))


    avg_days_between = cust_feat.get("Average_Days_Between_Purchases", 0.0)
    det_col4.metric("Avg Days Between Orders", f"{avg_days_between:.1f} days" if avg_days_between > 0 else "N/A (One-Time)")

    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("<div class='section-header'>Purchase History & Preferences</div>", unsafe_allow_html=True)

    hist_col1, hist_col2 = st.columns([1.3, 1])


    with hist_col1:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-bottom: 15px;'>Purchase History & Trends</h4>", unsafe_allow_html=True)
        tab_history, tab_trend = st.tabs(["🛒 Purchase Ledger", "📈 Spending Trend Over Time"])

        with tab_history:
            if not cust_txns.empty:
                display_cols = ["Purchase Date", "Product Name", "Product Category", "Quantity", "Purchase Amount"]
                ledger_df = cust_txns[display_cols].copy()
                ledger_df["Purchase Date"] = pd.to_datetime(ledger_df["Purchase Date"]).dt.strftime("%Y-%m-%d")
                ledger_df["Purchase Amount"] = ledger_df["Purchase Amount"].map(lambda x: f"${x:,.2f}")
                ledger_df.columns = ["Date", "Product", "Category", "Quantity", "Spend"]
                st.dataframe(ledger_df, use_container_width=True, hide_index=True, height=280)
            else:
                st.info("No transaction history available.")

        with tab_trend:
            if not cust_txns.empty:
                trend_df = cust_txns.copy()
                trend_df["Purchase Date"] = pd.to_datetime(trend_df["Purchase Date"])


                fig_trend = create_line_chart(
                    trend_df,
                    x="Purchase Date",
                    y="Purchase Amount",
                    title="Transaction Spending Trend",
                    x_label="Date",
                    y_label="Order Spend ($)",
                    color_hex=CYAN
                )
                fig_trend.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10))
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("No purchases recorded to plot trend.")


    with hist_col2:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-bottom: 15px;'>Product Category Preferences</h4>", unsafe_allow_html=True)


        cat_pref = cust_txns.groupby("Product Category").agg({
            "Purchase Amount": "sum",
            "Quantity": "sum"
        }).reset_index()

        if not cat_pref.empty:
            fig_cat_bar = px.bar(
                cat_pref, x="Purchase Amount", y="Product Category",
                color="Product Category",
                color_discrete_sequence=COLOR_PALETTE,
                title="Spend Contribution by Product Category",
                labels={"Purchase Amount": "Spend ($)", "Product Category": "Category"},
                orientation="h"
            )
            fig_cat_bar.update_traces(marker_line_color=CARD_COLOR, marker_line_width=1, opacity=0.85)
            apply_dark_theme(fig_cat_bar)
            fig_cat_bar.update_layout(height=280, showlegend=False, margin=dict(t=30, b=10, l=10, r=10))
            st.plotly_chart(fig_cat_bar, use_container_width=True)
        else:
            st.info("No purchases recorded to plot category preferences.")
