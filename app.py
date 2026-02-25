import streamlit as st

import requests
import time

WEBHOOK_URL = "https://cabetocc.app.n8n.cloud/webhook-test/stock-analysis"

ticker = st.text_input("Enter stock ticker", value="NVDA").upper().strip()
generate = st.button("Generate")

if generate:
    if not ticker:
        st.warning("Please enter a ticker.")
    else:
        with st.spinner(f"Generating analysis for {ticker}..."):
            requests.post(WEBHOOK_URL, json={"ticker": ticker}, timeout=30)
            time.sleep(2)
        st.rerun()


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Microsoft (MSFT) Financial Ecosystem Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Data and Text ---
# This data is illustrative and not real-time. In a real app, this would come from APIs.
# For demonstration, we'll use placeholder values based on the provided analysis.

# Key Metrics (Illustrative)
key_metrics_data = {
    "Metric": [
        "Intelligent Cloud Revenue (TTM)",
        "Productivity & Business Processes Revenue (TTM)",
        "More Personal Computing Revenue (TTM)",
        "Commercial Cloud ARR Growth",
        "Gross Margin",
        "Operating Margin",
        "Free Cash Flow (TTM)",
        "R&D Expense (TTM)",
        "Capital Expenditures (TTM)",
    ],
    "Value": [
        "$85.0B",
        "$70.0B",
        "$55.0B",
        "20%",
        "68%",
        "42%",
        "$75.0B",
        "$25.0B",
        "$20.0B",
    ],
    "Description": [
        "Revenue from Azure, server products, and enterprise services.",
        "Revenue from Office 365, LinkedIn, Dynamics 365.",
        "Revenue from Windows, Surface, Xbox, Search/advertising.",
        "Year-over-year growth rate for Annual Recurring Revenue of commercial cloud services.",
        "Overall company gross profit as a percentage of revenue.",
        "Overall company operating income as a percentage of revenue.",
        "Cash generated from operations after capital expenditures.",
        "Investment in research and development to drive innovation.",
        "Investment in data centers, equipment, and facilities.",
    ],
}
df_metrics = pd.DataFrame(key_metrics_data)

# Segment Revenue (Illustrative) - Simplified for visualization
segment_revenue_data = {
    "Segment": ["Intelligent Cloud", "Productivity & Business Processes", "More Personal Computing"],
    "Revenue (Illustrative TTM)": [85.0, 70.0, 55.0], # in Billions
    "Revenue %": [42.0, 33.0, 25.0],
}
df_segment_revenue = pd.DataFrame(segment_revenue_data)

# Revenue Trend (Illustrative - simplified)
revenue_trend_data = {
    "Year": [2021, 2022, 2023],
    "Total Revenue (B)": [168.0, 198.0, 211.9],
    "Intelligent Cloud (B)": [60.0, 73.0, 85.0],
    "Productivity & Business Processes (B)": [53.0, 60.0, 70.0],
    "More Personal Computing (B)": [55.0, 65.0, 56.9],
}
df_revenue_trend = pd.DataFrame(revenue_trend_data)

# --- Sidebar ---
st.sidebar.title("Microsoft (MSFT) Analysis")
st.sidebar.markdown(
    "This app analyzes the financial ecosystem of Microsoft Corporation, "
    "breaking down its business segments, market dependencies, and competitive landscape."
)
st.sidebar.markdown("---")
st.sidebar.header("Navigation")
st.sidebar.markdown("[Key Metrics](#key-metrics)")
st.sidebar.markdown("[Business Segments](#business-segments)")
st.sidebar.markdown("[Revenue Trends](#revenue-trends)")
st.sidebar.markdown("[Financial Relationships & Dependencies](#financial-relationships--dependencies)")
st.sidebar.markdown("[Competitive Landscape](#competitive-landscape)")
st.sidebar.markdown("[Economic & Market Factors](#economic--market-factors)")
st.sidebar.markdown("[Risks & Catalysts](#risks--catalysts)")
st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info(
    "This analysis is based on a qualitative financial ecosystem breakdown. "
    "Illustrative data is used for demonstration purposes."
)

# --- Main Content ---

st.title("Microsoft Corporation (MSFT): Financial Ecosystem Analysis 📊")
st.markdown(
    "An in-depth look at the intricate network of relationships, dependencies, "
    "and factors influencing Microsoft's financial performance and market position."
)
st.markdown("---")

# --- Key Metrics Section ---
st.header("Key Metrics")
st.markdown(
    "A snapshot of Microsoft's financial health and operational performance. "
    "Note: Values are illustrative and represent a general understanding."
)

# Display metrics in a more visual way
col1, col2, col3 = st.columns(3)

for index, row in df_metrics.iterrows():
    if index < 3:
        with col1:
            st.metric(row["Metric"], row["Value"], delta=None, help=row["Description"])
    elif index < 6:
        with col2:
            st.metric(row["Metric"], row["Value"], delta=None, help=row["Description"])
    else:
        with col3:
            st.metric(row["Metric"], row["Value"], delta=None, help=row["Description"])

st.markdown("---")


# --- Business Segments Section ---
st.header("Business Segments")
st.markdown(
    "Microsoft's diverse operations are categorized into three primary segments, each with unique growth drivers and market dynamics."
)

segment_col1, segment_col2 = st.columns([1, 1])

with segment_col1:
    st.subheader("Revenue by Segment")
    fig_segment_pie = px.pie(
        df_segment_revenue,
        values="Revenue %",
        names="Segment",
        title="Illustrative Revenue Contribution by Segment",
        hole=0.3,
    )
    fig_segment_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_segment_pie, use_container_width=True)

with segment_col2:
    st.subheader("Segment Summary")
    st.markdown("1.  **Intelligent Cloud (≈42% of revenue):**")
    st.markdown(
        "    *   **Core:** Azure (IaaS/PaaS), server products, enterprise services."
    )
    st.markdown(
        "    *   **Driver:** Digital transformation spend, cloud adoption. Primary growth engine."
    )
    st.markdown("2.  **Productivity and Business Processes (≈33% of revenue):**")
    st.markdown(
        "    *   **Core:** Office 365, LinkedIn, Dynamics 365."
    )
    st.markdown(
        "    *   **Driver:** Recurring revenue, enterprise stickiness, SaaS adoption."
    )
    st.markdown("3.  **More Personal Computing (≈25% of revenue):**")
    st.markdown(
        "    *   **Core:** Windows, Surface, Xbox, Search/advertising."
    )
    st.markdown(
        "    *   **Driver:** PC market cycles, consumer spending, gaming content."
    )
st.markdown("---")


# --- Revenue Trends Section ---
st.header("Revenue Trends")
st.markdown(
    "Visualizing the growth trajectory of Microsoft's total revenue and its key segments over recent years."
)

fig_revenue_trend = go.Figure()

fig_revenue_trend.add_trace(
    go.Scatter(
        x=df_revenue_trend["Year"],
        y=df_revenue_trend["Total Revenue (B)"],
        mode="lines+markers",
        name="Total Revenue",
        line=dict(color="#1f77b4", width=2),
        hovertemplate='Year: %{x}<br>Total Revenue: $%{y:.1f}B<extra></extra>',
    )
)
fig_revenue_trend.add_trace(
    go.Scatter(
        x=df_revenue_trend["Year"],
        y=df_revenue_trend["Intelligent Cloud (B)"],
        mode="lines+markers",
        name="Intelligent Cloud",
        line=dict(color="#ff7f0e", width=2),
        hovertemplate='Year: %{x}<br>Intelligent Cloud: $%{y:.1f}B<extra></extra>',
    )
)
fig_revenue_trend.add_trace(
    go.Scatter(
        x=df_revenue_trend["Year"],
        y=df_revenue_trend["Productivity & Business Processes (B)"],
        mode="lines+markers",
        name="Productivity & Business Processes",
        line=dict(color="#2ca02c", width=2),
        hovertemplate='Year: %{x}<br>Productivity & Business Processes: $%{y:.1f}B<extra></extra>',
    )
)
fig_revenue_trend.add_trace(
    go.Scatter(
        x=df_revenue_trend["Year"],
        y=df_revenue_trend["More Personal Computing (B)"],
        mode="lines+markers",
        name="More Personal Computing",
        line=dict(color="#d62728", width=2),
        hovertemplate='Year: %{x}<br>More Personal Computing: $%{y:.1f}B<extra></extra>',
    )
)

fig_revenue_trend.update_layout(
    title="Illustrative Revenue Trend (Billions USD)",
    xaxis_title="Year",
    yaxis_title="Revenue (Billion USD)",
    legend_title="Segments",
    hovermode="x unified",
    margin=dict(l=40, r=40, t=40, b=40),
    height=500,
)

st.plotly_chart(fig_revenue_trend, use_container_width=True)
st.markdown(
    "*Data is illustrative. Intelligent Cloud and Productivity segments show consistent growth, "
    "while More Personal Computing exhibits more cyclical behavior.*"
)
st.markdown("---")


# --- Financial Relationships & Dependencies Section ---
st.header("Financial Relationships & Dependencies")
st.markdown(
    "Understanding the intricate web of internal dependencies that create Microsoft's powerful ecosystem."
)

st.subheader("1. Interdependence of Cloud and Software")
st.markdown(
    "**Azure (Cloud) drives Office 365/Microsoft 365 adoption:** As businesses migrate to Azure, they increasingly adopt Microsoft 365, creating a sticky ecosystem. "
    "Conversely, the widespread use of Microsoft 365 generates data and computational needs, fueling Azure consumption. This creates a virtuous cycle."
)

st.subheader("2. Gaming (Xbox) and Content Synergy")
st.markdown(
    "**Xbox Game Pass** leverages acquired studios (Activision Blizzard) to drive recurring revenue. Azure infrastructure supports these cloud gaming initiatives."
)

st.subheader("3. LinkedIn's Data and Professional Networking")
st.markdown(
    "LinkedIn's revenue (Talent Solutions, Advertising) is enhanced by its vast professional network data. Integration into Microsoft 365 (e.g., Outlook) strengthens both platforms."
)

st.subheader("4. Segment Interdependencies")
st.markdown(
    "-   **Productivity & Business Processes** enhances enterprise stickiness, driving Azure consumption (e.g., Teams meetings on Azure)."
    "<br>-   **Intelligent Cloud (Azure)** acts as both a revenue generator and a platform that makes other businesses (Office, Dynamics, LinkedIn) more valuable via integrated services and AI."
    "<br>-   **More Personal Computing (Windows)** controls client endpoints, acting as a distribution channel for Microsoft services (Edge, Office, Store)."
)
st.markdown("---")


# --- Competitive Landscape Section ---
st.header("Competitive Landscape")
st.markdown(
    "Microsoft operates in highly competitive markets, facing giants across cloud, software, gaming, and AI."
)

competitor_data = {
    "Market": [
        "Public Cloud (IaaS/PaaS)",
        "Software & Productivity",
        "Operating Systems",
        "Gaming",
        "Artificial Intelligence",
        "Professional Networking",
    ],
    "Primary Competitors": [
        "AWS, Google Cloud",
        "Google Workspace, Salesforce",
        "Apple (macOS), Google (ChromeOS)",
        "Sony (PlayStation), Nintendo",
        "Google, Amazon, Meta",
        "Seek, Indeed, niche platforms",
    ],
    "Microsoft's Position & Strategy": [
        "Strong #2 globally. Competes on hybrid cloud, enterprise trust, stack integration.",
        "Dominant leader. Leverages M365 ecosystem and sticky subscriptions.",
        "Near-monopoly in desktop OS. Windows is a cash cow and ecosystem funnel.",
        "Major player. Focus on content (Activision), Game Pass subscription, cloud gaming.",
        "Current perceived leader via OpenAI partnership, integrating Copilot across suite.",
        "Dominant via LinkedIn, unique data for B2B marketing.",
    ],
}
df_competitors = pd.DataFrame(competitor_data)

st.dataframe(df_competitors, use_container_width=True)

st.subheader("Key Dynamics:")
st.markdown(
    "-   **Cloud Competition:** Fierce rivalry with AWS and GCP on price, features, and innovation."
    "<br>-   **AI Race:** Microsoft's strategic partnership with OpenAI is a key differentiator, but competitors are rapidly advancing."
    "<br>-   **Ecosystem Lock-in:** Microsoft leverages deep integration across its products (e.g., M365 + Azure) to create high switching costs."
    "<br>-   **Co-opetition:** Microsoft often partners with companies it competes with in other areas (e.g., Oracle running on Azure)."
)
st.markdown("---")


# --- Economic & Market Factors Section ---
st.header("Economic & Market Factors")
st.markdown(
    "External economic forces and market trends significantly influence Microsoft's performance."
)

economic_data = {
    "Factor": [
        "Enterprise IT Spending",
        "PC Market Cycles",
        "Interest Rates",
        "Foreign Exchange (FX)",
        "Labor Market",
        "Digital Transformation Spend",
        "Cloud Market Growth",
    ],
    "Impact on MSFT": [
        "Directly drives Azure and enterprise software sales. Downturns slow growth.",
        "Impacts Windows OEM revenue. Less critical but still relevant.",
        "Affects valuation multiples (higher rates = lower multiples for growth stocks).",
        "Strong USD reduces reported international revenue and profits.",
        "Tight markets increase costs but boost demand for LinkedIn and productivity tools.",
        "A primary demand driver for Azure and Microsoft 365.",
        "Azure's growth rate is key to market share narrative and valuation.",
    ],
}
df_economic = pd.DataFrame(economic_data)

st.dataframe(df_economic, use_container_width=True)
st.markdown("---")


# --- Risks & Catalysts Section ---
st.header("Risks & Catalysts")
st.markdown(
    "Key factors that could either impede or accelerate Microsoft's growth and profitability."
)

col_risk_cat1, col_risk_cat2 = st.columns(2)

with col_risk_cat1:
    st.subheader("Key Risks:")
    st.markdown("-   **Regulatory Scrutiny:** Antitrust investigations globally (cloud, gaming, AI).")
    st.markdown("-   **AI Execution Risk:** Failure to monetize AI investments or competitive gains.")
    st.markdown("-   **Cloud Growth Deceleration:** Market maturity impacting Azure growth rates.")
    st.markdown("-   **Security Breaches:** Major vulnerabilities damaging enterprise trust.")
    st.markdown("-   **Geopolitical Tensions:** Impacting market access and supply chains.")

with col_risk_cat2:
    st.subheader("Key Catalysts:")
    st.markdown("-   **AI Monetization:** Successful rollout of Copilot across all products.")
    st.markdown("-   **Margin Re-acceleration:** Leverage from AI investments as capex stabilizes.")
    st.markdown("-   **Cloud Market Share Gains:** Continued dominance in enterprise cloud.")
    st.markdown("-   **Gaming Synergies:** Realizing full potential of Activision Blizzard acquisition.")
    st.markdown("-   **New Product Innovation:** Continued leadership in AI and enterprise solutions.")

st.markdown("---")


# --- Conclusion Section ---
st.header("Conclusion: The Microsoft Ecosystem Thesis")
st.markdown(
    "Microsoft has transformed into a vertically and horizontally integrated technology powerhouse. "
    "Its strength lies in the **interconnection of its segments**: Azure fuels Office 365, which runs on Windows, secured by Microsoft's tools, and marketed via LinkedIn. This creates significant customer lock-in."
)
st.markdown(
    "The investment narrative has evolved from **'growth of Azure'** to **'monetization of AI'** across its vast installed base. While subject to broader tech spending, competition, and regulation, Microsoft's moats, financial flexibility, and strategic AI positioning make it a core holding, reflecting the health of the technology sector and global enterprise economy."
)
st.markdown(
    "The performance of MSFT serves as a key bellwether for worldwide digital transformation trends."
)

st.markdown("---")

# --- Additional Details from Analysis ---
st.header("Deeper Dive Insights")

st.subheader("Core Business Model & Revenue Drivers")
st.markdown(
    "**Shift to Recurring Revenue:** From one-time licenses to high-margin, predictable Annual Recurring Revenue (ARR) via cloud (Azure) and SaaS (Microsoft 365) has improved revenue visibility and profit stability."
)
st.markdown(
    "**Segments:**<br>"
    "1.  **Intelligent Cloud (≈42%):** Azure is the primary growth engine.<br>"
    "2.  **Productivity & Business Processes (≈33%):** High-margin, recurring revenue powerhouse.<br>"
    "3.  **More Personal Computing (≈25%):** More cyclical, tied to PC and consumer markets."
)

st.subheader("Financial Health & Capital Allocation")
st.markdown(
    "**Balance Sheet Strength:** Pristine AAA-rated balance sheet with massive cash reserves enables strategic M&A and R&D."
    "<br>**Capital Returns:** Consistent dividend growth and significant share repurchases."
    "<br>**Profit Margins:** Expanding with cloud shift, though AI investments currently impact near-term margins."
)

st.subheader("Key Competitor Dynamics")
st.markdown(
    "-   **Cloud:** Intense competition with AWS and GCP.<br>"
    "-   **AI:** Strategic OpenAI partnership is a key differentiator.<br>"
    "-   **Ecosystem Lock-in:** Leverages product integration for high switching costs.<br>"
    "-   **Co-opetition:** Partnerships with competitors in certain areas."
)