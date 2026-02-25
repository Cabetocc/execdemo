import streamlit as st

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

            # If it didn't update in time, tell the user what to do
            if updated == before:
                status.warning("Still processing. Please wait a bit longer and press Generate again (or refresh).")

        # Refresh the page so the rest of the app renders with the new file
        st.rerun()


import pandas as pd
import plotly.express as px

# --- App Configuration ---
st.set_page_config(
    page_title="AstraZeneca (AZN) Financial Ecosystem Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Helper Functions ---
def display_section_title(title):
    st.markdown(f"## {title}")
    st.markdown("---")

def display_metric(label, value, is_percentage=False):
    if is_percentage and value is not None:
        formatted_value = f"{value:.1%}"
    elif value is not None:
        formatted_value = f"{value:,.2f}"
    else:
        formatted_value = "N/A"
    st.metric(label, formatted_value)

def create_bar_chart(data, x_col, y_col, title, color_col=None, hover_data=None):
    if data is None or data.empty:
        st.warning("No data available for chart.")
        return
    fig = px.bar(data, x=x_col, y=y_col, title=title, color=color_col,
                 labels={x_col: x_col.replace("_", " ").title(), y_col: y_col.replace("_", " ").title()},
                 hover_data=hover_data)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def create_pie_chart(data, names_col, values_col, title):
    if data is None or data.empty:
        st.warning("No data available for chart.")
        return
    fig = px.pie(data, names=names_col, values=values_col, title=title)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

# --- Load Data (Simulated) ---
# In a real application, this would come from APIs, databases, or files.
# For demonstration, we'll create sample dataframes.

# --- Key Metrics (Extracted/Simulated) ---
key_metrics_data = {
    "Metric": [
        "Revenue (USD)", "Gross Profit Margin", "Operating Profit Margin",
        "Net Profit Margin", "R&D as % of Revenue", "Debt-to-Equity Ratio",
        "Dividend Yield"
    ],
    "Value": [
        79.0e9, 0.75, 0.22, 0.15, 0.20, 0.8, 0.025
    ],
    "Is_Percentage": [
        False, True, True, True, True, False, True
    ]
}
df_key_metrics = pd.DataFrame(key_metrics_data)

# --- Revenue Breakdown (Simulated) ---
revenue_breakdown_data = {
    "Source": [
        "Product Sales", "Partnerships & Licensing", "Acquisitions"
    ],
    "Revenue": [
        75.0e9, 3.0e9, 1.0e9
    ]
}
df_revenue_breakdown = pd.DataFrame(revenue_breakdown_data)

# --- Cost Structure Breakdown (Simulated) ---
cost_structure_data = {
    "Cost_Category": [
        "R&D", "COGS", "SG&A", "Amortization"
    ],
    "Cost": [
        15.8e9, 19.75e9, 17.38e9, 3.95e9
    ]
}
df_cost_structure = pd.DataFrame(cost_structure_data)

# --- Therapeutic Area Revenue (Simulated) ---
therapeutic_area_revenue_data = {
    "Therapeutic_Area": [
        "Oncology", "CVRM", "Respiratory/Immunology", "Rare Disease", "Other"
    ],
    "Revenue": [
        31.6e9, 19.75e9, 15.8e9, 7.9e9, 4.0e9
    ]
}
df_therapeutic_area = pd.DataFrame(therapeutic_area_area_revenue_data)

# --- Geographic Revenue (Simulated) ---
geographic_revenue_data = {
    "Region": [
        "United States", "Europe", "China", "Emerging Markets", "Rest of World"
    ],
    "Revenue": [
        28.0e9, 19.0e9, 12.0e9, 14.0e9, 6.0e9
    ]
}
df_geographic_revenue = pd.DataFrame(geographic_revenue_data)

# --- Competitor Revenue (Simulated - relative scale) ---
competitor_revenue_data = {
    "Competitor": [
        "Pfizer", "Novartis", "Roche", "Merck & Co.", "Bristol Myers Squibb", "AstraZeneca (AZN)"
    ],
    "Revenue_Billion_USD": [
        100.0, 65.0, 60.0, 59.0, 46.0, 79.0
    ]
}
df_competitors = pd.DataFrame(competitor_revenue_data)

# --- Market Dependencies (Qualitative Summary) ---
market_dependencies_summary = """
- **Drug Pricing & Reimbursement**: Highly sensitive to government policies (e.g., US Inflation Reduction Act), payer negotiations (PBMs, national health systems), and overall healthcare spending trends.
- **Patent Expirations & Generic Competition**: Critical for maintaining revenue streams. Loss of exclusivity (LOE) for key drugs significantly impacts top-line. Pipeline is crucial to offset these losses.
- **Clinical Trial Success Rates**: Positive Phase I, II, and III trial results and subsequent regulatory approvals (FDA, EMA, etc.) are major value drivers. Failures lead to R&D write-offs.
- **Disease Prevalence & Demographics**: Aging populations and rising chronic disease rates drive demand. Emerging diseases can create new opportunities (e.g., COVID-19 vaccine).
- **Geopolitical Factors**: Trade relations, political stability, and regional regulatory environments (e.g., China's market dynamics) can affect market access and costs.
"""

# --- Sector Connections (Qualitative Summary) ---
sector_connections_summary = """
- **Pharmaceutical & Biotechnology Sector**: Characterized by high R&D intensity, strict regulation, long product lifecycles, capital intensity, and innovation-driven growth.
- **Healthcare Services**: AZN's products are integrated into the healthcare delivery system, relying on prescribers, pharmacies, and distributors.
- **Life Sciences**: Fundamental research in biology, chemistry, and medicine underpins drug discovery and development.
- **Biotechnology Advancements**: Leverages progress in areas like genomics, gene editing, and AI for drug discovery.
"""

# --- Economic Factors (Qualitative Summary) ---
economic_factors_summary = """
- **Global Economic Growth**: Strong economies tend to boost healthcare spending. Recessions can lead to budget constraints and price sensitivity.
- **Interest Rates**: Higher rates increase borrowing costs for R&D and M&A, and affect discount rates used in valuation models.
- **Inflation**: Can increase the cost of raw materials, manufacturing, and labor, potentially requiring price adjustments which face payer resistance.
- **Currency Exchange Rates**: As a global company, fluctuations in USD, EUR, GBP, CNY, etc., impact reported earnings.
- **Government Healthcare Policy & Reforms**: Changes in healthcare access, drug pricing regulations, and R&D incentives (e.g., ACA, IRA) are highly impactful.
- **Technological Advancements**: AI, genomics, and personalized medicine create both opportunities and potential disruptions.
- **Supply Chain Stability**: Global supply chain disruptions can affect manufacturing, costs, and availability of essential materials.
- **Demographic Shifts**: Aging populations and changing disease patterns directly influence demand for specific treatments.
"""

# --- Sidebar ---
st.sidebar.title("AstraZeneca (AZN) Analysis")
st.sidebar.markdown("Financial Ecosystem Analysis")

st.sidebar.markdown("---")
st.sidebar.markdown("### Sections")
st.sidebar.markdown("- [Company Overview & Snapshot](#company-overview--snapshot)")
st.sidebar.markdown("- [Key Metrics](#key-metrics)")
st.sidebar.markdown("- [Revenue Generation](#revenue-generation)")
st.sidebar.markdown("- [Cost Structure](#cost-structure)")
st.sidebar.markdown("- [Profitability & Margins](#profitability--margins)")
st.sidebar.markdown("- [Capital Allocation](#capital-allocation)")
st.sidebar.markdown("- [Debt & Liquidity](#debt--liquidity)")
st.sidebar.markdown("- [Market Dependencies](#market-dependencies)")
st.sidebar.markdown("- [Sector Connections](#sector-connections)")
st.sidebar.markdown("- [Competitor Relationships](#competitor-relationships)")
st.sidebar.markdown("- [Economic Factors](#economic-factors)")
st.sidebar.markdown("- [Conclusion](#conclusion)")

# --- Main Content ---

st.title("AstraZeneca (AZN) - Financial Ecosystem Analysis")
st.markdown("""
AstraZeneca (AZN) is a global, research-driven biopharmaceutical company operating within a complex and dynamic financial ecosystem. This analysis breaks down its key financial relationships, market dependencies, sector connections, competitor landscape, and relevant economic factors.
""")

# --- Company Overview & Snapshot ---
display_section_title("Company Overview & Snapshot")
st.markdown("""
AstraZeneca plc is a global pharmaceutical and biotechnology company focused on the discovery, development, and commercialization of prescription medicines. It operates primarily in oncology, cardiovascular, renal & metabolism (CVRM), respiratory & immunology, and rare diseases. Key products include Tagrisso (oncology), Farxiga (CVRM), and Imfinzi (oncology). The company has dual primary listings on the London Stock Exchange and NASDAQ (as an ADR).
""")

# --- Key Metrics ---
display_section_title("Key Metrics")
st.markdown("Key financial indicators that reflect AstraZeneca's performance and financial health.")

col1, col2, col3 = st.columns(3)
for i, row in df_key_metrics.iterrows():
    if i < 3:
        with col1:
            display_metric(row["Metric"], row["Value"], row["Is_Percentage"])
    elif i < 6:
        with col2:
            display_metric(row["Metric"], row["Value"], row["Is_Percentage"])
    else:
        with col3:
            display_metric(row["Metric"], row["Value"], row["Is_Percentage"])

# --- Revenue Generation ---
display_section_title("Revenue Generation")
st.markdown("AstraZeneca's revenue streams are diversified across product sales and strategic collaborations.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Primary Revenue Sources:**")
    st.markdown("""
    *   **Product Sales**: The core driver, generated from its diverse portfolio of prescription medicines across various therapeutic areas.
    *   **Partnerships & Licensing**: Agreements for co-development, licensing, and co-commercialization generate upfront payments, milestones, and royalties.
    *   **Acquisitions**: Strategic M&A activity can significantly boost revenue and expand market share (e.g., Alexion acquisition).
    """)
with col2:
    create_pie_chart(df_revenue_breakdown, "Source", "Revenue", "Revenue Breakdown by Source")

# --- Cost Structure ---
display_section_title("Cost Structure")
st.markdown("Understanding the significant expenses incurred by AstraZeneca.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Key Cost Components:**")
    st.markdown("""
    *   **Research & Development (R&D)**: A substantial investment essential for pipeline advancement and future growth.
    *   **Cost of Goods Sold (COGS)**: Manufacturing, production, and distribution expenses.
    *   **Sales, General & Administrative (SG&A)**: Costs associated with marketing, sales force, and operations.
    *   **Amortization of Intangible Assets**: Primarily related to acquired patents and intellectual property.
    """)
with col2:
    create_bar_chart(df_cost_structure, "Cost_Category", "Cost", "Cost Structure Breakdown", hover_data=["Cost_Category", "Cost"])

# --- Profitability & Margins ---
display_section_title("Profitability & Margins")
st.markdown("Indicators of AstraZeneca's profitability across its operations.")
# Metrics are already displayed in Key Metrics section, but we can emphasize them here
st.markdown("Key profitability metrics (Gross Profit Margin, Operating Profit Margin, Net Profit Margin) are detailed in the 'Key Metrics' section above. High gross margins from specialty drugs fund extensive R&D investments.")

# --- Capital Allocation ---
display_section_title("Capital Allocation")
st.markdown("How AstraZeneca reinvests its capital for growth and shareholder returns.")
st.markdown("""
AstraZeneca strategically allocates its capital through:
*   **R&D Investment**: Significant reinvestment to maintain a robust pipeline and drive future innovation.
*   **Capital Expenditures (CapEx)**: Investments in manufacturing facilities, research labs, and infrastructure.
*   **Share Buybacks**: Returning capital to shareholders by repurchasing its own stock.
*   **Dividends**: Distributing a portion of profits to shareholders, with a history of consistent payouts.
*   **Mergers & Acquisitions (M&A)**: Strategic investments to acquire new technologies, drugs, or market access.
""")

# --- Debt & Liquidity ---
display_section_title("Debt & Liquidity")
st.markdown("Assessment of AstraZeneca's financial leverage and ability to meet obligations.")
st.markdown("""
AstraZeneca maintains a **moderate level of debt**, typically around a **Debt-to-Equity ratio of ~0.8**. This financing supports its R&D programs and strategic acquisitions. The company generates **strong operating cash flow**, ensuring sufficient liquidity to meet short-term obligations and fund ongoing operations without excessive reliance on external financing. Analysts monitor its interest coverage ratios closely.
""")

# --- Market Dependencies ---
display_section_title("Market Dependencies")
st.markdown("External forces that significantly influence AstraZeneca's success and market performance.")
st.markdown(f"```{market_dependencies_summary}```")

# --- Sector Connections ---
display_section_title("Sector Connections")
st.markdown("AstraZeneca's position within the broader pharmaceutical and healthcare landscape.")
st.markdown(f"```{sector_connections_summary}```")

# --- Competitor Relationships ---
display_section_title("Competitor Relationships")
st.markdown("AstraZeneca operates in a highly competitive environment across its key therapeutic areas.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Key Competitors:**")
    st.markdown("""
    *   **Major Pharmaceutical Giants**: Pfizer, Novartis, Roche, Merck & Co., Bristol Myers Squibb, Johnson & Johnson.
    *   **Biotechnology Companies**: Amgen, Gilead Sciences, and numerous smaller, innovative biotech firms.
    *   **Generic & Biosimilar Manufacturers**: Compete once patent exclusivity expires.
    """)
    st.markdown("**Competitive Dynamics:**")
    st.markdown("""
    *   Focus on developing best-in-class therapies (efficacy, safety).
    *   Aggressive market share capture and sales strategies.
    *   Continuous pipeline advancement to replace aging products.
    *   Navigating complex global pricing environments.
    *   Strategic M&A to bolster portfolios.
    """)
with col2:
    create_bar_chart(df_competitors.sort_values("Revenue_Billion_USD", ascending=False),
                     "Competitor", "Revenue_Billion_USD", "Estimated Revenue of Key Competitors (USD Billion)",
                     color_col="Competitor", hover_data=["Competitor", "Revenue_Billion_USD"])

# --- Economic Factors ---
display_section_title("Economic Factors")
st.markdown("Macroeconomic trends and conditions impacting AstraZeneca's operations and financial outlook.")
st.markdown(f"```{economic_factors_summary}```")

# --- Additional Visualizations ---
display_section_title("Revenue Breakdown by Therapeutic Area")
st.markdown("AstraZeneca's revenue is significantly driven by its oncology and CVRM segments.")
create_pie_chart(df_therapeutic_area, "Therapeutic_Area", "Revenue", "Revenue by Therapeutic Area (USD)")

display_section_title("Geographic Revenue Distribution")
st.markdown("The United States and Europe are AstraZeneca's largest markets.")
create_bar_chart(df_geographic_revenue.sort_values("Revenue", ascending=False),
                 "Region", "Revenue", "Revenue by Geographic Region (USD)",
                 color_col="Region", hover_data=["Region", "Revenue"])


# --- Conclusion ---
display_section_title("Conclusion")
st.markdown("""
AstraZeneca (AZN) is a formidable player in the global pharmaceutical industry, deeply integrated into a complex financial ecosystem. Its financial performance is a testament to the intricate balance between successful research and development, effective commercialization strategies, navigating stringent regulatory and pricing environments, and managing intense competition.

Key drivers of AZN's success include the strength and longevity of its patent protections, the positive outcomes of its clinical trials, evolving global healthcare spending patterns, and its agility in adapting to scientific advancements and economic shifts. Understanding the interplay of these factors—from product sales and R&D investment to market access challenges and macroeconomic influences—is crucial for assessing the long-term prospects and valuation of AstraZeneca.
""")