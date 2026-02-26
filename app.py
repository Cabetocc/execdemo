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
import altair as alt

# Set page configuration for a wider layout and title
st.set_page_config(layout="wide", page_title="SATS Ltd. Financial Analysis")

# --- Data Extraction and Preparation ---
# Manually extracting structured data from the provided text analysis.
# In a real-world scenario, this would involve NLP or parsing structured financial reports.

# 1. Peer Benchmarking Data
# Removed Mandai Wildlife Group as it's not directly comparable.
# For ranges like "15-20%", the midpoint (17.5%) is used. "High teens" is estimated as 18.5%.
peer_data = {
    "Company": ["SATS", "Gategroup", "SSP Group PLC"],
    "P/E Ratio": [30, None, 20],  # Gategroup is private, so N/A
    "YoY Revenue Growth (%)": [17.5, 18.5, 27.5],
    "EBITDA Margin (%)": [9, 11, 8],
}
df_peers = pd.DataFrame(peer_data)

# 2. Key Metrics for SATS
key_metrics = {
    "Metric": ["P/E Ratio", "YoY Revenue Growth", "EBITDA Margin", "Net Debt/EBITDA"],
    "Value": ["~30x", "~15-20%", "~8-10%", "~1.0x"],
    "Notes": [
        "Premium P/E reflecting dominant position.",
        "Strong recovery driven by air travel.",
        "Pressured by inflation, focus on cost optimization.",
        "Concerns about high debt levels post-WFS acquisition (as of late 2023)."
    ]
}
df_key_metrics = pd.DataFrame(key_metrics)

# 3. Market Sentiment Points (Qualitative)
bullish_points = [
    "Recovery in Air Travel Demand (especially Asia) driving core aviation services.",
    "Strategic Acquisition of Worldwide Flight Services (WFS) – transforms SATS into a global top-three player in air cargo logistics.",
    "Positive Earnings Revisions for FY2024/25, with SATS reporting a return to profitability in recent quarters.",
    "Government Support for Aviation Hub Status, like Singapore’s continued investment in Changi Airport (e.g., Terminal 5 development)."
]
bearish_points = [
    "High Debt Levels (~1.0x net debt/EBITDA as of late 2023) due to WFS acquisition, raising concerns about interest expense.",
    "Integration Risks associated with merging two large organizations (SATS and WFS) across different regions.",
    "Macroeconomic Headwinds: Global economic uncertainty, inflation, and potential recessions could dampen air cargo demand and consumer spending.",
    "Competitive Pressures from rivals like dnata (Emirates) and local competitors expanding their operations."
]

# --- Streamlit App Layout ---

st.title("SATS Ltd. (SATS) - Comprehensive Financial Analysis")
st.markdown("---")

st.markdown("""
    This application provides a comprehensive forward-looking financial analysis of **SATS Ltd. (ticker: SATS)**, 
    presented from the perspective of a Senior Equity Research Analyst. The analysis covers fundamental evaluations, 
    peer benchmarking, adjacent industry impacts, risk assessments, and market sentiment, with a focus on key metrics 
    and meaningful visualizations.
""")

st.markdown("---")

# 1. Company Overview
st.header("1. Company Overview")
st.markdown("""
    **SATS** is a leading food services and gateway services group in Asia, operating and managing the 
    Singapore Changi Airport's catering and airline services. Its core businesses include airline catering, 
    food retail (food courts, cafes, and restaurants), cargo handling/ground services, and now, 
    significantly expanded global air cargo logistics capabilities through the acquisition of **Worldwide Flight Services (WFS)**.
""")
st.markdown("---")

# 2. Fundamental Evaluation & Outlook (Next 3-6 Months)
st.header("2. Fundamental Evaluation & Outlook (Next 3-6 Months)")

st.subheader("Recent Performance & Outlook")
st.markdown("""
    SATS has been navigating a dynamic post-pandemic recovery. The resurgence of air travel has been a significant tailwind, 
    directly boosting its airline catering and airport services segments. While revenue has been recovering strongly, 
    profitability has been pressured by inflationary headwinds, particularly rising food costs, labor expenses, and energy prices. 
    Management is focused on cost optimization and selective price adjustments, expecting margin pressure to persist 
    in the near term, but with some stabilization as supply chain issues ease and efficiencies are realized.
""")

st.subheader("Key Catalysts")
st.markdown("""
    For the next 3-6 months, the following catalysts are expected to drive SATS's performance:
    *   **Continued Air Travel Recovery & Increased Flight Frequencies:** As airlines ramp up operations, SATS's core airline services segment will see a direct uplift, especially from higher-margin long-haul routes.
    *   **Successful Integration of SATS Food Industries (SFI):** Realization of synergies, cross-selling opportunities, and improved economies of scale from the SFI acquisition (completed early 2024).
    *   **Resilient Food Retail Performance Amidst Inflationary Pressures:** Maintaining sales volume and pricing power in its diverse food retail portfolio through effective strategies.
""")
st.markdown("---")

# 3. Key Financial Metrics
st.header("3. Key Financial Metrics for SATS")
st.markdown("A quick glance at some critical metrics for SATS, highlighting key aspects of its financial health and operational performance.")

# Display key metrics using st.columns and st.metric
cols_metrics = st.columns(len(df_key_metrics))
for i, row in df_key_metrics.iterrows():
    with cols_metrics[i]:
        st.metric(label=row["Metric"], value=row["Value"], help=row["Notes"])
st.markdown("---")

# 4. Peer Benchmarking
st.header("4. Peer Benchmarking")
st.markdown("""
    Comparing SATS directly to its closest peers can be challenging due to its unique integrated model. 
    However, we can look at broader food services and airport services companies.
""")

st.dataframe(df_peers.set_index("Company"))

st.subheader("Comparative Analysis - Visualizations")

# Melt the DataFrame for Altair charting to easily compare multiple metrics
df_peers_melted = df_peers.melt('Company', var_name='Metric', value_name='Value')

# Function to create a bar chart for a given metric
def create_peer_chart(df, metric_name, title, y_axis_label, color_column='Company'):
    chart_data = df[df['Metric'] == metric_name].dropna()
    
    # Ensure data types are correct for charting
    chart_data['Value'] = pd.to_numeric(chart_data['Value'])

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Company:N', sort=None, title='Company'),
        y=alt.Y('Value:Q', title=y_axis_label),
        color=alt.Color(color_column, legend=alt.Legend(title="Company")),
        tooltip=['Company', alt.Tooltip('Value:Q', title=y_axis_label)]
    ).properties(
        title=title
    )
    return chart

col_chart1, col_chart2, col_chart3 = st.columns(3)

with col_chart1:
    pe_chart = create_peer_chart(df_peers_melted, 'P/E Ratio', 'P/E Ratio Comparison', 'P/E Ratio')
    st.altair_chart(pe_chart, use_container_width=True)

with col_chart2:
    rev_growth_chart = create_peer_chart(df_peers_melted, 'YoY Revenue Growth (%)', 'YoY Revenue Growth Comparison', 'YoY Revenue Growth (%)')
    st.altair_chart(rev_growth_chart, use_container_width=True)

with col_chart3:
    ebitda_margin_chart = create_peer_chart(df_peers_melted, 'EBITDA Margin (%)', 'EBITDA Margin Comparison', 'EBITDA Margin (%)')
    st.altair_chart(ebitda_margin_chart, use_container_width=True)

st.markdown("""
    **Analysis:** SATS trades at a premium P/E, reflecting its dominant position at a prime hub like Singapore Changi Airport 
    and its diversified business model. Its revenue growth is strong, driven by travel recovery. Compared to SSP, which 
    is heavily exposed to Western travel markets, SATS has a strong Asian footprint, which is also experiencing significant recovery. 
    The integration of SFI is expected to improve its margin profile over time.
""")
st.markdown("---")

# 5. Adjacent Industry Analysis
st.header("5. Adjacent Industry Impact")
st.markdown("SATS is significantly influenced by trends and developments in various adjacent industries, both upstream and downstream.")

col_adj1, col_adj2 = st.columns(2)

with col_adj1:
    st.subheader("Upstream Influences")
    st.markdown("""
    1.  **Global Aviation Industry (Airlines & Aircraft Manufacturers):**
        *   **Current State:** Airlines are experiencing robust demand and increasing flight schedules; manufacturers have strong order backlogs.
        *   **Impact on SATS:** This is a **significant tailwind**. Increased flight frequencies mean more catering, ground handling, and cargo demand for SATS.
    2.  **Agricultural Commodities & Food Supply Chains:**
        *   **Current State:** While food inflation has eased, certain commodities remain elevated due to geopolitical factors, weather, and labor availability.
        *   **Impact on SATS:** This represents a **headwind**. Rising food costs directly impact SATS's cost of goods sold for catering and food retail.
    """)

with col_adj2:
    st.subheader("Downstream Influences")
    st.markdown("""
    1.  **International Tourism & Business Travel Demand:**
        *   **Current State:** Leisure travel has recovered strongly; business travel is recovering more slowly but showing renewed growth.
        *   **Impact on SATS:** This is a **major tailwind**. Robust passenger traffic at Changi Airport directly translates into higher demand for all SATS's services.
    2.  **Retail & Consumer Spending:**
        *   **Current State:** Mixed spending patterns, but travel retail often shows resilience.
        *   **Impact on SATS:** A **mixed to positive impact**. Food retail benefits from footfall, while airport retail likely benefits from increased passenger traffic.
    """)
st.markdown("---")


# 6. Market Sentiment & Competitive Positioning
st.header("6. Market Sentiment & Competitive Positioning")

st.subheader("Market Sentiment (Last 3-6 Months)")
st.markdown("Discussions around SATS have been shaped by a blend of bullish factors driving recovery and bearish concerns related to integration and macro risks.")

st.markdown("**Bullish Perspectives:**")
for point in bullish_points:
    st.markdown(f"- {point}")

st.markdown("\n**Bearish Perspectives:**")
for point in bearish_points:
    st.markdown(f"- {point}")

st.markdown(f"""
    **Recurring Themes:** Most discussions focus on **debt management** and **integration success** from the WFS acquisition 
    as the key swing factors for SATS’s stock performance over the next 12–18 months. Sentiment is cautiously optimistic 
    but tempered by concerns over leverage.
""")

st.subheader("Competitive Positioning (Post-WFS Acquisition)")
st.markdown("""
    Post-WFS acquisition, SATS is positioned as a **global #3 in air cargo handling**. Here's a summary of its competitive standing:

    *   **Strengths:** Market leadership in Asia (dominant at Changi Airport), diversified portfolio (aviation & food solutions), global scale post-WFS, and strong government ties.
    *   **Weaknesses:** Elevated debt burden compared to many peers, continued dependence on cyclical aviation volumes, and the inherent challenges of WFS integration.
    *   **Opportunities:** Structural growth in air cargo (especially e-commerce), expansion in emerging Asian markets, and leveraging digitalization and automation for efficiency.
    *   **Threats:** Geopolitical tensions impacting trade/travel, labor shortages leading to increased wage costs, and stricter environmental regulations.
""")
st.markdown("---")

# 7. Risk Assessment & Critical Findings
st.header("7. Risk Assessment & Critical Findings")

st.subheader("Bear Case for the Upcoming Quarter")
st.markdown("""
    *   **Persistent Inflationary Pressures:** Unexpected spikes in food commodity prices and sustained high labor costs could further erode SATS's operating margins.
    *   **Slower-than-Anticipated Travel Recovery:** Any resurgence in geopolitical tensions, new pandemic variants, or airline operational disruptions could directly impact passenger traffic growth.
    *   **Execution Risks in SFI Integration:** Delays or underperformance in realizing synergies from the SATS Food Industries acquisition could hinder margin improvement.
""")

st.subheader("Bull Case for the Upcoming Quarter")
st.markdown("""
    *   **Stronger-than-Expected Travel Recovery:** A faster return of passenger volumes, particularly for long-haul and premium segments, would significantly boost SATS's revenue and profitability.
    *   **Successful Synergy Realization from SFI:** Demonstrating tangible cost savings and revenue enhancements from the SFI acquisition.
    *   **Resilient Food Retail Performance and Pricing Power:** SATS's ability to maintain strong sales volumes and implement price increases in its food retail segment despite potential consumer spending slowdowns.
""")

st.subheader("Critical Findings Summary")
st.markdown("""
    *   ✅ **Major Opportunities:** Successful integration of WFS creating a global aviation services champion; structural growth in air cargo and e-commerce; and Asia’s air travel recovery.
    *   ⚠️ **Major Risks:** High debt from the WFS acquisition increasing financial risk; significant execution risk in merging SATS and WFS across different geographies and cultures; and economic slowdowns in key markets affecting cargo and passenger volumes.
""")

st.markdown("---")

st.header("Overall Outlook")
st.markdown("""
    Analysts are generally **cautiously optimistic** on SATS, with most rating it a “Hold” or “Moderate Buy.” 
    The stock’s performance over the next 12–24 months will likely hinge on debt reduction progress and visible 
    synergies from the WFS integration. Investors should monitor quarterly earnings for signs of margin 
    improvement and deleveraging.

    *This analysis is forward-looking and evidence-based but not investment advice.*
""")

st.markdown("---")
st.caption("Sources Consulted: SATS Investor Relations (Q3 FY2024 results, WFS integration updates), Analyst reports (UOB Kay Hian, DBS, OCBC, March–May 2024), Aviation industry news (FlightGlobal, CAPA), Singapore business press (The Business Times, Straits Times), Social media discussions.")