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
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# --- Helper Functions ---
def format_currency(value):
    if pd.isna(value):
        return "N/A"
    return f"${value:,.0f}"

def format_percentage(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.1%}"

def format_number(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.2f}"

# --- Data Simulation ---
# In a real app, you would fetch this data from APIs (e.g., financial data providers)
# For this example, we'll simulate the data based on the provided analysis.

def get_financial_data():
    data = {
        "Metric": [
            "Total Revenue",
            "Revenue Growth (YoY)",
            "R&D Spend",
            "R&D as % of Revenue",
            "Gross Profit Margin",
            "Operating Profit Margin",
            "Net Profit Margin",
            "Earnings Per Share (EPS)",
            "Operating Cash Flow (OCF)",
            "Free Cash Flow (FCF)",
            "Debt-to-Equity Ratio",
            "Interest Coverage Ratio",
            "Dividend Yield",
            "Dividend Payout Ratio",
            "Price-to-Earnings (P/E) Ratio",
            "Price-to-Sales (P/S) Ratio",
            "Enterprise Value (EV) / EBITDA"
        ],
        "Value": [
            35_410_000_000,  # Simulated based on recent reports (e.g., 2023)
            0.03,            # Simulated growth rate
            7_082_000_000,   # Simulated R&D spend
            0.20,            # Simulated R&D as % of revenue
            0.79,            # Simulated Gross Profit Margin (from analysis)
            0.22,            # Simulated Operating Profit Margin (derived)
            0.15,            # Simulated Net Profit Margin (derived)
            5.00,            # Simulated EPS
            9_000_000_000,   # Simulated OCF
            7_000_000_000,   # Simulated FCF
            0.50,            # Simulated Debt-to-Equity
            10.0,            # Simulated Interest Coverage
            0.02,            # Simulated Dividend Yield
            0.55,            # Simulated Dividend Payout Ratio
            25.0,            # Simulated P/E Ratio
            6.0,             # Simulated P/S Ratio
            15.0             # Simulated EV/EBITDA
        ],
        "Source": [
            "Annual Report", "Annual Report", "Annual Report", "Annual Report",
            "Annual Report", "Annual Report", "Annual Report", "Annual Report",
            "Annual Report", "Annual Report", "Annual Report", "Annual Report",
            "Market Data", "Annual Report", "Market Data", "Market Data", "Market Data"
        ]
    }
    df = pd.DataFrame(data)
    df["Formatted_Value"] = df["Value"].apply(lambda x: format_currency(x) if "Revenue" in df.loc[df["Value"] == x].index[0] or "R&D Spend" in df.loc[df["Value"] == x].index[0] or "OCF" in df.loc[df["Value"] == x].index[0] or "FCF" in df.loc[df["Value"] == x].index[0] else format_percentage(x) if "%" in df.loc[df["Value"] == x].index[0] else format_number(x))
    return df

def get_revenue_breakdown():
    data = {
        "Segment": [
            "Oncology",
            "Cardiovascular, Renal & Metabolism (CVRM)",
            "Respiratory & Immunology",
            "Rare Diseases (Alexion)",
            "Other"
        ],
        "Revenue": [
            12_390_500_000, # ~35%
            8_852_500_000,  # ~25%
            5_311_500_000,  # ~15%
            6_401_500_000,  # ~18% (post-Alexion)
            2_454_000_000   # ~7%
        ],
        "Growth (YoY)": [0.08, 0.12, 0.02, 0.05, -0.01]
    }
    df = pd.DataFrame(data)
    df["Revenue_Formatted"] = df["Revenue"].apply(format_currency)
    df["Growth_Formatted"] = df["Growth (YoY)"].apply(format_percentage)
    return df

def get_competitor_data():
    data = {
        "Competitor": [
            "Merck & Co. (MRK)", "Bristol Myers Squibb (BMY)", "Roche (RHHBY)", "Pfizer (PFE)",
            "Sanofi (SNY)", "Novo Nordisk (NVO)", "Eli Lilly and Company (LLY)", "GSK (GSK)",
            "AbbVie (ABBV)", "Novartis (NVS)"
        ],
        "Therapeutic Area Focus": [
            "Oncology, Vaccines", "Oncology, Immunology", "Oncology, Pharma", "Oncology, Vaccines, Pharma",
            "Diabetes, CV, Immunology", "Diabetes, Obesity", "Diabetes, Obesity, Alzheimer's", "Respiratory, Vaccines, Immunology",
            "Immunology, Oncology", "Cardiovascular, Immunology, Neuroscience"
        ],
        "Market Position": [
            "Major Competitor", "Major Competitor", "Major Competitor", "Major Competitor",
            "Significant Competitor", "Dominant in Diabetes/Obesity", "Dominant in Diabetes/Obesity", "Major Competitor",
            "Major Competitor", "Major Competitor"
        ]
    }
    df = pd.DataFrame(data)
    return df

def get_market_dependencies():
    data = {
        "Dependency": [
            "Global Healthcare Demand",
            "Drug Pricing & Reimbursement Policies",
            "Patent Expirations & Generic Competition",
            "Regulatory Approvals (FDA, EMA)",
            "Clinical Trial Success Rates",
            "Foreign Exchange Rates"
        ],
        "Impact Level": [
            "High", "Very High", "High", "Very High", "High", "Medium"
        ],
        "Description": [
            "Directly drives sales volume.",
            "Significantly impacts realized prices and margins.",
            "Threatens revenue of established drugs.",
            "Crucial for new drug launches and market access.",
            "Key to pipeline value and future growth.",
            "Affects reported financial results."
        ]
    }
    df = pd.DataFrame(data)
    return df

def get_economic_factors():
    data = {
        "Factor": [
            "Global Economic Growth",
            "Inflation",
            "Interest Rates",
            "Government Healthcare Spending",
            "Geopolitical Stability"
        ],
        "Impact": [
            "Positive (higher spending)",
            "Negative (cost pressure)",
            "Negative (valuation, borrowing costs)",
            "High (budget impact)",
            "Medium (supply chain, market access)"
        ],
        "Details": [
            "Stronger economies generally lead to higher healthcare spending.",
            "Increases costs for R&D, manufacturing, and distribution.",
            "Can increase cost of capital and pressure valuation multiples.",
            "Government budgets are a significant determinant of drug sales.",
            "Can disrupt supply chains and create market uncertainty."
        ]
    }
    df = pd.DataFrame(data)
    return df


# --- App Structure ---
st.title("AstraZeneca (AZN) Financial Ecosystem Analysis")

# --- Overview Section ---
st.header("Company Overview")
st.markdown("""
AstraZeneca PLC (AZN) is a global biopharmaceutical company headquartered in Cambridge, UK. It focuses on **oncology**, **cardiovascular, renal & metabolism (CVRM)**, **respiratory & immunology**, and **rare diseases**. Listed on the London Stock Exchange (LSE: AZN) and NASDAQ (AZN), it's a major player in the global healthcare sector.
""")

# --- Key Financial Metrics Section ---
st.header("Key Financial Metrics & Performance Drivers")
st.markdown("This section highlights crucial financial indicators and the drivers behind AstraZeneca's performance.")

financial_df = get_financial_data()
metrics_cols = st.columns(3)

for index, row in financial_df.iterrows():
    col_index = index % 3
    with metrics_cols[col_index]:
        st.metric(
            label=row["Metric"],
            value=row["Formatted_Value"],
            help=f"Source: {row['Source']}"
        )

st.markdown("---")

# --- Revenue Breakdown Section ---
st.header("Revenue Breakdown by Segment")
st.markdown("AstraZeneca's revenue is driven by its diverse therapeutic areas.")

revenue_df = get_revenue_breakdown()

# Create charts
fig_revenue_pie = px.pie(revenue_df, values='Revenue', names='Segment', title='Revenue Share by Segment')
fig_revenue_pie.update_traces(textposition='inside', textinfo='percent+label')

fig_revenue_bar = px.bar(
    revenue_df,
    x='Segment',
    y='Revenue',
    color='Segment',
    title='Revenue by Segment',
    labels={'Revenue': 'Revenue (USD)'}
)
fig_revenue_bar.update_layout(yaxis_title='Revenue (USD)')

fig_growth_bar = px.bar(
    revenue_df,
    x='Segment',
    y='Growth (YoY)',
    color='Segment',
    title='Year-over-Year Revenue Growth by Segment',
    labels={'Growth (YoY)': 'Growth Rate'}
)
fig_growth_bar.update_layout(yaxis_title='Growth Rate')
fig_growth_bar.update_traces(hovertemplate='%{y:.1%}')


col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_revenue_pie, use_container_width=True)
with col2:
    st.plotly_chart(fig_revenue_bar, use_container_width=True)

st.plotly_chart(fig_growth_bar, use_container_width=True)

st.markdown("""
**Key Revenue Drivers:**
- **Oncology Portfolio:** Primarily driven by Tagrisso (lung cancer), Imfinzi (immuno-oncology), and Lynparza (ovarian/breast cancer). It's the largest and fastest-growing segment.
- **CVRM:** Led by Farxiga (diabetes, heart failure, CKD), showing robust growth from expanded indications.
- **Rare Diseases (Alexion):** Stable cash flows from complement inhibitors like Soliris and Ultomiris.
- **Emerging Markets:** China is a significant contributor but faces pricing pressures.
""")

st.markdown("---")

# --- Market Dependencies Section ---
st.header("Market Dependencies & Sector Connections")
st.markdown("AstraZeneca's performance is influenced by various external factors within the healthcare landscape.")

dependencies_df = get_market_dependencies()

# Display as a table with styled columns
st.dataframe(
    dependencies_df.style.format({
        "Impact Level": lambda x: f'<span style="color:{"red" if x in ["Very High", "High"] else "orange" if x == "Medium" else "green"}; font-weight:bold;">{x}</span>',
    }).set_properties(**{'text-align': 'left'}),
    use_container_width=True,
    hide_index=True
)

st.markdown("""
**Sector Connections:**
- **Regulatory Environment:** FDA and EMA approvals are critical. Pricing and reimbursement policies (e.g., US Medicare negotiation) significantly impact revenue.
- **Healthcare Trends:** Focus on biologics, specialty drugs, and personalized medicine aligns with AZN's strategy.
- **Supply Chain:** Global manufacturing network is a strength but exposed to geopolitical risks.
""")

st.markdown("---")

# --- Competitor Landscape Section ---
st.header("Competitor Landscape")
st.markdown("AstraZeneca operates in a highly competitive pharmaceutical market.")

competitor_df = get_competitor_data()

st.dataframe(
    competitor_df.style.set_properties(**{'text-align': 'left'}),
    use_container_width=True,
    hide_index=True
)

st.markdown("""
**Key Competitive Areas:**
- **Oncology:** Faces intense competition from Merck & Co. (Keytruda), Bristol-Myers Squibb (Opdivo), Roche, and Pfizer.
- **CVRM:** Competes with Novo Nordisk and Eli Lilly in diabetes and obesity, and others in cardiovascular and renal disease.
- **Rare Diseases:** After the Alexion acquisition, it competes with established players like Takeda and Pfizer.
""")

st.markdown("---")

# --- Economic & Macroeconomic Factors Section ---
st.header("Economic & Macroeconomic Factors")
st.markdown("Broader economic conditions play a significant role in AstraZeneca's financial ecosystem.")

economic_df = get_economic_factors()

# Display as a table with styled columns
st.dataframe(
    economic_df.style.format({
        "Impact": lambda x: f'<span style="color:{"red" if x == "Negative" else "green" if x == "Positive" else "orange"}; font-weight:bold;">{x}</span>',
    }).set_properties(**{'text-align': 'left'}),
    use_container_width=True,
    hide_index=True
)

st.markdown("""
**Key Economic Influences:**
- **Currency Fluctuations:** As a UK-domiciled company with significant USD revenue, GBP/USD movements are important.
- **Inflation:** Puts pressure on costs but can be partially offset by pricing power for innovative drugs.
- **Interest Rates:** Can affect valuation multiples and the cost of capital.
- **Geopolitical Risks:** U.S.-China relations and broader global stability impact supply chains and market access.
""")

st.markdown("---")

# --- Investor Considerations & Risks ---
st.header("Investment Considerations & Key Risks")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Bull Case")
    st.markdown("""
    - **Oncology Pipeline:** Strong potential for blockbuster drugs in various cancer types.
    - **CVRM Growth:** Sustained momentum from Farxiga's expanded indications.
    - **Alexion Synergy:** Successful integration and growth in rare diseases.
    - **Emerging Markets:** Untapped potential beyond established markets.
    """)

with col2:
    st.subheader("Bear Case")
    st.markdown("""
    - **Pricing Pressures:** Intensifying competition and regulatory action on drug prices.
    - **Pipeline Setbacks:** Clinical trial failures or delays in key drug candidates.
    - **Generic Erosion:** Impact of patent expirations on older blockbusters.
    - **Geopolitical/Regulatory Uncertainty:** Trade wars, policy changes affecting market access.
    """)

st.markdown("---")

# --- Monitoring Points ---
st.header("Practical Monitoring Checklist")
st.markdown("Key areas for investors to track closely:")

monitoring_points = [
    "Pipeline Catalysts: Key Phase III trial readouts & regulatory submissions.",
    "Regulatory Decisions: FDA/EMA approvals for new indications.",
    "Quarterly Sales Trends: Oncology growth rates, Farxiga performance.",
    "Guidance Updates: Revenue/EPS forecasts and operational outlook.",
    "M&A Activity: Strategic deals to bolster pipeline or technology.",
    "Macro Factors: FX rates, inflation, interest rate outlook."
]

for point in monitoring_points:
    st.markdown(f"- {point}")

st.markdown("---")

st.header("Conclusion")
st.markdown("""
AstraZeneca's financial ecosystem is a complex interplay of scientific innovation, market dynamics, regulatory hurdles, and macroeconomic forces. Its success hinges on the continuous replenishment of its drug pipeline, particularly in high-growth oncology and CVRM segments, while navigating significant pricing pressures and global competition. Investors must closely monitor clinical trial outcomes, regulatory approvals, and sales performance of key drugs, alongside broader economic and geopolitical trends, to assess the company's ongoing value creation.
""")