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

ticker = st.text_input("Enter stock ticker", value="NVDA").upper().strip()
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
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(page_title="Microsoft (MSFT) Financial Analysis", layout="wide", page_icon="📊")

st.title("📊 Microsoft (MSFT) - Forward-Looking Financial Analysis")
st.markdown("### Senior Equity Research Report | Q3 FY24")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Executive Summary", 
    "💰 Financial Performance", 
    "🔍 Competitive Analysis",
    "⚡ Industry Dynamics",
    "⚠️ Risk Assessment"
])

with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Outlook", "HIGHLY POSITIVE", "Strong Conviction")
        st.metric("Target Horizon", "3-6 Months")
    
    with col2:
        st.metric("Q3 FY24 Revenue", "$61.9B", "+17% YoY")
        st.metric("Q3 FY24 EPS", "$2.94", "+20% YoY")
    
    with col3:
        st.metric("Gross Margin", "70%")
        st.metric("Operating Margin", "43%")
    
    st.markdown("---")
    
    st.subheader("🎯 Investment Thesis")
    st.info("""
    **Microsoft is strategically positioned at the epicenter of secular growth trends in cloud computing and artificial intelligence.**
    
    The company leverages its ubiquitous enterprise footprint and substantial R&D investments to maintain competitive advantages
    across multiple high-growth segments.
    """)
    
    st.subheader("🔑 Key Investment Catalysts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🤖 AI Monetization")
        st.markdown("""
        - **Microsoft Copilot** rollout across M365, Dynamics 365, Power Platform
        - Azure AI services driving ARPU expansion
        - Enterprise adoption of generative AI accelerating
        """)
    
    with col2:
        st.markdown("#### ☁️ Cloud Migration")
        st.markdown("""
        - Azure's hybrid cloud capabilities
        - Expanding AI infrastructure capacity
        - Large-scale enterprise migrations
        """)
    
    with col3:
        st.markdown("#### 🎮 Gaming Synergies")
        st.markdown("""
        - Activision Blizzard integration
        - Game Pass subscriber growth
        - Enhanced content sales potential
        """)

with tab2:
    st.header("Financial Performance Deep Dive")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Q3 FY24 Segment Performance")
        
        segment_data = pd.DataFrame({
            'Segment': ['Intelligent Cloud', 'Productivity & Business', 'More Personal Computing'],
            'Revenue ($B)': [26.7, 19.6, 15.6],
            'YoY Growth (%)': [21, 12, 17]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=segment_data['Segment'],
            y=segment_data['Revenue ($B)'],
            text=segment_data['Revenue ($B)'],
            texttemplate='$%{text:.1f}B',
            textposition='outside',
            marker_color=['#0078D4', '#50E6FF', '#00BCF2'],
            name='Revenue'
        ))
        
        fig.update_layout(
            title="Revenue by Segment (Q3 FY24)",
            yaxis_title="Revenue (Billions USD)",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("YoY Growth Rates")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=segment_data['Segment'],
            y=segment_data['YoY Growth (%)'],
            text=segment_data['YoY Growth (%)'],
            texttemplate='%{text}%',
            textposition='outside',
            marker_color=['#107C10', '#00CC6A', '#10893E'],
            name='Growth'
        ))
        
        fig.update_layout(
            title="Year-over-Year Growth by Segment",
            yaxis_title="Growth (%)",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📊 Projected Performance Trajectory (Next 3-6 Months)")
    
    projection_data = {
        'Metric': [
            'Revenue Growth',
            'Azure Growth',
            'Operating Margin',
            'AI Revenue Contribution'
        ],
        'Current': [17, 31, 43, 'Emerging'],
        'Q4 FY24 Projection': ['Mid-High Teens', '30%+', '42-44%', 'Accelerating'],
        'Q1 FY25 Projection': ['Mid Teens', '28-32%', '43-45%', 'Substantial']
    }
    
    proj_df = pd.DataFrame(projection_data)
    st.dataframe(proj_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Key Segment Drivers")
        st.markdown("""
        **Intelligent Cloud:**
        - Azure 31% YoY growth (30% constant currency)
        - AI workload acceleration
        - Enterprise digital transformation
        
        **Productivity & Business:**
        - Office 365 Commercial +15%
        - LinkedIn +10%
        - Copilot monetization beginning
        
        **More Personal Computing:**
        - Windows OEM +11%
        - Xbox content & services +62%
        - Activision Blizzard contribution
        """)
    
    with col2:
        st.subheader("📈 Margin Profile")
        
        margin_data = pd.DataFrame({
            'Metric': ['Gross Margin', 'Operating Margin', 'Net Margin'],
            'Percentage': [70, 43, 36]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=70,
            title={'text': "Gross Margin"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#0078D4"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 65
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Competitive Benchmarking Analysis")
    
    peer_data = pd.DataFrame({
        'Company': ['Microsoft', 'Amazon', 'Alphabet', 'Salesforce'],
        'Ticker': ['MSFT', 'AMZN', 'GOOGL', 'CRM'],
        'P/E Ratio': [38.0, 55.0, 28.0, 70.0],
        'YoY Revenue Growth': [17, 13, 15, 11],
        'Cloud Market Share': [24, 31, 11, np.nan],
        'Primary Strength': [
            'Diversified ecosystem',
            'IaaS leadership',
            'AI research depth',
            'CRM dominance'
        ]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("P/E Ratio Comparison")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=peer_data['Company'],
            y=peer_data['P/E Ratio'],
            text=peer_data['P/E Ratio'],
            texttemplate='%{text:.1f}x',
            textposition='outside',
            marker_color=['#0078D4', '#FF9900', '#4285F4', '#00A1E0']
        ))
        
        fig.update_layout(
            yaxis_title="P/E Ratio",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Growth Comparison")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=peer_data['Company'],
            y=peer_data['YoY Revenue Growth'],
            text=peer_data['YoY Revenue Growth'],
            texttemplate='%{text}%',
            textposition='outside',
            marker_color=['#107C10', '#FF9900', '#4285F4', '#00A1E0']
        ))
        
        fig.update_layout(
            yaxis_title="YoY Growth (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("☁️ Cloud Market Share Distribution")
    
    cloud_share = pd.DataFrame({
        'Provider': ['AWS', 'Azure', 'Google Cloud', 'Others'],
        'Market Share': [31, 24, 11, 34]
    })
    
    fig = go.Figure(data=[go.Pie(
        labels=cloud_share['Provider'],
        values=cloud_share['Market Share'],
        hole=.4,
        marker_colors=['#FF9900', '#0078D4', '#4285F4', '#CCCCCC']
    )])
    
    fig.update_layout(
        title="Global Cloud Infrastructure Market Share (Q1 2024)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🎯 Competitive Positioning Matrix")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Microsoft's Competitive Advantages")
        st.success("""
        ✅ **Diversified Revenue Streams** - Cloud, Software, Gaming, LinkedIn  
        ✅ **Enterprise Moat** - Deep integration with Windows, Office, Active Directory  
        ✅ **AI First-Mover** - OpenAI partnership and Copilot integration  
        ✅ **Hybrid Cloud Leader** - Azure Arc appeals to regulated enterprises  
        ✅ **Strong Balance Sheet** - Enables aggressive R&D and M&A
        """)
    
    with col2:
        st.markdown("#### Relative Weaknesses")
        st.warning("""
        ⚠️ **Consumer Cloud** - Lags Google in search and consumer services  
        ⚠️ **Pure IaaS Pricing** - AWS maintains cost leadership in raw compute  
        ⚠️ **Mobile Ecosystem** - Minimal presence vs. Android/iOS  
        ⚠️ **GPU Dependency** - Relies on NVIDIA for AI infrastructure  
        ⚠️ **Regulatory Scrutiny** - Size invites antitrust attention
        """)
    
    st.markdown("---")
    
    st.subheader("📊 Detailed Peer Analysis")
    st.dataframe(peer_data, use_container_width=True, hide_index=True)
    
    st.info("""
    **Key Insight:** Microsoft's P/E of 38x sits between Google's 28x and Amazon's 55x, reflecting its balanced 
    risk/reward profile. The premium over Google is justified by superior revenue diversification and enterprise 
    ecosystem lock-in. The discount to Amazon reflects slightly lower pure cloud market share, though Azure's 
    growth rate is accelerating faster.
    """)

with tab4:
    st.header("Adjacent Industry Impact Analysis")
    
    st.subheader("🔗 Key Industry Transmission Channels")
    
    industry_impact = pd.DataFrame({
        'Industry': [
            'Semiconductors (GPUs)',
            'Enterprise IT Consulting',
            'Cybersecurity',
            'Energy & Utilities',
            'Telecommunications'
        ],
        'Impact Level': ['Critical', 'High', 'High', 'Medium', 'Medium'],
        'Sentiment': ['Positive', 'Positive', 'Positive', 'Mixed', 'Positive'],
        'Transmission Mechanism': [
            'AI capacity constraints & costs',
            'Cloud migration acceleration',
            'Security spending increase',
            'Data center power requirements',
            'Edge computing demand'
        ]
    })
    
    st.dataframe(industry_impact, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Upstream: Semiconductor Industry")
        
        st.markdown("##### Tailwinds")
        st.success("""
        - **AI Gold Rush**: Unprecedented demand for NVIDIA GPUs directly fuels Azure AI expansion
        - **Data Center CPU Strength**: Strong demand for Intel/AMD server processors supports general cloud growth
        - **Strategic Partnerships**: Microsoft's scale ensures priority access to cutting-edge silicon
        """)
        
        st.markdown("##### Headwinds")
        st.error("""
        - **Supply Constraints**: GPU shortages could bottleneck Azure AI service rollout
        - **Cost Inflation**: Premium pricing for AI accelerators pressures infrastructure margins
        - **HBM Shortages**: High-bandwidth memory constraints limit data center build-out speed
        """)
    
    with col2:
        st.subheader("📊 Downstream: Enterprise IT Spending")
        
        st.markdown("##### Tailwinds")
        st.success("""
        - **Digital Transformation Priority**: Corporate boards allocating increased budgets for AI/cloud
        - **Consulting Pipeline Strength**: Accenture, Deloitte report robust demand for Microsoft implementations
        - **Efficiency Mandate**: AI productivity gains (Copilot) justify sustained software spend
        """)
        
        st.markdown("##### Headwinds")
        st.error("""
        - **Macro Uncertainty**: Economic slowdown could trigger IT budget cuts
        - **Implementation Complexity**: Slower-than-expected Copilot rollouts due to change management
        - **ROI Scrutiny**: Enterprises demanding clearer AI ROI before scaling deployments
        """)
    
    st.markdown("---")
    
    st.subheader("⚡ Industry Sentiment Dashboard")
    
    sentiment_data = pd.DataFrame({
        'Industry': ['Semiconductors', 'Enterprise IT', 'Cybersecurity', 'Energy', 'Telecom'],
        'Sentiment Score': [85, 75, 80, 60, 70]
    })
    
    fig = go.Figure()
    
    colors = ['#107C10' if x >= 70 else '#FFB900' if x >= 50 else '#D83B01' 
              for x in sentiment_data['Sentiment Score']]
    
    fig.add_trace(go.Bar(
        x=sentiment_data['Industry'],
        y=sentiment_data['Sentiment Score'],
        text=sentiment_data['Sentiment Score'],
        texttemplate='%{text}',
        textposition='outside',
        marker_color=colors
    ))
    
    fig.update_layout(
        title="Adjacent Industry Sentiment (0-100 Scale)",
        yaxis_title="Sentiment Score",
        yaxis_range=[0, 100],
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **Interpretation:** Green bars (≥70) indicate strong positive tailwinds. Yellow (50-69) suggests mixed signals. 
    Red (<50) would indicate material headwinds. Current environment is broadly supportive of Microsoft's strategy.
    """)

with tab5:
    st.header("Risk Assessment & Scenario Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🐻 Bear Case Scenario")
        st.error("""
        ### Quarterly Downside Risks (Q4 FY24 / Q1 FY25)
        
        **Primary Threats:**
        
        1. **AI Monetization Miss**
           - Copilot adoption slower than expected
           - Implementation complexity delays
           - Weak ROI perception slows enterprise rollouts
           - *Impact:* Revenue miss of 2-3%, margin compression
        
        2. **Intensified Cloud Competition**
           - AWS/Google aggressive pricing wars
           - Market share losses in IaaS
           - *Impact:* Azure growth decelerates to low-20s%
        
        3. **Macro Deterioration**
           - Broad enterprise IT budget cuts
           - LinkedIn advertising weakness
           - SMB segment contraction
           - *Impact:* 10-15% stock correction possible
        
        4. **Regulatory Actions**
           - Antitrust fines or operational restrictions
           - OpenAI partnership scrutiny
           - Data localization requirements
           - *Impact:* Compliance costs, strategic limitations
        
        5. **Execution Failures**
           - Activision integration stumbles
           - Security breach damages reputation
           - Product launch delays
        """)
        
        st.metric("Bear Case Price Target", "$350-$375", "-12% to -16%")
    
    with col2:
        st.subheader("🐂 Bull Case Scenario")
        st.success("""
        ### Quarterly Upside Catalysts (Q4 FY24 / Q1 FY25)
        
        **Primary Opportunities:**
        
        1. **Hyper-Accelerated AI Adoption**
           - Copilot M365 becomes must-have productivity tool
           - Dramatic ARPU increases across user base
           - Azure AI consumption exceeds capacity
           - *Impact:* Revenue beat of 3-5%, margin expansion
        
        2. **Enterprise Cloud Lock-In**
           - Wave of Fortune 500 Azure migrations
           - Multi-year contracts secured
           - Hybrid cloud dominance solidifies
           - *Impact:* Azure growth sustains 30%+ for multiple quarters
        
        3. **Gaming Ecosystem Breakthrough**
           - Game Pass subscribers surge
           - Blockbuster Activision IP launches
           - Cloud gaming traction accelerates
           - *Impact:* Gaming segment revenue +25%+
        
        4. **AI Hardware/Services Innovation**
           - Breakthrough AI chip (Maia) reduces costs
           - New AI service category creation
           - Expansion into AI infrastructure-as-a-service
           - *Impact:* New $5B+ revenue stream identified
        
        5. **Strategic M&A or Partnerships**
           - Transformative AI acquisition
           - Major enterprise customer wins
           - Industry-specific AI solutions gain traction
        """)
        
        st.metric("Bull Case Price Target", "$525-$575", "+25% to +37%")
    
    st.markdown("---")
    
    st.subheader("📊 Risk-Reward Matrix")
    
    fig = go.Figure()
    
    scenarios = ['Bear Case', 'Base Case', 'Bull Case']
    probabilities = [20, 50, 30]
    returns = [-14, 12, 31]
    
    fig.add_trace(go.Scatter(
        x=probabilities,
        y=returns,
        mode='markers+text',
        marker=dict(size=[80, 100, 80], color=['#D83B01', '#FFB900', '#107C10']),
        text=scenarios,
        textposition='top center',
        textfont=dict(size=14, color='white')
    ))
    
    fig.update_layout(
        title="Scenario Probability vs. Expected Return",
        xaxis_title="Probability (%)",
        yaxis_title="Expected Return (%)",
        height=400,
        xaxis_range=[0, 60],
        yaxis_range=[-20, 40]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("⚖️ Risk Mitigation Factors")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### Financial Strength")
        st.info("""
        - $100B+ cash position
        - AAA credit rating
        - Strong FCF generation
        - Flexible capital allocation
        """)
    
    with col2:
        st.markdown("##### Business Diversification")
        st.info("""
        - Multiple revenue engines
        - Geographic diversity
        - Customer base breadth
        - Product portfolio depth
        """)
    
    with col3:
        st.markdown("##### Strategic Positioning")
        st.info("""
        - Enterprise ecosystem lock-in
        - AI technology leadership
        - Talent acquisition capability
        - Innovation track record
        """)
    
    st.markdown("---")
    
    st.subheader("🎯 Overall Risk Assessment")
    
    risk_metrics = pd.DataFrame({
        'Risk Category': [
            'Execution Risk',
            'Competitive Risk',
            'Macro Risk',
            'Regulatory Risk',
            'Technology Risk'
        ],
        'Severity (1-10)': [4, 5, 6, 5, 3],
        'Probability (%)': [25, 40, 35, 30, 20],
        'Mitigation Strength': ['Strong', 'Moderate', 'Moderate', 'Moderate', 'Strong']
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=risk_metrics['Probability (%)'],
        y=risk_metrics['Severity (1-10)'],
        mode='markers+text',
        marker=dict(
            size=risk_metrics['Severity (1-10)'] * 10,
            color=risk_metrics['Severity (1-10)'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="Severity")
        ),
        text=risk_metrics['Risk Category'],
        textposition='top center'
    ))
    
    fig.update_layout(
        title="Risk Severity vs. Probability Matrix",
        xaxis_title="Probability of Occurrence (%)",
        yaxis_title="Severity (1-10 Scale)",
        height=500,
        xaxis_range=[0, 50],
        yaxis_range=[0, 10]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("""
    **Conclusion:** While risks exist, Microsoft's strong fundamentals, diversified business model, and strategic 
    positioning in high-growth markets (AI, cloud) provide substantial downside protection. The risk-reward profile 
    remains favorable for investors with a 3-6 month horizon, with base case expectations for continued outperformance.
    """)

st.markdown("---")
st.caption("Disclaimer: This analysis is for informational purposes only and does not constitute investment advice. Past performance does not guarantee future results.")
