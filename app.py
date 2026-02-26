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
from datetime import datetime

# Page configuration
st.set_page_config(page_title="MSFT Financial Analysis", layout="wide", page_icon="📊")

# Custom CSS
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; font-weight: bold; color: #0078D4; margin-bottom: 0;}
    .sub-header {font-size: 1.5rem; font-weight: bold; color: #106EBE; margin-top: 2rem;}
    .metric-card {background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #0078D4;}
    .bull-case {background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;}
    .bear-case {background-color: #f8d7da; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #dc3545;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">📊 Microsoft (MSFT) Financial Analysis</p>', unsafe_allow_html=True)
st.markdown("**Senior Equity Research Analysis | 3-6 Month Outlook**")
st.markdown(f"*Analysis Date: {datetime.now().strftime('%B %Y')}*")

# Key Metrics Section
st.markdown('<p class="sub-header">Key Investment Metrics</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Recommendation", "OUTPERFORM", help="Analyst Rating")
with col2:
    st.metric("Price Target", "$500", delta="12-month", help="Target Price")
with col3:
    st.metric("Forward P/E", "~32x", help="Forward Price-to-Earnings Ratio")
with col4:
    st.metric("Revenue Growth", "+17% YoY", help="Year-over-Year Growth")

# Recent Performance Data
st.markdown('<p class="sub-header">Recent Financial Performance (FQ3 2024)</p>', unsafe_allow_html=True)

performance_data = {
    'Metric': ['Revenue', 'Intelligent Cloud', 'Productivity & Business', 'Personal Computing', 'Operating Income', 'EPS'],
    'Value': ['$61.9B', '$26.7B', '$19.6B', '$15.6B', '$27.6B', '$2.94'],
    'YoY Growth': [17, 21, 12, 17, 20, 20]
}
df_performance = pd.DataFrame(performance_data)

col1, col2 = st.columns([2, 1])
with col1:
    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Bar(
        x=df_performance['Metric'],
        y=df_performance['YoY Growth'],
        text=[f"+{val}%" for val in df_performance['YoY Growth']],
        textposition='outside',
        marker=dict(color=['#0078D4', '#50E6FF', '#00BCF2', '#008272', '#107C10', '#FFB900'])
    ))
    fig_revenue.update_layout(
        title='Year-over-Year Growth by Segment (%)',
        xaxis_title='',
        yaxis_title='Growth %',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    st.markdown("### 💼 Key Figures")
    for _, row in df_performance.iterrows():
        st.markdown(f"**{row['Metric']}**")
        st.markdown(f"{row['Value']} ({row['YoY Growth']:+d}% YoY)")
        st.markdown("---")

# Segment Revenue Breakdown
st.markdown('<p class="sub-header">Revenue Breakdown by Segment</p>', unsafe_allow_html=True)

segment_data = {
    'Segment': ['Intelligent Cloud', 'Productivity & Business', 'Personal Computing'],
    'Revenue': [26.7, 19.6, 15.6],
    'Growth': [21, 12, 17]
}
df_segments = pd.DataFrame(segment_data)

col1, col2 = st.columns(2)
with col1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=df_segments['Segment'],
        values=df_segments['Revenue'],
        hole=0.4,
        marker_colors=['#0078D4', '#50E6FF', '#008272']
    )])
    fig_pie.update_layout(
        title='Revenue Distribution (FQ3 2024)',
        height=400
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(
        x=df_segments['Segment'],
        y=df_segments['Growth'],
        mode='lines+markers+text',
        text=[f"+{val}%" for val in df_segments['Growth']],
        textposition='top center',
        marker=dict(size=15, color='#0078D4'),
        line=dict(width=3, color='#0078D4')
    ))
    fig_growth.update_layout(
        title='YoY Growth Rate by Segment',
        xaxis_title='',
        yaxis_title='Growth %',
        height=400,
        yaxis=dict(range=[0, 25])
    )
    st.plotly_chart(fig_growth, use_container_width=True)

# Peer Comparison
st.markdown('<p class="sub-header">Competitive Benchmarking</p>', unsafe_allow_html=True)

peer_data = {
    'Company': ['Microsoft', 'Amazon', 'Alphabet', 'Salesforce'],
    'Forward P/E': [32, 38, 27, 35],
    'YoY Revenue Growth': [17, 13, 15, 11],
    'Cloud Market Share': [24, 31, 11, 0]
}
df_peers = pd.DataFrame(peer_data)

col1, col2 = st.columns(2)
with col1:
    fig_pe = go.Figure()
    fig_pe.add_trace(go.Bar(
        x=df_peers['Company'],
        y=df_peers['Forward P/E'],
        text=df_peers['Forward P/E'].apply(lambda x: f"{x}x"),
        textposition='outside',
        marker=dict(color=['#0078D4', '#FF9900', '#4285F4', '#00A1E0'])
    ))
    fig_pe.update_layout(
        title='Forward P/E Ratio Comparison',
        xaxis_title='',
        yaxis_title='P/E Ratio',
        height=400
    )
    st.plotly_chart(fig_pe, use_container_width=True)

with col2:
    fig_growth_peer = go.Figure()
    fig_growth_peer.add_trace(go.Bar(
        x=df_peers['Company'],
        y=df_peers['YoY Revenue Growth'],
        text=df_peers['YoY Revenue Growth'].apply(lambda x: f"+{x}%"),
        textposition='outside',
        marker=dict(color=['#0078D4', '#FF9900', '#4285F4', '#00A1E0'])
    ))
    fig_growth_peer.update_layout(
        title='YoY Revenue Growth Comparison',
        xaxis_title='',
        yaxis_title='Growth %',
        height=400
    )
    st.plotly_chart(fig_growth_peer, use_container_width=True)

# Cloud Market Share
st.markdown("### ☁️ Cloud Infrastructure Market Share (Q4 2023)")
cloud_share = df_peers[df_peers['Cloud Market Share'] > 0]
fig_cloud = go.Figure(data=[go.Bar(
    x=cloud_share['Company'],
    y=cloud_share['Cloud Market Share'],
    text=cloud_share['Cloud Market Share'].apply(lambda x: f"{x}%"),
    textposition='outside',
    marker=dict(color=['#0078D4', '#FF9900', '#4285F4'])
)])
fig_cloud.update_layout(
    title='',
    xaxis_title='',
    yaxis_title='Market Share %',
    height=350
)
st.plotly_chart(fig_cloud, use_container_width=True)

# Key Catalysts
st.markdown('<p class="sub-header">📈 Key Growth Catalysts (3-6 Months)</p>', unsafe_allow_html=True)

catalyst_data = {
    'Catalyst': ['AI Monetization', 'Azure Growth', 'Gaming (ABK)', 'Copilot Adoption', 'Enterprise Cloud Migration'],
    'Impact Score': [95, 85, 70, 90, 80],
    'Timeframe': ['Immediate', 'Ongoing', 'Q4 2024', 'Ramping', 'Ongoing']
}
df_catalysts = pd.DataFrame(catalyst_data)

fig_catalysts = go.Figure()
fig_catalysts.add_trace(go.Bar(
    y=df_catalysts['Catalyst'],
    x=df_catalysts['Impact Score'],
    orientation='h',
    text=df_catalysts['Timeframe'],
    textposition='inside',
    marker=dict(color=['#107C10', '#0078D4', '#8764B8', '#FFB900', '#00BCF2'])
))
fig_catalysts.update_layout(
    title='Catalyst Impact Score (0-100)',
    xaxis_title='Impact Score',
    yaxis_title='',
    height=400
)
st.plotly_chart(fig_catalysts, use_container_width=True)

# Bull vs Bear Case
st.markdown('<p class="sub-header">🎯 Scenario Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="bull-case">', unsafe_allow_html=True)
    st.markdown("### 🐂 Bull Case")
    st.markdown("""
    - **Accelerated AI Adoption**: Faster-than-expected Copilot uptake driving ARPU expansion
    - **Robust Enterprise Spending**: Strong corporate IT budgets fueling Azure consumption
    - **Gaming Synergies**: ABK integration exceeds expectations with Game Pass growth
    - **Margin Expansion**: Operating leverage from AI scaling and cost efficiency
    - **Market Share Gains**: Azure continues taking share from AWS in AI workloads
    """)
    st.metric("Bull Case Target", "$550+", help="Upside scenario")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="bear-case">', unsafe_allow_html=True)
    st.markdown("### 🐻 Bear Case")
    st.markdown("""
    - **Slower AI Monetization**: Enterprises hesitant on Copilot ROI and pricing
    - **Macro Headwinds**: Economic slowdown leads to IT budget cuts and cloud optimization
    - **Intense Competition**: Price wars with AWS/GCP pressure margins
    - **Integration Challenges**: ABK synergies take longer than expected
    - **Regulatory Risk**: Antitrust scrutiny impacts AI strategy and OpenAI partnership
    """)
    st.metric("Bear Case Target", "$380-400", help="Downside scenario")
    st.markdown('</div>', unsafe_allow_html=True)

# Risk Assessment
st.markdown('<p class="sub-header">⚠️ Risk Assessment Matrix</p>', unsafe_allow_html=True)

risk_data = {
    'Risk Factor': ['Macro Economic Slowdown', 'AI Monetization Execution', 'Competitive Pricing Pressure', 
                    'Regulatory/Antitrust', 'GPU Supply Constraints', 'Cybersecurity Incidents'],
    'Probability': [60, 40, 55, 45, 30, 35],
    'Impact': [80, 90, 65, 70, 60, 75]
}
df_risks = pd.DataFrame(risk_data)
df_risks['Risk Score'] = (df_risks['Probability'] * df_risks['Impact']) / 100

fig_risk = go.Figure()
fig_risk.add_trace(go.Scatter(
    x=df_risks['Probability'],
    y=df_risks['Impact'],
    mode='markers+text',
    text=df_risks['Risk Factor'],
    textposition='top center',
    marker=dict(
        size=df_risks['Risk Score'],
        color=df_risks['Risk Score'],
        colorscale='Reds',
        showscale=True,
        colorbar=dict(title="Risk Score"),
        sizemode='diameter',
        sizeref=2
    )
))
fig_risk.update_layout(
    title='Risk Probability vs Impact Matrix',
    xaxis_title='Probability (%)',
    yaxis_title='Impact Severity (%)',
    height=500,
    xaxis=dict(range=[0, 100]),
    yaxis=dict(range=[0, 100])
)
st.plotly_chart(fig_risk, use_container_width=True)

# Adjacent Industry Impact
st.markdown('<p class="sub-header">🔗 Adjacent Industry Analysis</p>', unsafe_allow_html=True)

industry_data = {
    'Industry': ['Semiconductors (GPU)', 'Enterprise IT Spending', 'Cybersecurity', 
                 'Gaming & Consumer', 'Cloud Infrastructure', 'Regulatory/Policy'],
    'Impact': ['Tailwind', 'Tailwind', 'Tailwind', 'Mixed', 'Tailwind', 'Headwind'],
    'Strength': [85, 80, 75, 50, 90, -40]
}
df_industry = pd.DataFrame(industry_data)

colors = ['#107C10' if x > 0 else '#D13438' for x in df_industry['Strength']]
fig_industry = go.Figure()
fig_industry.add_trace(go.Bar(
    y=df_industry['Industry'],
    x=df_industry['Strength'],
    orientation='h',
    text=df_industry['Impact'],
    textposition='inside',
    marker_color=colors
))
fig_industry.update_layout(
    title='Adjacent Industry Impact Score (-100 to +100)',
    xaxis_title='Impact Score',
    yaxis_title='',
    height=400,
    xaxis=dict(range=[-50, 100])
)
st.plotly_chart(fig_industry, use_container_width=True)

# SWOT Analysis
st.markdown('<p class="sub-header">📊 SWOT Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ Strengths")
    st.markdown("""
    - **Enterprise Ecosystem Dominance**: Unmatched installed base with Office 365, Windows, Azure AD
    - **Full-Stack AI Integration**: End-to-end control from infrastructure to applications
    - **OpenAI Partnership**: First-mover advantage in generative AI
    - **Diversified Revenue**: Resilient across cloud, productivity, gaming, and LinkedIn
    - **Strong Cash Flow**: AAA credit rating, robust free cash flow generation
    """)
    
    st.markdown("### 🎯 Opportunities")
    st.markdown("""
    - **AI-Priced Tiers**: Converting enterprise users to premium Copilot subscriptions
    - **Cybersecurity Growth**: $20B+ business growing 30%+ annually
    - **Gaming Expansion**: 3rd largest gaming company post-ABK acquisition
    - **Edge Computing**: 5G partnerships expanding Azure footprint
    - **Vertical Solutions**: Industry-specific cloud and AI offerings
    """)

with col2:
    st.markdown("### ⚠️ Weaknesses")
    st.markdown("""
    - **Consumer Hardware Lag**: Surface and Xbox face tough competition from Apple/Sony
    - **Search Market Share**: Google maintains dominance despite AI-powered Bing
    - **Complex Product Portfolio**: Integration challenges across diverse offerings
    - **Premium Valuation**: Limited margin of safety at current P/E levels
    """)
    
    st.markdown("### 🚨 Threats")
    st.markdown("""
    - **Cloud Competition**: Google Cloud's aggressive growth and AWS's market leadership
    - **Open-Source AI**: Powerful alternatives reducing OpenAI partnership differentiation
    - **Regulatory Scrutiny**: Antitrust concerns in US, EU regarding AI and market dominance
    - **Cyclical IT Spending**: Economic downturns impact enterprise cloud migrations
    - **Energy Costs**: Massive data center footprint exposed to energy price volatility
    """)

# Investment Thesis
st.markdown('<p class="sub-header">💡 Investment Thesis Summary</p>', unsafe_allow_html=True)

st.markdown("""
<div class="metric-card">

### Core Thesis: **Best-Positioned AI Beneficiary with Durable Enterprise Moat**

Microsoft represents the **highest-conviction play on enterprise AI adoption** with multiple structural advantages:

1. **Unmatched Distribution**: 400M+ Office 365 commercial users provide unprecedented distribution for Copilot
2. **Azure AI Leadership**: 31% YoY cloud growth with 6-7 points from AI services; winning enterprise AI workloads
3. **Margin Expansion Path**: AI monetization (Copilot at $30/user/month) can drive significant ARPU uplift
4. **Diversification**: Unlike pure-play cloud competitors, MSFT has stable productivity and gaming revenue cushion
5. **Execution Track Record**: Consistent delivery on cloud and AI promises validates management credibility

### Key Monitorables (Next 3-6 Months):
- **Azure AI Growth**: Must maintain 30%+ growth with increasing AI contribution
- **Copilot Adoption Metrics**: Enterprise uptake rates and retention data
- **Margin Trajectory**: Operating leverage demonstration despite heavy AI capex
- **Competitive Dynamics**: AWS and Google Cloud pricing and product responses
- **Macro Indicators**: Enterprise IT spending sentiment and budget allocation

### Valuation Consideration:
At ~32x forward P/E, MSFT trades at a premium to historical averages and the S&P 500. The premium is **justified if**:
- AI monetization meets aggressive targets (Copilot adds $10B+ ARR by FY25)
- Azure maintains premium growth while expanding margins
- Gaming integration delivers promised synergies

The premium is **at risk if**:
- AI adoption slows or price resistance emerges
- Macro deterioration triggers enterprise spending cuts
- Regulatory action materially constrains OpenAI partnership

</div>
""", unsafe_allow_html=True)

# Outlook Timeline
st.markdown('<p class="sub-header">📅 3-6 Month Outlook Timeline</p>', unsafe_allow_html=True)

timeline_data = {
    'Month': ['Month 1-2', 'Month 2-3', 'Month 3-4', 'Month 4-5', 'Month 5-6'],
    'Key Events': [
        'FQ4 2024 Earnings | Azure growth data | Initial Copilot metrics',
        'Ignite Conference | New AI product announcements | Enterprise feedback',
        'Holiday Gaming Performance | ABK integration updates',
        'FY2025 Guidance | Capex outlook | AI infrastructure investments',
        'Q1 FY2025 Results | Copilot adoption trajectory | Competitive responses'
    ],
    'Importance': [95, 80, 65, 90, 85]
}
df_timeline = pd.DataFrame(timeline_data)

fig_timeline = go.Figure()
fig_timeline.add_trace(go.Scatter(
    x=df_timeline['Month'],
    y=df_timeline['Importance'],
    mode='lines+markers+text',
    text=df_timeline['Importance'],
    textposition='top center',
    marker=dict(size=15, color='#0078D4'),
    line=dict(width=4, color='#0078D4'),
    fill='tozeroy',
    fillcolor='rgba(0, 120, 212, 0.2)'
))
fig_timeline.update_layout(
    title='Event Importance Score (Next 6 Months)',
    xaxis_title='Timeline',
    yaxis_title='Strategic Importance',
    height=300,
    yaxis=dict(range=[0, 100])
)
st.plotly_chart(fig_timeline, use_container_width=True)

for _, row in df_timeline.iterrows():
    with st.expander(f"**{row['Month']}** - Importance: {row['Importance']}/100"):
        st.markdown(row['Key Events'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>Disclaimer:</strong> This analysis is for informational purposes only and does not constitute investment advice. 
    Past performance does not guarantee future results. Consult with a qualified financial advisor before making investment decisions.</p>
    <p><em>Analysis based on publicly available information as of Q3 FY2024 (ended March 31, 2024)</em></p>
</div>
""", unsafe_allow_html=True)