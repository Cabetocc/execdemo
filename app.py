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

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="AAPL Equity Research Analysis", initial_sidebar_state="expanded")

# --- Title and Introduction ---
st.title("🍎 Apple Inc. (AAPL) Equity Research Analysis")
st.subheader("Senior Equity Research Analyst Perspective")
st.markdown(
    "This application visualizes and summarizes a comprehensive equity research analysis of "
    "Apple Inc. (AAPL), providing a high-conviction forward-looking view."
)
st.write(f"**Date of Analysis:** March 2025 (Based on information from Q4 2024 to Q1 2025)")
st.markdown("---")


# --- Data Extraction and Preparation ---

# Key Metrics
key_metrics_data = {
    "Metric": ["P/E Ratio (TTM)", "YoY Revenue Growth", "Smartphone Market Share", "Wearables Market Share", "Services Revenue % of Total"],
    "Apple (AAPL)": ["~27x", "~3%", "~20%", "~30%+", "~20%"],
    "Samsung (SSNLF)": ["~10x", "~10% (Electronics)", "~20%", "~10%", "Lower"],
    "Google (GOOGL)": ["~25x", "~5%", "<1%", "N/A", "Higher (Ads/Cloud)"],
    "Microsoft (MSFT)": ["~35x", "~15%", "<1%", "<1%", "Higher (Cloud/Software)"]
}
df_metrics = pd.DataFrame(key_metrics_data)

# Convert numerical columns for charting
df_chart_metrics = df_metrics.copy()
df_chart_metrics["Apple (AAPL) Numeric"] = df_chart_metrics["Apple (AAPL)"].str.replace('x', '').str.replace('%', '').str.replace('+', '').astype(float, errors='ignore')
df_chart_metrics["Samsung (SSNLF) Numeric"] = df_chart_metrics["Samsung (SSNLF)"].str.replace('x', '').str.replace('%', '').str.replace(' (Electronics)', '').astype(float, errors='ignore')
df_chart_metrics["Google (GOOGL) Numeric"] = df_chart_metrics["Google (GOOGL)"].str.replace('x', '').str.replace('%', '').str.replace('<', '').astype(float, errors='ignore')
df_chart_metrics["Microsoft (MSFT) Numeric"] = df_chart_metrics["Microsoft (MSFT)"].str.replace('x', '').str.replace('%', '').str.replace('<', '').astype(float, errors='ignore')


# Company Overview
company_overview_text = """
- **Ticker/Company:** AAPL — Apple Inc.
- **Primary Industry:** Consumer electronics and services (smartphones, personal computing, wearables, software/App Store and digital services).
- **Business Model:** Premium hardware (iPhone, Mac, iPad, Apple Watch, AirPods, accessories) tightly integrated with recurring, higher-margin services (App Store, Apple Music/TV/Cloud, iCloud, AppleCare, advertising/payments). Vertical integration (in-house silicon design, close supplier relationships) and a large installed base drive recurring revenue and high gross/operating margins relative to most consumer electronics peers.
"""

# Bullish and Bearish Perspectives
bullish_perspectives = [
    "**AI Integration:** Strong anticipation for 'Apple Intelligence' to drive a significant iPhone upgrade cycle.",
    "**Services Growth:** High-margin, recurring revenue from App Store, Apple Music, iCloud, Apple TV+ providing stability.",
    "**Capital Return:** Massive shareholder returns through dividends and share buybacks supporting the stock."
]
bearish_perspectives = [
    "**China Headwinds:** Sustained competitive pressure and declining market share from rivals like Huawei; government restrictions on iPhone use.",
    "**Hardware Sales Slump:** iPhone sales weakness, particularly in China, and inconsistent iPad/Mac sales.",
    "**Regulatory Scrutiny:** Ongoing antitrust challenges (EU's DMA, U.S. DOJ lawsuit) threatening the 'walled garden' model."
]

# SWOT Analysis Data (from the second analysis block)
swot_data = {
    "Strengths": [
        "**Ecosystem Lock-in:** Unmatched integration of hardware, software, and services creates high switching costs and customer loyalty.",
        "**Brand Power & Premium Positioning:** Commands the highest profit margins in the smartphone industry.",
        "**Financial Fortress:** Massive cash reserves provide unparalleled R&D and strategic flexibility."
    ],
    "Weaknesses": [
        "**AI Perception Lag:** Seen as behind Microsoft/Google in the public AI race; needs clear consumer messaging for its 'on-device' approach.",
        "**Dependence on iPhone:** Over-reliance on a single product category for a majority of revenue makes it vulnerable to market saturation.",
        "**Limited Flexibility:** Integrated model can be slower to respond to market trends compared to Google's open Android ecosystem."
    ],
    "Opportunities": [
        "**Apple Intelligence:** A chance to redefine its products and spark a multi-year upgrade cycle.",
        "**Emerging Markets:** Growth potential in India and Southeast Asia, though at lower price points.",
        "**New Product Categories:** Long-term speculation around AR/VR glasses and automotive technology."
    ],
    "Threats": [
        "**Competition in China:** Huawei's resurgence is a direct and potent threat.",
        "**Regulatory Erosion:** Regulations (DMA, U.S. actions) could systematically weaken the competitive moat.",
        "**Market Saturation:** The global high-end smartphone market is largely mature."
    ]
}

# --- Layout and Visualization ---

# Section 1: Company Overview & Key Metrics
st.header("1. Company Overview & Key Financial Metrics")
st.markdown(company_overview_text)

st.subheader("Key Performance Indicators (Current / Projected)")
col1_m, col2_m, col3_m = st.columns(3)
with col1_m:
    st.metric(label="P/E Ratio (TTM) - AAPL", value=df_chart_metrics.loc[0, "Apple (AAPL)"])
with col2_m:
    st.metric(label="YoY Revenue Growth - AAPL", value=df_chart_metrics.loc[1, "Apple (AAPL)"])
with col3_m:
    st.metric(label="Services Revenue % of Total - AAPL", value=df_chart_metrics.loc[4, "Apple (AAPL)"])

st.markdown("---")

# Section 2: Market Sentiment & Near-Term Outlook
st.header("2. Market Sentiment & Near-Term Outlook (Next 3-6 Months)")

st.write("Overall, sentiment toward Apple remains cautiously optimistic but is tempered by significant near-term concerns. The consensus is that the company is navigating a transition period, with a recurring theme of **short-term pain** (China, hardware sales) and **long-term potential** (AI-driven supercycle).")

col_bull, col_bear = st.columns(2)
with col_bull:
    st.subheader("📈 Bullish Perspectives")
    for item in bullish_perspectives:
        st.markdown(f"- {item}")
with col_bear:
    st.subheader("📉 Bearish Perspectives & Concerns")
    for item in bearish_perspectives:
        st.markdown(f"- {item}")

st.markdown("---")

# Section 3: Fundamental Evaluation & Catalysts
st.header("3. Fundamental Evaluation & Key Catalysts")

st.markdown("""
**Recent Performance:** Apple's recent performance has been characterized by resilience, particularly within its Services segment, which continues to be a significant growth driver and margin enhancer. While iPhone sales have shown some cyclicality, the installed base and increasing customer loyalty support consistent demand. Gross margins have remained robust, a testament to pricing power and efficient supply chain management.
""")

st.subheader("Projected Performance (Next 3-6 Months)")
st.markdown("""
We anticipate continued steady performance for AAPL over the next 3-6 months, driven by a combination of seasonal factors and ongoing product cycles.
*   **iPhone:** Upcoming launch of the next iPhone generation (fall) will be a key focus; strong demand expected from loyal user base.
*   **Services:** Poised for continued double-digit growth, fueled by Apple Music, iCloud, Apple TV+, App Store, and expanding ecosystem. Offers higher margins and greater predictability.
*   **Wearables, Home, and Accessories:** Expected continued growth (Apple Watch, AirPods).
*   **Mac and iPad:** Performance sensitive to broader economic conditions and refresh cycles, but innovation should support demand.
""")

st.subheader("Key Catalysts (Next 3-6 Months)")
st.markdown("""
1.  **Next-Generation iPhone Launch & Initial Demand:** Positive reception to new features, camera improvements, and potential AI integrations could drive significant upgrade cycles.
2.  **Continued Strength in Services Growth:** Any acceleration (new bundles, expanded content, increased App Store revenue) would be a significant positive due to high margins.
3.  **Potential for AI Integration Announcements:** Concrete announcements or demonstrations of Apple's AI strategy (integrated into iOS/hardware) could create significant investor excitement.
""")

st.markdown("---")

# Section 4: Peer Benchmarking
st.header("4. Peer Benchmarking & Competitive Analysis")
st.markdown("Comparing Apple (AAPL) against key competitors across various financial and market share metrics.")

st.subheader("Peer Comparison Table")
st.dataframe(df_metrics.style.set_properties(**{'background-color': '#f0f2f6', 'color': 'black'}), hide_index=True, use_container_width=True)

st.markdown("""
**Analysis:** AAPL trades at a premium valuation compared to Samsung, reflecting its stronger brand loyalty, higher-margin Services business, and more integrated ecosystem. While Google and Microsoft have impressive growth, their primary revenue drivers (advertising and cloud, respectively) are different. Apple's strength lies in its hardware-centric ecosystem, complemented by a rapidly growing and profitable Services segment. Samsung, while a formidable competitor in hardware, lacks the same level of ecosystem lock-in and services profitability.
""")

st.subheader("Visualizing Key Peer Metrics")

col1_chart, col2_chart = st.columns(2)

# P/E Ratio Chart
with col1_chart:
    df_pe = df_chart_metrics[df_chart_metrics["Metric"] == "P/E Ratio (TTM)"].melt(id_vars=["Metric"], value_vars=["Apple (AAPL) Numeric", "Samsung (SSNLF) Numeric", "Google (GOOGL) Numeric", "Microsoft (MSFT) Numeric"], var_name="Company", value_name="P/E Ratio")
    df_pe["Company"] = df_pe["Company"].str.replace(' Numeric', '').str.replace(' (AAPL)', '').str.replace(' (SSNLF)', '').str.replace(' (GOOGL)', '').str.replace(' (MSFT)', '')
    fig_pe = px.bar(df_pe, x="Company", y="P/E Ratio", title="P/E Ratio (TTM) Comparison",
                    labels={"P/E Ratio": "P/E Ratio (x)"},
                    color="Company",
                    color_discrete_map={
                        "Apple": "#76A96E",
                        "Samsung": "#66C2A5",
                        "Google": "#FC8D62",
                        "Microsoft": "#8DA0CB"
                    })
    fig_pe.update_layout(showlegend=False)
    st.plotly_chart(fig_pe, use_container_width=True)

# YoY Revenue Growth Chart
with col2_chart:
    df_rev = df_chart_metrics[df_chart_metrics["Metric"] == "YoY Revenue Growth"].melt(id_vars=["Metric"], value_vars=["Apple (AAPL) Numeric", "Samsung (SSNLF) Numeric", "Google (GOOGL) Numeric", "Microsoft (MSFT) Numeric"], var_name="Company", value_name="Revenue Growth")
    df_rev["Company"] = df_rev["Company"].str.replace(' Numeric', '').str.replace(' (AAPL)', '').str.replace(' (SSNLF)', '').str.replace(' (GOOGL)', '').str.replace(' (MSFT)', '')
    fig_rev = px.bar(df_rev, x="Company", y="Revenue Growth", title="YoY Revenue Growth Comparison",
                     labels={"Revenue Growth": "Growth (%)"},
                     color="Company",
                     color_discrete_map={
                        "Apple": "#76A96E",
                        "Samsung": "#66C2A5",
                        "Google": "#FC8D62",
                        "Microsoft": "#8DA0CB"
                    })
    fig_rev.update_layout(showlegend=False)
    st.plotly_chart(fig_rev, use_container_width=True)

col3_chart, col4_chart = st.columns(2)

# Smartphone Market Share Chart
with col3_chart:
    df_sm_share = df_chart_metrics[df_chart_metrics["Metric"] == "Smartphone Market Share"].melt(id_vars=["Metric"], value_vars=["Apple (AAPL) Numeric", "Samsung (SSNLF) Numeric", "Google (GOOGL) Numeric", "Microsoft (MSFT) Numeric"], var_name="Company", value_name="Market Share")
    df_sm_share["Company"] = df_sm_share["Company"].str.replace(' Numeric', '').str.replace(' (AAPL)', '').str.replace(' (SSNLF)', '').str.replace(' (GOOGL)', '').str.replace(' (MSFT)', '')
    # Filter out companies with negligible market share for better visualization
    df_sm_share = df_sm_share[df_sm_share["Market Share"] > 1]
    fig_sm_share = px.pie(df_sm_share, values="Market Share", names="Company", title="Smartphone Market Share (Top Competitors)",
                          color_discrete_map={
                              "Apple": "#76A96E",
                              "Samsung": "#66C2A5"
                          })
    fig_sm_share.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_sm_share, use_container_width=True)

# Wearables Market Share Chart
with col4_chart:
    df_wear_share = df_chart_metrics[df_chart_metrics["Metric"] == "Wearables Market Share"].melt(id_vars=["Metric"], value_vars=["Apple (AAPL) Numeric", "Samsung (SSNLF) Numeric"], var_name="Company", value_name="Market Share")
    df_wear_share["Company"] = df_wear_share["Company"].str.replace(' Numeric', '').str.replace(' (AAPL)', '').str.replace(' (SSNLF)', '')
    fig_wear_share = px.pie(df_wear_share, values="Market Share", names="Company", title="Wearables Market Share (Top Competitors)",
                            color_discrete_map={
                                "Apple": "#76A96E",
                                "Samsung": "#66C2A5"
                            })
    fig_wear_share.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_wear_share, use_container_width=True)

# SWOT Analysis
st.subheader("SWOT Analysis vs. Key Peers")
col_s, col_w, col_o, col_t = st.columns(4)
with col_s:
    st.success("### 💪 Strengths")
    for item in swot_data["Strengths"]:
        st.markdown(f"- {item}")
with col_w:
    st.warning("### 🧐 Weaknesses")
    for item in swot_data["Weaknesses"]:
        st.markdown(f"- {item}")
with col_o:
    st.info("### ✨ Opportunities")
    for item in swot_data["Opportunities"]:
        st.markdown(f"- {item}")
with col_t:
    st.error("### ⚠️ Threats")
    for item in swot_data["Threats"]:
        st.markdown(f"- {item}")

st.markdown("---")

# Section 5: Adjacent Industry Impact
st.header("5. Adjacent Industry Impact")
st.write("Several external industries are significantly influencing Apple's outlook:")

# Using expanders for a cleaner look
with st.expander("Semiconductor & AI Hardware: Critical Dependency"):
    st.markdown("""
    Apple's AI ambitions depend on advanced chips. Its relationship with **TSMC** for cutting-edge 3nm and future 2nm production is vital. Any disruption in the semiconductor supply chain or failure to secure leading-edge nodes would cripple its product roadmap. Conversely, success in designing its own silicon (M-series, A-series) is a major competitive advantage.
    """)

with st.expander("Entertainment & Media: Mixed Impact"):
    st.markdown("""
    The streaming video industry (adjacent to Apple TV+) remains fiercely competitive and unprofitable for most players. This pressures Apple to continue investing heavily in content without a clear path to dominance. However, bundling services like Apple TV+ with Apple One is a key retention tool for the ecosystem.
    """)

with st.expander("Financial Technology (FinTech): Opportunity & Risk"):
    st.markdown("""
    Apple Pay and the nascent Apple Card/Buy Now, Pay Later services position Apple in the payments industry. Growth here boosts Services revenue. However, this also attracts scrutiny from financial regulators and competes with banks and dedicated fintech firms.
    """)

with st.expander("Global Trade & Geopolitics: Major Headwind"):
    st.markdown("""
    U.S.-China tensions directly impact Apple. It faces the dual challenge of navigating export controls on technology while managing its immense supply chain and market presence within China. Decoupling or "de-risking" is a costly, multi-year operational challenge.
    """)

with st.expander("Healthcare & Wearables: Growth Niche"):
    st.markdown("""
    The Apple Watch and health-focused features (ECG, temperature sensing) tie the company to the digital health monitoring trend. This strengthens ecosystem loyalty but requires navigating stringent medical device regulations.
    """)

st.markdown("---")

# Section 6: Risk Assessment
st.header("6. Risk Assessment (Upcoming Quarter)")

col_bear_case, col_bull_case = st.columns(2)

with col_bear_case:
    st.subheader("📉 Bear Case")
    st.markdown("""
    *   **Weaker-than-expected iPhone sales:** Less compelling new iPhone, increased competition, or significant economic downturn.
    *   **Stagnation or deceleration in Services growth:** Failure to introduce new high-margin services or slowdown in app store spending.
    *   **Supply chain disruptions or component cost increases:** Unforeseen issues in semiconductor supply or significant increases in key component costs.
    """)

with col_bull_case:
    st.subheader("📈 Bull Case")
    st.markdown("""
    *   **"Super Cycle" iPhone launch:** Next iPhone introduces highly sought-after features (e.g., significant AI capabilities, groundbreaking camera tech) triggering a stronger-than-anticipated upgrade cycle.
    *   **Accelerated Services growth:** Launch of new subscription bundles, a significant content hit on Apple TV+, or surge in App Store activity.
    *   **Positive AI integration announcements:** Clear and impactful demonstrations of generative AI integration enhancing user experience across devices and services.
    """)

st.markdown("---")

# Section 7: Overall Conclusion & Disclaimer
st.header("7. Overall Conclusion")
st.write(
    "Apple is at an inflection point. Its near-term performance is pressured by cyclical hardware weakness and structural challenges in China. "
    "However, the company's financial health and ecosystem strength provide a robust foundation. **The critical factor for its stock performance "
    "over the next 12-18 months will be the market's verdict on 'Apple Intelligence.'** If perceived as a compelling, must-have innovation, "
    "it could catalyze the next major growth phase. If it falls flat or is seen as merely catching up, the bear case of a stagnating hardware "
    "giant under regulatory siege will gain credence. Investors are advised to monitor China sales data, regulatory developments, and, most "
    "importantly, the early adoption metrics and reviews of its AI features in late 2025."
)

st.success("**Outlook: Positive**")

st.markdown("---")
st.caption("Disclaimer: This analysis is for informational and academic purposes and is not investment advice.")