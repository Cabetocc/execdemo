import streamlit as st



def _safe_text(x):
    return str(x or '')

def _safe_strip(x):
    return _safe_text(x).strip()

import requests
import time
from pathlib import Path

WEBHOOK_URL = "https://cabetocc.app.n8n.cloud/webhook-test/stock-analysis"
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

            # Wait up to 120 seconds for latest.md to change
            max_wait_seconds = 120
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

# Set Streamlit page configuration
st.set_page_config(
    page_title="MSFT Financial Ecosystem Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data for Visualizations (Hardcoded based on the analysis text) ---

# 1. Cloud Market Share (estimated for MSFT based on common knowledge/reports)
# AWS (31%), Google Cloud (11%) from text. MSFT Azure is commonly estimated around 20-25%. Let's use 23%.
# Others: 100 - 31 - 23 - 11 = 35%
cloud_market_data = {
    'Provider': ['AWS', 'Microsoft Azure', 'Google Cloud', 'Others'],
    'Share (%)': [31, 23, 11, 35]
}
df_cloud_market = pd.DataFrame(cloud_market_data)

# 2. Revenue Segment Breakdown (FY23, based on Intelligent Cloud 42% and estimates for others)
# Intelligent Cloud (42%) from text. PBP and MPC are estimated to sum to 58%.
# Based on typical MSFT reporting, PBP is usually larger than MPC.
# PBP ~32%, MPC ~26% (these sum to 58%)
revenue_segments_data = {
    'Segment': ['Intelligent Cloud', 'Productivity & Business Processes', 'More Personal Computing'],
    'Revenue Share (%)': [42, 32, 26]
}
df_revenue_segments = pd.DataFrame(revenue_segments_data)

# 3. Profitability Margins (from text)
margins_data = {
    'Metric': ['Operating Margin', 'Net Margin'],
    'Value (%)': [44, 36]
}
df_margins = pd.DataFrame(margins_data)

# 4. Capital Allocation (from text, 'Billion USD')
capital_allocation_data = {
    'Item': ['Annual Share Repurchases', 'Annual Data Center CapEx', 'OpenAI Investment'],
    'Value (Billion USD)': [60, 50, 13] # Share repurchases $60B+, CapEx $50B+, OpenAI $13B
}
df_capital_allocation = pd.DataFrame(capital_allocation_data)

# --- Helper function for section headers ---
def section_header(title, level=2):
    if level == 1:
        st.header(title)
    elif level == 2:
        st.subheader(title)
    elif level == 3:
        st.markdown(f"#### {title}")
    else:
        st.markdown(f"##### {title}")

# --- Streamlit App ---

st.title("📊 Microsoft Corporation (MSFT) Financial Ecosystem Analysis")

st.markdown("""
This application provides an interactive analysis and visualization of Microsoft Corporation's (MSFT) financial ecosystem,
drawing insights from a comprehensive financial overview.
""")

st.sidebar.header("Navigation & Quick Overview")

# --- Key Metrics in Sidebar ---
st.sidebar.markdown("---")
st.sidebar.markdown("**Quick Metrics (from Analysis):**")
st.sidebar.metric("Azure Cloud Growth", "≈30% YoY")
st.sidebar.metric("Intelligent Cloud Rev Share", "42%")
st.sidebar.metric("Operating Margin", "44%")
st.sidebar.metric("Net Margin", "36%")
st.sidebar.metric("Cash & Equivalents", "$111 Billion")
st.sidebar.metric("Annual Share Buybacks", "$60 Billion+")
st.sidebar.metric("P/E Valuation", "~35x")
st.sidebar.markdown("---")


# --- Main Content Area ---

# 1. Key Financial Overview & Metrics Dashboard
section_header("1. Key Financial Overview & Metrics Dashboard", level=2)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Azure Cloud Growth", "≈30% YoY", "Dominant growth driver")
    st.metric("Operating Margin", "44%", "Industry-leading profitability")
    st.metric("Windows OS Market Share", "75%", "PC market dominance")

with col2:
    st.metric("Intelligent Cloud Rev Share", "42% of FY23 Revenue", "Largest segment")
    st.metric("Net Margin", "36%", "Strong bottom-line performance")
    st.metric("Total Cloud Market Size", "$270 Billion", "Significant opportunity")

with col3:
    st.metric("Cash & Equivalents", "$111 Billion", "Robust balance sheet")
    st.metric("Annual Share Buybacks", "$60 Billion+", "Significant capital return")
    st.metric("Gaming Market Size", "$200 Billion", "Key growth area")

st.markdown("---")

# 2. Key Financial Relationships (Internal to MSFT)
section_header("2. Key Financial Relationships (Internal to MSFT)", level=2)
st.markdown("""
Microsoft's financial health and performance are driven by the interplay of its various business segments.
""")

with st.expander("Cloud Services (Azure & Microsoft 365) as the Growth Engine"):
    st.write("""
    Azure's growth directly fuels Microsoft 365 adoption, and vice-versa, creating a powerful sticky ecosystem.
    Significant portions of revenue are reinvested into R&D. While cloud infrastructure (Azure) has significant capital expenditure,
    the subscription-based model of Microsoft 365 offers strong and predictable recurring revenue with high gross margins.
    """)
    fig_revenue_segments = px.pie(df_revenue_segments, values='Revenue Share (%)', names='Segment',
                                  title='FY23 Revenue Segment Breakdown',
                                  color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_revenue_segments, use_container_width=True)

with st.expander("Gaming (Xbox) and its Ecosystem"):
    st.write("""
    Xbox console sales are a driver, but the true financial strength lies in recurring revenue from Game Pass subscriptions,
    game sales (digital and physical), and in-game purchases. Microsoft's significant investments in acquiring gaming studios
    (e.g., Activision Blizzard) aim to bolster exclusive content for Game Pass, thereby increasing subscriber retention.
    """)

with st.expander("LinkedIn and its Monetization"):
    st.write("""
    LinkedIn generates revenue through premium subscriptions for professionals and recruiters, as well as advertising.
    The vast professional data provides valuable insights that can be leveraged across other Microsoft products and services.
    """)

with st.expander("Windows & Devices (Surface)"):
    st.write("""
    While Windows licensing remains a significant revenue source, the revenue from Surface devices offers a more direct hardware play.
    The success of Surface devices is tied to seamless integration with Windows and Microsoft 365, reinforcing the company's ecosystem.
    """)

with st.expander("Search & Advertising (Bing)"):
    st.write("""
    Primarily driven by search advertising, competing with Google. The integration of advanced AI models (like those powering Copilot)
    into Bing is a strategic move to enhance its search capabilities and attract more users, thereby increasing advertising inventory.
    """)

with st.expander("Inter-segment Synergies and Cost Efficiencies"):
    st.write("""
    Microsoft leverages its massive infrastructure and R&D across segments. For example, AI advancements benefit Azure, Bing,
    Microsoft 365, and even gaming. Shared sales teams and marketing efforts can lead to cost efficiencies.
    """)

st.markdown("---")

# 3. Market Dependencies
section_header("3. Market Dependencies", level=2)
st.write("""
MSFT's stock performance is influenced by a variety of market forces:
- **Digital Transformation Spending:** As businesses globally continue to invest in digital transformation, cloud adoption,
  and AI integration, MSFT is a primary beneficiary.
- **Enterprise IT Budgets:** A significant portion of MSFT's revenue comes from enterprise clients. Fluctuations in enterprise
  IT spending, driven by economic conditions, directly affect MSFT.
- **Consumer Spending (Gaming & Devices):** For the Xbox and Surface segments, consumer discretionary spending plays a role.
- **Advertising Market:** The performance of Bing and LinkedIn's advertising businesses is tied to the overall health of the digital advertising market.
- **Talent Market:** The availability and cost of skilled tech talent are crucial for MSFT's innovation and growth.
- **Geopolitical Factors:** As a global company, MSFT is exposed to trade wars, sanctions, and regional conflicts.
""")
st.markdown("---")

# 4. Sector Connections
section_header("4. Sector Connections", level=2)
st.write("""
Microsoft operates at the intersection of several critical technology sectors:
- **Cloud Computing:** Azure is a direct competitor in the IaaS, PaaS, and SaaS markets.
- **Software & Productivity Suites:** Microsoft 365 is a leader in the productivity software market.
- **Hardware & Devices:** The Surface line connects MSFT to the PC and tablet hardware market.
- **Gaming:** Xbox places MSFT in the video game industry.
- **Artificial Intelligence (AI):** This is a foundational technology for MSFT, impacting all segments.
- **Business Networking & Professional Services:** LinkedIn connects MSFT to the professional networking and talent management space.
""")

st.subheader("Cloud Computing Market Landscape")
fig_cloud_market = px.bar(df_cloud_market, x='Provider', y='Share (%)',
                          title='Estimated Global Cloud Infrastructure Market Share',
                          color='Provider',
                          color_discrete_map={'AWS': 'orange', 'Microsoft Azure': 'blue', 'Google Cloud': 'green', 'Others': 'lightgrey'})
fig_cloud_market.update_layout(xaxis_title="Cloud Provider", yaxis_title="Market Share (%)")
st.plotly_chart(fig_cloud_market, use_container_width=True)

st.markdown("---")

# 5. Competitor Relationships
section_header("5. Competitor Relationships", level=2)
st.write("""
MSFT faces intense competition across its diverse product lines:
- **Direct Cloud Competitors:** Amazon (AWS) and Google (GCP) are its fiercest rivals in the public cloud market.
- **Productivity & Collaboration:** Google Workspace is the primary competitor to Microsoft 365.
- **Gaming:** Sony (PlayStation) is the main competitor in the console gaming market.
- **Operating Systems:** While Windows dominates the PC market, Apple (macOS) is a significant competitor in the premium segment.
- **Search & Advertising:** Google Search is the dominant player, making Bing's battle for market share a constant challenge.
- **CRM & Enterprise Software:** Salesforce is a major competitor in the customer relationship management.
- **Hardware:** Apple is a direct competitor with its Surface line, especially in premium laptops and tablets.
""")
st.markdown("---")

# 6. Economic Factors Impacting MSFT
section_header("6. Economic Factors Impacting MSFT", level=2)
st.write("""
Numerous macroeconomic factors influence Microsoft's financial performance:
- **Interest Rates:** Higher interest rates can increase the cost of capital for MSFT's investments and impact tech stock valuations.
- **Inflation:** Can impact the cost of components and operating costs. MSFT's subscription-based models often have mechanisms to adjust.
- **GDP Growth:** Global economic growth is a strong indicator of enterprise IT spending and demand for MSFT's services.
- **Currency Fluctuations:** As a global company, MSFT's reported earnings are affected by exchange rates.
- **Technological Disruption & Innovation Pace:** Rapid advancements from competitors or new paradigms can disrupt markets.
- **Regulatory Environment:** Increased scrutiny on Big Tech can lead to compliance costs, fines, or business restrictions.
- **Supply Chain Stability:** Disruptions can affect production and availability of Surface devices and hardware components.
""")
st.markdown("---")

# 7. Capital Allocation & Investment Profile
section_header("7. Capital Allocation & Investment Profile", level=2)

col_alloc1, col_alloc2 = st.columns(2)

with col_alloc1:
    st.markdown("#### Profitability Highlights")
    fig_margins = px.bar(df_margins, x='Metric', y='Value (%)',
                         title='Key Profitability Margins',
                         color='Metric',
                         color_discrete_sequence=['darkblue', 'teal'])
    fig_margins.update_yaxes(range=[0, 50])
    st.plotly_chart(fig_margins, use_container_width=True)

with col_alloc2:
    st.markdown("#### Strategic Investments & Returns")
    # New chart for Capital Allocation
    fig_capital_alloc = px.bar(df_capital_allocation, x='Item', y='Value (Billion USD)',
                               title='Key Capital Allocations (Billion USD)',
                               color='Item',
                               color_discrete_sequence=px.colors.qualitative.Dark24)
    fig_capital_alloc.update_yaxes(title="Value (Billion USD)")
    st.plotly_chart(fig_capital_alloc, use_container_width=True)

st.markdown("---")

# 8. Summary of MSFT's Financial Ecosystem
section_header("8. Summary of MSFT's Financial Ecosystem", level=2)
st.markdown("""
Microsoft's financial ecosystem is characterized by:
*   **Dominant Cloud and Productivity Pillars:** Azure and Microsoft 365 form the bedrock of its recurring revenue and future growth, creating a strong "sticky" ecosystem.
*   **Diversification as a Strength:** Its presence in gaming, business networking, search, and hardware provides multiple avenues for revenue and market penetration.
*   **Interconnected Segments:** The company strategically leverages its technologies (especially AI) and customer bases across different business units, creating synergies.
*   **Intense Competitive Landscape:** MSFT operates in highly competitive markets, constantly needing to innovate and adapt to rivals like Amazon, Google, and Apple.
*   **Sensitivity to Digital Transformation Trends:** Its fortunes are closely tied to the ongoing digital transformation of businesses worldwide.
*   **Exposure to Global Economic and Regulatory Forces:** Like any multinational corporation, MSFT is subject to macroeconomic shifts and evolving regulatory frameworks.

In conclusion, MSFT's financial health is robust, driven by its dominant position in cloud computing and productivity software,
a strong recurring revenue model, and strategic investments in future growth areas like AI and gaming.
However, its continued success hinges on its ability to navigate intense competition, adapt to technological shifts,
and manage the complexities of the global economic and regulatory environment.
""")

st.markdown("---")

# 9. Future Catalysts & Risks
section_header("9. Future Catalysts & Risks", level=2)

col_cat, col_risk = st.columns(2)

with col_cat:
    st.markdown("### Future Catalysts")
    st.markdown("""
    - **Continued strong Azure and cloud services growth** (accelerates top-line and increases enterprise stickiness).
    - **Successful monetization of AI products** (Copilot, Azure AI services) raising ARPU and margins.
    - **Xbox/Game Pass growth** and integration of Activision content driving recurring gaming revenue.
    - **Expansion into new vertical cloud offerings** and industry-specific solutions (healthcare, financial services).
    - **Continued share buybacks and steady dividend increases** boosting EPS.
    """)

with col_risk:
    st.markdown("### Key Risks")
    st.markdown("""
    - **Intense price competition in cloud** leading to margin compression (AWS and GCP competitive dynamics).
    - **Dependence on NVIDIA and other chip suppliers** for AI workloads — supply constraint or price spikes could increase costs.
    - **Regulatory/legal outcomes** (antitrust challenges, privacy fines, acquisition approvals/blocks) could limit strategic moves or create remediation costs.
    - **Slowing enterprise IT spend** or macro recession curbing cloud adoption.
    - **Integration risk from large acquisitions** (execution and culture risks) and the high cost of content for gaming.
    """)

st.markdown("---")

# Final Note
st.info("This analysis is based on the provided text and publicly available general knowledge about Microsoft. Specific financial figures and estimations are illustrative based on the document's content and general market understanding.")