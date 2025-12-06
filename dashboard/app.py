"""
Streamlit Dashboard for Government Scheme Targeting
Interactive policy simulation and district prioritization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Govt Scheme Targeting", page_icon="🏛️", layout="wide")

st.title("🏛️ Smart Government Scheme Targeting Dashboard")
st.markdown("Data-driven district prioritization for welfare scheme allocation")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('../data/district_scores.csv')
        return df
    except:
        return None

df = load_data()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 District Prioritization", "💰 Budget Simulator", "🗺️ State Analysis"])

with tab1:
    st.header("District Development Overview")

    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Districts", len(df))
        with col2:
            st.metric("States Covered", df['state'].nunique())
        with col3:
            st.metric("Avg Literacy", f"{df['literacy_rate'].mean():.1f}%")
        with col4:
            st.metric("Avg BPL", f"{df['bpl_population_pct'].mean():.1f}%")

        # Development cluster distribution
        st.subheader("District Development Distribution")
        if 'development_category' in df.columns:
            cluster_counts = df['development_category'].value_counts()
            fig = px.pie(values=cluster_counts.values, names=cluster_counts.index,
                        title="Districts by Development Category")
            st.plotly_chart(fig, use_container_width=True)

        # Correlation heatmap
        st.subheader("Indicator Correlations")
        numeric_cols = ['literacy_rate', 'infant_mortality_rate', 'per_capita_income',
                       'bpl_population_pct', 'sanitation_coverage', 'electrification_pct']
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                       title="Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("District Prioritization")

    if df is not None:
        scheme = st.selectbox("Select Scheme", ["Health", "Education", "PM-KISAN", "Infrastructure"])
        top_n = st.slider("Number of Priority Districts", 10, 50, 20)

        score_col = f'{scheme}_need_score'
        if score_col in df.columns:
            priority_df = df.nlargest(top_n, score_col)

            st.subheader(f"Top {top_n} Priority Districts for {scheme}")

            # Bar chart
            fig = px.bar(priority_df, x='district_name', y=score_col, color='state',
                        title=f"{scheme} Need Scores by District")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

            # Data table
            display_cols = ['district_name', 'state', score_col, 'population_lakhs']
            if scheme == 'Health':
                display_cols.extend(['infant_mortality_rate', 'immunization_coverage'])
            elif scheme == 'Education':
                display_cols.extend(['literacy_rate', 'dropout_rate'])

            st.dataframe(priority_df[display_cols], use_container_width=True, hide_index=True)

with tab3:
    st.header("Budget Allocation Simulator")

    if df is not None:
        col1, col2 = st.columns(2)
        with col1:
            sim_scheme = st.selectbox("Scheme", ["Health", "Education", "PM-KISAN", "Infrastructure"], key='sim')
            total_budget = st.number_input("Total Budget (Rs. Crores)", 1000, 100000, 10000)
        with col2:
            method = st.selectbox("Allocation Method", ["Proportional to Need", "Per Capita Weighted", "Equal (Top 50%)"])

        if st.button("Simulate Allocation", type="primary"):
            score_col = f'{sim_scheme}_need_score'

            if method == "Proportional to Need":
                total_score = df[score_col].sum()
                df['allocated_budget'] = (df[score_col] / total_score) * total_budget
            elif method == "Per Capita Weighted":
                weighted_pop = df['population_lakhs'] * df[score_col]
                df['allocated_budget'] = (weighted_pop / weighted_pop.sum()) * total_budget
            else:
                median_score = df[score_col].median()
                eligible = len(df[df[score_col] >= median_score])
                df['allocated_budget'] = np.where(df[score_col] >= median_score, total_budget / eligible, 0)

            st.subheader("Allocation Results")

            col1, col2 = st.columns(2)
            with col1:
                top_alloc = df.nlargest(15, 'allocated_budget')
                fig = px.bar(top_alloc, x='district_name', y='allocated_budget',
                            color='state', title="Top 15 Budget Allocations (Rs. Cr)")
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                state_alloc = df.groupby('state')['allocated_budget'].sum().sort_values(ascending=True)
                fig = px.bar(x=state_alloc.values, y=state_alloc.index, orientation='h',
                            title="State-wise Total Allocation (Rs. Cr)")
                st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("State-wise Analysis")

    if df is not None:
        selected_state = st.selectbox("Select State", sorted(df['state'].unique()))
        state_df = df[df['state'] == selected_state]

        st.subheader(f"Districts in {selected_state}")

        # Key indicators
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Districts", len(state_df))
        with col2:
            st.metric("Avg Literacy", f"{state_df['literacy_rate'].mean():.1f}%")
        with col3:
            st.metric("Avg IMR", f"{state_df['infant_mortality_rate'].mean():.1f}")
        with col4:
            st.metric("Avg Income", f"₹{state_df['per_capita_income'].mean():,.0f}")

        # Radar chart for state indicators
        indicators = ['literacy_rate', 'immunization_coverage', 'sanitation_coverage',
                     'electrification_pct', 'clean_water_access']
        state_means = state_df[indicators].mean()
        national_means = df[indicators].mean()

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=state_means.values, theta=indicators, fill='toself', name=selected_state))
        fig.add_trace(go.Scatterpolar(r=national_means.values, theta=indicators, fill='toself', name='National Avg'))
        fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])), title="State vs National Average")
        st.plotly_chart(fig, use_container_width=True)

        # District details
        st.dataframe(state_df[['district_name', 'population_lakhs', 'literacy_rate',
                              'infant_mortality_rate', 'per_capita_income', 'bpl_population_pct']],
                    use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("**Government Scheme Targeting Tool** | Data-Driven Policy Planning | © 2024")
