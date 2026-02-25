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
import numpy as np

# --- Configuration ---
st.set_page_config(
    page_title="Financial Analysis Dashboard (Simulated)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Function for Data Generation (Simulated) ---
# Since live data fetching is not allowed and no specific data was provided,
# this function generates realistic-looking mock data for demonstration.
def generate_mock_financial_data(ticker="AAPL"):
    """
    Generates simulated financial data for a given ticker.
    This data is entirely mock and does not reflect real company financials.
    """
    # Simulate historical annual data for 5 years
    years = pd.to_datetime([f'{y}-12-31' for y in range(2019, 2024)])
    
    # Base values for a large tech company like Apple
    base_revenue = 260e9
    base_net_income = 55e9
    base_eps = 2.97

    # Apply some growth and slight variability
    revenue = [base_revenue * (1 + i * 0.05 + np.random.uniform(-0.01, 0.01)) for i in range(5)]
    net_income = [base_net_income * (1 + i * 0.07 + np.random.uniform(-0.02, 0.02)) for i in range(5)]
    eps = [base_eps * (1 + i * 0.08 + np.random.uniform(-0.02, 0.02)) for i in range(5)]

    financial_df = pd.DataFrame({
        'Year': years,
        'Revenue ($B)': [r / 1e9 for r in revenue], # Convert to Billions
        'Net Income ($B)': [ni / 1e9 for ni in net_income], # Convert to Billions
        'EPS ($)': eps
    }).set_index('Year')

    # Simulated key metrics for the latest year
    latest_year_idx = len(financial_df) - 1
    
    # Ensure no division by zero for growth/margins if base data is too small
    current_revenue = revenue[latest_year_idx]
    prev_revenue = revenue[latest_year_idx - 1] if latest_year_idx > 0 else current_revenue
    
    current_net_income = net_income[latest_year_idx]

    key_metrics = {
        "Ticker": ticker,
        "Market Cap ($B)": np.random.randint(1500, 3000), # Billion USD
        "P/E Ratio (TTM)": round(np.random.uniform(25.0, 35.0), 1),
        "Dividend Yield": round(np.random.uniform(0.5, 1.0), 2),
        "Net Margin (TTM)": round((current_net_income / current_revenue) * 100, 1) if current_revenue != 0 else 0,
        "Revenue Growth (YoY)": round(((current_revenue - prev_revenue) / prev_revenue) * 100, 1) if prev_revenue != 0 else 0
    }

    # Simulated competitive data (including the selected ticker)
    # This data is also mock, designed for a large-cap tech comparison
    competitors = {
        "AAPL": {"Revenue Growth (%)": key_metrics["Revenue Growth (YoY)"], "Net Margin (%)": key_metrics["Net Margin (TTM)"], "P/E Ratio": 29.5, "Market Cap ($B)": 2800},
        "MSFT": {"Revenue Growth (%)": 13.0, "Net Margin (%)": 36.5, "P/E Ratio": 35.2, "Market Cap ($B)": 3000},
        "GOOGL": {"Revenue Growth (%)": 10.5, "Net Margin (%)": 25.1, "P/E Ratio": 27.8, "Market Cap ($B)": 2200},
        "AMZN": {"Revenue Growth (%)": 12.0, "Net Margin (%)": 6.8, "P/E Ratio": 50.1, "Market Cap ($B)": 1900},
    }

    # If the selected ticker is not one of the predefined, add it with generated data
    if ticker not in competitors:
        competitors[ticker] = {
            "Revenue Growth (%)": key_metrics["Revenue Growth (YoY)"],
            "Net Margin (%)": key_metrics["Net Margin (TTM)"],
            "P/E Ratio": key_metrics["P/E Ratio (TTM)"],
            "Market Cap ($B)": key_metrics["Market Cap ($B)"]
        }
    else: # Update predefined ticker with generated values to ensure consistency
        competitors[ticker]["Revenue Growth (%)"] = key_metrics["Revenue Growth (YoY)"]
        competitors[ticker]["Net Margin (%)"] = key_metrics["Net Margin (TTM)"]
        competitors[ticker]["P/E Ratio"] = key_metrics["P/E Ratio (TTM)"]
        competitors[ticker]["Market Cap ($B)"] = key_metrics["Market Cap ($B)"]


    comp_df = pd.DataFrame.from_dict(competitors, orient='index')

    return financial_df, key_metrics, comp_df

# --- Main App ---
st.title("🍎 Financial Analysis Dashboard (Simulated Data)")
st.caption("This dashboard presents a simulated financial analysis, demonstrating visualization capabilities based on hypothetical data.")

# Sidebar for controls
st.sidebar.header("Analysis Controls")
selected_ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL)", "AAPL").upper()
st.sidebar.markdown("---")
st.sidebar.warning("Note: All financial data presented here is **simulated** for demonstration purposes and does not reflect real-time market data or actual company performance.")

# Generate mock data based on the (mock) selected ticker
financial_df, key_metrics, comp_df = generate_mock_financial_data(selected_ticker)

# Calculate peer averages for delta metrics
peer_metrics_for_avg = comp_df.drop(selected_ticker, errors='ignore')
avg_peer_net_margin = peer_metrics_for_avg['Net Margin (%)'].mean() if not peer_metrics_for_avg.empty else key_metrics['Net Margin (TTM)']
avg_peer_revenue_growth = peer_metrics_for_avg['Revenue Growth (%)'].mean() if not peer_metrics_for_avg.empty else key_metrics['Revenue Growth (YoY)']


# --- 1. Key Metrics ---
st.header("📊 Key Metrics")
st.markdown("A quick glance at the most recent fundamental indicators.")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(label="Ticker", value=key_metrics["Ticker"])
with col2:
    st.metric(label="Market Cap", value=f"${key_metrics['Market Cap ($B)']:.0f}B")
with col3:
    st.metric(label="P/E Ratio (TTM)", value=f"{key_metrics['P/E Ratio (TTM)']:.1f}x")
with col4:
    st.metric(label="Dividend Yield", value=f"{key_metrics['Dividend Yield']:.2f}%")
with col5:
    net_margin_diff = key_metrics['Net Margin (TTM)'] - avg_peer_net_margin
    st.metric(label="Net Margin (TTM)", value=f"{key_metrics['Net Margin (TTM)']:.1f}%", 
              delta=f"{net_margin_diff:.1f}% vs Peer Avg", 
              delta_color="normal" if net_margin_diff >= 0 else "inverse")
with col6:
    revenue_growth_diff = key_metrics['Revenue Growth (YoY)'] - avg_peer_revenue_growth
    st.metric(label="Revenue Growth (YoY)", value=f"{key_metrics['Revenue Growth (YoY)']:.1f}%", 
              delta=f"{revenue_growth_diff:.1f}% vs Peer Avg", 
              delta_color="normal" if revenue_growth_diff >= 0 else "inverse")

st.markdown("---")

# --- 2. Company Overview ---
st.header(f"🏛️ {selected_ticker} - Company Overview")
st.write(f"""
**Industry:** Technology, Consumer Electronics, Software & Services.
**Business Model:** {selected_ticker} designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells related services. The company's products are known for their premium design, strong brand loyalty, and integrated ecosystem.
**Key Products:** iPhone, Mac, iPad, Apple Watch, AirPods, Apple TV.
**Services:** Apple Music, iCloud, App Store, Apple Pay, Apple Care, Apple TV+.
""")

st.markdown("---")

# --- 3. Financial Performance Visualizations ---
st.header("📈 Financial Performance (Last 5 Years)")
st.markdown("Analyzing historical trends in key financial indicators.")

# Revenue Chart
fig_revenue = px.line(
    financial_df,
    x=financial_df.index,
    y='Revenue ($B)',
    title=f'{selected_ticker} Annual Revenue',
    labels={'index': 'Year', 'Revenue ($B)': 'Revenue (Billions USD)'},
    markers=True,
    line_shape='spline' # Smooth the line
)
fig_revenue.update_layout(hovermode="x unified")
st.plotly_chart(fig_revenue, use_container_width=True)

# Net Income Chart
fig_net_income = px.line(
    financial_df,
    x=financial_df.index,
    y='Net Income ($B)',
    title=f'{selected_ticker} Annual Net Income',
    labels={'index': 'Year', 'Net Income ($B)': 'Net Income (Billions USD)'},
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Plotly[1:2],
    line_shape='spline'
)
fig_net_income.update_layout(hovermode="x unified")
st.plotly_chart(fig_net_income, use_container_width=True)

# EPS Chart
fig_eps = px.line(
    financial_df,
    x=financial_df.index,
    y='EPS ($)',
    title=f'{selected_ticker} Annual Earnings Per Share (EPS)',
    labels={'index': 'Year', 'EPS ($)': 'EPS (USD)'},
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Plotly[2:3],
    line_shape='spline'
)
fig_eps.update_layout(hovermode="x unified")
st.plotly_chart(fig_eps, use_container_width=True)

st.markdown("---")

# --- 4. Competitive Comparison ---
st.header("🆚 Competitive Landscape")
st.markdown(f"Comparing {selected_ticker} against selected peers on key financial and valuation metrics.")

# Display competitive data in a sortable table
st.dataframe(comp_df.style.highlight_max(subset=['Revenue Growth (%)', 'Net Margin (%)', 'Market Cap ($B)'], axis=0, props='background-color: #d1ffd1;')
                               .highlight_min(subset=['Revenue Growth (%)', 'Net Margin (%)', 'P/E Ratio'], axis=0, props='background-color: #ffd1d1;')
                               .format("{:.1f}", subset=['Revenue Growth (%)', 'Net Margin (%)', 'P/E Ratio'])
                               .format("${:,.0f}B", subset=['Market Cap ($B)']),
             use_container_width=True)

# Competitive Charts
col_comp1, col_comp2 = st.columns(2)

with col_comp1:
    fig_comp_growth = px.bar(
        comp_df.sort_values('Revenue Growth (%)', ascending=False),
        x=comp_df.index,
        y='Revenue Growth (%)',
        title='Revenue Growth (%) Last Year',
        labels={'index': 'Company'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_comp_growth.update_traces(marker_line_width=1, marker_line_color='black')
    st.plotly_chart(fig_comp_growth, use_container_width=True)

with col_comp2:
    fig_comp_margin = px.bar(
        comp_df.sort_values('Net Margin (%)', ascending=False),
        x=comp_df.index,
        y='Net Margin (%)',
        title='Net Margin (%) Last Year',
        labels={'index': 'Company'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_comp_margin.update_traces(marker_line_width=1, marker_line_color='black')
    st.plotly_chart(fig_comp_margin, use_container_width=True)

fig_comp_pe = px.bar(
    comp_df.sort_values('P/E Ratio', ascending=True),
    x=comp_df.index,
    y='P/E Ratio',
    title='P/E Ratio (Lower generally indicates better value)',
    labels={'index': 'Company'},
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig_comp_pe.update_traces(marker_line_width=1, marker_line_color='black')
st.plotly_chart(fig_comp_pe, use_container_width=True)

st.markdown("---")

# --- 5. 3-6 Month Outlook ---
st.header("🔭 3-6 Month Outlook")
st.markdown(f"""
The outlook for {selected_ticker} appears stable with continued strong demand for its premium products, especially within the services segment which shows consistent growth and higher margins.

**Fundamentals:** Expected to remain robust, driven by innovation in new product categories (e.g., Vision Pro, though initial impact is small) and continued expansion of its services ecosystem.
**Macro:** Potential headwinds include global economic slowdowns affecting consumer spending on high-ticket items and increased regulatory scrutiny in major markets. However, the company's strong cash flow and brand resilience offer a buffer.
**Industry Dynamics:** The consumer electronics market remains highly competitive. {selected_ticker}'s ability to differentiate through design, ecosystem lock-in, and powerful branding continues to be a key advantage. The AI trend is a significant opportunity, and {selected_ticker}'s strategy in integrating AI into its devices and services will be crucial.
""")

st.markdown("---")

# --- 6. Key Risks and Opportunities ---
st.header("⚠️ Key Risks & Opportunities")

col_risk, col_opp = st.columns(2)

with col_risk:
    st.subheader("Risks")
    st.markdown("""
    *   **Supply Chain Disruptions:** Over-reliance on a few key manufacturing partners and geopolitical tensions (e.g., US-China) pose risks to production.
    *   **Regulatory Scrutiny:** Antitrust investigations and new regulations targeting large tech companies could impact business practices and profitability.
    *   **Increased Competition:** Aggressive competition from Android manufacturers and emerging tech players could erode market share.
    *   **Innovation Cycle:** The market's high expectations for groundbreaking products mean failure to innovate consistently could lead to investor disappointment.
    """)

with col_opp:
    st.subheader("Opportunities")
    st.markdown("""
    *   **Services Growth:** Continued expansion of its high-margin services segment (App Store, Apple Music, iCloud, Advertising) offers a stable and growing revenue stream.
    *   **Emerging Markets:** Untapped potential in certain emerging markets could drive future growth.
    *   **New Product Categories:** Successful ventures into new areas like AR/VR (Vision Pro) or automotive could unlock significant long-term value.
    *   **AI Integration:** Deep integration of AI capabilities into its devices and software ecosystem could enhance user experience and create new revenue streams.
    """)

st.markdown("---")

# --- 7. Summary Judgment ---
st.header("✨ Summary Judgment")
st.markdown(f"""
{selected_ticker} remains a market leader with a robust business model characterized by strong brand loyalty, an integrated ecosystem, and significant cash generation. While facing macro-economic headwinds and intense competition, its consistent innovation, especially in the services segment and potential new product categories, positions it well for long-term growth. Investors should monitor regulatory developments and the company's execution on its AI strategy.
""")

st.markdown("---")
st.info("Disclaimer: This analysis is based on simulated data and for informational purposes only. It is not investment advice.")