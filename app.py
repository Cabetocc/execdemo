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

            # Wait up to 180 seconds for latest.md to change
            max_wait_seconds = 180
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
import textwrap

st.set_page_config(layout="wide", page_title="Financial Analysis Dashboard")

# --- Helper Functions ---
def clean_text(text):
    """Cleans and wraps text for better display."""
    if text is None:
        return "N/A"
    return text.strip()

def extract_key_metrics(analysis_text):
    """
    A simple placeholder to extract potential key metrics.
    In a real application, this would involve more sophisticated NLP.
    """
    metrics = {}
    # Example: Looking for patterns like "ratio of X to Y is Z" or "growth of X by Y%"
    # This is highly simplified and would need to be robust for real-world data.
    lines = analysis_text.split('\n')
    for line in lines:
        line = line.lower()
        if "ratio" in line and (" of " in line or " and " in line):
            parts = line.split("is")
            if len(parts) > 1:
                metric_name = parts[0].replace("ratio", "").strip()
                try:
                    metric_value = float(parts[1].strip())
                    metrics[f"Ratio: {metric_name.title()}"] = metric_value
                except ValueError:
                    pass
        elif "growth" in line and "%" in line:
            parts = line.split("growth")
            if len(parts) > 1:
                try:
                    growth_value = float(parts[1].split("%")[0].strip())
                    metrics[f"Growth: {parts[0].strip().title()}"] = growth_value
                except ValueError:
                    pass
        elif "level" in line and "debt" in line:
            parts = line.split("is")
            if len(parts) > 1:
                try:
                    debt_level = float(parts[1].strip())
                    metrics[f"Debt Level: {parts[0].strip().title()}"] = debt_level
                except ValueError:
                    pass
        elif "margins" in line and ":" in line:
            parts = line.split(":")
            if len(parts) > 1:
                try:
                    margin_value = float(parts[1].strip().replace('%', ''))
                    metrics[f"Margin: {parts[0].strip().title()}"] = margin_value
                except ValueError:
                    pass
        elif "valuation" in line and "multiple" in line:
            parts = line.split(":")
            if len(parts) > 1:
                try:
                    valuation_value = float(parts[1].strip())
                    metrics[f"Valuation Multiple: {parts[0].strip().title()}"] = valuation_value
                except ValueError:
                    pass
    return metrics

def format_section_title(title):
    """Formats section titles for better readability."""
    return f"**{title}**"

def format_summary_point(point):
    """Formats individual summary points."""
    return f"- {point}"

# --- Sample Data (to simulate analysis output) ---
# In a real app, this would come from an API call or a more complex parser.
sample_analysis = {
    "AAPL": {
        "overview": "Apple Inc. is a multinational technology company headquartered in Cupertino, California. It designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories, and sells related services. Apple's key revenue drivers are its iPhone, Mac, iPad, and Wearables, Home and Accessories segments, alongside its growing Services business (App Store, Apple Music, iCloud, AppleCare, etc.).",
        "key_financial_relationships": {
            "Gross Profit Margin": "67.1%",
            "Operating Profit Margin": "29.7%",
            "Net Profit Margin": "25.3%",
            "Return on Equity (ROE)": "155.0%",
            "Debt to Equity Ratio": "1.8",
            "Current Ratio": "1.0",
            "Revenue Growth (YoY)": "2.0%",
            "EPS Growth (YoY)": "5.0%"
        },
        "market_dependencies": {
            "market_sentiment": "Generally positive, influenced by consumer spending trends and product innovation cycles.",
            "beta_vs_sp500": 1.1,
            "volatility": "Moderate, typically tracks broader tech market movements.",
            "key_drivers": ["consumer confidence", "disposable income", "new product launches", "global supply chain stability"]
        },
        "sector_connections": {
            "sector": "Technology (Consumer Electronics, Software & Services)",
            "industry_trends": "Growth in cloud computing, AI integration, subscription services, and demand for premium devices.",
            "sector_performance": "Historically strong, but subject to cyclical consumer spending and regulatory scrutiny.",
            "regulatory_impact": "Antitrust concerns, privacy regulations, and App Store policies can influence operations."
        },
        "competitor_relationships": {
            "major_competitors": ["Samsung", "Google (Alphabet)", "Microsoft", "Amazon"],
            "competitive_landscape": "Highly competitive, especially in smartphones and PCs. Apple maintains strong brand loyalty and ecosystem integration.",
            "market_share_dynamics": "Dominant in premium smartphone segment, significant player in tablets and PCs. Services continue to gain share.",
            "pricing_power": "Strong pricing power for its hardware due to brand and ecosystem."
        },
        "economic_factors": {
            "macro_influence": "Sensitive to global economic growth, inflation affecting consumer spending, and currency fluctuations (due to international sales).",
            "interest_rates": "Higher interest rates can impact consumer borrowing for expensive devices and increase the cost of debt for the company.",
            "gdp_growth": "Direct correlation with global GDP growth, especially in developed markets.",
            "fx_impact": "Significant impact from USD strength/weakness on international revenues and profits."
        },
        "revenue_drivers": [
            "iPhone Sales",
            "Mac and iPad Sales",
            "Wearables, Home and Accessories",
            "Apple Services (App Store, iCloud, Apple Music, Apple TV+)",
            "Advertising"
        ],
        "financial_highlights": {
            "income_statement": {
                "revenue": "$383.3 Billion (FY23)",
                "gross_profit": "$257.0 Billion (FY23)",
                "net_income": "$97.0 Billion (FY23)"
            },
            "balance_sheet": {
                "total_assets": "$352.6 Billion (FY23)",
                "total_liabilities": "$290.4 Billion (FY23)",
                "total_equity": "$62.2 Billion (FY23)"
            },
            "cash_flow": {
                "operating_cash_flow": "$110.5 Billion (FY23)",
                "free_cash_flow": "$99.6 Billion (FY23)"
            }
        },
        "valuation_context": {
            "pe_ratio": 28.5,
            "ps_ratio": 7.2,
            "ev_ebitda": 19.0,
            "peer_comparison": "Trades at a premium compared to many tech hardware peers, reflecting its strong brand, profitability, and ecosystem."
        },
        "risks_scenarios": {
            "key_risks": [
                "Intensifying competition",
                "Regulatory pressures (antitrust, privacy)",
                "Supply chain disruptions",
                "Dependence on iPhone sales",
                "Geopolitical tensions impacting manufacturing and sales",
                "Macroeconomic slowdown impacting consumer spending"
            ],
            "upside_scenarios": [
                "Successful new product categories (e.g., AR/VR)",
                "Accelerated growth in Services",
                "Stronger than expected consumer adoption of new iPhone models",
                "Favorable regulatory outcomes"
            ],
            "sensitivity": "Sensitive to consumer discretionary spending, global economic health, and technological innovation pace."
        },
        "catalyst_calendar": {
            "upcoming_events": [
                "Q4 2023 Earnings (expected Nov 2023)",
                "WWDC (Worldwide Developers Conference) - typically June",
                "Annual iPhone/Mac Product Launches - typically September/October"
            ]
        },
        "suggested_next_steps": [
            "Review latest 10-K and 10-Q filings for detailed financial data.",
            "Read recent analyst reports and earnings call transcripts.",
            "Compare detailed valuation multiples against a curated list of peers.",
            "Analyze geographic revenue breakdown in filings."
        ]
    },
    "TSLA": {
        "overview": "Tesla, Inc. designs, develops, manufactures, sells, leases, and arranges for the charging of electric vehicles, and generates and sells solar energy and energy storage systems. Its primary revenue streams come from electric vehicle sales and regulatory credits.",
        "key_financial_relationships": {
            "Gross Profit Margin": "18.0%",
            "Operating Profit Margin": "10.0%",
            "Net Profit Margin": "9.0%",
            "Return on Equity (ROE)": "28.0%",
            "Debt to Equity Ratio": "0.2",
            "Current Ratio": "1.5",
            "Revenue Growth (YoY)": "25.0%",
            "EPS Growth (YoY)": "30.0%"
        },
        "market_dependencies": {
            "market_sentiment": "Highly volatile, driven by Elon Musk's statements, production news, and broader market sentiment towards growth stocks and EVs.",
            "beta_vs_sp500": 1.8,
            "volatility": "Very high, subject to significant daily price swings.",
            "key_drivers": ["production numbers", "delivery targets", "Elon Musk's public statements", "competitor EV launches", "government EV incentives", "interest rates"]
        },
        "sector_connections": {
            "sector": "Automotive (Electric Vehicles), Energy Storage",
            "industry_trends": "Rapid growth in EV adoption, increasing competition, focus on autonomous driving technology, battery technology advancements.",
            "sector_performance": "High growth potential but subject to capital intensity, regulatory changes, and technological disruption.",
            "regulatory_impact": "Emissions standards, safety regulations, and EV subsidies play a crucial role."
        },
        "competitor_relationships": {
            "major_competitors": ["BYD", "Volkswagen", "Ford", "General Motors", "Rivian", "Lucid"],
            "competitive_landscape": "Increasingly crowded. Tesla is a pioneer but faces growing competition from legacy automakers and new EV startups.",
            "market_share_dynamics": "Historically dominant in premium EVs, but market share is gradually being eroded by new entrants.",
            "pricing_power": "Has shown willingness to cut prices to maintain volume, impacting pricing power."
        },
        "economic_factors": {
            "macro_influence": "Sensitive to consumer purchasing power for high-ticket items, availability of financing, and commodity prices (lithium, cobalt for batteries).",
            "interest_rates": "Higher interest rates significantly impact car affordability and the cost of capital for expansion.",
            "gdp_growth": "Correlates with global GDP growth, but also with specific trends in EV adoption and renewable energy.",
            "fx_impact": "Significant exposure to currency fluctuations due to global manufacturing and sales."
        },
        "revenue_drivers": [
            "Electric Vehicle Sales (Model S, 3, X, Y)",
            "Energy Generation and Storage (Solar Roof, Powerwall)",
            "Automotive Leasing",
            "Automotive Software and Services (FSD, Premium Connectivity)",
            "Regulatory Credits"
        ],
        "financial_highlights": {
            "income_statement": {
                "revenue": "$96.77 Billion (FY22)",
                "gross_profit": "$21.58 Billion (FY22)",
                "net_income": "$12.59 Billion (FY22)"
            },
            "balance_sheet": {
                "total_assets": "$67.45 Billion (FY22)",
                "total_liabilities": "$23.56 Billion (FY22)",
                "total_equity": "$43.89 Billion (FY22)"
            },
            "cash_flow": {
                "operating_cash_flow": "$14.71 Billion (FY22)",
                "free_cash_flow": "$7.57 Billion (FY22)"
            }
        },
        "valuation_context": {
            "pe_ratio": 75.0,
            "ps_ratio": 8.0,
            "ev_ebitda": 30.0,
            "peer_comparison": "Trades at a significant premium to traditional automakers due to its growth prospects, technology leadership, and perceived future potential (robotaxis, AI)."
        },
        "risks_scenarios": {
            "key_risks": [
                "Intense competition from established and new EV players",
                "Production ramp-up challenges and quality control issues",
                "Reliance on Elon Musk's leadership and public persona",
                "Regulatory hurdles and safety recalls",
                "Supply chain disruptions (especially batteries)",
                "Execution risk for ambitious projects (FSD, Optimus)",
                "Interest rate sensitivity affecting consumer demand"
            ],
            "upside_scenarios": [
                "Breakthroughs in autonomous driving (FSD)",
                "Successful launch and scaling of new models (Cybertruck, new platform)",
                "Significant growth in energy storage business",
                "Profitability from robotaxi network or AI services",
                "Successful battery cost reductions and production scaling"
            ],
            "sensitivity": "Extremely sensitive to news flow, production numbers, regulatory pronouncements, and Elon Musk's actions."
        },
        "catalyst_calendar": {
            "upcoming_events": [
                "Q4 2023 Earnings (expected Jan 2024)",
                "Delivery/Production Updates (quarterly)",
                "New Model Announcements/Launches (e.g., Cybertruck)",
                "Updates on FSD Beta progress"
            ]
        },
        "suggested_next_steps": [
            "Monitor production and delivery numbers closely.",
            "Track competitor EV launches and market share shifts.",
            "Read Musk's Twitter/X feed and official company updates.",
            "Analyze the impact of regulatory changes on EV incentives.",
            "Assess progress and timeline for FSD and other ambitious projects."
        ]
    }
}


# --- Streamlit App Layout ---
st.title("Financial Analysis Dashboard")

st.sidebar.header("Analysis Configuration")
ticker_input = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL")
analysis_detail = st.sidebar.selectbox(
    "Level of Detail",
    ["High-Level Overview", "Deep Quantitative Analysis"],
    index=0
)
timeframe = st.sidebar.selectbox(
    "Timeframe/Focus",
    ["Near-term Catalysts", "12-24 Month Outlook", "Long-term Secular View"],
    index=1
)
specific_concerns = st.sidebar.multiselect(
    "Specific Concerns",
    ["Valuation", "Dividend Safety", "Debt", "FX", "Commodity Exposure", "Cyclical Risk", "Regulatory Risk", "Competition"]
)

# --- Load Data ---
analysis_data = sample_analysis.get(ticker_input.upper())

if not analysis_data:
    st.warning(f"No analysis found for ticker: {ticker_input}. Please try AAPL or TSLA for a sample.")
else:
    # --- Main Content Area ---
    st.header(f"Financial Analysis for {ticker_input.upper()}")

    # --- Section: Overview ---
    st.subheader(format_section_title("Company Overview"))
    st.write(clean_text(analysis_data.get("overview", "N/A")))

    # --- Section: Key Financial Metrics ---
    st.subheader(format_section_title("Key Financial Metrics & Relationships"))
    key_metrics = analysis_data.get("key_financial_relationships", {})
    if key_metrics:
        metrics_df = pd.DataFrame(list(key_metrics.items()), columns=['Metric', 'Value'])
        # Attempt to convert values for charting
        metrics_df['Numeric_Value'] = pd.to_numeric(metrics_df['Value'].str.replace('%', '').str.replace(',', ''), errors='coerce')
        metrics_df['Type'] = metrics_df['Metric'].apply(lambda x: 'Percentage' if '%' in x else ('Ratio' if 'Ratio' in x or 'Level' in x else 'Growth'))

        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(metrics_df[['Metric', 'Value']].to_html(escape=False), use_container_width=True)

        with col2:
            # Filter for numeric values to plot
            numeric_metrics_df = metrics_df.dropna(subset=['Numeric_Value'])

            # Pie chart for percentages (margins, ROE)
            percentage_metrics = numeric_metrics_df[numeric_metrics_df['Type'] == 'Percentage']
            if not percentage_metrics.empty:
                fig_pie = px.pie(percentage_metrics,
                                 values='Numeric_Value',
                                 names='Metric',
                                 title='Key Percentage Metrics')
                st.plotly_chart(fig_pie, use_container_width=True)

            # Bar chart for growth and ratios
            other_metrics = numeric_metrics_df[numeric_metrics_df['Type'] != 'Percentage']
            if not other_metrics.empty:
                fig_bar = px.bar(other_metrics,
                                 x='Metric',
                                 y='Numeric_Value',
                                 color='Type',
                                 title='Growth & Ratio Metrics')
                st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No specific key financial relationships detailed in this sample.")

    # --- Section: Market Dependencies ---
    st.subheader(format_section_title("Market Dependencies"))
    market_deps = analysis_data.get("market_dependencies", {})
    if market_deps:
        st.write(f"**Market Sentiment:** {clean_text(market_deps.get('market_sentiment'))}")
        st.write(f"**Beta vs. S&P 500:** {market_deps.get('beta_vs_sp500', 'N/A')}")
        st.write(f"**Volatility:** {clean_text(market_deps.get('volatility'))}")
        st.write(f"**Key Drivers:** {', '.join(market_deps.get('key_drivers', ['N/A']))}")
        if 'beta_vs_sp500' in market_deps:
            beta = market_deps['beta_vs_sp500']
            if beta > 1.2:
                st.warning("High Beta: Stock is more volatile than the broader market.")
            elif beta < 0.8:
                st.info("Low Beta: Stock is less volatile than the broader market.")
            else:
                st.info("Moderate Beta: Stock volatility is similar to the broader market.")
    else:
        st.info("No specific market dependencies detailed in this sample.")

    # --- Section: Sector Connections ---
    st.subheader(format_section_title("Sector Connections"))
    sector_conns = analysis_data.get("sector_connections", {})
    if sector_conns:
        st.write(f"**Sector:** {clean_text(sector_conns.get('sector'))}")
        st.write(f"**Industry Trends:** {clean_text(sector_conns.get('industry_trends'))}")
        st.write(f"**Sector Performance:** {clean_text(sector_conns.get('sector_performance'))}")
        st.write(f"**Regulatory Impact:** {clean_text(sector_conns.get('regulatory_impact'))}")
    else:
        st.info("No specific sector connections detailed in this sample.")

    # --- Section: Competitor Relationships ---
    st.subheader(format_section_title("Competitor Relationships"))
    competitor_rels = analysis_data.get("competitor_relationships", {})
    if competitor_rels:
        st.write(f"**Major Competitors:** {', '.join(competitor_rels.get('major_competitors', ['N/A']))}")
        st.write(f"**Competitive Landscape:** {clean_text(competitor_rels.get('competitive_landscape'))}")
        st.write(f"**Market Share Dynamics:** {clean_text(competitor_rels.get('market_share_dynamics'))}")
        st.write(f"**Pricing Power:** {clean_text(competitor_rels.get('pricing_power'))}")
    else:
        st.info("No specific competitor relationships detailed in this sample.")

    # --- Section: Economic Factors ---
    st.subheader(format_section_title("Economic Factors"))
    economic_factors = analysis_data.get("economic_factors", {})
    if economic_factors:
        st.write(f"**Macro Influence:** {clean_text(economic_factors.get('macro_influence'))}")
        st.write(f"**Interest Rates Sensitivity:** {clean_text(economic_factors.get('interest_rates'))}")
        st.write(f"**GDP Growth Correlation:** {clean_text(economic_factors.get('gdp_growth'))}")
        st.write(f"**FX Impact:** {clean_text(economic_factors.get('fx_impact'))}")
    else:
        st.info("No specific economic factors detailed in this sample.")

    # --- Section: Financial Highlights ---
    st.subheader(format_section_title("Financial Highlights (Illustrative)"))
    financial_highlights = analysis_data.get("financial_highlights", {})
    if financial_highlights:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Income Statement**")
            for key, value in financial_highlights.get("income_statement", {}).items():
                st.write(f"*{key}:* {value}")

        with col2:
            st.write("**Balance Sheet**")
            for key, value in financial_highlights.get("balance_sheet", {}).items():
                st.write(f"*{key}:* {value}")

        with col3:
            st.write("**Cash Flow**")
            for key, value in financial_highlights.get("cash_flow", {}).items():
                st.write(f"*{key}:* {value}")
    else:
        st.info("No specific financial highlights detailed in this sample.")

    # --- Section: Valuation Context ---
    st.subheader(format_section_title("Valuation Context"))
    valuation_context = analysis_data.get("valuation_context", {})
    if valuation_context:
        valuation_metrics = {k: v for k, v in valuation_context.items() if k not in ['peer_comparison']}
        if valuation_metrics:
            val_df = pd.DataFrame(list(valuation_metrics.items()), columns=['Metric', 'Value'])
            val_df['Numeric_Value'] = pd.to_numeric(val_df['Value'], errors='coerce')
            st.dataframe(val_df.to_html(escape=False), use_container_width=True)

            numeric_val_df = val_df.dropna(subset=['Numeric_Value'])
            if not numeric_val_df.empty:
                fig_val = px.bar(numeric_val_df, x='Metric', y='Numeric_Value', title='Common Valuation Multiples')
                st.plotly_chart(fig_val, use_container_width=True)

        st.write(f"**Peer Comparison:** {clean_text(valuation_context.get('peer_comparison'))}")
    else:
        st.info("No specific valuation context detailed in this sample.")

    # --- Section: Risks and Scenarios ---
    st.subheader(format_section_title("Key Risks and Upside Scenarios"))
    risks_scenarios = analysis_data.get("risks_scenarios", {})
    if risks_scenarios:
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Key Risks**")
            for risk in risks_scenarios.get("key_risks", []):
                st.write(format_summary_point(clean_text(risk)))
        with col2:
            st.write("**Upside Scenarios**")
            for scenario in risks_scenarios.get("upside_scenarios", []):
                st.write(format_summary_point(clean_text(scenario)))
        st.write(f"**Sensitivity:** {clean_text(risks_scenarios.get('sensitivity'))}")
    else:
        st.info("No specific risks and scenarios detailed in this sample.")

    # --- Section: Catalyst Calendar ---
    st.subheader(format_section_title("Catalyst Calendar (Illustrative)"))
    catalyst_calendar = analysis_data.get("catalyst_calendar", {})
    if catalyst_calendar:
        st.write("**Upcoming Events:**")
        for event in catalyst_calendar.get("upcoming_events", []):
            st.write(format_summary_point(clean_text(event)))
    else:
        st.info("No specific catalyst calendar detailed in this sample.")

    # --- Section: Suggested Next Steps ---
    st.subheader(format_section_title("Suggested Next Steps"))
    next_steps = analysis_data.get("suggested_next_steps", [])
    if next_steps:
        for step in next_steps:
            st.write(format_summary_point(clean_text(step)))
    else:
        st.info("No specific next steps provided in this sample.")

# --- Footer ---
st.markdown("---")
st.markdown("This is a simplified financial analysis dashboard. Real-world analysis requires access to live data and more advanced NLP/quantitative methods.")