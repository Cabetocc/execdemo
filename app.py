import streamlit as st
import pandas as pd
import altair as alt

# --- Page Configuration ---
st.set_page_config(
    page_title="Financial Ecosystem Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# --- Helper Functions ---
def highlight_key_metric(value):
    """Highlights important numerical metrics."""
    return f'<span style="color: #1f77b4; font-weight: bold;">{value}</span>'

def format_percentage(value):
    """Formats a float as a percentage string with one decimal place."""
    return f"{value:.1f}%"

def create_bar_chart(data, x_col, y_col, title, x_label="", y_label=""):
    """Creates an Altair bar chart."""
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(x_col, title=x_label if x_label else x_col),
        y=alt.Y(y_col, title=y_label if y_label else y_col),
        tooltip=[x_col, y_col]
    ).properties(
        title=title
    ).interactive()
    return chart

def create_pie_chart(data, value_col, color_col, title):
    """Creates an Altair pie chart."""
    base = alt.Chart(data).encode(
        theta=alt.Theta(value_col, stack=True)
    )
    pie = base.mark_arc(outerRadius=120).encode(
        color=alt.Color(color_col),
        tooltip=[color_col, value_col]
    )
    text = base.mark_text(radius=140).encode(
        text=alt.Text(value_col, format=".1f"),
        order=alt.Order(value_col, sort="descending"),
        color=alt.value("black")  # Set the color to black
    )
    chart = (pie + text).properties(
        title=title
    )
    return chart

# --- Data Loading and Parsing ---
# Using a simplified representation of the financial analysis for demonstration
# In a real app, you'd likely parse structured data (JSON, CSV) or use APIs

analysis_text = """
## NVDA: A Deep Dive into its Financial Ecosystem

NVIDIA Corporation (NVDA) is a dominant force in the technology sector, primarily known for its graphics processing units (GPUs). However, its influence extends far beyond gaming, impacting a wide array of industries. Analyzing NVDA requires understanding its intricate financial ecosystem, which is shaped by technological advancements, market demand, competitive pressures, and broader economic trends.

Here's a comprehensive analysis of NVDA's financial ecosystem:

### 1. Key Financial Relationships within NVDA:

*   **Revenue Drivers:**
    *   **Data Center:** This is NVDA's largest and fastest-growing segment, fueled by demand for AI training and inference, cloud computing, and high-performance computing (HPC). This segment is crucial to NVDA's valuation and future growth prospects.
    *   **Gaming:** Historically NVDA's bread and butter, gaming GPUs still represent a significant revenue stream, driven by consumer demand for immersive gaming experiences and PC upgrades.
    *   **Professional Visualization:** This segment caters to industries like design, engineering, and media, providing powerful visualization tools.
    *   **Automotive:** NVDA is a major player in the automotive industry, providing platforms for autonomous driving, in-car infotainment, and driver assistance systems.
    *   **OEM & IP:** This segment includes sales of their silicon to other manufacturers and licensing of their intellectual property.

*   **Cost Structure:**
    *   **Cost of Revenue:** Primarily driven by manufacturing costs of their complex GPUs and other hardware. This is a significant expenditure, especially given the advanced fabrication processes required.
    *   **Research & Development (R&D):** NVDA invests heavily in R&D to maintain its technological edge. This includes innovation in chip architecture, AI software, and specialized hardware. This is a critical investment for future competitiveness.
    *   **Sales, General & Administrative (SG&A):** Standard operational costs associated with running a global technology company.

*   **Profitability Metrics:**
    *   **Gross Profit Margin:** NVDA consistently boasts high gross profit margins, reflecting its strong pricing power and the value proposition of its advanced technology.
    *   **Operating Profit Margin:** Driven by the balance between gross profit and operating expenses (R&D and SG&A), this metric is a key indicator of NVDA's operational efficiency.
    *   **Net Profit Margin:** The ultimate measure of profitability after all expenses, taxes, and interest.

*   **Cash Flow Dynamics:**
    *   **Operating Cash Flow:** NVDA typically generates substantial operating cash flow, demonstrating its ability to convert sales into cash. This cash is vital for funding R&D, acquisitions, and returning value to shareholders.
    *   **Capital Expenditures (CapEx):** Investments in manufacturing facilities, research labs, and infrastructure.
    *   **Free Cash Flow (FCF):** A critical metric indicating the cash available after CapEx, which can be used for debt repayment, dividends, share buybacks, or strategic investments.

### 2. Market Dependencies:

*   **Demand for AI and Machine Learning:** This is the single most significant market dependency for NVDA. The exponential growth in AI applications across various sectors directly translates to demand for NVDA's data center GPUs.
*   **Growth in Cloud Computing:** Major cloud providers (AWS, Azure, Google Cloud) are significant customers for NVDA's data center solutions, making their expansion plans and infrastructure investments crucial.
*   **Consumer Spending on Gaming:** While less dominant than data center, the health of the global PC gaming market and consumer willingness to upgrade gaming hardware directly impact NVDA's gaming segment.
*   **Automotive Industry Trends:** The shift towards electric vehicles (EVs) and autonomous driving technologies is a growing dependency for NVDA's automotive segment.
*   **Semiconductor Supply Chain:** NVDA is heavily reliant on advanced semiconductor foundries (like TSMC) for manufacturing its chips. Disruptions in this supply chain can severely impact production and revenue.
*   **Geopolitical Factors:** Trade tensions, export controls, and regional political stability can affect NVDA's access to manufacturing partners and key markets.

### 3. Sector Connections:

*   **Semiconductor Sector:** NVDA is a leader in the high-performance computing segment of the semiconductor industry. Its performance is closely watched as a bellwether for the broader chip market.
*   **Cloud Computing Sector:** NVDA's data center products are integral to the infrastructure of major cloud providers, creating a symbiotic relationship.
*   **Artificial Intelligence (AI) Sector:** NVDA is a foundational enabler of the AI revolution, providing the hardware that powers AI research, development, and deployment.
*   **Gaming & Entertainment Sector:** NVDA's GPUs are essential for modern gaming, influencing the capabilities of consoles and PCs and impacting game development.
*   **Automotive Sector:** As the industry embraces electrification and autonomy, NVDA's role in providing advanced computing platforms connects it deeply to automotive innovation.
*   **Enterprise Hardware Sector:** NVDA's high-performance computing solutions are used by enterprises for various tasks beyond AI, including scientific simulations and data analytics.

### 4. Competitor Relationships:

*   **Advanced Micro Devices (AMD):** AMD is NVDA's primary competitor in both the GPU market (gaming and data center) and increasingly in AI accelerators. AMD's recent progress in its Instinct accelerators for data centers poses a direct threat.
*   **Intel:** While Intel has historically focused on CPUs, it is making a significant push into discrete GPUs (both gaming and data center) and AI accelerators, posing a future competitive threat.
*   **Qualcomm, Broadcom, and other specialized chip designers:** These companies compete in specific niches, particularly in the automotive and networking segments.
*   **Cloud Providers (in-house chip development):** Companies like Amazon (AWS Inferentia, Trainium), Google (TPUs), and Microsoft are investing in designing their own custom AI chips, aiming to reduce reliance on third-party vendors like NVDA. This represents a long-term strategic challenge.
*   **Emerging AI Chip Startups:** A constant stream of new startups are developing innovative AI-specific hardware, which could disrupt the market.

### 5. Economic Factors Impacting NVDA:

*   **Global Economic Growth:** Strong economic growth generally translates to higher demand for technology, benefiting NVDA's data center and gaming segments. Conversely, economic downturns can dampen consumer and enterprise spending.
*   **Inflation and Interest Rates:** High inflation can increase manufacturing costs, while rising interest rates can make it more expensive for NVDA and its customers to borrow money, potentially slowing down investment in new technologies.
*   **Supply Chain Costs and Availability:** Fluctuations in the cost of raw materials, manufacturing capacity, and logistics significantly impact NVDA's cost of goods sold and ability to meet demand.
*   **Technological Advancements and R&D Spending:** The pace of innovation is a critical economic driver. Companies that invest heavily in R&D and can bring next-generation products to market quickly tend to thrive.
*   **Government Policies and Regulations:** Trade policies, export controls (especially concerning AI chips to certain regions), and incentives for technology development can have a material impact.
*   **Capital Markets and Investor Sentiment:** NVDA's valuation is heavily influenced by investor confidence in its future growth. Market sentiment towards technology stocks and AI specifically plays a significant role.
*   **Currency Exchange Rates:** As a global company, fluctuations in currency exchange rates can impact NVDA's reported revenues and profits.

### Conclusion:

NVIDIA operates within a dynamic and highly competitive financial ecosystem. Its success is deeply intertwined with the explosive growth of AI and cloud computing, making these its most critical growth drivers. However, it faces significant competition from established players like AMD and Intel, as well as the emerging threat of in-house chip development by major cloud providers.

NVDA's ability to maintain its technological leadership through relentless R&D, secure its supply chain, and adapt to evolving market demands and economic conditions will be crucial for its continued financial success. Investors will closely monitor its performance in the data center segment, its competitive positioning against emerging threats, and its ability to capitalize on new technological frontiers. Understanding these interconnected factors is essential for a comprehensive analysis of NVDA's stock.

---

Below is a concise, practical “financial ecosystem” analysis for NVDA (NVIDIA Corporation). I cover the company’s revenue and cost relationships, market and sector linkages, competitive dynamics, supply‑chain and customer dependencies, macro and policy risks, and the key indicators you should watch. Note: my factual cutoff is June 2024 — for the latest data (revenues, margins, guidance, product launches, regulatory developments) check NVIDIA’s most recent filings and earnings releases.

1) Company / business overview (context)
- Ticker: NVDA (Nasdaq). Primary business: high‑performance GPUs and AI/accelerated compute platforms plus associated software and networking solutions.
- Revenue drivers: data center (AI training + inference accelerators), gaming GPUs, professional visualization, automotive/edge, OEM & embedded, plus network and interconnect products (Mellanox assets integrated into data center stack). NVIDIA also monetizes software (CUDA ecosystem, enterprise AI stacks, drivers, SDKs) which increases customer “stickiness” and translates hardware sales into platform value.

2) Major revenue streams and financial relationships
- Data center: Historically the fastest‑growing and highest‑margin segment. Sales tied to hyperscaler capex cycles, AI model training demand, and adoption of inference deployments. Large orders are lumpy and can materially affect quarter/annual results.
- Gaming: Drives volume, but is more cyclical and sensitive to consumer spending, GPU cycle timing, and crypto mining demand (which has diminished post‑Ethereum merge).
- Professional visualization & automotive: Smaller but strategic; longer sales cycles and often tied to OEM relationships and software integration.
- Software & services: Lower % of revenue but higher margin and recurring — licensing, NVIDIA AI Enterprise, SDK support, and cloud marketplace placements.
- Networking/interconnect: Mellanox NICs and switches help vertically integrate NVIDIA’s data center offerings, enhancing per‑system ASP (average selling price).

3) Key customers and concentration risks
- Hyperscalers/cloud providers (Amazon, Microsoft, Google, Meta, Alibaba, Baidu, etc.) are major buyers for data center GPUs. A few customers account for a large share of revenue; their demand swings greatly influence NVDA’s top line and inventory dynamics.
- OEMs and system integrators (Dell, HPE, Lenovo, Supermicro) are also important; enterprise refresh cycles affect gaming/visualization revenue.

4) Supply chain & manufacturing dependencies
- Foundry concentration: Heavy reliance on TSMC for leading‑edge process nodes for high‑performance GPUs (node allocation and capacity are critical). Any TSMC capacity constraints, yield issues, or geopolitical risks involving Taiwan materially affect supply.
- Memory suppliers: HBM providers (Micron, Samsung, SK Hynix) affect product performance, cost, and availability. HBM pricing and supply swings impact margins and the ability to ship top‑end cards.
- Packaging/test partners: Outsourced partners (e.g., ASE, Amkor and others) can be bottlenecks for assembly/packaging.
- Suppliers for interconnect and networking components are also relevant (post‑Mellanox integration reduces some dependency but still requires complex components).

5) Technology & ecosystem moat
- CUDA ecosystem: A major competitive advantage — broad software libraries, developer adoption, and model optimization create switching costs for customers. This supports long‑term hardware demand and pricing power.
- Integrated stack: GPUs + networking + software suites (NVIDIA AI Enterprise, drivers, SDKs) create a vertically integrated solution that is attractive to hyperscalers and enterprises running large AI workloads.

6) Main competitors and how they impact NVIDIA
- AMD: Competes on GPUs for gaming and data center accelerators (Instinct line). AMD offers x86 + GPU integrations and has improved data center presence; pricing and performance competition can pressure ASPs and share.
- Intel: Competes via discrete GPUs, data center accelerators, and Habana accelerators (if still relevant). Intel’s scale in CPUs gives it a channel advantage, but historically trailing in GPU performance.
- Cloud providers’ custom silicon: Google TPU family, AWS Inferentia/Trainium, Meta custom HW, and other hyperscaler ASICs for inference/training reduce dependency on NVIDIA for certain workloads (especially inference at scale). If cloud providers shift meaningful workloads to their own accelerators, NVIDIA’s data center growth could be impacted.
- Specialized accelerator startups: Cerebras, Graphcore, Groq and others target AI training/inference markets; they can win specific workloads but have limited share vs NVIDIA’s ecosystem.
- Edge/phone vendors: Qualcomm, Apple and others compete at edge AI inference and consumer SoCs (different market but can reduce NVIDIA opportunities in certain segments).

7) Macroeconomic and market dependencies
- Interest rates & risk premia: NVIDIA’s valuation is tied to growth expectations; rising rates/flattening growth expectations compress multiples for high‑growth tech.
- Data center capex cycles: Hyperscaler and enterprise spending patterns drive demand for high‑end accelerators; slowdowns cause rapid inventory adjustments and weaker bookings.
- Consumer spending: Impacts gaming GPU sales (seasonality around new game releases and holidays).
- Semiconductor cycle: Capital intensity means swings in demand and inventory impact revenue volatility; margin pressure occurs when pricing weakens.
- Memory & component price cycles: HBM and other component price movements affect cost of goods sold and gross margin.

8) Geopolitics, regulation, and policy risks
- Export controls & sanctions: U.S. restrictions on advanced AI chips to China and related licensing rules can materially change addressable markets and cause product redesigns (e.g., creation of “China‑specific” SKUs). Policy shifts can either expand or constrain revenue streams.
- Supply chain concentration in Taiwan (TSMC) creates geopolitical exposure (cross‑strait tensions, natural disaster risk).
- Antitrust & competition regulation: Big tech rivalry and regulatory scrutiny can affect partnerships and M&A opportunities.

9) Financial characteristics to monitor (key KPIs)
- Revenue growth by segment (Data center vs Gaming vs Professional vs Automotive).
- Gross margin and ASP trends (data center ASPs typically lift margins).
- R&D and operating expense trajectory (investment to maintain tech lead vs margin tradeoffs).
- Operating leverage and free cash flow generation (important for buybacks, M&A).
- Inventory levels and days sales of inventory (to detect channel stuffing or end‑market weakness).
- Large customer order concentration and any shift in top customer mix.
- Capital allocation: share repurchases, dividends, and M&A activity.

10) Valuation & investor sensitivities
- Market assigns premium multiple to NVDA when growth visibility (AI demand, data center bookings) is strong; multiples compress when hyperscaler demand is uncertain or macro risk rises.
- Investors watch guidance — because forward bookings and shipments can swing expectations materially.
- Long‑term valuation depends on TAM assumptions for AI accelerators, software monetization, and networking penetration.

11) Scenario risks and stress points
- Demand shock from hyperscalers or a pivot to custom accelerators.
- TSMC capacity or yield problems creating product shortages (or inability to scale).
- Export control tightening that reduces access to China (or forces lower‑performance SKUs).
- Competitive architectures or major open‑source momentum that undermines CUDA lock‑in.
- Rapid price erosion / increased supply leading to margin compression.

12) Where to get the most informative near‑term signals
- NVIDIA quarterly earnings (segment revenue detail and guidance).
- 10‑K/10‑Q (customer concentration, risk factors, backlog).
- TSMC capacity commentary and foundry allocation notes.
- Hyperscaler capital expenditure reports and cloud instance pricing/availability.
- Memory supplier earnings (Micron, Samsung, SK Hynix) for HBM pricing trends.
- Industry conferences (GTC, Computex) for product roadmaps and software announcements.
- Export control and government policy announcements from the U.S., EU, and China.

13) Summary view (ecosystem map in words)
- NVIDIA sits at the intersection of semiconductors, AI software, cloud infrastructure, and networking. Its financial performance is a function of AI adoption (driving high‑ASP, high‑margin data center GPU sales), hyperscaler capex cycles, supply chain capacity (TSMC, HBM suppliers), and the stickiness of its CUDA/software ecosystem. Major threats are geopolitical/export controls, hyperscalers internalizing workloads with custom silicon, and competition that erodes performance or price advantage. Key drivers to watch are data center revenue/growth, margin trends, customer concentration shifts, foundry and HBM supply, and software/recurring revenue traction.

If you want, I can:
- Pull together a watchlist of the most recent quarterly KPIs (revenue by segment, gross margin, EPS, guidance) from the latest filings (you’d need to confirm a date range).
- Provide a competitor valuation comparison (P/S, EV/Revenue, P/E) using the most recent market data you provide or authorize me to fetch.
"""

# --- Data Extraction (Simplified) ---
# In a real-world scenario, this would involve more robust parsing or a structured data source.
# This is a simplified extraction for demonstration purposes.

# Key Metrics (Example values, these should be dynamically extracted or provided)
key_metrics_data = {
    "Ticker": "NVDA",
    "Primary Business": "High-performance GPUs & AI platforms",
    "Market Share (Discrete GPU)": "80%",
    "Gross Margin (Recent)": "74.0%",
    "Operating Margin (Recent)": "57.0%",
    "Net Income Margin (Recent)": "46.0%",
    "ROE (Recent)": "70.0%",
    "Free Cash Flow (Est.)": "$17B",
    "R&D Investment (Annual)": "$8B",
    "Net Cash Position": "$18B"
}

# Revenue Streams Data (Example values)
revenue_streams_data = {
    "Data Center": 80.0,
    "Gaming": 16.0,
    "Professional Visualization": 3.0,
    "Automotive": 2.0,
    "OEM & IP": 0.0 # Assuming this is part of others or zero for simplicity
}
revenue_df = pd.DataFrame(list(revenue_streams_data.items()), columns=['Segment', 'Percentage'])

# Competitor Data (Example)
competitor_data = {
    "Competitor": ["AMD", "Intel", "Google (TPU)", "AWS (Inferentia)", "Meta Custom"],
    "Impact": ["Direct GPU & AI Accelerator Competition", "Discrete GPU & AI Chip Competition", "Custom AI Accelerator (Cloud)", "Custom AI Accelerator (Cloud)", "Custom AI Accelerator (Cloud)"]
}
competitor_df = pd.DataFrame(competitor_data)

# Market Dependencies (Example)
market_dependencies_data = {
    "Dependency": ["Demand for AI/ML", "Cloud Computing Growth", "Consumer Gaming Spending", "Automotive Trends", "Semiconductor Supply Chain", "Geopolitical Factors"],
    "Impact": ["Critical Growth Driver", "Key Customer Base", "Significant Revenue Stream", "Emerging Growth Area", "Manufacturing Reliant", "Market Access & Production Risk"]
}
market_dependencies_df = pd.DataFrame(market_dependencies_data)

# --- Sidebar ---
st.sidebar.title("NVIDIA Financial Ecosystem Analysis")
st.sidebar.markdown("This app provides an overview of NVIDIA's financial landscape, key metrics, and market interdependencies.")
st.sidebar.markdown("---")
st.sidebar.header("Sections")
st.sidebar.markdown("- **Key Metrics & Overview**")
st.sidebar.markdown("- **Revenue Streams**")
st.sidebar.markdown("- **Profitability & Financial Health**")
st.sidebar.markdown("- **Market & Sector Connections**")
st.sidebar.markdown("- **Competitive Landscape**")
st.sidebar.markdown("- **Economic & Geopolitical Factors**")
st.sidebar.markdown("- **Risks & Catalysts**")
st.sidebar.markdown("- **Conclusion**")

# --- Main Content ---

# --- Section 1: Key Metrics & Overview ---
st.header("1. Key Metrics & Overview")

st.markdown("""
NVIDIA Corporation (NVDA) is a pivotal player in the technology sector, primarily renowned for its **Graphics Processing Units (GPUs)**. Its financial ecosystem is deeply intertwined with the rapid advancements in AI, cloud computing, and high-performance computing.
""")

# Display Key Metrics using Markdown and HTML for styling
st.subheader("Core Financial Snapshot")
metric_html = "<table>"
for key, value in key_metrics_data.items():
    metric_html += f"<tr><td style='padding-right: 10px;'><b>{key}:</b></td><td style='text-align: right;'>{value}</td></tr>"
metric_html += "</table>"
st.markdown(metric_html, unsafe_allow_html=True)

st.markdown("---")

# --- Section 2: Revenue Streams ---
st.header("2. Revenue Streams")

st.markdown("""
NVDA's revenue is diversified across several key segments, with **Data Center** being the dominant and fastest-growing contributor.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Revenue Mix (Example Data)")
    st.markdown("The pie chart below illustrates the approximate revenue distribution across NVDA's major business segments.")
    # Create and display the pie chart for revenue streams
    revenue_pie_chart = create_pie_chart(revenue_df, "Percentage", "Segment", "NVDA Revenue Segments")
    st.altair_chart(revenue_pie_chart, use_container_width=True)

with col2:
    st.subheader("Key Revenue Drivers")
    st.markdown("""
    *   **Data Center**: Fueled by AI training/inference, cloud computing, and High-Performance Computing (HPC). This segment is critical for NVDA's valuation and future growth.
    *   **Gaming**: Historically the core business, still a significant revenue stream driven by consumer demand for advanced gaming experiences.
    *   **Professional Visualization**: Caters to industries like design and engineering.
    *   **Automotive**: Growing segment providing platforms for autonomous driving and in-car systems.
    *   **OEM & IP**: Includes sales to other manufacturers and IP licensing.
    """)
    st.markdown("---")
    st.subheader("Cost Structure Insights")
    st.markdown("""
    *   **Cost of Revenue**: Primarily manufacturing costs for complex GPUs.
    *   **R&D**: Heavy investment to maintain technological leadership in chip architecture and AI software.
    *   **SG&A**: Standard operating costs.
    """)

st.markdown("---")

# --- Section 3: Profitability & Financial Health ---
st.header("3. Profitability & Financial Health")

st.markdown("""
NVDA consistently demonstrates exceptionally high profitability metrics, reflecting its strong market position and pricing power.
""")

# Placeholder for Profitability Metrics
profitability_metrics = {
    "Metric": ["Gross Profit Margin", "Operating Profit Margin", "Net Profit Margin"],
    "Value": [74.0, 57.0, 46.0]
}
profitability_df = pd.DataFrame(profitability_metrics)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Profitability Ratios")
    st.markdown("These metrics highlight NVDA's efficiency and market strength:")
    profit_bar_chart = create_bar_chart(
        profitability_df,
        "Metric",
        "Value",
        "Profitability Margins",
        y_label="Percentage (%)"
    )
    st.altair_chart(profit_bar_chart, use_container_width=True)

with col2:
    st.subheader("Cash Flow Dynamics")
    st.markdown("""
    *   **Operating Cash Flow**: NVDA generates substantial operating cash flow, crucial for funding R&D, acquisitions, and shareholder returns.
    *   **Free Cash Flow (FCF)**: Indicates significant cash availability after capital expenditures, enabling strategic flexibility.
    *   **Balance Sheet Strength**: A robust net cash position provides financial flexibility for growth initiatives.
    """)

st.markdown("---")

# --- Section 4: Market & Sector Connections ---
st.header("4. Market & Sector Connections")

st.markdown("""
NVDA operates at the nexus of several critical and rapidly evolving industries.
""")

# Market Dependencies Chart
st.subheader("Key Market Dependencies")
dependency_bar_chart = create_bar_chart(
    market_dependencies_df,
    "Dependency",
    "Impact",
    "NVDA's Market Dependencies",
    y_label="Significance"
)
st.altair_chart(dependency_bar_chart, use_container_width=True)

st.markdown("---")

st.subheader("Sector Interdependencies")
st.markdown("""
*   **Semiconductor Sector**: NVDA is a bellwether for the high-performance computing segment.
*   **AI/ML Infrastructure**: As a foundational enabler of AI hardware.
*   **Cloud Computing**: Integral to cloud provider offerings.
*   **Gaming & Entertainment**: Essential hardware for modern gaming.
*   **Automotive**: Key player in autonomous driving and in-car tech.
*   **Enterprise Hardware**: Powers advanced simulations and data analytics.
""")

st.markdown("---")

# --- Section 5: Competitive Landscape ---
st.header("5. Competitive Landscape")

st.markdown("""
NVDA faces intense competition from established players, cloud providers developing custom silicon, and emerging startups.
""")

st.subheader("Major Competitors")
st.dataframe(competitor_df, use_container_width=True, hide_index=True)

st.markdown("""
*   **Direct Competitors**: AMD (GPUs, AI accelerators), Intel (GPUs, AI chips).
*   **Custom Silicon**: Cloud giants (Google, AWS, Meta) are increasingly developing in-house AI chips, posing a strategic challenge.
*   **Emerging Startups**: Develop specialized AI hardware that can target specific workloads.
*   **Ecosystem Moat**: NVDA's CUDA ecosystem provides a significant competitive advantage through software libraries and developer adoption, creating high switching costs.
""")

st.markdown("---")

# --- Section 6: Economic & Geopolitical Factors ---
st.header("6. Economic & Geopolitical Factors")

st.markdown("""
NVDA's financial performance is significantly influenced by broader economic trends and geopolitical developments.
""")

st.subheader("Economic Factors")
st.markdown("""
*   **Global Economic Growth**: Directly impacts demand for technology products.
*   **Interest Rates & Inflation**: Affects borrowing costs and R&D investment.
*   **Supply Chain Costs**: Fluctuations in raw materials and manufacturing impact COGS.
*   **Technological Advancements**: Pace of innovation is a critical driver.
""")

st.subheader("Geopolitical & Regulatory Risks")
st.markdown("""
*   **Export Controls & Sanctions**: U.S. policies impacting sales to regions like China.
*   **Supply Chain Concentration**: Heavy reliance on TSMC in Taiwan creates geopolitical exposure.
*   **Antitrust Scrutiny**: Regulatory oversight of large technology companies.
*   **Currency Exchange Rates**: As a global company, FX fluctuations impact revenue and profit.
""")

st.markdown("---")

# --- Section 7: Risks & Catalysts ---
st.header("7. Risks & Catalysts")

st.markdown("""
Understanding potential risks and growth catalysts is crucial for a comprehensive analysis.
""")

st.subheader("Key Risks")
st.markdown("""
*   **Customer Concentration**: High reliance on a few major cloud providers.
*   **Supplier Concentration**: Dependence on TSMC for advanced manufacturing.
*   **Inventory Corrections**: Potential for channel buildup and demand slowdowns.
*   **Competition**: From AMD, Intel, and custom silicon by cloud providers.
*   **Geopolitical Tensions**: Impacting supply chains and market access.
""")

st.subheader("Growth Catalysts")
st.markdown("""
*   **AI Market Expansion**: Continued explosive growth in AI/ML adoption.
*   **Platform Expansion**: Strengthening the CUDA ecosystem and software offerings.
*   **New Markets**: Growth in automotive, Omniverse, robotics, and healthcare.
*   **Vertical Integration**: Expanding into networking and systems.
""")

st.markdown("---")

# --- Section 8: Conclusion ---
st.header("8. Conclusion")

st.markdown("""
NVIDIA operates at the forefront of transformative technological trends, including AI, cloud computing, and accelerated computing. Its financial ecosystem is characterized by:

*   **Exceptional Profitability**: Driven by its dominant market position and high-value offerings.
*   **Platform Moat**: The CUDA software ecosystem creates significant competitive barriers.
*   **Strategic Dependencies**: Reliant on key suppliers like TSMC and major cloud customers.
*   **Cyclical Exposure**: Vulnerable to capital expenditure cycles and market inventory corrections.
*   **Geopolitical Sensitivity**: Affected by international trade policies and supply chain risks.

NVDA's stock performance is closely tied to the sustained growth in AI investments, the broader semiconductor market sentiment, and its ability to navigate competitive pressures and geopolitical complexities. Monitoring key indicators like data center revenue growth, margin trends, customer concentration, and supply chain health provides critical insights into its future trajectory.
""")

st.markdown("---")
st.markdown("This analysis is based on information available up to June 2024. For the latest data, please refer to NVIDIA's official filings and earnings reports.")
