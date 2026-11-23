"""Dataset Insights and Exploratory Data Analysis Page for AgriSmart."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.ui.styles import render_hero
from src.data.loaders import load_crop_data, load_fertilizer_data, load_yield_data, get_dataset_summary


@st.cache_data
def get_all_dataset_summaries():
    c_df = load_crop_data()
    f_df = load_fertilizer_data()
    y_df = load_yield_data(deduplicate=True)
    return {
        "crop": (c_df, get_dataset_summary(c_df, "Crop Recommendation")),
        "fert": (f_df, get_dataset_summary(f_df, "Fertilizer Recommendation")),
        "yield": (y_df, get_dataset_summary(y_df, "FAO Global Crop Yield")),
    }


def render_insights_page():
    render_hero(
        title="Dataset Insights & Exploratory Data Analysis",
        subtitle="Comprehensive data exploration covering schema architectures, missing value audits, class imbalance distributions, and feature correlations.",
        badge="Audited Data Insights",
    )

    datasets = get_all_dataset_summaries()

    tab_crop, tab_fert, tab_yield, tab_audit = st.tabs([
        "🌾 Crop Recommendation Data",
        "🧪 Fertilizer Recommendation Data",
        "📈 Crop Yield Data",
        "🔍 Data Audit Findings & Warnings",
    ])

    # Crop Tab
    with tab_crop:
        df_crop, summary_crop = datasets["crop"]
        st.markdown("#### Crop Recommendation Dataset Profile")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Rows", f"{summary_crop['rows']:,}")
        c2.metric("Total Features", f"{summary_crop['columns']}")
        c3.metric("Missing Values", f"{summary_crop['missing_values_total']}")
        c4.metric("Exact Duplicates", f"{summary_crop['exact_duplicates']}")

        st.markdown("##### Target Class Distribution (22 Crops)")
        counts_crop = df_crop["label"].value_counts().reset_index()
        counts_crop.columns = ["Crop", "Count"]
        fig_c = px.bar(
            counts_crop,
            x="Crop",
            y="Count",
            title="Class Counts (Perfect 100 Samples Per Class)",
            color_discrete_sequence=["#10b981"],
        )
        fig_c.update_layout(height=350)
        st.plotly_chart(fig_c, use_container_width=True)

        st.markdown("##### Feature Correlation Heatmap")
        num_crop = df_crop.select_dtypes(include=[np.number])
        corr_crop = num_crop.corr()
        fig_corr_c = px.imshow(
            corr_crop,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Nutrient & Climatic Pearson Correlations",
        )
        fig_corr_c.update_layout(height=420)
        st.plotly_chart(fig_corr_c, use_container_width=True)

    # Fertilizer Tab
    with tab_fert:
        df_fert, summary_fert = datasets["fert"]
        st.markdown("#### Fertilizer Recommendation Dataset Profile")
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Total Rows", f"{summary_fert['rows']:,}")
        f2.metric("Features (Numeric + Cat)", f"{summary_fert['columns']}")
        f3.metric("Missing Values", f"{summary_fert['missing_values_total']}")
        f4.metric("Exact Duplicates", f"{summary_fert['exact_duplicates']}")

        st.markdown("##### Target Class Distribution & Class Imbalance")
        counts_fert = df_fert["Recommended_Fertilizer"].value_counts().reset_index()
        counts_fert.columns = ["Fertilizer", "Count"]
        counts_fert["Percentage"] = (counts_fert["Count"] / len(df_fert) * 100).round(1)

        fig_f = px.bar(
            counts_fert,
            x="Fertilizer",
            y="Count",
            text=counts_fert["Percentage"].apply(lambda p: f"{p}%"),
            title="Fertilizer Class Frequency (SSP Rare Class: 1.8%)",
            color="Count",
            color_continuous_scale="Teal",
        )
        fig_f.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_f, use_container_width=True)

        st.markdown("##### Soil Nutrient Deficiencies by Recommended Fertilizer")
        mean_nutrients = df_fert.groupby("Recommended_Fertilizer")[["Nitrogen_Level", "Phosphorus_Level", "Potassium_Level"]].mean().reset_index()
        fig_nutrients = px.bar(
            mean_nutrients.melt(id_vars="Recommended_Fertilizer", var_name="Nutrient", value_name="Mean kg/ha"),
            x="Recommended_Fertilizer",
            y="Mean kg/ha",
            color="Nutrient",
            barmode="group",
            title="Mean Soil N-P-K Levels per Recommended Fertilizer (Visualizing Trigger Boundaries)",
            color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981"],
        )
        fig_nutrients.update_layout(height=380)
        st.plotly_chart(fig_nutrients, use_container_width=True)

    # Yield Tab
    with tab_yield:
        df_yield, summary_yield = datasets["yield"]
        st.markdown("#### FAO Global Crop Yield Dataset Profile")
        y1, y2, y3, y4 = st.columns(4)
        y1.metric("Deduplicated Rows", f"{summary_yield['rows']:,}")
        y2.metric("Temporal Span", f"{df_yield['Year'].min()} – {df_yield['Year'].max()}")
        y3.metric("Global Territories", f"{df_yield['Area'].nunique()}")
        y4.metric("Crop Species", f"{df_yield['Item'].nunique()}")

        st.markdown("##### Yield Distribution Across Major Crop Species")
        fig_box = px.box(
            df_yield,
            x="Item",
            y="hg/ha_yield",
            color="Item",
            title="Crop Yield Variations (in hg/ha; 10,000 hg/ha = 1 tonne/ha)",
        )
        fig_box.update_layout(height=450, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("##### Temporal Distribution of FAO Observations")
        year_counts = df_yield["Year"].value_counts().sort_index().reset_index()
        year_counts.columns = ["Year", "Observations"]
        fig_yr = px.line(
            year_counts,
            x="Year",
            y="Observations",
            markers=True,
            title="Annual Observations (Highlighting 2010 Chronological Split Boundary)",
        )
        fig_yr.add_vline(x=2009.5, line_dash="dash", line_color="red", annotation_text="Train (≤2009) | Test (≥2010)")
        fig_yr.update_layout(height=340)
        st.plotly_chart(fig_yr, use_container_width=True)

    # Audit Tab
    with tab_audit:
        st.markdown("#### Data Audit Findings, Risks, and Mitigations")
        
        st.markdown(
            """
            <div class="agrismart-card">
                <h4 style="color:#1e293b;margin-bottom:0.4rem;">1. Duplicate Area–Item–Year Combinations in yield_df.csv</h4>
                <p style="color:#475569;font-size:0.92rem;line-height:1.5;">
                    <strong>Finding:</strong> <code>yield_df.csv</code> contained 15,112 repeated <code>[Area, Item, Year]</code> rows.<br>
                    <strong>Root Cause:</strong> Raw weather table <code>temp.csv</code> contains 42,797 duplicate <code>[country, year]</code> rows representing multiple meteorological weather stations per country. Merging this onto <code>yield.csv</code> produced 1-to-many Cartesian multiplication.<br>
                    <strong>Resolution:</strong> Purged 2,310 exact duplicate rows across all features to guarantee train/test isolation, and validated that yield, rainfall, and pesticide values have 0 variance within any (Area, Item, Year) combination.
                </p>
            </div>

            <div class="agrismart-card">
                <h4 style="color:#b91c1c;margin-bottom:0.4rem;">2. Critical Target Leakage Risk in crop_yield.csv</h4>
                <p style="color:#475569;font-size:0.92rem;line-height:1.5;">
                    <strong>Finding:</strong> The workspace also included an alternative dataset <code>crop_yield.csv</code> containing <code>['Crop', 'State', 'Area', 'Production', 'Yield']</code>.<br>
                    <strong>Hazard:</strong> Because <code>Yield = Production / Area</code>, using <code>Production</code> as an input yields a trivial mathematical identity ($R^2 \approx 1.0$), constituting complete target leakage.<br>
                    <strong>Decision:</strong> Rejected <code>crop_yield.csv</code> in favor of the canonical FAO global dataset (<code>yield_df.csv</code>) which strictly abides by pre-harvest observable inputs.
                </p>
            </div>

            <div class="agrismart-card">
                <h4 style="color:#0f766e;margin-bottom:0.4rem;">3. Triple Duplicate Files in Crop Recommendation</h4>
                <p style="color:#475569;font-size:0.92rem;line-height:1.5;">
                    <strong>Finding:</strong> <code>Crop Reccomendation Dataset 2.csv</code>, <code>Crop_recommendation 2.csv</code>, and <code>Crop_recommendation.csv</code> all possess identical MD5 checksums (<code>5e743dd4cf49f84d23a904cd51c9b5b8</code>).<br>
                    <strong>Decision:</strong> Selected <code>Crop_recommendation.csv</code> as canonical; preserved source files untouched.
                </p>
            </div>

            <div class="agrismart-card">
                <h4 style="color:#92400e;margin-bottom:0.4rem;">4. Fertilizer Class Imbalance & SSP Rare Class</h4>
                <p style="color:#475569;font-size:0.92rem;line-height:1.5;">
                    <strong>Finding:</strong> Urea (31.0%) and DAP (29.2%) dominate the dataset, while SSP (Single Super Phosphate) constitutes only 1.82% of records.<br>
                    <strong>Resolution:</strong> Enforced cost-sensitive sample weighting (<code>class_weight='balanced'</code>) and stratified 80:20 partitioning to guarantee minority class representation.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
