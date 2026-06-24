import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.visualization.charts import apply_dark_theme, create_bar_chart, create_donut_chart, COLOR_PALETTE, CYAN, PURPLE, MAGENTA, CARD_COLOR

def render(df_features):
    st.markdown("<h2 style='color: #93C5FD; font-family: Inter, sans-serif;'>⚠️ Behavioral Churn Risk Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>After understanding customer behavior and segmentation, predictive machine learning models help identify customers who are becoming inactive.</p>", unsafe_allow_html=True)

    if df_features is None or df_features.empty:
        st.warning("Please load database data first.")
        st.stop()

    churn_results = st.session_state.get("churn_results", None)
    if churn_results is None:
        st.warning("Churn model results not found. Re-run pipeline.")
        st.stop()


    with st.expander("📖 Churn Prediction Glossary"):
        st.markdown("""
        * **Churn Probability**: The likelihood (from 0% to 100%) that a customer will become inactive. Calculated using a machine learning classifier based on demographic features and engagement metrics.
        * **Churn Risk Categories**:
          * 🟢 **Low Risk**: Churn probability under 30%.
          * 🟡 **Medium Risk (Savable)**: Churn probability between 30% and 70%. These customers are prime targets for retention campaigns.
          * 🔴 **High Risk**: Churn probability over 70%. These customers require immediate win-back outreach.
        """)


    best_name = churn_results.get("best_model_name", "N/A")
    metrics = churn_results.get("metrics")
    feature_importance_df = churn_results.get("feature_importance")


    high_risk_mask = df_features["Churn_Risk"] == "High Risk"
    num_high_risk = int(high_risk_mask.sum())
    rev_at_risk = float(df_features[high_risk_mask]["Monetary"].sum())

    med_risk_mask = df_features["Churn_Risk"] == "Medium Risk"
    num_medium_risk = int(med_risk_mask.sum())


    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)


    avg_churn_prob = df_features["Churn_Probability"].mean() * 100

    kpi_col1.markdown(f"""
    <div class="card" style="border-top: 3px solid #FECDD3;">
         <div class="card-title">Average Churn Probability</div>
         <div class="card-value" style="color: #FECDD3;">{avg_churn_prob:.1f}%</div>
         <div class="card-sub">Database average probability</div>
     </div>
     """, unsafe_allow_html=True)

    kpi_col2.markdown(f"""
    <div class="card" style="border-top: 3px solid #FECDD3;">
        <div class="card-title">High Risk Customers</div>
        <div class="card-value" style="color: #FECDD3;">{num_high_risk:,}</div>
        <div class="card-sub">Churn probability &gt; 70%</div>
    </div>
    """, unsafe_allow_html=True)

    kpi_col3.markdown(f"""
    <div class="card" style="border-top: 3px solid #FED7AA;">
        <div class="card-title">Revenue at Risk</div>
        <div class="card-value" style="color: #FED7AA;">${rev_at_risk:,.2f}</div>
        <div class="card-sub">From high-risk accounts</div>
    </div>
    """, unsafe_allow_html=True)

    kpi_col4.markdown(f"""
    <div class="card" style="border-top: 3px solid #A7F3D0;">
        <div class="card-title">Medium Risk (Savable)</div>
        <div class="card-value" style="color: #A7F3D0;">{num_medium_risk:,}</div>
        <div class="card-sub">Churn probability 30% - 70%</div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<br><div class='section-header'>Prediction Analysis & Model Tuning</div>", unsafe_allow_html=True)

    col_ch1, col_ch2 = st.columns(2)

    with col_ch1:

        risk_counts = df_features["Churn_Risk"].value_counts().reset_index()
        risk_counts.columns = ["Churn Risk", "Count"]


        risk_order = {"Low Risk": 0, "Medium Risk": 1, "High Risk": 2}
        risk_counts["Sort"] = risk_counts["Churn Risk"].map(risk_order)
        risk_counts = risk_counts.sort_values("Sort").drop(columns=["Sort"])

        fig_dist = create_donut_chart(risk_counts, names="Churn Risk", values="Count", title="Predicted Churn Risk Distribution")
        st.plotly_chart(fig_dist, use_container_width=True)

    with col_ch2:

        metrics_rows = []
        for model_name, score_dict in metrics.items():
            for score_name, val in score_dict.items():
                metrics_rows.append({
                    "Model": model_name,
                    "Metric": score_name,
                    "Score": val
                })
        metrics_df = pd.DataFrame(metrics_rows)

        fig_metrics = px.bar(
            metrics_df, x="Metric", y="Score", color="Model",
            barmode="group", title="Algorithm Comparison Metrics (Stratified Test-Set)",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_metrics.update_traces(marker_line_color=CARD_COLOR, marker_line_width=1, opacity=0.85)
        apply_dark_theme(fig_metrics)
        fig_metrics.update_layout(yaxis_range=[0, 1.05], height=350)
        st.plotly_chart(fig_metrics, use_container_width=True)


    st.markdown("<br><div class='section-header'>At-Risk Target Directory & Driver Insights</div>", unsafe_allow_html=True)

    col_dir1, col_dir2 = st.columns([1.1, 1])

    with col_dir1:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-top:0;'>At-Risk Customers Directory</h4>", unsafe_allow_html=True)

        at_risk_list = df_features[df_features["Churn_Probability"] >= 0.30].sort_values(by="Churn_Probability", ascending=False)

        if not at_risk_list.empty:
            table_df = at_risk_list[["Customer ID", "Churn_Probability", "Churn_Risk", "Monetary", "Recency"]].head(15).copy()
            table_df.columns = ["Customer ID", "Probability", "Risk Tier", "Total Spend", "Recency (Days)"]


            table_df["Probability"] = (table_df["Probability"] * 100).round(1).astype(str) + "%"
            table_df["Total Spend"] = table_df["Total Spend"].map(lambda x: f"${x:,.2f}")
            table_df["Recency (Days)"] = table_df["Recency (Days)"].astype(int)

            st.dataframe(table_df, use_container_width=True, hide_index=True, height=280)
        else:
            st.info("No customers at risk (probability >= 30%) in the database.")

    with col_dir2:
        st.markdown("<h4 style='color: #93C5FD; font-family: Inter; margin-top:0;'>Global Model Feature Importance</h4>", unsafe_allow_html=True)

        if feature_importance_df is not None and not feature_importance_df.empty:
            feat_imp_top = feature_importance_df.head(8).copy()
            fig_imp = create_bar_chart(
                feat_imp_top, x="Importance", y="Feature",
                title=f"Top Driver Factors for Champion Model ({best_name})",
                x_label="Normalized Importance Weight", y_label="Feature", color_hex=PURPLE,
                horizontal=True
            )
            fig_imp.update_layout(yaxis=dict(autorange="reversed"), height=280)
            st.plotly_chart(fig_imp, use_container_width=True)
        else:
            st.warning("No global feature importance calculation available.")


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background-color: #111827; padding: 15px; border-radius: 8px; border: 1px solid #1F2937;">
        <h4 style="margin: 0 0 5px 0; color:#93C5FD; font-family:Inter;">🏆 Champion Algorithm: {best_name}</h4>
        <p style="margin: 0; font-size:13px; color:#9CA3AF; line-height:1.5;">
            The model selected balances precision and recall folds to target likely churners accurately.
            The feature importance represents how heavily the algorithm weighs each feature to evaluate a customer's churn risk score.
        </p>
    </div>
    """, unsafe_allow_html=True)
