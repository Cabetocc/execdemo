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
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# --- Configuration ---
st.set_page_config(
    page_title="Financial Ecosystem Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Helper Functions ---
def fetch_financial_data(ticker):
    """Fetches financial data using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1y")
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cash_flow
        recommendations = stock.recommendations
        institutional_holders = stock.institutional_holders
        major_holders = stock.major_holders
        earnings = stock.earnings
        quarterly_financials = stock.quarterly_financials
        quarterly_balance_sheet = stock.quarterly_balance_sheet
        quarterly_cash_flow = stock.quarterly_cash_flow
        return {
            "info": info,
            "history": hist,
            "financials": financials,
            "balance_sheet": balance_sheet,
            "cash_flow": cash_flow,
            "recommendations": recommendations,
            "institutional_holders": institutional_holders,
            "major_holders": major_holders,
            "earnings": earnings,
            "quarterly_financials": quarterly_financials,
            "quarterly_balance_sheet": quarterly_balance_sheet,
            "quarterly_cash_flow": quarterly_cash_flow,
        }
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def clean_financial_data(df):
    """Cleans financial dataframes by selecting relevant columns and resetting index."""
    if df is None or df.empty:
        return pd.DataFrame()
    # Select only numeric columns (usually '2023-12-31', '2022-12-31', etc.)
    numeric_cols = df.apply(pd.to_numeric, errors='coerce').notna().all(axis=0)
    df_cleaned = df.loc[:, numeric_cols]
    df_cleaned.index.name = 'Metric'
    return df_cleaned.reset_index()

def get_sector_peers(sector):
    """Placeholder for fetching sector peers. In a real app, this would involve an API or database."""
    if sector:
        return {
            "Technology": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
            "Financial Services": ["JPM", "BAC", "WFC", "GS", "MS"],
            "Healthcare": ["JNJ", "PFE", "MRK", "ABBV", "LLY"],
            "Consumer Discretionary": ["AMZN", "TSLA", "HD", "MCD", "NKE"],
            "Energy": ["XOM", "CVX", "SHEL", "TTE", "COP"],
        }.get(sector, [])
    return []

def analyze_financials(data, ticker):
    """Analyzes and visualizes key financial metrics."""

    st.header(f"Financial Analysis for {ticker.upper()}")

    # --- Company Snapshot ---
    st.subheader("Company Snapshot")
    info = data.get("info")
    if info:
        st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Market Cap:** {info.get('marketCap', 'N/A'):,.2f}" if info.get('marketCap') else "N/A")
        st.write(f"**Forward P/E:** {info.get('forwardPE', 'N/A')}")
        st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A'):.2%}" if info.get('dividendYield') else "N/A")
        st.write(f"**Short Description:** {info.get('longBusinessSummary', 'N/A')}")

    # --- Key Financial Relationships ---
    st.subheader("Key Financial Relationships")

    # Revenue and Profitability
    st.markdown("#### Revenue & Profitability Trends")
    financials_q = data.get("quarterly_financials")
    if financials_q is not None and not financials_q.empty:
        financials_q = financials_q.iloc[:, :4] # Last 4 quarters
        financials_q = financials_q.T
        financials_q.index = pd.to_datetime(financials_q.index)
        financials_q = financials_q.sort_index()

        revenue = financials_q.get('Total Revenue')
        gross_profit = financials_q.get('Gross Profit')
        operating_income = financials_q.get('Operating Income')
        net_income = financials_q.get('Net Income')

        fig, ax = plt.subplots(figsize=(12, 6))
        if revenue is not None:
            ax.plot(revenue.index, revenue.values, marker='o', label='Total Revenue')
        if gross_profit is not None:
            ax.plot(gross_profit.index, gross_profit.values, marker='o', label='Gross Profit')
        if operating_income is not None:
            ax.plot(operating_income.index, operating_income.values, marker='o', label='Operating Income')
        if net_income is not None:
            ax.plot(net_income.index, net_income.values, marker='o', label='Net Income')

        ax.set_title("Quarterly Revenue and Profitability")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount (USD)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # Margins
        gross_margin = (gross_profit / revenue * 100) if revenue is not None and gross_profit is not None else None
        operating_margin = (operating_income / revenue * 100) if revenue is not None and operating_income is not None else None
        net_margin = (net_income / revenue * 100) if revenue is not None and net_income is not None else None

        fig, ax = plt.subplots(figsize=(12, 6))
        if gross_margin is not None:
            ax.plot(gross_margin.index, gross_margin.values, marker='o', label='Gross Margin (%)')
        if operating_margin is not None:
            ax.plot(operating_margin.index, operating_margin.values, marker='o', label='Operating Margin (%)')
        if net_margin is not None:
            ax.plot(net_margin.index, net_margin.values, marker='o', label='Net Margin (%)')

        ax.set_title("Quarterly Profit Margins")
        ax.set_xlabel("Date")
        ax.set_ylabel("Margin (%)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    # Balance Sheet Health
    st.markdown("#### Balance Sheet Health")
    balance_sheet_q = data.get("quarterly_balance_sheet")
    if balance_sheet_q is not None and not balance_sheet_q.empty:
        balance_sheet_q = balance_sheet_q.iloc[:, :4]
        balance_sheet_q = balance_sheet_q.T
        balance_sheet_q.index = pd.to_datetime(balance_sheet_q.index)
        balance_sheet_q = balance_sheet_q.sort_index()

        total_debt = balance_sheet_q.get('Total Debt')
        total_equity = balance_sheet_q.get('Stockholders Equity')

        if total_debt is not None and total_equity is not None and not total_equity.isnull().all() and not total_debt.isnull().all():
            debt_to_equity = total_debt / total_equity
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(debt_to_equity.index, debt_to_equity.values, marker='o', label='Debt-to-Equity Ratio')
            ax.set_title("Quarterly Debt-to-Equity Ratio")
            ax.set_xlabel("Date")
            ax.set_ylabel("Ratio")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    # Cash Flow
    st.markdown("#### Cash Flow Dynamics")
    cash_flow_q = data.get("quarterly_cash_flow")
    if cash_flow_q is not None and not cash_flow_q.empty:
        cash_flow_q = cash_flow_q.iloc[:, :4]
        cash_flow_q = cash_flow_q.T
        cash_flow_q.index = pd.to_datetime(cash_flow_q.index)
        cash_flow_q = cash_flow_q.sort_index()

        operating_cashflow = cash_flow_q.get('Operating Cash Flow')
        investing_cashflow = cash_flow_q.get('Investing Cash Flow')
        financing_cashflow = cash_flow_q.get('Financing Cash Flow')

        fig, ax = plt.subplots(figsize=(12, 6))
        if operating_cashflow is not None:
            ax.plot(operating_cashflow.index, operating_cashflow.values, marker='o', label='Operating Cash Flow')
        if investing_cashflow is not None:
            ax.plot(investing_cashflow.index, investing_cashflow.values, marker='o', label='Investing Cash Flow')
        if financing_cashflow is not None:
            ax.plot(financing_cashflow.index, financing_cashflow.values, marker='o', label='Financing Cash Flow')

        ax.set_title("Quarterly Cash Flow Components")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount (USD)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # Free Cash Flow
        free_cash_flow = None
        capital_expenditures = cash_flow_q.get('Capital Expenditures')
        if operating_cashflow is not None and capital_expenditures is not None:
            free_cash_flow = operating_cashflow + capital_expenditures # Capex is usually negative in yfinance
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(free_cash_flow.index, free_cash_flow.values, marker='o', label='Free Cash Flow')
            ax.set_title("Quarterly Free Cash Flow")
            ax.set_xlabel("Date")
            ax.set_ylabel("Amount (USD)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    # Valuation Metrics
    st.markdown("#### Valuation Metrics")
    info = data.get("info")
    if info:
        valuation_metrics = {
            "P/E Ratio (TTM)": info.get('trailingPE'),
            "Forward P/E": info.get('forwardPE'),
            "P/S Ratio (TTM)": info.get('priceToSalesTrailing12Months'),
            "P/B Ratio": info.get('priceToBook'),
            "EV/EBITDA": info.get('enterpriseToEbitda'),
            "Dividend Yield": info.get('dividendYield', 0) * 100,
        }
        valid_metrics = {k: v for k, v in valuation_metrics.items() if v is not None and v != 0}

        if valid_metrics:
            st.write("Key Valuation Ratios:")
            for metric, value in valid_metrics.items():
                if "%" in metric:
                    st.write(f"- **{metric}:** {value:.2f}%")
                else:
                    st.write(f"- **{metric}:** {value:,.2f}")
        else:
            st.write("No readily available valuation metrics found.")

    # Shareholder Returns
    st.markdown("#### Shareholder Returns")
    earnings_data = data.get("earnings")
    if earnings_data is not None and not earnings_data.empty:
        earnings_data = earnings_data.T
        earnings_data.index = pd.to_datetime(earnings_data.index)
        earnings_data = earnings_data.sort_index(ascending=False)
        st.write("Recent Earnings Per Share (EPS):")
        st.dataframe(earnings_data[['EPS Estimate', 'Reported EPS']].head())

    # --- Market Dependencies ---
    st.subheader("Market Dependencies")

    # Broad Market Performance
    st.markdown("#### Performance vs. Market Indices")
    hist = data.get("history")
    if hist is not None and not hist.empty:
        hist = hist[['Close']].copy()
        hist.rename(columns={'Close': ticker.upper()}, inplace=True)

        # Fetch S&P 500 data
        try:
            sp500_ticker = "^GSPC"
            sp500_data = yf.Ticker(sp500_ticker).history(period="1y")
            if not sp500_data.empty:
                sp500_data = sp500_data[['Close']].copy()
                sp500_data.rename(columns={'Close': 'S&P 500'}, inplace=True)

                combined_performance = pd.merge(hist, sp500_data, left_index=True, right_index=True, how='outer')
                combined_performance = combined_performance.fillna(method='ffill') # Forward fill missing values
                combined_performance = combined_performance / combined_performance.iloc[0] * 100 # Normalize to 100

                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(combined_performance.index, combined_performance[ticker.upper()], label=f"{ticker.upper()}")
                ax.plot(combined_performance.index, combined_performance['S&P 500'], label='S&P 500')
                ax.set_title(f"{ticker.upper()} vs. S&P 500 Performance (Last Year)")
                ax.set_xlabel("Date")
                ax.set_ylabel("Normalized Price (Base 100)")
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)
            else:
                st.warning("Could not fetch S&P 500 data for comparison.")
        except Exception as e:
            st.warning(f"Could not fetch or plot S&P 500 data: {e}")

    # Investor Sentiment (using recommendations as a proxy)
    st.markdown("#### Investor Sentiment (Analyst Recommendations)")
    recommendations = data.get("recommendations")
    if recommendations is not None and not recommendations.empty:
        recommendations['Date'] = pd.to_datetime(recommendations['Date'])
        recommendations = recommendations.set_index('Date').sort_index(ascending=False)
        st.dataframe(recommendations[['Firm', 'To Grade', 'From Grade', 'Action']].head())
    else:
        st.write("Analyst recommendations data not available.")


    # --- Sector Connections ---
    st.subheader("Sector Connections")
    sector = info.get('sector', 'N/A') if info else 'N/A'
    industry = info.get('industry', 'N/A') if info else 'N/A'

    st.write(f"**Sector:** {sector}")
    st.write(f"**Industry:** {industry}")

    st.markdown("#### Peer Analysis (High-Level)")
    peer_tickers = get_sector_peers(sector)
    if peer_tickers:
        peer_data = {}
        for peer_ticker in peer_tickers:
            if peer_ticker.upper() != ticker.upper(): # Avoid self-comparison
                try:
                    peer_info = yf.Ticker(peer_ticker).info
                    peer_data[peer_ticker] = {
                        "Market Cap": peer_info.get('marketCap', 0),
                        "Forward P/E": peer_info.get('forwardPE', float('inf')),
                        "Revenue Growth (YoY)": peer_info.get('revenueGrowth', 0) * 100 if peer_info.get('revenueGrowth') else 0,
                        "Gross Margin": (peer_info.get('grossMargins') or 0) * 100,
                    }
                except Exception as e:
                    st.warning(f"Could not fetch data for peer {peer_ticker}: {e}")

        if peer_data:
            peer_df = pd.DataFrame.from_dict(peer_data, orient='index')
            peer_df.index.name = "Ticker"
            st.dataframe(peer_df)

            # Simple visualization for comparison
            metrics_to_compare = ["Market Cap", "Forward P/E", "Revenue Growth (YoY)", "Gross Margin"]
            for metric in metrics_to_compare:
                if metric in peer_df.columns and not peer_df[metric].isnull().all():
                    fig, ax = plt.subplots(figsize=(10, 5))
                    plot_data = peer_df[metric].sort_values(ascending=False)
                    sns.barplot(x=plot_data.values, y=plot_data.index, ax=ax, palette="viridis")
                    ax.set_title(f"Peer Comparison: {metric}")
                    ax.set_xlabel(metric)
                    ax.set_ylabel("Ticker")
                    st.pyplot(fig)
        else:
            st.write("No comparable peer data found.")
    else:
        st.write("Could not determine sector peers for this industry.")

    # --- Competitor Relationships ---
    st.subheader("Competitor Relationships")
    st.write("Identifying direct and indirect competitors requires a deeper dive into the company's specific products/services and market positioning. This section provides a high-level overview based on sector and industry.")
    # In a more advanced version, this would involve NLP on business descriptions, news analysis, etc.
    if sector and industry:
        st.write(f"Within the {industry} industry in the {sector} sector, key competitors often include companies with similar business models and target markets. Further analysis would involve examining their market share, product offerings, and strategic initiatives.")

    # --- Economic Factors ---
    st.subheader("Economic Factors")
    st.write("The sensitivity of a company to macroeconomic factors depends heavily on its business model, customer base, and cost structure. Here's a general assessment:")

    # Interest Rate Sensitivity (General Indicator)
    st.markdown("#### Interest Rate Sensitivity")
    if info:
        sector_lower = sector.lower() if sector else ""
        if "technology" in sector_lower or "growth" in sector_lower:
            st.write("Companies in high-growth sectors, especially technology, can be sensitive to interest rates. Higher rates increase borrowing costs for expansion and can make future earnings less valuable due to higher discount rates, potentially impacting valuations.")
        elif "financial services" in sector_lower or "banks" in sector_lower:
            st.write("Financial services companies (like banks) have a complex relationship with interest rates. Rising rates can increase net interest margins, but also pose risks to loan demand and credit quality.")
        elif "consumer discretionary" in sector_lower:
            st.write("Consumer discretionary spending is often tied to consumer confidence, which can be influenced by interest rates impacting mortgage payments and overall disposable income.")
        elif "utilities" in sector_lower or "real estate" in sector_lower:
            st.write("Industries with significant debt financing, like utilities or real estate investment trusts (REITs), are typically sensitive to interest rate changes due to higher borrowing costs.")
        else:
            st.write("General sensitivity to interest rates depends on the company's debt levels and reliance on consumer/business spending.")

    # Inflation Exposure
    st.markdown("#### Inflation Exposure")
    if info:
        revenue_drivers = info.get('revenueGrowth', None) # A weak proxy, actual drivers are complex
        cost_structure = info.get('grossMargins', None) # Another weak proxy

        if cost_structure is not None and cost_structure < 0.3: # Assume lower margins might be more exposed to cost inflation
             st.write("Companies with lower gross margins may have less pricing power to pass on increased input costs (raw materials, labor) to consumers, making them more vulnerable to inflation.")
        elif "energy" in sector.lower() or "materials" in sector.lower():
            st.write("Companies in sectors like Energy or Materials often have direct exposure to commodity prices, which are key drivers of inflation.")
        else:
            st.write("Sensitivity to inflation depends on the ability to pass on cost increases through higher prices (pricing power) and the proportion of costs subject to inflation.")

    # --- Summary & Risks ---
    st.subheader("Summary & Potential Risks")
    st.write("This section provides a high-level synthesis. A full risk assessment requires more in-depth qualitative analysis.")

    risk_summary = []
    if info:
        # Market Cap Size
        market_cap = info.get('marketCap')
        if market_cap:
            if market_cap < 2e9:
                risk_summary.append("Small-cap companies can be more volatile and subject to greater risks than larger companies.")
            elif market_cap > 10e9:
                risk_summary.append("Large-cap companies may face slower growth rates but often possess greater stability and market influence.")

        # Debt levels
        balance_sheet_q = data.get("quarterly_balance_sheet")
        if balance_sheet_q is not None and not balance_sheet_q.empty:
            total_debt = balance_sheet_q.iloc[:, 0].get('Total Debt')
            total_equity = balance_sheet_q.iloc[:, 0].get('Stockholders Equity')
            if total_debt is not None and total_equity is not None and total_equity > 0:
                debt_ratio = total_debt / total_equity
                if debt_ratio > 2.0:
                    risk_summary.append(f"High Debt-to-Equity ratio ({debt_ratio:.2f}x) indicates significant financial leverage, increasing risk during economic downturns or rising interest rates.")
                elif debt_ratio < 0.5:
                    risk_summary.append("Low Debt-to-Equity ratio suggests a strong balance sheet with minimal financial risk from leverage.")

        # Dependence on specific markets/customers (difficult to infer automatically)
        risk_summary.append("Potential dependence on specific geographic markets, customer segments, or supply chain partners could pose risks.")

    # Sector specific risks
    if sector:
        if "technology" in sector.lower():
            risk_summary.append("Rapid technological change and disruption are inherent risks in the technology sector.")
        if "healthcare" in sector.lower():
            risk_summary.append("Regulatory changes and patent expirations are significant considerations in the healthcare sector.")
        if "energy" in sector.lower():
            risk_summary.append("Volatility in commodity prices and environmental regulations are key risks for the energy sector.")

    if risk_summary:
        st.markdown("#### Potential Risks:")
        for risk in risk_summary:
            st.markdown(f"- {risk}")
    else:
        st.write("No specific significant risks identified based on readily available data.")

    st.success("Analysis complete. Please note that this is a high-level automated analysis and should not be considered financial advice.")

# --- Streamlit App Layout ---
st.title("Financial Ecosystem Analyzer 📈")
st.markdown("Analyze a stock's financial health, market dependencies, sector connections, and economic sensitivity.")

with st.sidebar:
    st.header("Input Parameters")
    ticker_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA)", "AAPL").strip().upper()
    st.markdown("---")
    st.markdown("This tool uses `yfinance` to fetch data. Please ensure the ticker is valid.")
    st.markdown("---")
    st.markdown("The analysis covers:")
    st.markdown("- Company Snapshot")
    st.markdown("- Key Financial Relationships (Revenue, Profitability, Balance Sheet, Cash Flow)")
    st.markdown("- Market Dependencies (Index Comparison, Sentiment Proxy)")
    st.markdown("- Sector Connections (Peer Comparison)")
    st.markdown("- Economic Sensitivity (General Indicators)")
    st.markdown("- Summary & Potential Risks")
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit")

if ticker_symbol:
    data = fetch_financial_data(ticker_symbol)
    if data:
        analyze_financials(data, ticker_symbol)
else:
    st.warning("Please enter a stock ticker symbol to begin the analysis.")