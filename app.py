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


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="MSFT Financial Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Extraction and Preparation ---
# Key metrics from the text
msft_pe_ratio = 35
msft_yoy_revenue_growth = 13
msft_free_cash_flow_billion = 70
msft_q3_fy24_azure_growth = 31
msft_q3_fy24_ai_contribution_to_azure = 7

# Peer Benchmarking Data
peer_data = {
    "Company": ["Microsoft (MSFT)", "Amazon (AMZN)", "Alphabet (GOOGL)"],
    "P/E Ratio (TTM)": [35, 45, 25],
    "YoY Revenue Growth (%)": [13, 12, 8],
    "Cloud Market Share (%)": [23, 32, 11] # Averaging the given ranges
}
df_peers = pd.DataFrame(peer_data)

# Productivity Market Share - Qualitative, hard to chart directly against AWS
productivity_share_data = {
    "Company": ["Microsoft (M365)", "Alphabet (Workspace)"],
    "Market Share (%) (Estimate)": [70, 20] # Representative, based on "Dominant (>70%)" and "Significant challenger"
}
df_productivity_share = pd.DataFrame(productivity_share_data)

# Risk/Opportunity assessment for a radar chart (simplified quantification)
risk_opportunity_data = {
    'Category': ['AI Monetization', 'Cloud Competition', 'Macro Economy', 'Regulatory', 'GPU Supply'],
    'Risk Score': [3, 4, 3, 3, 4],  # 1 (low risk) to 5 (high risk)
    'Opportunity Score': [5, 3, 2, 2, 3] # 1 (low opp) to 5 (high opp)
}
df_risk_opp = pd.DataFrame(risk_opportunity_data)


# --- Streamlit UI ---

st.title("📈 Microsoft (MSFT) – Forward-Looking Financial Analysis")
st.markdown("A Senior Equity Research Analyst's comprehensive view on MSFT's next 3-6 months outlook, competitive landscape, and critical findings.")

st.sidebar.header("Analysis Overview")
st.sidebar.metric("Overall Conviction", "High Conviction Bullish 🚀")
st.sidebar.markdown(f"""
    **Key Metrics:**
    - P/E Ratio (TTM): **~{msft_pe_ratio}x**
    - YoY Revenue Growth: **~{msft_yoy_revenue_growth}%**
    - Free Cash Flow: **>${msft_free_cash_flow_billion}B annually**
""")
st.sidebar.info("Disclaimer: This assessment is evidence-based analysis and not investment advice.")

# --- Tabs for organized content ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Company Overview & Fundamentals",
    "Peer Benchmarking",
    "Adjacent Industries",
    "Risks & Opportunities",
    "Critical Findings Summary"
])

with tab1:
    st.header("1. Company Overview & Fundamental Evaluation")

    st.subheader("Company Profile")
    st.write("""
        Microsoft is a diversified technology giant with a dominant presence in cloud computing (Azure),
        productivity software (Microsoft 365), gaming (Xbox), and increasingly, artificial intelligence.
        - **Ticker/Company:** MSFT — Microsoft Corporation
        - **Primary Industry:** Technology — enterprise software, cloud infrastructure & platform services,
          productivity applications, AI services, and consumer devices/gaming.
        - **Core Businesses:** Microsoft Azure (cloud infrastructure and AI services), Microsoft 365
          (Office productivity and collaboration), Windows and Surface devices, LinkedIn, GitHub,
          Dynamics business applications, Xbox/Activision gaming, and investments/partnerships
          in generative AI (notably a strategic partnership with OpenAI).
    """)

    st.subheader("Recent Performance & Forward Projection (Next 3-6 Months)")
    st.markdown("""
        Microsoft has demonstrated remarkable resilience and strong growth, largely driven by the continued acceleration
        of its **Intelligent Cloud segment, spearheaded by Azure**. The company has successfully navigated a challenging
        macroeconomic environment by leveraging its sticky enterprise customer base and the growing demand for AI-powered solutions.
        
        **Key Growth Drivers:**
        *   **Azure Growth:** Continued adoption of cloud services by enterprises, coupled with increasing AI workloads
            on the platform, will remain the primary growth engine. We anticipate Azure's growth rate to remain strong,
            potentially even accelerating as more customers integrate AI into their operations.
        *   **Microsoft 365 & Copilot Integration:** The ongoing digital transformation within businesses fuels demand
            for Microsoft 365. The widespread rollout and adoption of **Microsoft Copilot** across various M365 applications
            will be a significant catalyst for upselling and increased customer stickiness, driving both revenue and ARPU.
        *   **AI Monetization:** Microsoft's deep integration of AI across its product portfolio, particularly through
            Azure AI services and Copilot, presents a substantial opportunity for new revenue streams and increased
            value proposition for existing customers.
    """)

    st.subheader("Key Catalysts (Next 3-6 Months)")
    st.markdown("""
    1.  **Widespread Copilot Adoption & Monetization:** Clear indicators of customer uptake, subscription attach rates,
        and higher average revenue per user (ARPU) for Microsoft 365 subscriptions due to Copilot.
    2.  **Continued Azure Cloud Dominance with AI Integration:** Monitoring Azure's growth rate and indications of
        AI workload migration to the platform.
    3.  **Productivity Gains & Enterprise Spending Recovery:** Potential stabilization or slight recovery in enterprise IT spending,
        further boosting M365 and Azure adoption.
    """)

    st.subheader("Key Financial Metrics (MSFT)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="P/E Ratio (TTM)", value=f"~{msft_pe_ratio}x", delta="In line with growth peers")
    with col2:
        st.metric(label="YoY Revenue Growth", value=f"~{msft_yoy_revenue_growth}%", delta="Robust, double-digit growth")
    with col3:
        st.metric(label="Free Cash Flow (Annual)", value=f">${msft_free_cash_flow_billion}B+", delta="Strong financial position")
    with col4:
        st.metric(label="Q3 FY24 Azure Growth", value=f"{msft_q3_fy24_azure_growth}%", delta=f"AI contributed {msft_q3_fy24_ai_contribution_to_azure} pts")

with tab2:
    st.header("2. Peer Benchmarking")
    st.write("Microsoft operates across several segments, making direct one-to-one comparisons challenging. However, for its core cloud and productivity businesses, its primary competitors are Amazon (AWS) and Google (GCP/Workspace).")

    st.subheader("Comparative Financials & Market Share")
    st.dataframe(df_peers.set_index("Company"), use_container_width=True)

    st.markdown("---")
    st.subheader("Visualizing Peer Comparison")

    # Chart 1: P/E Ratio
    fig_pe = px.bar(df_peers, x="Company", y="P/E Ratio (TTM)",
                    title="P/E Ratio (TTM) Comparison",
                    labels={"P/E Ratio (TTM)": "P/E Ratio"},
                    color="Company",
                    color_discrete_map={
                        "Microsoft (MSFT)": "teal",
                        "Amazon (AMZN)": "orange",
                        "Alphabet (GOOGL)": "red"
                    })
    fig_pe.update_layout(yaxis_title="P/E Ratio")
    st.plotly_chart(fig_pe, use_container_width=True)

    # Chart 2: YoY Revenue Growth
    fig_rev_growth = px.bar(df_peers, x="Company", y="YoY Revenue Growth (%)",
                            title="Year-over-Year Revenue Growth Comparison",
                            labels={"YoY Revenue Growth (%)": "Revenue Growth (%)"},
                            color="Company",
                            color_discrete_map={
                                "Microsoft (MSFT)": "teal",
                                "Amazon (AMZN)": "orange",
                                "Alphabet (GOOGL)": "red"
                            })
    fig_rev_growth.update_layout(yaxis_title="Revenue Growth (%)")
    st.plotly_chart(fig_rev_growth, use_container_width=True)

    # Chart 3: Cloud Market Share
    fig_cloud_share = px.bar(df_peers, x="Company", y="Cloud Market Share (%)",
                             title="Cloud Infrastructure Market Share (Azure vs. AWS vs. GCP)",
                             labels={"Cloud Market Share (%)": "Market Share (%)"},
                             color="Company",
                             color_discrete_map={
                                "Microsoft (MSFT)": "teal",
                                "Amazon (AMZN)": "orange",
                                "Alphabet (GOOGL)": "red"
                             })
    fig_cloud_share.update_layout(yaxis_title="Market Share (%)")
    st.plotly_chart(fig_cloud_share, use_container_width=True)

    st.subheader("Productivity Software Market Share")
    st.markdown("""
        - **Microsoft (M365):** Dominant (>70%)
        - **Alphabet (Workspace):** Significant challenger
        
        Microsoft's dominance in productivity software is a significant moat that Google Workspace competes against.
        AWS is not a direct competitor in this segment.
    """)

    st.subheader("Relative Strengths of Microsoft")
    st.markdown("""
    *   **Integrated enterprise stack:** Unique bundling of productivity (M365), identity, collaboration (Teams),
        and cloud infrastructure that creates strong customer retention and multiple upsell pathways for AI features.
    *   **Large existing enterprise customer base** and long-term contracts, easing monetization of AI add-ons.
    *   **Financial position:** High cash flow generation and a strong balance sheet to fund capex for data centers and strategic investments.
    *   **AI positioning:** Early and visible partnership with OpenAI and broad rollouts of Copilot features across enterprise products.
    """)

    st.subheader("Relative Weaknesses")
    st.markdown("""
    *   Heavy capital intensity for AI infrastructure (data centers, GPUs) and potential exposure to GPU supply cycles and pricing.
    *   Regulatory and antitrust scrutiny because of size and breadth across markets.
    *   Competition from hyperscalers (AWS, Google) that are also making aggressive AI investments and competing on price and innovation.
    """)

with tab3:
    st.header("3. Adjacent Industry Impact")
    st.write("Several adjacent industries are significantly influencing Microsoft's trajectory, presenting both positive impacts and risks.")

    st.subheader("Positive Impacts (Tailwinds)")
    st.markdown("""
    *   **Semiconductor/GPU Industry (NVIDIA, AMD):** Microsoft is one of the largest buyers of high-end AI chips (GPUs). The **scarcity of advanced GPUs** has actually acted as a moat, as Microsoft's early and large orders with NVIDIA give it an infrastructure advantage over smaller cloud rivals.
    *   **Energy & Utilities:** The boom in AI data center construction is forcing Microsoft to innovate in **next-generation nuclear power (SMRs)** and renewable energy deals to power its facilities and meet sustainability goals. This positions it as a leader in green tech.
    *   **Cybersecurity Industry:** The increasing complexity of AI-powered cyber threats is driving demand for integrated, AI-native security platforms, playing directly into Microsoft's strength in this adjacent field.
    """)

    st.subheader("Negative Impacts / Risks (Headwinds)")
    st.markdown("""
    *   **Telecom & Networking:** The AI data center boom requires massive new investments in **global networking infrastructure**. Bottlenecks or cost overruns here could delay Microsoft's cloud expansion.
    *   **Regulatory & Legal Landscape:** Increased global scrutiny on **data privacy, AI ethics, and antitrust** (from adjacent legal/regulatory sectors) poses a constant risk of slower rollout, higher compliance costs, or even forced changes to its business practices (e.g., the OpenAI partnership structure).
    *   **Content & Media Industry:** In gaming, the Activision acquisition brings it directly into the turbulent media landscape, with challenges in mobile app store policies (Apple, Google) and shifting gamer demographics.
    """)

with tab4:
    st.header("4. Risk Assessment: Bear vs. Bull Cases")

    col_bull, col_bear = st.columns(2)

    with col_bull:
        st.subheader("🐂 Bull Case (Next Quarter)")
        st.markdown("""
        *   **Accelerated Copilot Monetization:** Stronger-than-anticipated attach rates and positive customer feedback
            on Copilot's productivity benefits, leading to increased ARPU and clear revenue contributions.
        *   **Robust Azure Growth Driven by AI Workloads:** Continued strong growth in Azure, with clear evidence of
            AI workloads migrating to the platform and higher customer spending on AI services.
        *   **Resilient Enterprise Spending & Strategic Wins:** Demonstrating resilience in enterprise IT spending
            despite economic headwinds, coupled with significant large-scale cloud or AI wins.
        """)

    with col_bear:
        st.subheader("🐻 Bear Case (Next Quarter)")
        st.markdown("""
        *   **Slower than expected Copilot adoption:** If the initial uptake and monetization of Microsoft Copilot
            fall short of aggressive market expectations.
        *   **Intensified Cloud Competition:** Increased price competition from AWS and GCP, coupled with aggressive
            market share grabs by competitors, pressuring Azure's growth rates and margins.
        *   **Macroeconomic Deterioration:** A sharp downturn in the global economy leading to significant cuts
            in enterprise IT spending.
        """)

    st.subheader("Quantitative Risk & Opportunity Outlook")
    st.write("A simplified view of key categories impacting MSFT.")

    # Radar chart for risks and opportunities
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=df_risk_opp['Risk Score'],
        theta=df_risk_opp['Category'],
        fill='toself',
        name='Risk Score',
        line_color='red'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=df_risk_opp['Opportunity Score'],
        theta=df_risk_opp['Category'],
        fill='toself',
        name='Opportunity Score',
        line_color='green'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['Low', 'Low-Mid', 'Mid', 'Mid-High', 'High']
            )),
        showlegend=True,
        title="Risk & Opportunity Assessment (1=Low, 5=High)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with tab5:
    st.header("5. Critical Findings Summary")
    st.write("A distillation of the most important takeaways from this analysis.")

    st.markdown("""
    *   **🚀 Major Opportunity:** Microsoft is the best-positioned mega-cap to monetize enterprise AI through its ubiquitous
        software stack. **Copilot adoption is the single most important metric to watch.**
    *   **⚠️ Major Risk:** The stock's **premium valuation leaves little room for error**. A stumble in AI monetization
        or a broader tech sell-off would disproportionately impact MSFT.
    *   **⚔️ Key Battle:** The cloud AI war with **AWS and Google Cloud** will define the next decade. Microsoft's
        current lead is strong but not unassailable.
    *   **🔗 External Dependency:** Its strategy is heavily reliant on the **continued innovation and stability of OpenAI**,
        making that relationship a critical, non-financial asset.
    """)

    st.subheader("Overall Conviction")
    st.success("""
    We maintain a **high conviction bullish stance** on Microsoft. The company's strategic positioning at the
    intersection of cloud and AI, coupled with its strong execution and diversified revenue streams, provides a
    powerful platform for continued growth and innovation. The ongoing integration and monetization of AI,
    particularly through Copilot, represent a significant, underappreciated growth driver. While risks exist,
    we believe the company is well-equipped to navigate them.
    """)

    st.subheader("Key Indicators to Watch (Next 3-6 Months)")
    st.markdown("""
    Investors and stakeholders should watch:
    - Quarterly guidance on Azure/AI revenue.
    - Metrics on Copilot and M365 AI adoption.
    - Large-enterprise contract wins.
    - GPU-capacity disclosures.
    """)

    st.caption("Sources: Recent analyst reports from Morgan Stanley, Goldman Sachs; Q3 FY24 Earnings Call Transcript; Reuters/Bloomberg coverage on AI investments; CNBC interviews with CEO Satya Nadella; industry commentary from Stratechery and Ben Thompson; regulatory news from The Wall Street Journal.")

# --- End of Streamlit App ---