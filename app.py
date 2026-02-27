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
st.set_page_config(page_title="Zscaler (ZS) Financial Analysis", layout="wide", page_icon="📊")

# Title and header
st.title("📊 Zscaler (ZS) - Comprehensive Financial Analysis")
st.markdown("### Cloud Security & Zero Trust Network Access Leader")
st.markdown("---")

# Key Metrics Section
st.header("🎯 Key Financial Metrics (Q3 FY24)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Revenue", "$553.0M", "32% YoY", delta_color="normal")
with col2:
    st.metric("Calculated Billings", "$628.2M", "29% YoY", delta_color="normal")
with col3:
    st.metric("Non-GAAP Op. Margin", "20.3%", help="Strong profitability focus")
with col4:
    st.metric("Free Cash Flow", "$134.4M", "24% of revenue", delta_color="normal")

col5, col6, col7, col8 = st.columns(4)
with col5:
    st.metric("RPO", "$3.90B", "31% YoY", delta_color="normal")
with col6:
    st.metric("Market Cap", "~$27B", help="Approximate as of mid-2024")
with col7:
    st.metric("Forward P/E", "70-80x", help="Premium valuation")
with col8:
    st.metric("Revenue Growth", "32%", help="Latest quarter YoY")

st.markdown("---")

# Revenue Growth Trend
st.header("📈 Revenue & Growth Trajectory")
quarters = ['Q1 FY24', 'Q2 FY24', 'Q3 FY24', 'Q4 FY24E', 'Q1 FY25E']
revenue = [430, 490, 553, 610, 670]
yoy_growth = [35, 33, 32, 30, 29]

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Bar(x=quarters, y=revenue, name="Revenue ($M)", marker_color='#1f77b4'),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=quarters, y=yoy_growth, name="YoY Growth (%)", 
               marker_color='#ff7f0e', mode='lines+markers', line=dict(width=3)),
    secondary_y=True,
)
fig.update_xaxes(title_text="Quarter")
fig.update_yaxes(title_text="Revenue ($ Millions)", secondary_y=False)
fig.update_yaxes(title_text="YoY Growth (%)", secondary_y=True)
fig.update_layout(height=400, hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

# Peer Comparison
st.markdown("---")
st.header("🔍 Competitive Peer Benchmarking")

col1, col2 = st.columns(2)

with col1:
    # Market Cap and Growth Comparison
    peer_data = {
        'Company': ['Zscaler (ZS)', 'Palo Alto (PANW)', 'CrowdStrike (CRWD)', 'Fortinet (FTNT)'],
        'Market Cap ($B)': [27, 98, 90, 48],
        'YoY Revenue Growth (%)': [32, 15, 33, 6]
    }
    df_peers = pd.DataFrame(peer_data)
    
    fig = px.scatter(df_peers, x='Market Cap ($B)', y='YoY Revenue Growth (%)', 
                     text='Company', size='Market Cap ($B)',
                     color='YoY Revenue Growth (%)',
                     color_continuous_scale='Viridis',
                     title='Market Cap vs Revenue Growth')
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=2, color='white')))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # P/E Ratio Comparison
    pe_data = {
        'Company': ['Zscaler', 'Palo Alto', 'CrowdStrike', 'Fortinet'],
        'Forward P/E (Mid)': [75, 45, 75, 35],
        'Category': ['Premium', 'Moderate', 'Premium', 'Value']
    }
    df_pe = pd.DataFrame(pe_data)
    
    fig = px.bar(df_pe, x='Company', y='Forward P/E (Mid)', 
                 color='Category',
                 title='Forward P/E Ratio Comparison',
                 color_discrete_map={'Premium': '#e74c3c', 'Moderate': '#f39c12', 'Value': '#27ae60'})
    fig.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# Detailed Peer Table
st.subheader("Detailed Peer Comparison Table")
peer_detailed = {
    'Metric': ['Market Cap', 'Forward P/E', 'YoY Revenue Growth', 'Market Position'],
    'Zscaler (ZS)': ['~$27B', '70-80x', '32%', '🥇 Leader (SSE/ZTNA)'],
    'Palo Alto (PANW)': ['~$98B', '40-50x', '15%', '💪 Strong (Prisma)'],
    'CrowdStrike (CRWD)': ['~$90B', '70-80x', '33%', '🚀 Emerging (Cloud Sec)'],
    'Fortinet (FTNT)': ['~$48B', '30-40x', '6%', '⚙️ Mid-tier (FortiSASE)']
}
df_peer_detail = pd.DataFrame(peer_detailed)
st.dataframe(df_peer_detail, use_container_width=True, hide_index=True)

# Key Catalysts
st.markdown("---")
st.header("🚀 Key Catalysts & Growth Drivers")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🤖 AI Integration")
    st.markdown("""
    - AI-powered DLP
    - Generative AI security
    - Advanced threat detection
    - ZDX monitoring enhancement
    """)
    st.progress(0.85)
    st.caption("Impact Score: 85/100")

with col2:
    st.subheader("🏢 Enterprise Consolidation")
    st.markdown("""
    - SASE platform adoption
    - Cloud migration acceleration
    - Zero Trust architecture
    - Legacy vendor displacement
    """)
    st.progress(0.90)
    st.caption("Impact Score: 90/100")

with col3:
    st.subheader("💰 Macro Environment")
    st.markdown("""
    - IT budget normalization
    - Economic stabilization
    - Pent-up demand unlock
    - Non-discretionary security spend
    """)
    st.progress(0.70)
    st.caption("Impact Score: 70/100")

# Sentiment Analysis
st.markdown("---")
st.header("📊 Market Sentiment Analysis")

col1, col2 = st.columns(2)

with col1:
    sentiment_data = {
        'Factor': ['Strong Fundamentals', 'Platform Leadership', 'Large Deal Momentum', 
                   'Analyst Support', 'Billings Deceleration', 'Competition (PANW)', 
                   'Macro Headwinds', 'Valuation Premium'],
        'Sentiment': [90, 85, 80, 75, -60, -70, -55, -50],
        'Type': ['Bullish', 'Bullish', 'Bullish', 'Bullish', 
                 'Bearish', 'Bearish', 'Bearish', 'Bearish']
    }
    df_sentiment = pd.DataFrame(sentiment_data)
    
    fig = px.bar(df_sentiment, x='Sentiment', y='Factor', 
                 orientation='h',
                 color='Type',
                 title='Bullish vs Bearish Factors',
                 color_discrete_map={'Bullish': '#27ae60', 'Bearish': '#e74c3c'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Risk/Opportunity Matrix
    risk_opp = {
        'Factor': ['SASE Migration', 'Net Retention', 'New Modules', 'PANW Competition', 
                   'Macro Slowdown', 'Execution Risk', 'Security Incident'],
        'Impact': [9, 8, 7, 8, 7, 6, 9],
        'Probability': [8, 8, 7, 7, 6, 4, 2],
        'Type': ['Opportunity', 'Opportunity', 'Opportunity', 'Risk', 'Risk', 'Risk', 'Risk']
    }
    df_risk = pd.DataFrame(risk_opp)
    
    fig = px.scatter(df_risk, x='Probability', y='Impact', 
                     text='Factor', size='Impact',
                     color='Type',
                     title='Risk/Opportunity Matrix',
                     color_discrete_map={'Opportunity': '#3498db', 'Risk': '#e67e22'})
    fig.update_traces(textposition='top center', textfont_size=9)
    fig.update_layout(height=400, xaxis_range=[0, 10], yaxis_range=[0, 10])
    st.plotly_chart(fig, use_container_width=True)

# Adjacent Industries Impact
st.markdown("---")
st.header("🌐 Adjacent Industry Impact Analysis")

col1, col2 = st.columns(2)

with col1:
    adj_industries = {
        'Industry': ['Cloud Infrastructure', 'AI/ML Sector', 'Remote Work Tech', 
                     'Regulatory/Compliance', 'SD-WAN Market'],
        'Impact Score': [85, 75, 90, 80, 70],
        'Direction': ['Positive', 'Positive', 'Positive', 'Positive', 'Mixed']
    }
    df_adj = pd.DataFrame(adj_industries)
    
    fig = px.bar(df_adj, x='Industry', y='Impact Score', 
                 color='Direction',
                 title='Adjacent Industry Impact Scores',
                 color_discrete_map={'Positive': '#27ae60', 'Mixed': '#f39c12', 'Negative': '#e74c3c'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Industry Transmission Channels")
    st.markdown("""
    #### ☁️ Cloud Infrastructure (AWS, Azure, GCP)
    - **Impact**: Strong Positive Tailwind (85/100)
    - Cloud migration drives Zero Trust adoption
    - Co-selling and marketplace distribution
    
    #### 🤖 Enterprise IT Spending
    - **Impact**: Mixed (60/100)
    - Security remains top priority
    - Budget scrutiny lengthens sales cycles
    
    #### 🔐 Identity & Access Management
    - **Impact**: Positive with Competition (70/100)
    - IAM accelerates Zero Trust adoption
    - Potential encroachment risk
    """)

# Financial Projections
st.markdown("---")
st.header("📅 3-6 Month Outlook & Projections")

projection_data = {
    'Metric': ['Revenue Growth', 'Billings Growth', 'Operating Margin', 'Free Cash Flow Margin'],
    'Q3 FY24 Actual': ['32%', '29%', '20.3%', '24%'],
    'Q4 FY24 Estimate': ['28-30%', '27-30%', '20-21%', '24-25%'],
    'Q1 FY25 Estimate': ['27-29%', '26-29%', '21-22%', '25-26%']
}
df_projection = pd.DataFrame(projection_data)
st.dataframe(df_projection, use_container_width=True, hide_index=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🐂 Bull Case Scenario")
    st.success("""
    **Key Drivers:**
    - Economic improvement unlocks pent-up demand
    - Strong AI feature adoption drives upsell
    - Shortened sales cycles accelerate billings
    - Competitive wins against legacy vendors
    - Margin expansion from operational leverage
    
    **Expected Impact**: Revenue growth >32%, stock appreciation
    """)

with col2:
    st.subheader("🐻 Bear Case Scenario")
    st.error("""
    **Key Risks:**
    - Deeper economic slowdown tightens budgets
    - Elongated sales cycles beyond expectations
    - Aggressive competitor discounting (PANW)
    - Pressure on deal sizes and billings
    - Execution missteps or security incidents
    
    **Expected Impact**: Revenue growth <25%, valuation pressure
    """)

# Competitive Strengths/Weaknesses
st.markdown("---")
st.header("⚔️ Competitive Position Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Competitive Strengths")
    strengths = {
        'Strength': ['Pure-Cloud Architecture', 'Zero Trust Pioneer', 'Global Network Scale', 
                     'Platform Breadth', 'FedRAMP Authorization'],
        'Score': [95, 90, 88, 85, 92]
    }
    df_strengths = pd.DataFrame(strengths)
    fig = px.bar(df_strengths, x='Score', y='Strength', orientation='h',
                 color='Score', color_continuous_scale='Greens')
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⚠️ Competitive Challenges")
    weaknesses = {
        'Challenge': ['Limited EDR/Endpoint', 'No Network Hardware', 'Premium Pricing', 
                      'PANW Bundling Threat', 'Microsoft Integration'],
        'Risk Level': [65, 60, 70, 85, 75]
    }
    df_weaknesses = pd.DataFrame(weaknesses)
    fig = px.bar(df_weaknesses, x='Risk Level', y='Challenge', orientation='h',
                 color='Risk Level', color_continuous_scale='Reds')
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Summary Dashboard
st.markdown("---")
st.header("📋 Executive Summary & Investment Thesis")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Overall Rating", "BUY", help="Cautiously Optimistic")
    st.metric("Growth Trajectory", "Strong", help="High 20s to low 30s % YoY")
    st.metric("Competitive Moat", "Robust", help="Leader in SSE/ZTNA")

with col2:
    st.metric("Valuation", "Premium", help="70-80x forward P/E")
    st.metric("Risk Level", "Moderate", help="Competitive & macro pressures")
    st.metric("Time Horizon", "3-6 Months", help="Near-term outlook")

with col3:
    st.metric("Primary Catalyst", "AI Integration", help="Key growth driver")
    st.metric("Primary Risk", "PANW Competition", help="Main threat")
    st.metric("Margin Trend", "Expanding", help="Improving profitability")

st.markdown("---")
st.subheader("🎯 Key Takeaways")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### Positive Factors
    - ✅ **32% revenue growth** with strong fundamentals
    - ✅ **Leader in Zero Trust/SASE** market segment
    - ✅ **Expanding margins** show operational leverage
    - ✅ **$3.90B RPO** provides revenue visibility
    - ✅ **Secular tailwinds** from cloud migration
    - ✅ **AI integration** drives product innovation
    """)

with col2:
    st.markdown("""
    #### Watch Points
    - ⚠️ **Billings deceleration** needs monitoring
    - ⚠️ **PANW competitive threat** intensifying
    - ⚠️ **Premium valuation** sensitive to misses
    - ⚠️ **Macro headwinds** affecting enterprise IT
    - ⚠️ **Sales cycle elongation** risk
    - ⚠️ **Execution critical** for maintaining growth
    """)

# Investment Considerations
st.markdown("---")
st.info("""
**📌 Investment Consideration**

Zscaler represents a **high-conviction long-term play** on the secular shift to cloud-native security and Zero Trust architectures. 
The company's pure-cloud platform, market leadership, and strong financial execution position it well for sustained growth.

**Near-term (3-6 months)**: Expect continued solid performance with revenue growth in the high 20s to low 30s percent range. 
Key catalysts include AI feature adoption, enterprise consolidation wins, and potential macro improvement.

**Primary risk**: Intensifying competition from Palo Alto Networks through aggressive bundling and pricing, combined with macro-driven 
budget scrutiny that could elongate sales cycles.

**Verdict**: Suitable for growth-oriented investors with moderate risk tolerance. Monitor quarterly billings, large deal traction, 
and competitive dynamics closely.

⚠️ *This analysis is for informational purposes only and does not constitute investment advice.*
""")

# Footer
st.markdown("---")
st.caption("Data sources: Company filings (Q3 FY24), analyst reports, market research. Last updated: Mid-2024")
st.caption("Analysis generated from comprehensive equity research reports on Zscaler (ZS)")