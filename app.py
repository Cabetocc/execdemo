import streamlit as st



def _safe_text(x):
    return str(x or '')

def _safe_strip(x):
    return _safe_text(x).strip()

import requests
import time
from pathlib import Path

WEBHOOK_URL = "https://cabetocc.app.n8n.cloud/webhook/stock-analysis"
LATEST_FILE = Path("data/latest.md")

def read_latest():
    if not LATEST_FILE.exists():
        return ""
    return LATEST_FILE.read_text(encoding="utf-8")

ticker = st.text_input("Enter stock ticker", value="-").upper().strip()
generate = st.button("Generate")

if generate:
    if not ticker:
        st.warning("Please enter a ticker.")
    else:
        before = read_latest()

        status = st.empty()
        progress = st.progress(0)

        with st.spinner(f"Generating analysis for {ticker}..."):
            # Trigger n8n
            try:
                requests.post(WEBHOOK_URL, json={"ticker": ticker}, timeout=30)
            except Exception as e:
                st.error(f"Could not start analysis: {e}")
                st.stop()

            # Wait up to 300 seconds for latest.md to change
            max_wait_seconds = 300
            interval_seconds = 2
            steps = max_wait_seconds // interval_seconds

            updated = before
            for i in range(int(steps)):
                time.sleep(interval_seconds)
                updated = read_latest()

                pct = int(((i + 1) / steps) * 100)
                progress.progress(pct)
                status.write(f"Still working… {pct}%")

                if updated and updated.strip() and updated != before:
                    status.success("New analysis is ready!")
                    progress.progress(100)
                    break

            if updated == before:
                status.warning("Still processing. Please wait a bit longer and press Generate again (or refresh).")

        st.rerun()


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="UAL Financial Analysis", layout="wide", page_icon="✈️")

# Title and header
st.title("✈️ United Airlines Holdings Inc. (UAL) - Financial Analysis")
st.markdown("### Comprehensive Investment Analysis & Outlook (Q2-Q3 2024)")

# Key metrics at the top
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Outlook", "POSITIVE", delta="3-6 Months")
with col2:
    st.metric("Market Cap", "$17.5B", delta="vs DAL: $31B")
with col3:
    st.metric("Forward P/E", "5.5x", delta="-1.0x vs DAL")
with col4:
    st.metric("Operating Margin", "5.5%", delta="Improving")
with col5:
    st.metric("Net Debt/EBITDA", "2.5x", delta="Moderate")

st.markdown("---")

# Executive Summary
with st.expander("📊 EXECUTIVE SUMMARY", expanded=True):
    st.markdown("""
    **Investment Thesis:** High-conviction **POSITIVE** outlook driven by:
    - ✅ Robust international & premium travel demand
    - ✅ Strategic network advantages (leading US international capacity)
    - ✅ Potential margin expansion in peak summer season
    - ⚠️ Tempered by operational pressures and Boeing delivery delays
    
    **Q4 2023 Performance:**
    - Revenue: $13.6B (+9.9% YoY)
    - Adjusted Net Income: $237M ($0.81/share)
    - Capacity (ASM): +14.7% YoY
    - PRASM: -4.7% YoY (healthy on multi-year basis)
    """)

# Recent Performance Visualization
st.markdown("## 📈 Financial Performance Metrics")

col1, col2 = st.columns(2)

with col1:
    # Q4 2023 Key Metrics
    metrics_data = {
        'Metric': ['Revenue', 'Net Income', 'Capacity Growth', 'PRASM Change'],
        'Value': [13.6, 0.237, 14.7, -4.7],
        'Unit': ['$B', '$B', '%', '%']
    }
    df_metrics = pd.DataFrame(metrics_data)
    
    fig_metrics = go.Figure()
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
    
    for i, row in df_metrics.iterrows():
        fig_metrics.add_trace(go.Bar(
            x=[row['Metric']],
            y=[row['Value']],
            name=row['Metric'],
            text=[f"{row['Value']}{row['Unit']}"],
            textposition='outside',
            marker_color=colors[i],
            showlegend=False
        ))
    
    fig_metrics.update_layout(
        title="Q4 2023 Performance Highlights",
        yaxis_title="Value",
        height=400,
        template="plotly_white"
    )
    st.plotly_chart(fig_metrics, use_container_width=True)

with col2:
    # Projected Growth Q2-Q3 2024
    quarters = ['Q4 2023', 'Q1 2024E', 'Q2 2024E', 'Q3 2024E']
    revenue = [13.6, 13.0, 15.2, 15.8]
    op_margin = [5.5, -1.0, 8.5, 9.2]
    
    fig_proj = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_proj.add_trace(
        go.Bar(name='Revenue ($B)', x=quarters, y=revenue, marker_color='#1f77b4'),
        secondary_y=False
    )
    
    fig_proj.add_trace(
        go.Scatter(name='Operating Margin (%)', x=quarters, y=op_margin, 
                   marker_color='#ff7f0e', mode='lines+markers', line=dict(width=3)),
        secondary_y=True
    )
    
    fig_proj.update_layout(
        title="Projected Performance Trajectory",
        height=400,
        template="plotly_white",
        legend=dict(x=0.01, y=0.99)
    )
    fig_proj.update_xaxes(title_text="Quarter")
    fig_proj.update_yaxes(title_text="Revenue ($B)", secondary_y=False)
    fig_proj.update_yaxes(title_text="Operating Margin (%)", secondary_y=True)
    
    st.plotly_chart(fig_proj, use_container_width=True)

# Peer Comparison
st.markdown("## 🏆 Competitive Benchmarking")

peer_data = {
    'Metric': ['Market Cap ($B)', 'Forward P/E', 'Revenue Growth (%)', 
               'Operating Margin (%)', 'Net Debt/EBITDA', 'Intl Market Share (%)'],
    'UAL': [17.5, 5.5, 18.5, 5.5, 2.5, 25],
    'DAL': [31.0, 6.5, 15.0, 10.5, 1.5, 22],
    'AAL': [9.0, 4.0, 10.5, 6.0, 4.0, 18]
}

df_peers = pd.DataFrame(peer_data)

# Radar chart for competitive comparison
categories = ['Market Cap', 'P/E Ratio', 'Revenue Growth', 'Op Margin', 'Intl Share']
fig_radar = go.Figure()

# Normalize values for radar chart
ual_norm = [17.5/31, 5.5/6.5, 18.5/18.5, 5.5/10.5, 25/25]
dal_norm = [31.0/31, 6.5/6.5, 15.0/18.5, 10.5/10.5, 22/25]
aal_norm = [9.0/31, 4.0/6.5, 10.5/18.5, 6.0/10.5, 18/25]

fig_radar.add_trace(go.Scatterpolar(r=ual_norm, theta=categories, fill='toself', name='UAL', line_color='#1f77b4'))
fig_radar.add_trace(go.Scatterpolar(r=dal_norm, theta=categories, fill='toself', name='DAL', line_color='#2ca02c'))
fig_radar.add_trace(go.Scatterpolar(r=aal_norm, theta=categories, fill='toself', name='AAL', line_color='#d62728'))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
    title="Competitive Position (Normalized)",
    height=500
)

col1, col2 = st.columns([1, 1])

with col1:
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    st.markdown("### Key Competitive Insights")
    st.markdown("""
    **🥇 UAL Advantages:**
    - Leading international market share (25%)
    - Strongest YoY revenue growth (18.5%)
    - Competitive valuation (5.5x P/E)
    
    **⚠️ Areas for Improvement:**
    - Operating margin trails DAL by 5 percentage points
    - Higher debt than DAL (but better than AAL)
    - Market cap reflects growth potential
    
    **🎯 Strategic Position:**
    UAL positioned between DAL's premium brand and AAL's higher leverage profile
    """)

# Detailed peer comparison table
st.markdown("### Detailed Peer Comparison Table")
st.dataframe(df_peers.set_index('Metric'), use_container_width=True)

# Key Catalysts
st.markdown("## 🚀 Key Growth Catalysts (Next 3-6 Months)")

catalysts = {
    'Catalyst': [
        'International & Premium Demand',
        'Operational Excellence',
        'Favorable Fuel Pricing'
    ],
    'Impact': ['High', 'Medium', 'High'],
    'Probability': [85, 70, 60],
    'Description': [
        'Strong summer bookings for transatlantic/transpacific routes driving high-yield revenue',
        'Improved on-time performance and network optimization reducing costs',
        'Stable/declining jet fuel prices reducing largest operating expense (25-30% of costs)'
    ]
}

df_catalysts = pd.DataFrame(catalysts)

# Impact visualization
fig_catalysts = go.Figure()

colors_impact = {'High': '#2ca02c', 'Medium': '#ff7f0e', 'Low': '#d62728'}

fig_catalysts.add_trace(go.Bar(
    y=df_catalysts['Catalyst'],
    x=df_catalysts['Probability'],
    orientation='h',
    marker_color=[colors_impact[i] for i in df_catalysts['Impact']],
    text=df_catalysts['Probability'].apply(lambda x: f"{x}%"),
    textposition='outside'
))

fig_catalysts.update_layout(
    title="Catalyst Probability Assessment",
    xaxis_title="Probability (%)",
    yaxis_title="",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig_catalysts, use_container_width=True)

for idx, row in df_catalysts.iterrows():
    with st.expander(f"📌 {row['Catalyst']} - {row['Impact']} Impact"):
        st.write(row['Description'])

# Adjacent Industry Analysis
st.markdown("## 🔗 Adjacent Industry Impact Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⛽ Oil & Gas (Upstream)")
    st.markdown("""
    **Impact:** Headwind → Potential Tailwind
    
    - Jet fuel = 25-30% of operating costs
    - Current volatility from geopolitics
    - $5-$10/barrel crude swing = material earnings impact
    
    **Lead Indicator:** Brent Crude, WTI futures
    """)
    
    # Fuel impact chart
    fuel_scenarios = pd.DataFrame({
        'Scenario': ['Low ($70)', 'Base ($85)', 'High ($100)'],
        'Margin Impact': [2.5, 0, -3.0]
    })
    
    fig_fuel = go.Figure(go.Waterfall(
        x=fuel_scenarios['Scenario'],
        y=fuel_scenarios['Margin Impact'],
        marker_color=['green', 'gray', 'red']
    ))
    fig_fuel.update_layout(title="Fuel Price Impact on Margins (%)", height=300)
    st.plotly_chart(fig_fuel, use_container_width=True)

with col2:
    st.markdown("### 🏨 Travel & Hospitality (Downstream)")
    st.markdown("""
    **Impact:** Strong Tailwind
    
    - Robust recovery in leisure travel
    - High hotel occupancy & pricing power
    - Strong consumer confidence
    
    **Lead Indicator:** Hotel ADR, occupancy rates, cruise bookings
    """)
    
    # Demand strength gauge
    fig_demand = go.Figure(go.Indicator(
        mode="gauge+number",
        value=85,
        title={'text': "Travel Demand Strength"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "green"},
               'steps': [
                   {'range': [0, 50], 'color': "lightgray"},
                   {'range': [50, 75], 'color': "yellow"},
                   {'range': [75, 100], 'color': "lightgreen"}
               ]}
    ))
    fig_demand.update_layout(height=300)
    st.plotly_chart(fig_demand, use_container_width=True)

with col3:
    st.markdown("### ✈️ Aircraft Manufacturing (Upstream)")
    st.markdown("""
    **Impact:** Moderate Headwind
    
    - Boeing delivery delays impacting fleet modernization
    - Supply chain disruptions
    - Higher maintenance costs
    
    **Lead Indicator:** Boeing/Airbus delivery schedules, production rates
    """)
    
    # Delivery delay impact
    delivery_impact = pd.DataFrame({
        'Factor': ['Fleet Age', 'Fuel Efficiency', 'Capacity Growth'],
        'Impact': [-2, -1.5, -3]
    })
    
    fig_delivery = go.Figure(go.Bar(
        x=delivery_impact['Impact'],
        y=delivery_impact['Factor'],
        orientation='h',
        marker_color='orange'
    ))
    fig_delivery.update_layout(title="Delivery Delay Impact", height=300)
    st.plotly_chart(fig_delivery, use_container_width=True)

# Risk Assessment
st.markdown("## ⚖️ Risk Assessment - Bull vs Bear Case")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🐻 Bear Case Scenarios")
    bear_risks = {
        'Risk': ['Fuel Price Spike', 'Weak Summer Demand', 'Operational Disruptions', 'Boeing Delays'],
        'Severity': [9, 7, 8, 6],
        'Likelihood': [6, 4, 5, 8]
    }
    df_bear = pd.DataFrame(bear_risks)
    
    fig_bear = px.scatter(df_bear, x='Likelihood', y='Severity', size='Severity',
                          text='Risk', color='Severity',
                          color_continuous_scale='Reds',
                          range_x=[0, 10], range_y=[0, 10])
    fig_bear.update_traces(textposition='top center')
    fig_bear.update_layout(title="Bear Case Risk Matrix", height=400)
    st.plotly_chart(fig_bear, use_container_width=True)
    
    st.markdown("""
    **Key Downside Risks:**
    - Sharp jet fuel price increases
    - Macroeconomic downturn reducing business travel
    - Major operational meltdowns
    - Extended Boeing delivery delays
    """)

with col2:
    st.markdown("### 🐂 Bull Case Opportunities")
    bull_opps = {
        'Opportunity': ['Exceptional Intl Demand', 'Declining Fuel', 'Operational Excellence', 'Strong GDP Growth'],
        'Upside': [9, 8, 7, 8],
        'Likelihood': [7, 5, 6, 6]
    }
    df_bull = pd.DataFrame(bull_opps)
    
    fig_bull = px.scatter(df_bull, x='Likelihood', y='Upside', size='Upside',
                          text='Opportunity', color='Upside',
                          color_continuous_scale='Greens',
                          range_x=[0, 10], range_y=[0, 10])
    fig_bull.update_traces(textposition='top center')
    fig_bull.update_layout(title="Bull Case Opportunity Matrix", height=400)
    st.plotly_chart(fig_bull, use_container_width=True)
    
    st.markdown("""
    **Key Upside Drivers:**
    - Stronger-than-expected international bookings
    - Stable or declining crude oil prices
    - Flawless peak summer execution
    - Robust consumer spending & GDP growth
    """)

# Scenario Analysis
st.markdown("## 📊 Scenario Analysis (Q2-Q3 2024)")

scenarios_data = {
    'Metric': ['Revenue Growth (%)', 'Operating Margin (%)', 'EPS ($)', 'Stock Performance'],
    'Bear': [3, 2, 0.50, '-15%'],
    'Base': [9, 5.5, 2.50, '+10%'],
    'Bull': [15, 9, 4.00, '+30%']
}

df_scenarios = pd.DataFrame(scenarios_data)
st.dataframe(df_scenarios.set_index('Metric'), use_container_width=True)

# EPS scenario visualization
eps_data = pd.DataFrame({
    'Scenario': ['Bear', 'Base', 'Bull'],
    'EPS': [0.50, 2.50, 4.00],
    'Color': ['red', 'yellow', 'green']
})

fig_eps = go.Figure(go.Bar(
    x=eps_data['Scenario'],
    y=eps_data['EPS'],
    marker_color=['#d62728', '#ff7f0e', '#2ca02c'],
    text=eps_data['EPS'].apply(lambda x: f"${x:.2f}"),
    textposition='outside'
))

fig_eps.update_layout(
    title="Q2-Q3 2024 EPS Scenarios",
    yaxis_title="EPS ($)",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig_eps, use_container_width=True)

# Investment Recommendation
st.markdown("## 🎯 Investment Recommendation")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.success("### ✅ POSITIVE OUTLOOK - BUY RECOMMENDATION")
    
    st.markdown("""
    **Target Horizon:** 3-6 Months (Q2-Q3 2024)
    
    **Key Investment Thesis:**
    1. **Leading International Position:** 25% international market share provides competitive moat
    2. **Peak Summer Catalyst:** Strong positioning for high-yield summer travel season
    3. **Valuation Opportunity:** 5.5x Forward P/E offers upside vs. fundamentals
    4. **Margin Expansion Path:** Operating leverage from capacity growth + demand strength
    
    **Expected Returns:**
    - Base Case: +10% to +15%
    - Bull Case: +25% to +35%
    
    **Risk Mitigation:**
    - Monitor fuel prices weekly (Brent crude)
    - Track booking trends and forward revenue indicators
    - Watch Boeing delivery updates
    - Set stop-loss at -12% for downside protection
    """)

# Additional Context from 2025 Analysis
st.markdown("## 📅 Extended Outlook: 2025 Context")

with st.expander("🔮 2025 Market Sentiment & Strategic Factors"):
    st.markdown("""
    ### Market Sentiment (Early 2025)
    **Overall:** Cautiously Optimistic with Near-Term Headwinds
    
    **Bullish Factors:**
    - ✅ Sustained strong demand for international & premium travel
    - ✅ Strategic network advantage in key hubs (EWR, SFO, ORD)
    - ✅ Confident FY2025 earnings guidance from management
    
    **Key Concerns:**
    - ⚠️ Labor cost inflation from new pilot/FA contracts
    - ⚠️ Geopolitical uncertainty affecting fuel prices
    - ⚠️ Higher debt servicing costs vs. peers
    - ⚠️ Boeing manufacturing delays constraining growth
    
    ### Critical 2025 Strategic Issues
    
    **🏭 Boeing Crisis Impact:**
    > *"Boeing's instability is the single largest external operational and strategic risk to United's near-term growth plans"*
    
    - Production delays on 737 MAX 7/10 and 787 constrain capacity
    - Cannot retire older, less efficient aircraft as planned
    - CEO Kirby: "Boeing is the biggest challenge we face"
    
    **💳 Ancillary Revenue Opportunities:**
    - Co-branded Chase credit card partnership is major profit center
    - MileagePlus loyalty program monetization
    - NDC (New Distribution Capability) direct sales push
    
    **🌱 Sustainability Initiatives:**
    - Leading U.S. carrier in SAF (Sustainable Aviation Fuel) investment
    - Near-term cost pressure but long-term brand advantage
    - Regulatory compliance positioning
    """)

# Footer with data sources
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p><b>Data Sources:</b> Q4 2023 Earnings Report, Industry Analysis, Peer Benchmarking, Forward Estimates</p>
    <p><b>Analysis Date:</b> Q1 2024 | <b>Target Period:</b> Q2-Q3 2024 | <b>Extended Context:</b> Early 2025</p>
    <p><b>Disclaimer:</b> This analysis is for informational purposes only and does not constitute investment advice.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with quick navigation
with st.sidebar:
    st.markdown("## 📋 Quick Navigation")
    st.markdown("""
    - [Executive Summary](#executive-summary)
    - [Financial Performance](#financial-performance-metrics)
    - [Peer Comparison](#competitive-benchmarking)
    - [Growth Catalysts](#key-growth-catalysts-next-3-6-months)
    - [Industry Impact](#adjacent-industry-impact-analysis)
    - [Risk Assessment](#risk-assessment-bull-vs-bear-case)
    - [Recommendation](#investment-recommendation)
    """)
    
    st.markdown("---")
    st.markdown("## 📊 Key Metrics Summary")
    st.metric("Recommendation", "BUY")
    st.metric("Price Target Upside", "+10-15%")
    st.metric("Risk Rating", "MODERATE")
    
    st.markdown("---")
    st.markdown("## 🔔 Watch List")
    st.markdown("""
    - ⛽ Brent Crude Oil Price
    - 📈 Forward Bookings Data
    - ✈️ Boeing Delivery Updates  
    - 💼 Corporate Travel Trends
    - 🌍 International Capacity
    """)