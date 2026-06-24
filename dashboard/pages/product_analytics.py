import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.visualization.charts import apply_dark_theme, create_bar_chart, COLOR_PALETTE, CYAN, PURPLE, MAGENTA, SEGMENT_COLORS, CARD_COLOR

def render(df_cleaned, df_features):
    st.markdown("<h2 style='color: #93C5FD; font-family: Inter, sans-serif;'>📦 Product Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Discover top-performing inventory items and categories aligned with customer purchase preferences.</p>", unsafe_allow_html=True)

    if df_cleaned is None or df_cleaned.empty:
        st.warning("Please load database data first.")
        return

    st.markdown("<div class='section-header'>Product Category Revenue Performance</div>", unsafe_allow_html=True)

    col_inv1, col_inv2 = st.columns(2)


    cat_perf = df_cleaned.groupby("Product Category").agg({
        "Purchase Amount": "sum",
        "Quantity": "sum"
    }).reset_index()

    fig_tree = px.treemap(
        cat_perf,
        path=["Product Category"],
        values="Purchase Amount",
        title="Revenue Contribution by Product Category (Size = Spend)",
        color="Quantity",
        color_continuous_scale=[[0, "#111827"], [0.5, PURPLE], [1, CYAN]]
    )
    apply_dark_theme(fig_tree)
    col_inv1.plotly_chart(fig_tree, use_container_width=True)


    top_qty = df_cleaned.groupby("Product Name")["Quantity"].sum().reset_index().sort_values(by="Quantity", ascending=False).head(10)
    fig_qty = create_bar_chart(
        top_qty, x="Quantity", y="Product Name",
        title="Top 10 Products by Volume Sold (Units)",
        x_label="Units Sold", y_label="Product", color_hex=CYAN,
        horizontal=True
    )
    fig_qty.update_layout(yaxis=dict(autorange="reversed"))
    col_inv2.plotly_chart(fig_qty, use_container_width=True)


    df_merged = None
    if df_features is not None and not df_features.empty and "Segment" in df_features.columns:
        st.markdown("<br><div class='section-header'>Segment Category Preferences</div>", unsafe_allow_html=True)


        df_merged = pd.merge(df_cleaned, df_features[["Customer ID", "Segment"]], on="Customer ID", how="inner")

        if not df_merged.empty:

            seg_cat_perf = df_merged.groupby(["Segment", "Product Category"])["Purchase Amount"].sum().reset_index()


            fig_seg_cat = px.bar(
                seg_cat_perf,
                x="Product Category",
                y="Purchase Amount",
                color="Segment",
                barmode="group",
                title="Total Spend per Category across Customer Segments",
                labels={"Purchase Amount": "Spend ($)", "Segment": "Customer Segment"},
                color_discrete_map=SEGMENT_COLORS
            )
            fig_seg_cat.update_traces(marker_line_color=CARD_COLOR, marker_line_width=1, opacity=0.85)
            apply_dark_theme(fig_seg_cat)
            fig_seg_cat.update_layout(height=350)
            st.plotly_chart(fig_seg_cat, use_container_width=True)
        else:
            st.info("No transaction-segment data available to map preferences.")


    st.markdown("<br><div class='section-header'>Granular Product Performance</div>", unsafe_allow_html=True)

    col_inv3, col_inv4 = st.columns(2)


    top_rev = df_cleaned.groupby("Product Name")["Purchase Amount"].sum().reset_index().sort_values(by="Purchase Amount", ascending=False).head(10)

    with col_inv3:
        fig_rev = create_bar_chart(
            top_rev, x="Purchase Amount", y="Product Name",
            title="Top 10 Products by Revenue ($)",
            x_label="Revenue ($)", y_label="Product", color_hex=MAGENTA,
            horizontal=True
        )
        fig_rev.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_rev, use_container_width=True)

    with col_inv4:

        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-top:0;'>Product Inventory Scorecard</h4>", unsafe_allow_html=True)

        prod_table = df_cleaned.groupby("Product Name").agg({
            "Quantity": "sum",
            "Purchase Amount": "sum"
        }).reset_index().sort_values(by="Purchase Amount", ascending=False)

        prod_table.columns = ["Product", "Units Sold", "Spend"]
        prod_table["Spend"] = prod_table["Spend"].map(lambda x: f"${x:,.2f}")
        prod_table["Units Sold"] = prod_table["Units Sold"].astype(int)

        st.dataframe(prod_table, use_container_width=True, hide_index=True, height=280)


    if not cat_perf.empty and not top_rev.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Key Product Insights</div>", unsafe_allow_html=True)

        top_cat = cat_perf.sort_values(by="Purchase Amount", ascending=False).iloc[0]["Product Category"]
        top_prod_rev = top_rev.iloc[0]["Product Name"]


        top_champ_cat = "N/A"
        if df_merged is not None and not df_merged.empty:
            champs_txns = df_merged[df_merged["Segment"] == "Champions"]
            if not champs_txns.empty:
                champs_cat_spend = champs_txns.groupby("Product Category")["Purchase Amount"].sum()
                if not champs_cat_spend.empty:
                    top_champ_cat = champs_cat_spend.idxmax()

        st.markdown(f"""
        <div style="background-color: #111827; padding: 20px; border-radius: 10px; border: 1px solid #1F2937;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px;">
                <div>
                    <b style="color: #A98EA3; font-size: 14px;">📦 Category Dominance:</b>
                    <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                        <b>{top_cat}</b> is the leading product category by sales volume, representing the highest spend contribution across historical transactions.
                    </p>
                </div>
                <div>
                    <b style="color: #7C9BB8; font-size: 14px;">⭐ Best Selling Product:</b>
                    <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                        <b>{top_prod_rev}</b> has generated the highest revenue share among all inventory items.
                    </p>
                </div>
                <div>
                    <b style="color: #8FB79A; font-size: 14px;">🏆 Champions Preference:</b>
                    <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0;">
                        Our high-value Champions segment shows the strongest purchase affinity toward the <b>{top_champ_cat}</b> category.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
