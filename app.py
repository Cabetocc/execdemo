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

# --- Configuration ---
st.set_page_config(layout="wide", page_title="EchoStar (SATS) Financial Analysis")

# --- Data Extraction (Simulated/Qualitative for Charts) ---
# Since the analysis is descriptive, we create qualitative data points
# to illustrate the relative importance or impact mentioned in the text.

# Qualitative data for Revenue Streams
revenue_data = pd.DataFrame({
    'Stream': ['Subscription Services (TV & Broadband)', 'Equipment Sales', 'Satellite Leasing'],
    'Contribution': [70, 15, 15] # Arbitrary percentages based on text description
})

# Qualitative data for Profitability Challenges
profitability_data = pd.DataFrame({
    'Challenge': ['High Capital Expenditures', 'Debt Burden', 'Operational Costs'],
    'Impact': [50, 40, 10] # Arbitrary percentages for impact severity
})

# Qualitative data for Competitive Pressures
competitive_data = pd.DataFrame({
    'Pressure': ['Price Wars (Streaming)', 'Technology Disruption (Starlink)', 'Scale Disadvantages (Larger Telecoms)'],
    'Severity': [45, 40, 15] # Arbitrary percentages for severity
})

# --- Streamlit App ---

st.title("📡 EchoStar Corporation (SATS) Financial Ecosystem Analysis")
st.markdown("---")

st.info("""
This interactive analysis is based on a comprehensive financial assessment of EchoStar Corporation (SATS), 
which completed its merger with Dish Network in December 2023. 
It covers key financial relationships, market dependencies, competitive landscape, and economic factors.
""")

# --- Company Overview ---
st.header("1. Company Overview")
st.markdown("""
- **Full Name:** EchoStar Corporation (post-merger with Dish Network, completed in December 2023).
- **Business Model:** Provides satellite communication, broadband, and streaming services globally. Operates through segments like Hughes (satellite broadband), EchoStar Satellite Services (satellite capacity), and Dish Wireless (5G network).
- **Key Products/Services:** Satellite TV (Dish Network), satellite broadband (HughesNet), satellite capacity leasing, and a nascent 5G wireless network (Dish Wireless).
- **Market Position:** A major player in satellite communications but faces intense competition from cable, fiber, and streaming services.
""")

st.markdown("---")

# --- Key Financial Relationships ---
st.header("2. Key Financial Relationships")

st.subheader("Revenue Streams")
st.write("EchoStar's primary revenue sources and their estimated contribution:")
col1, col2 = st.columns([0.6, 0.4])
with col1:
    st.dataframe(revenue_data.set_index('Stream'))
with col2:
    chart_revenue = alt.Chart(revenue_data).mark_arc(outerRadius=120).encode(
        theta=alt.Theta(field="Contribution", type="quantitative"),
        color=alt.Color(field="Stream", type="nominal", title="Revenue Stream"),
        order=alt.Order(field="Contribution", sort="descending"),
        tooltip=["Stream", alt.Tooltip("Contribution", format=".1f", title="Contribution (%)")]
    ).properties(
        title="Estimated Revenue Contribution"
    )
    st.altair_chart(chart_revenue, use_container_width=True)
st.write("") # Add some space

st.subheader("Profitability Challenges")
st.write("The company faces significant pressures on its profitability due to:")
col_p1, col_p2 = st.columns(2)
with col_p1:
    st.markdown("""
    - **High Capital Expenditures:** Extensive investments in satellite launches and 5G network rollout.
    - **Debt Burden:** Over **$20 billion** in long-term debt post-merger, leading to substantial interest expenses.
    - **Operational Costs:** Managing a vast satellite and ground infrastructure.
    """)
with col_p2:
    st.metric(label="Long-term Debt Burden", value="$20+ Billion", delta="High Impact on Profitability", delta_color="inverse")
    chart_profitability = alt.Chart(profitability_data).mark_bar(color='#B76E79').encode(
        x=alt.X('Impact', type='quantitative', title='Estimated Impact (%)'),
        y=alt.Y('Challenge', type='nominal', sort='-x', title='Challenge'),
        tooltip=['Challenge', 'Impact']
    ).properties(
        title="Major Profitability Challenges"
    )
    st.altair_chart(chart_profitability, use_container_width=True)

st.subheader("Cash Flow & Balance Sheet")
st.markdown("""
- **Cash Flow:** Operations generate cash, but heavy investments in spectrum and 5G infrastructure lead to negative free cash flow.
- **Balance Sheet:** Highly leveraged with significant intangible assets (spectrum licenses) from past acquisitions. Liquidity is managed through revolving credit facilities and potential asset sales.
""")
st.markdown("---")

# --- Market Dependencies ---
st.header("3. Market Dependencies")
st.markdown("""
EchoStar's performance is heavily influenced by:
-   **Consumer Demand:** Relies on subscription growth for TV and broadband, facing secular declines due to cord-cutting and competition.
-   **Regulatory Environment:** Heavily influenced by FCC policies on spectrum allocation, satellite licensing, and broadband subsidies (e.g., Rural Digital Opportunity Fund).
-   **Technology Shifts:** Dependent on successful deployment of its 5G network to offset satellite declines.
-   **Capital Markets:** Access to financing is critical given high debt levels; stock performance is sensitive to interest rate changes and investor sentiment.
""")
st.markdown("---")

# --- Sector Connections ---
st.header("4. Sector Connections")
st.markdown("""
EchoStar operates at the intersection of several key sectors:
-   **Satellite Communications:** Part of the broader telecom sector, facing trends like consolidation and demand for rural broadband/IoT services.
-   **Media & Entertainment:** Satellite TV competes with streaming (Netflix, Disney+) and traditional cable; content partnerships affect costs.
-   **Wireless Telecommunications:** Dish Wireless aims to be a fourth U.S. 5G carrier, competing with Verizon, AT&T, and T-Mobile.
-   **Technology:** Relies on advancements in satellite technology (e.g., LEO satellites) and 5G infrastructure.
""")
st.markdown("---")

# --- Competitor Relationships ---
st.header("5. Competitor Relationships")

st.subheader("Direct Competitors")
st.markdown("""
-   **Satellite TV/Broadband:** DirecTV (owned by AT&T), Viasat, Starlink (SpaceX).
-   **Wireless:** Verizon, AT&T, T-Mobile (for 5G ambitions).
-   **Streaming/Content:** Netflix, Hulu, YouTube TV, Disney+.
""")

st.subheader("Competitive Pressures")
st.write("The company faces intense competitive pressures:")
col_c1, col_c2 = st.columns([0.4, 0.6])
with col_c1:
    st.markdown("""
    -   **Price Wars:** Streaming services undercut satellite TV pricing significantly.
    -   **Technology Disruption:** Starlink’s LEO satellites threaten HughesNet’s geostationary broadband advantage with lower latency and higher speeds.
    -   **Scale Disadvantages:** Larger telecoms have more resources for 5G deployment and market penetration.
    """)
with col_c2:
    chart_competitive = alt.Chart(competitive_data).mark_bar(color='#E58C4B').encode(
        x=alt.X('Severity', type='quantitative', title='Estimated Severity (%)'),
        y=alt.Y('Pressure', type='nominal', sort='-x', title='Competitive Pressure'),
        tooltip=['Pressure', 'Severity']
    ).properties(
        title="Key Competitive Pressures"
    )
    st.altair_chart(chart_competitive, use_container_width=True)

st.markdown("---")

# --- Economic Factors ---
st.header("6. Economic Factors")
st.markdown("""
-   **Macroeconomic Sensitivity:** Subscription services are somewhat recession-resistant but may see churn if consumers cut discretionary spending.
-   **Interest Rates:** High debt makes SATS vulnerable to rising rates, increasing interest expenses and refinancing risks.
-   **Inflation:** Increases costs for equipment, satellite launches, and labor, potentially squeezing margins if not passed to customers.
-   **Global Supply Chains:** Disruptions can delay satellite components or consumer equipment (e.g., set-top boxes, routers).
""")
st.markdown("---")

# --- SWOT Analysis ---
st.header("7. SWOT Analysis")

st.markdown("""
<style>
.swot-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
.swot-table th, .swot-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    vertical-align: top;
}
.swot-table th {
    background-color: #f2f2f2;
    font-weight: bold;
}
.swot-strength { background-color: #d4edda; } /* Greenish */
.swot-weakness { background-color: #f8d7da; } /* Reddish */
.swot-opportunity { background-color: #cfe2ff; } /* Bluish */
.swot-threat { background-color: #fff3cd; } /* Yellowish */
</style>

<table class="swot-table">
    <thead>
        <tr>
            <th>Category</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr class="swot-strength">
            <td><strong>Strengths</strong></td>
            <td>
                <ul>
                    <li>Extensive satellite fleet and spectrum portfolio.</li>
                    <li>Nationwide 5G network potential.</li>
                    <li>Strong brand recognition in satellite TV.</li>
                </ul>
            </td>
        </tr>
        <tr class="swot-weakness">
            <td><strong>Weaknesses</strong></td>
            <td>
                <ul>
                    <li>Declining satellite TV subscribers.</li>
                    <li>High debt and negative earnings.</li>
                    <li>Execution risks in 5G rollout.</li>
                </ul>
            </td>
        </tr>
        <tr class="swot-opportunity">
            <td><strong>Opportunities</strong></td>
            <td>
                <ul>
                    <li>Rural broadband expansion with government subsidies.</li>
                    <li>5G network leasing to other carriers (e.g., Amazon, AT&T).</li>
                    <li>IoT and enterprise satellite services.</li>
                </ul>
            </td>
        </tr>
        <tr class="swot-threat">
            <td><strong>Threats</strong></td>
            <td>
                <ul>
                    <li>Intense competition from Starlink and fiber broadband.</li>
                    <li>Regulatory hurdles for 5G/satellite integration.</li>
                    <li>Technological obsolescence of geostationary satellites.</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)
st.markdown("---")

# --- Investment Considerations ---
st.header("8. Investment Considerations")
st.markdown("""
-   **Bull Case:** Successful 5G monetization, rural broadband growth, and debt reduction could drive upside.
-   **Bear Case:** Prolonged satellite declines, 5G delays, or liquidity issues may lead to further stock volatility or restructuring.
-   **Valuation:** Currently trades at low revenue multiples due to uncertainties; key metrics to watch include subscriber trends, 5G coverage milestones, and EBITDA margins.
""")
st.markdown("---")

# --- Conclusion ---
st.header("Conclusion")
st.markdown("""
EchoStar (SATS) operates in a rapidly evolving ecosystem where its legacy satellite business is challenged, but its 5G and broadband initiatives offer potential transformation. Investors must monitor execution on 5G, competitive threats from Starlink, and debt management. The stock is speculative, suited for those with high risk tolerance and a long-term view on telecom convergence.

*Note: This analysis is based on public information as of early 2024. Always conduct updated due diligence before investment decisions.*
""")