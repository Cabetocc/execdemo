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


import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="UAL Stock Analysis Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0A2463;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3E92CC;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3E92CC;
    }
    .bullish {
        color: #00B050;
        font-weight: bold;
    }
    .bearish {
        color: #C00000;
        font-weight: bold;
    }
    .neutral {
        color: #FFA500;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">✈️ United Airlines Holdings (UAL) - Financial Analysis Dashboard</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/0A2463/FFFFFF?text=UAL", use_container_width=True)
    st.markdown("### Analysis Overview")
    st.markdown("**Ticker:** UAL")
    st.markdown("**Industry:** Passenger Air Transportation")
    st.markdown("**Outlook:** <span class='bullish'>Moderately Bullish</span>", unsafe_allow_html=True)
    st.markdown("**Time Horizon:** 3-6 Months")
    st.markdown("---")
    st.markdown("**Analysis Date:** Q2 2024")
    st.markdown("**Report Type:** Equity Research")

# Key Metrics Section
st.markdown('<div class="sub-header">📊 Key Financial Metrics (Q1 2024)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Operating Revenue",
        value="$12.4B",
        delta="9.7% YoY",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="Net Loss (Q1)",
        value="$124M",
        delta="Improved vs Prior Year",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="Operating Margin (TTM)",
        value="4.8%",
        delta="Industry Competitive"
    )

with col4:
    st.metric(
        label="Market Cap",
        value="$16.5B",
        delta="Stable"
    )

# Peer Comparison Section
st.markdown('<div class="sub-header">🏆 Peer Comparison Analysis</div>', unsafe_allow_html=True)

peer_data = pd.DataFrame({
    'Airline': ['United (UAL)', 'Delta (DAL)', 'American (AAL)', 'Southwest (LUV)'],
    'Market Cap ($B)': [16.5, 31.5, 10.0, 16.5],
    'Forward P/E': [5.1, 6.0, 4.6, 20.0],
    'Revenue Growth (%)': [9.7, 7.8, 3.1, 1.1],
    'Operating Margin (%)': [4.8, 8.3, 4.2, 3.4],
    'Net Debt/EBITDA': [2.5, 1.9, 3.2, 1.0]
})

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["📈 Revenue & Growth", "💰 Profitability & Valuation", "📊 Leverage & Balance Sheet"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue Growth Chart
        fig_revenue = go.Figure(data=[
            go.Bar(
                x=peer_data['Airline'],
                y=peer_data['Revenue Growth (%)'],
                marker_color=['#3E92CC', '#6CA6CD', '#90CAF9', '#B3E5FC'],
                text=peer_data['Revenue Growth (%)'],
                textposition='auto',
            )
        ])
        fig_revenue.update_layout(
            title='YoY Revenue Growth Comparison (Q1 2024)',
            yaxis_title='Growth (%)',
            xaxis_title='Airline',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Market Cap Comparison
        fig_mcap = go.Figure(data=[
            go.Bar(
                x=peer_data['Airline'],
                y=peer_data['Market Cap ($B)'],
                marker_color=['#0A2463', '#1E3A5F', '#3E5C76', '#6C8299'],
                text=peer_data['Market Cap ($B)'],
                textposition='auto',
            )
        ])
        fig_mcap.update_layout(
            title='Market Capitalization Comparison',
            yaxis_title='Market Cap ($B)',
            xaxis_title='Airline',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_mcap, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Operating Margin Chart
        fig_margin = go.Figure(data=[
            go.Bar(
                x=peer_data['Airline'],
                y=peer_data['Operating Margin (%)'],
                marker_color=['#FFA500', '#00B050', '#FF6B6B', '#FFD93D'],
                text=peer_data['Operating Margin (%)'],
                textposition='auto',
            )
        ])
        fig_margin.update_layout(
            title='Operating Margin Comparison (TTM)',
            yaxis_title='Operating Margin (%)',
            xaxis_title='Airline',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_margin, use_container_width=True)
    
    with col2:
        # P/E Ratio Chart
        fig_pe = go.Figure(data=[
            go.Scatter(
                x=peer_data['Airline'],
                y=peer_data['Forward P/E'],
                mode='markers+lines',
                marker=dict(size=15, color=['#3E92CC', '#6CA6CD', '#90CAF9', '#B3E5FC']),
                line=dict(color='#0A2463', width=2),
                text=peer_data['Forward P/E'],
                textposition='top center'
            )
        ])
        fig_pe.update_layout(
            title='Forward P/E Ratio Comparison',
            yaxis_title='Forward P/E',
            xaxis_title='Airline',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_pe, use_container_width=True)

with tab3:
    # Leverage Chart
    fig_leverage = go.Figure(data=[
        go.Bar(
            x=peer_data['Airline'],
            y=peer_data['Net Debt/EBITDA'],
            marker_color=['#FFA500', '#00B050', '#C00000', '#90EE90'],
            text=peer_data['Net Debt/EBITDA'],
            textposition='auto',
        )
    ])
    fig_leverage.update_layout(
        title='Net Debt/EBITDA Comparison',
        yaxis_title='Net Debt/EBITDA Ratio',
        xaxis_title='Airline',
        height=400,
        showlegend=False
    )
    fig_leverage.add_hline(y=2.5, line_dash="dash", line_color="red", 
                           annotation_text="Industry Threshold")
    st.plotly_chart(fig_leverage, use_container_width=True)
    
    st.info("💡 **Insight:** UAL's leverage (2.5x) is competitive with DAL but better than AAL. Continued deleveraging is a key focus.")

# Outlook Section
st.markdown('<div class="sub-header">🔮 3-6 Month Outlook</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🐂 Bull Case Drivers")
    bull_factors = [
        ("International Summer Demand", 85),
        ("Premium Cabin Growth", 75),
        ("Moderating Fuel Prices", 60),
        ("Ancillary Revenue Growth", 70),
        ("Business Travel Recovery", 65)
    ]
    
    for factor, probability in bull_factors:
        st.markdown(f"**{factor}**")
        st.progress(probability / 100)
        st.markdown(f"<small>Impact Probability: {probability}%</small>", unsafe_allow_html=True)
        st.markdown("")

with col2:
    st.markdown("#### 🐻 Bear Case Risks")
    bear_factors = [
        ("Fuel Price Surge", 55),
        ("Boeing Delivery Delays", 75),
        ("Demand Weakness", 40),
        ("Operational Disruptions", 50),
        ("Labor Cost Pressures", 65)
    ]
    
    for factor, probability in bear_factors:
        st.markdown(f"**{factor}**")
        st.progress(probability / 100)
        st.markdown(f"<small>Risk Probability: {probability}%</small>", unsafe_allow_html=True)
        st.markdown("")

# Strategic Positioning
st.markdown('<div class="sub-header">🎯 Strategic Positioning & Competitive Advantages</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### ✅ Strengths")
    st.markdown("""
    - **Global Hub Network**: Dominant international presence
    - **Premium Focus**: United Polaris & Premium Plus
    - **Star Alliance**: Largest global partnership
    - **United Next Plan**: Fleet modernization
    - **Strong Revenue Growth**: Leading peers at 9.7%
    """)

with col2:
    st.markdown("##### ⚠️ Challenges")
    st.markdown("""
    - **Boeing Dependency**: 737 MAX delays
    - **Labor Costs**: Post-pandemic agreements
    - **Operating Margin**: Gap vs Delta (4.8% vs 8.3%)
    - **Leverage**: Higher debt than Delta
    - **Operational Reliability**: Historical variability
    """)

with col3:
    st.markdown("##### 🎲 Key Risks")
    st.markdown("""
    - **Fuel Price Volatility**: Major cost exposure
    - **Economic Slowdown**: Demand sensitivity
    - **Geopolitical Events**: Route disruptions
    - **Regulatory Changes**: Compliance costs
    - **Fleet Constraints**: Capacity limitations
    """)

# Adjacent Industries Impact
st.markdown('<div class="sub-header">🔗 Adjacent Industry Analysis</div>', unsafe_allow_html=True)

industry_impact = pd.DataFrame({
    'Industry': ['Oil & Gas (Jet Fuel)', 'Aerospace Mfg (Boeing/Airbus)', 
                 'Leisure & Hospitality', 'Corporate Travel', 'Payments/Credit Cards'],
    'Impact': ['High Headwind', 'High Headwind', 'Strong Tailwind', 'Moderate Tailwind', 'Moderate Tailwind'],
    'Trend': ['↑ Rising Costs', '↓ Delivery Delays', '↑ Strong Demand', '↑ Gradual Recovery', '↑ Loyalty Growth'],
    'Priority': [95, 90, 85, 70, 65]
})

# Create horizontal bar chart for industry impact
fig_industry = go.Figure()

colors = ['#C00000', '#C00000', '#00B050', '#FFA500', '#FFA500']

fig_industry.add_trace(go.Bar(
    y=industry_impact['Industry'],
    x=industry_impact['Priority'],
    orientation='h',
    marker_color=colors,
    text=industry_impact['Trend'],
    textposition='auto',
))

fig_industry.update_layout(
    title='Adjacent Industry Impact Priority Matrix',
    xaxis_title='Impact Priority Score',
    yaxis_title='Industry Sector',
    height=400,
    showlegend=False
)

st.plotly_chart(fig_industry, use_container_width=True)

# Financial Projections
st.markdown('<div class="sub-header">📈 Projected Performance (Q2-Q3 2024)</div>', unsafe_allow_html=True)

quarters = ['Q1 2024\n(Actual)', 'Q2 2024\n(Projected)', 'Q3 2024\n(Projected)']
revenue = [12.4, 13.8, 14.2]
margin = [-1.0, 6.5, 7.8]

fig_projection = go.Figure()

fig_projection.add_trace(go.Bar(
    name='Revenue ($B)',
    x=quarters,
    y=revenue,
    yaxis='y',
    marker_color='#3E92CC',
    text=revenue,
    textposition='auto',
))

fig_projection.add_trace(go.Scatter(
    name='Operating Margin (%)',
    x=quarters,
    y=margin,
    yaxis='y2',
    mode='lines+markers',
    marker=dict(size=12, color='#FFA500'),
    line=dict(width=3, color='#FFA500'),
    text=margin,
    textposition='top center'
))

fig_projection.update_layout(
    title='Revenue & Operating Margin Projection',
    yaxis=dict(title='Revenue ($B)', side='left'),
    yaxis2=dict(title='Operating Margin (%)', side='right', overlaying='y'),
    height=450,
    hovermode='x unified',
    legend=dict(x=0.01, y=0.99)
)

st.plotly_chart(fig_projection, use_container_width=True)

# Investment Thesis Summary
st.markdown('<div class="sub-header">📋 Investment Thesis Summary</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Overall Rating: <span class='bullish'>MODERATELY BULLISH</span>
    
    **Key Investment Highlights:**
    
    1. **Strong Revenue Momentum**: UAL leads network carrier peers with 9.7% YoY revenue growth, 
       driven by robust international demand and premium cabin strength.
    
    2. **Summer Seasonality Tailwind**: Q2-Q3 2024 peak travel season expected to drive significant 
       sequential improvement in profitability and load factors.
    
    3. **Strategic Network Advantage**: Largest international network among U.S. carriers provides 
       competitive moat and access to high-yield routes.
    
    4. **Balanced Risk-Reward**: While Boeing delays and fuel costs present headwinds, disciplined 
       capacity management and strong forward bookings support positive outlook.
    
    **Target Price Justification:**
    - Forward P/E of 5.1x remains attractive vs. historical average
    - Expected EPS growth from seasonal strength and operational leverage
    - Valuation discount to Delta (6.0x) may compress as margins improve
    
    **Recommended Action**: ACCUMULATE on weakness; suitable for investors with moderate risk tolerance 
    seeking exposure to travel recovery with 3-6 month horizon.
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Rating Breakdown")
    
    # Rating gauge
    fig_rating = go.Figure(go.Indicator(
        mode="gauge+number",
        value=7.2,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Conviction Score", 'font': {'size': 20}},
        number={'suffix': "/10", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 1},
            'bar': {'color': "#3E92CC"},
            'steps': [
                {'range': [0, 4], 'color': "#FFE5E5"},
                {'range': [4, 7], 'color': "#FFF4E5"},
                {'range': [7, 10], 'color': "#E5F5E5"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 8}}))
    
    fig_rating.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_rating, use_container_width=True)
    
    st.markdown("#### Timeframe")
    st.info("**3-6 Months** (Q2-Q3 2024)")
    
    st.markdown("#### Risk Level")
    st.warning("**Moderate-High** (Operational & Cost Volatility)")

# Key Catalysts Timeline
st.markdown('<div class="sub-header">📅 Key Catalysts & Events</div>', unsafe_allow_html=True)

timeline_data = {
    'Event': [
        'Q2 2024 Earnings',
        'Summer Travel Peak',
        'Boeing 737 MAX Updates',
        'Labor Agreement Reviews',
        'Q3 2024 Earnings',
        'Fuel Price Trends'
    ],
    'Timing': [
        'July 2024',
        'June-August 2024',
        'Ongoing',
        'Q3 2024',
        'October 2024',
        'Continuous'
    ],
    'Impact': [
        'High - Guidance & Performance',
        'Very High - Revenue Driver',
        'High - Capacity Constraints',
        'Medium - Cost Implications',
        'High - Profitability Validation',
        'Very High - Margin Impact'
    ],
    'Sentiment': ['Positive', 'Positive', 'Negative', 'Neutral', 'Positive', 'Negative']
}

timeline_df = pd.DataFrame(timeline_data)

st.dataframe(
    timeline_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Event": st.column_config.TextColumn("Catalyst Event", width="medium"),
        "Timing": st.column_config.TextColumn("Expected Timing", width="small"),
        "Impact": st.column_config.TextColumn("Impact Assessment", width="large"),
        "Sentiment": st.column_config.TextColumn("Sentiment", width="small")
    }
)

# Comparative Advantage Matrix
st.markdown('<div class="sub-header">⚖️ Competitive Advantage Matrix</div>', unsafe_allow_html=True)

categories = ['International\nNetwork', 'Premium\nProduct', 'Operational\nReliability', 
              'Cost\nEfficiency', 'Balance\nSheet', 'Digital/Tech']
ual_scores = [9, 8, 6, 6, 6, 7]
dal_scores = [8, 9, 9, 8, 9, 8]
aal_scores = [7, 6, 5, 5, 4, 5]

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=ual_scores,
    theta=categories,
    fill='toself',
    name='United (UAL)',
    line_color='#3E92CC'
))

fig_radar.add_trace(go.Scatterpolar(
    r=dal_scores,
    theta=categories,
    fill='toself',
    name='Delta (DAL)',
    line_color='#00B050'
))

fig_radar.add_trace(go.Scatterpolar(
    r=aal_scores,
    theta=categories,
    fill='toself',
    name='American (AAL)',
    line_color='#C00000'
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 10])
    ),
    showlegend=True,
    height=500,
    title='Competitive Positioning Radar (Score out of 10)'
)

st.plotly_chart(fig_radar, use_container_width=True)

# Risk Matrix
st.markdown('<div class="sub-header">🎲 Risk-Return Matrix</div>', unsafe_allow_html=True)

risk_return = pd.DataFrame({
    'Factor': ['Summer Demand Upside', 'International Premium Growth', 'Fuel Stabilization', 
               'Ancillary Revenue', 'Boeing Delays', 'Fuel Price Spike', 
               'Demand Deterioration', 'Labor Disputes'],
    'Probability': [75, 70, 50, 65, 70, 50, 35, 30],
    'Impact': [8, 7, 9, 5, 8, 9, 9, 7],
    'Type': ['Opportunity', 'Opportunity', 'Opportunity', 'Opportunity', 
             'Risk', 'Risk', 'Risk', 'Risk']
})

fig_scatter = px.scatter(
    risk_return,
    x='Probability',
    y='Impact',
    size='Impact',
    color='Type',
    text='Factor',
    title='Risk-Return Assessment Matrix',
    labels={'Probability': 'Probability of Occurrence (%)', 
            'Impact': 'Financial Impact (1-10)'},
    color_discrete_map={'Opportunity': '#00B050', 'Risk': '#C00000'},
    height=500
)

fig_scatter.update_traces(textposition='top center')
fig_scatter.update_layout(showlegend=True)
fig_scatter.add_hline(y=7, line_dash="dash", line_color="gray", opacity=0.5)
fig_scatter.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)

st.plotly_chart(fig_scatter, use_container_width=True)

# Conclusion
st.markdown('<div class="sub-header">🎯 Final Verdict</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
    <h4>📈 Upside Potential</h4>
    <h2 class="bullish">+20-25%</h2>
    <p>Based on strong summer demand, international recovery, and potential fuel moderation</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
    <h4>📉 Downside Risk</h4>
    <h2 class="bearish">-15-20%</h2>
    <p>If fuel spikes, Boeing issues worsen, or demand deteriorates significantly</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
    <h4>⚖️ Risk-Reward</h4>
    <h2 class="bullish">FAVORABLE</h2>
    <p>Asymmetric upside from seasonal strength and strategic positioning</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
**Disclaimer:** This analysis is for informational purposes only and does not constitute investment advice. 
Past performance is not indicative of future results. Investors should conduct their own due diligence and 
consult with financial advisors before making investment decisions.

**Data Sources:** Company earnings reports (Q1 2024), analyst commentary, industry research, and public filings.

**Analysis Date:** May 2024 | **Next Review:** Post Q2 2024 Earnings (July 2024)
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>United Airlines Holdings, Inc. (UAL) - Equity Research Analysis Dashboard</strong></p>
    <p>Senior Equity Research Analyst Report | Airline Sector | Q2 2024</p>
</div>
""", unsafe_allow_html=True)