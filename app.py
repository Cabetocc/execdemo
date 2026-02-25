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

def create_peer_benchmarking_charts():
    """Generates Plotly charts for peer benchmarking metrics."""

    # Data from the provided text, using mid-points for ranges
    data = {
        "Company": ["Nokia (NOK)", "Ericsson (ERIC)", "Cisco Systems (CSCO)", "Ciena (CIEN)"],
        "P/E Ratio (TTM)": [22.5, 17.5, 13.5, 27.5],  # Mid-points of given ranges
        "YoY Revenue Growth (%)": [2.5, 2.5, 5.0, 7.5],  # Mid-points of given ranges
        "Market Share (5G Infrastructure)": ["Significant (3rd/4th)", "Significant (2nd)", "Varies", "Growing (Optical)"]
    }
    df_peers = pd.DataFrame(data)

    # P/E Ratio Chart
    fig_pe = px.bar(
        df_peers,
        x="Company",
        y="P/E Ratio (TTM)",
        title="Peer Benchmarking: P/E Ratio (TTM)",
        labels={"P/E Ratio (TTM)": "P/E Ratio"},
        color="Company",
        color_discrete_map={
            "Nokia (NOK)": "#1f77b4",  # A distinct color for Nokia
            "Ericsson (ERIC)": "#ff7f0e",
            "Cisco Systems (CSCO)": "#2ca02c",
            "Ciena (CIEN)": "#d62728"
        },
        template="plotly_white"
    )
    fig_pe.update_layout(xaxis_title="", yaxis_title="P/E Ratio (TTM)", showlegend=False)

    # YoY Revenue Growth Chart
    fig_rev = px.bar(
        df_peers,
        x="Company",
        y="YoY Revenue Growth (%)",
        title="Peer Benchmarking: YoY Revenue Growth (%)",
        labels={"YoY Revenue Growth (%)": "YoY Revenue Growth (%)"},
        color="Company",
        color_discrete_map={
            "Nokia (NOK)": "#1f77b4",
            "Ericsson (ERIC)": "#ff7f0e",
            "Cisco Systems (CSCO)": "#2ca02c",
            "Ciena (CIEN)": "#d62728"
        },
        template="plotly_white"
    )
    fig_rev.update_layout(xaxis_title="", yaxis_title="YoY Revenue Growth (%)", showlegend=False)

    return fig_pe, fig_rev, df_peers

# --- Streamlit App Setup ---
st.set_page_config(
    page_title="Nokia (NOK) Financial Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("📊 Nokia (NOK): Navigating the Network Infrastructure Landscape")
st.markdown("""
This application provides a forward-looking financial analysis and visualization of Nokia (NOK), 
focusing on key metrics, competitive positioning, and industry dynamics.
""")

st.divider()

# --- 1. Company Overview ---
st.header("Company Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ticker", "NOK")
with col2:
    st.metric("Company", "Nokia Corporation")
with col3:
    st.metric("Headquarters", "Finland")

st.markdown("""
Nokia is a global supplier of telecommunications equipment, software, and services. 
Its primary industry involves telecom/network equipment and services (RAN, core, optical/IP, 
cloud software, managed services) with a growing focus on software/subscription revenues and private networks.
""")

st.divider()

# --- 2. Key Metrics & Recent Performance ---
st.header("Key Metrics & Recent Performance")

st.markdown("### Fundamental Evaluation: Navigating the Transition")
st.markdown("""
Nokia has been in a period of strategic transition, focusing on optimizing its portfolio and improving profitability. 
While revenue growth has been somewhat muted, efforts to enhance margins through cost efficiencies and a focus on 
higher-value software and services are evident.
""")

col_metric_1, col_metric_2, col_metric_3 = st.columns(3)
with col_metric_1:
    st.metric(
        "Q1 2024 Gross Margin",
        "40.7%",
        delta="Up from 37.8% YoY",
        help="Improvement seen due to cost efficiencies and portfolio optimization."
    )
with col_metric_2:
    st.metric(
        "Q1 2024 Sales Decline",
        "-19%",
        delta="YoY at constant currency",
        delta_color="inverse",
        help="Driven by significant reduction in CapEx by major telecom operators."
    )
with col_metric_3:
    st.metric(
        "Cost Savings Target (by 2026)",
        "€800M to €1.2B",
        help="Part of Nokia's restructuring program to enhance profitability."
    )

st.divider()

# --- 3. 3-6 Month Outlook ---
st.header("3-6 Month Outlook: Cautiously Optimistic")

st.markdown("""
The near-term outlook for Nokia is cautiously optimistic, with a focus on execution and market share gains. 
Continued revenue growth is anticipated from ongoing 5G deployments, especially in emerging markets, 
and an increased focus on cloudification of networks and enterprise solutions.
""")

with st.expander("Drivers & Rationale", expanded=False):
    st.subheader("Drivers & Rationale")
    st.markdown("""
    *   **Financial Trends & Fundamentals:** Expect sensitivity to gross margin recovery, services revenue mix, and working capital swings. Steady free cash flow is crucial.
    *   **Macroeconomic Conditions:** Telco CapEx correlates with GDP growth, operator balance-sheet strength, and interest rates. Stable global growth means steady CapEx; weakening macro could delay discretionary projects.
    *   **Industry Dynamics:** 5G rollout is maturing, with incremental spending on capacity densification, software features (O-RAN, Cloud RAN), and enterprise/private 5G. Optical/IP spending is a parallel growth engine.
    *   **Company-specific Catalysts/Risks:** Catalysts include multi-country 5G deals, large optical/IP contracts, acceleration in software subscription revenue, and visible margin improvement. Risks involve execution delays, margin pressure, and missed order expectations.
    """)

st.subheader("Key Catalysts for the Next 3-6 Months")
col_cat_1, col_cat_2, col_cat_3 = st.columns(3)
with col_cat_1:
    st.info("**Increased 5G Capex in Key Markets**\n\nResurgence in capital expenditure from certain operators, especially in emerging markets and specific use-case deployments (e.g., industrial 5G, private networks).")
with col_cat_2:
    st.info("**Enterprise Digitalization & Private Networks Growth**\n\nSignificant demand for private wireless networks for enterprises (manufacturing, logistics, utilities). Nokia is well-positioned with its end-to-end solutions.")
with col_cat_3:
    st.info("**AI-Driven Network Operations & Automation**\n\nOperators seek to optimize network performance and reduce operational costs using AI and automation for network management. Nokia's investments in these areas can drive adoption.")

st.divider()

# --- 4. Peer Benchmarking ---
st.header("Peer Benchmarking: A Competitive Landscape")
st.markdown("Nokia operates in a highly competitive environment. Here's how it compares to key peers:")

fig_pe, fig_rev, df_peers = create_peer_benchmarking_charts()

col_chart_1, col_chart_2 = st.columns(2)
with col_chart_1:
    st.plotly_chart(fig_pe, use_container_width=True)
with col_chart_2:
    st.plotly_chart(fig_rev, use_container_width=True)

st.subheader("Market Share (5G Infrastructure) & Analysis")
st.dataframe(df_peers[['Company', 'Market Share (5G Infrastructure)']], hide_index=True, use_container_width=True)
st.markdown("""
*Note: These are indicative ranges and can fluctuate. Market share figures are complex and often debated.*

**Analysis:** Nokia often trades at a slightly higher P/E than some of its larger, more diversified competitors like Cisco, 
reflecting investor expectations for its turnaround and potential in emerging technologies. Ericsson, its most direct 
competitor in mobile network infrastructure, often sees similar revenue growth patterns but can be subject to different 
market sensitivities. Ciena operates in a more specialized segment (optical networking) and has shown robust growth. 
Nokia's challenge is to consistently demonstrate margin expansion and accelerate revenue growth in a competitive and 
capital-intensive industry.
""")

st.divider()

# --- 5. Competitive Positioning (vs. Key Peers: Ericsson, Huawei) ---
st.header("Competitive Positioning")

st.markdown("A deep dive into Nokia's strengths, weaknesses, opportunities, and threats against key rivals.")

st.subheader("Strengths")
st.success("""
*   **Diversified Portfolio:** Strong position in fixed networks (optical, broadband), IP routing, and submarine cables, providing insulation from mobile downturns.
*   **Strong IP & Licensing Business:** Patent portfolio generates reliable, high-margin income (e.g., Honor renewal).
*   **Private Wireless & Enterprise Focus:** Leader in private 4G/5G networks for industrial and enterprise customers.
""")

st.subheader("Weaknesses")
st.warning("""
*   **Profitability in Networks:** Operating margin has historically lagged Ericsson's; closing this gap is a key focus.
*   **Perception of Innovation Pace:** Perception of Ericsson being more agile in technology development in RAN market.
""")

st.subheader("Opportunities")
st.info("""
*   **Open RAN (Open Radio Access Network):** Investments in Open RAN could capture market share in new deployments.
*   **Network Infrastructure Upgrade Cycle:** Eventual rebound in operator spending (5G-Advanced, fiber expansion, cloudification) represents significant future opportunity.
""")

st.subheader("Threats")
st.error("""
*   **Prolonged Operator CapEx Weakness:** If the current downturn extends beyond 2024, revenues will remain pressured.
*   **Geopolitical Fragmentation:** Bifurcation of global markets creates complexity and limits growth.
*   **Aggressive Pricing from Competitors:** Intense competition, especially from Huawei, can pressure margins.
""")

st.divider()

# --- 6. Adjacent Industry Analysis ---
st.header("Adjacent Industry Analysis: Upstream & Downstream Indicators")

st.markdown("""
Nokia's performance is influenced by various adjacent industries, both upstream (suppliers) and downstream (customers).
""")

st.subheader("1. Semiconductor & Component Manufacturers (Upstream)")
st.info("""
*   **Influence:** Negative (Historically), Positive (Current Stability)
*   **Details:** Normalization after intense demand and supply chain constraints. Stable pricing and better component availability are positive for Nokia. Renewed shortages or price hikes would be a headwind; stability is a tailwind.
""")

st.subheader("2. Telecommunication Operators (Downstream)")
st.info("""
*   **Influence:** Negative (Current CapEx Pressure), Positive (Long-term 5G/6G Imperative)
*   **Details:** Operator health and spending appetite directly impact Nokia. Interest rate hikes make CapEx expensive, but the imperative to upgrade to 5G/6G remains strong. Positive CapEx guidance from major operators is a strong tailwind.
""")

st.subheader("3. Cloud & Hyperscalers Industry")
st.info("""
*   **Influence:** Mixed (Positive Partnership, Negative Disruption)
*   **Details:** Partners for core network software and private wireless. Growth of cloud-native network functions is a strength. However, hyperscalers also compete in telecom service layers, potentially disintermediating traditional vendors.
""")

st.subheader("4. Industrial & Manufacturing Sector")
st.info("""
*   **Influence:** Positive (Direct Tailwaind)
*   **Details:** Digital transformation (Industry 4.0) drives demand for private wireless and industrial automation solutions, a high-margin segment for Nokia.
""")

st.subheader("5. Government Policy & Regulation")
st.info("""
*   **Influence:** Mixed (Positive for "Trusted" Vendors, Negative for Trade Restrictions)
*   **Details:** "Buy local" and security-focused policies (US, Europe, India) benefit Nokia. Export controls and trade restrictions can complicate supply chains and market access.
""")

st.divider()

# --- 7. Risk Assessment ---
st.header("Risk Assessment")

st.markdown("""
Understanding potential scenarios for Nokia's near-term performance.
""")

col_bear, col_bull = st.columns(2)
with col_bear:
    st.subheader("🐻 Bear Case (Upcoming Quarter)")
    st.error("""
    *   **Delayed 5G Rollouts & Fierce Competition:** Slower CapEx from operators combined with intensified pricing pressure could lead to flat or declining revenues and compressed margins.
    *   **Execution Challenges in New Growth Areas:** Nokia struggles to gain traction or achieve profitability in emerging areas (private networks, cloud-native) due to complexities or slow adoption.
    *   **Macroeconomic Headwinds:** Persistent inflation or global economic slowdown dampens overall telecom spending and profitability.
    """)
with col_bull:
    st.subheader("🐂 Bull Case (Upcoming Quarter)")
    st.success("""
    *   **Accelerated 5G Deployments & Market Share Gains:** Stronger-than-expected surge in 5G CapEx allows Nokia to capture market share, especially in less dominant regions.
    *   **Strong Performance in Enterprise & Software:** Significant wins and early revenue traction in enterprise (private networks, managed services), plus successful upsells of software/AI solutions, boost revenue and margins.
    *   **Positive Progress on Margin Improvement Initiatives:** Tangible progress in cost optimization and economies of scale lead to better-than-expected gross and operating margins, signaling a successful turnaround.
    """)

st.divider()

# --- 8. Summary Judgement & What to Watch ---
st.header("Summary Judgment")
st.info("""
Nokia is viewed as a company with solid underlying assets (strong patents, diversified portfolio) navigating a 
difficult cyclical downturn in its core market. The critical near-term factor is the timing and strength of 
the rebound in telecom operator spending. Success will be measured by its ability to continue improving margins 
through its restructuring while positioning its technology (especially in Open RAN and enterprise solutions) to 
capture the next wave of network investment. The stock's performance is likely to remain volatile until clear 
signs of revenue growth re-emerge.
""")

st.subheader("What to Watch (High Signal Items)")
st.markdown("""
*   Upcoming quarterly results (order intake, backlog, services/software revenue mix).
*   Any announced large contracts (RAN/optical/private networks).
*   Guidance changes from management.
*   Free cash flow and net debt trajectory.
*   Public policy moves affecting vendor access in key markets.
""")

st.markdown("---")
st.caption("Note: This is an evidence-based, forward-looking assessment based on industry dynamics and typical financial drivers. It is not investment advice.")