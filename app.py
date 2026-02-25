import streamlit as st

import requests
import time
from pathlib import Path

WEBHOOK_URL = "https://cabetocc.app.n8n.cloud/webhook-test/stock-analysis"
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


import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# --- Configuration ---
st.set_page_config(layout="wide", page_title="Financial Ecosystem Analyzer", page_icon="📈")

# --- Helper Functions for Data Fetching and Calculations ---

@st.cache_data(ttl=3600) # Cache data for 1 hour
def get_stock_data(ticker_symbol):
    """Fetches comprehensive stock data using yfinance."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        history = ticker.history(period="5y") # 5 years historical data
        balance_sheet = ticker.quarterly_balance_sheet
        income_stmt = ticker.quarterly_financials
        cash_flow = ticker.quarterly_cashflow
        recommendations = ticker.recommendations
        dividends = ticker.dividends
        
        # Check if dataframes are empty and transpose if not
        if not balance_sheet.empty:
            balance_sheet = balance_sheet.T
            balance_sheet.index = pd.to_datetime(balance_sheet.index)
        if not income_stmt.empty:
            income_stmt = income_stmt.T
            income_stmt.index = pd.to_datetime(income_stmt.index)
        if not cash_flow.empty:
            cash_flow = cash_flow.T
            cash_flow.index = pd.to_datetime(cash_flow.index)
            
        return ticker, info, history, balance_sheet, income_stmt, cash_flow, recommendations, dividends
    except Exception as e:
        st.error(f"Error fetching data for {ticker_symbol}: {e}")
        return None, None, None, None, None, None, None, None

def calculate_financial_ratios(balance_sheet, income_stmt, cash_flow, current_price, info):
    """Calculates key financial ratios from fetched data."""
    ratios = pd.DataFrame(index=balance_sheet.index) # Use balance sheet dates as index
    
    if income_stmt.empty or balance_sheet.empty or cash_flow.empty:
        return ratios # Return empty if no data

    # Align dates for income_stmt and cash_flow to balance_sheet
    income_stmt = income_stmt.reindex(balance_sheet.index, method='nearest')
    cash_flow = cash_flow.reindex(balance_sheet.index, method='nearest')
    
    # Profitability Ratios
    # Ensure columns exist before accessing
    for idx in balance_sheet.index:
        gross_profit = income_stmt.loc[idx, 'Gross Profit'] if 'Gross Profit' in income_stmt.columns else None
        revenue = income_stmt.loc[idx, 'Total Revenue'] if 'Total Revenue' in income_stmt.columns else None
        operating_income = income_stmt.loc[idx, 'Operating Income'] if 'Operating Income' in income_stmt.columns else None
        net_income = income_stmt.loc[idx, 'Net Income'] if 'Net Income' in income_stmt.columns else None
        total_assets = balance_sheet.loc[idx, 'Total Assets'] if 'Total Assets' in balance_sheet.columns else None
        total_equity = balance_sheet.loc[idx, 'Stockholders Equity'] if 'Stockholders Equity' in balance_sheet.columns else None
        
        ratios.loc[idx, 'Gross Profit Margin'] = (gross_profit / revenue) * 100 if revenue and revenue != 0 else pd.NA
        ratios.loc[idx, 'Operating Profit Margin'] = (operating_income / revenue) * 100 if revenue and revenue != 0 else pd.NA
        ratios.loc[idx, 'Net Profit Margin'] = (net_income / revenue) * 100 if revenue and revenue != 0 else pd.NA
        ratios.loc[idx, 'Return on Equity (ROE)'] = (net_income / total_equity) * 100 if total_equity and total_equity != 0 else pd.NA
        ratios.loc[idx, 'Return on Assets (ROA)'] = (net_income / total_assets) * 100 if total_assets and total_assets != 0 else pd.NA

        # Liquidity Ratios
        current_assets = balance_sheet.loc[idx, 'Total Current Assets'] if 'Total Current Assets' in balance_sheet.columns else None
        current_liabilities = balance_sheet.loc[idx, 'Total Current Liabilities'] if 'Total Current Liabilities' in balance_sheet.columns else None
        inventory = balance_sheet.loc[idx, 'Inventory'] if 'Inventory' in balance_sheet.columns else None
        
        ratios.loc[idx, 'Current Ratio'] = current_assets / current_liabilities if current_liabilities and current_liabilities != 0 else pd.NA
        ratios.loc[idx, 'Quick Ratio'] = (current_assets - inventory) / current_liabilities if current_liabilities and current_liabilities != 0 else pd.NA
        
        # Solvency/Leverage Ratios
        total_debt = balance_sheet.loc[idx, 'Total Debt'] if 'Total Debt' in balance_sheet.columns else (balance_sheet.loc[idx, 'Long Term Debt'] + balance_sheet.loc[idx, 'Short Term Debt']) if 'Long Term Debt' in balance_sheet.columns and 'Short Term Debt' in balance_sheet.columns else None
        interest_expense = income_stmt.loc[idx, 'Interest Expense'] if 'Interest Expense' in income_stmt.columns else None
        ebit = income_stmt.loc[idx, 'EBIT'] if 'EBIT' in income_stmt.columns else None
        
        ratios.loc[idx, 'Debt-to-Equity Ratio'] = total_debt / total_equity if total_equity and total_equity != 0 else pd.NA
        ratios.loc[idx, 'Interest Coverage Ratio'] = ebit / interest_expense if interest_expense and interest_expense != 0 else pd.NA
        
        # Efficiency Ratios
        cost_of_revenue = income_stmt.loc[idx, 'Cost Of Revenue'] if 'Cost Of Revenue' in income_stmt.columns else None
        avg_inventory = (balance_sheet.loc[idx, 'Inventory'] + balance_sheet.shift(1).loc[idx, 'Inventory']) / 2 if 'Inventory' in balance_sheet.columns and not balance_sheet.shift(1).empty and 'Inventory' in balance_sheet.shift(1).columns else None
        accounts_receivable = balance_sheet.loc[idx, 'Accounts Receivable'] if 'Accounts Receivable' in balance_sheet.columns else None
        avg_accounts_receivable = (accounts_receivable + balance_sheet.shift(1).loc[idx, 'Accounts Receivable']) / 2 if 'Accounts Receivable' in balance_sheet.columns and not balance_sheet.shift(1).empty and 'Accounts Receivable' in balance_sheet.shift(1).columns else None
        
        ratios.loc[idx, 'Inventory Turnover'] = cost_of_revenue / avg_inventory if avg_inventory and avg_inventory != 0 else pd.NA
        ratios.loc[idx, 'Accounts Receivable Turnover'] = revenue / avg_accounts_receivable if avg_accounts_receivable and avg_accounts_receivable != 0 else pd.NA
        
        # Growth Ratios (Year-over-year where possible)
        # Revenue Growth
        prev_revenue = income_stmt.shift(-1).loc[idx, 'Total Revenue'] if not income_stmt.shift(-1).empty and 'Total Revenue' in income_stmt.shift(-1).columns else None
        ratios.loc[idx, 'Revenue Growth'] = ((revenue - prev_revenue) / prev_revenue) * 100 if revenue and prev_revenue and prev_revenue != 0 else pd.NA
        
        # EPS Growth
        eps = income_stmt.loc[idx, 'Basic EPS'] if 'Basic EPS' in income_stmt.columns else None
        prev_eps = income_stmt.shift(-1).loc[idx, 'Basic EPS'] if not income_stmt.shift(-1).empty and 'Basic EPS' in income_stmt.shift(-1).columns else None
        ratios.loc[idx, 'EPS Growth'] = ((eps - prev_eps) / prev_eps) * 100 if eps and prev_eps and prev_eps != 0 else pd.NA

    # Valuation Ratios (most are current or TTM)
    # Using 'info' for the most up-to-date
    if current_price and info:
        if 'trailingPE' in info and info['trailingPE']:
            ratios.loc[ratios.index[0], 'Price-to-Earnings (P/E) Ratio'] = info['trailingPE']
        elif 'regularMarketPrice' in info and 'trailingEps' in info and info['trailingEps'] != 0:
            ratios.loc[ratios.index[0], 'Price-to-Earnings (P/E) Ratio'] = info['regularMarketPrice'] / info['trailingEps']

        if 'marketCap' in info and 'totalRevenue' in info and info['totalRevenue'] != 0:
            ratios.loc[ratios.index[0], 'Price-to-Sales (P/S) Ratio'] = info['marketCap'] / info['totalRevenue']
        elif 'currentPrice' in info and info['currentPrice'] and revenue and info['sharesOutstanding']:
            ratios.loc[ratios.index[0], 'Price-to-Sales (P/S) Ratio'] = (info['currentPrice'] * info['sharesOutstanding']) / revenue # approximated with last known revenue

        if 'enterpriseValue' in info and 'ebitda' in info and info['ebitda'] != 0:
            ratios.loc[ratios.index[0], 'Enterprise Value to EBITDA (EV/EBITDA)'] = info['enterpriseValue'] / info['ebitda']
    
    return ratios.sort_index(ascending=False).round(2) # Sort by most recent first

def plot_historical_data(df, title, y_axis_label, type='line', fill=False):
    """Generates a Plotly chart for historical data."""
    if df.empty:
        st.warning(f"No data to plot for {title}.")
        return go.Figure()

    fig = go.Figure()
    if type == 'line':
        for col in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines+markers', name=col))
    elif type == 'bar':
        for col in df.columns:
            fig.add_trace(go.Bar(x=df.index, y=df[col], name=col))

    fig.update_layout(
        title_text=title,
        xaxis_rangeslider_visible=False,
        xaxis_title="Date",
        yaxis_title=y_axis_label,
        hovermode="x unified",
        height=400
    )
    return fig

def format_large_number(num):
    """Formats large numbers into a readable string (e.g., 1.23M, 4.56B)."""
    if pd.isna(num):
        return "N/A"
    num = float(num)
    if abs(num) >= 1e12:
        return f"{num / 1e12:.2f}T"
    elif abs(num) >= 1e9:
        return f"{num / 1e9:.2f}B"
    elif abs(num) >= 1e6:
        return f"{num / 1e6:.2f}M"
    elif abs(num) >= 1e3:
        return f"{num / 1e3:.2f}K"
    else:
        return f"{num:.2f}"


# --- Streamlit App Layout ---
st.title("📈 Financial Ecosystem Analyzer")

st.sidebar.header("Input Ticker")
ticker_input = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA)", "AAPL").upper()
analyze_button = st.sidebar.button("Analyze Stock")

st.markdown(
    """
    This app provides a comprehensive financial ecosystem analysis for a given stock ticker.
    It extracts key financial metrics, visualizes trends, and outlines the various qualitative factors
    that influence a company's performance and market standing.
    """
)

if analyze_button and ticker_input:
    with st.spinner(f"Fetching data for {ticker_input}..."):
        (ticker, info, history, balance_sheet, income_stmt,
         cash_flow, recommendations, dividends) = get_stock_data(ticker_input)

    if info:
        st.header(f"Analysis for {info.get('longName', ticker_input)}")
        st.markdown(f"**Ticker:** `{ticker_input}`")

        # --- Section 1: Company Overview ---
        st.subheader("1. Company Overview")
        col1, col2 = st.columns([1, 2])
        with col1:
            if 'logo_url' in info:
                st.image(info['logo_url'], width=100)
            st.metric("Current Price", f"${info.get('currentPrice', 'N/A'):.2f}")
            st.metric("Market Cap", format_large_number(info.get('marketCap')))
            st.metric("Sector", info.get('sector', 'N/A'))
            st.metric("Industry", info.get('industry', 'N/A'))
        with col2:
            st.write(f"**Business Summary:**")
            st.write(info.get('longBusinessSummary', 'No business summary available.'))
            st.write(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', '#')})")

        st.markdown("---")

        # --- Section 2: Key Financial Relationships ---
        st.subheader("2. Key Financial Relationships")
        
        current_price = info.get('currentPrice', None)
        if current_price:
            financial_ratios = calculate_financial_ratios(balance_sheet, income_stmt, cash_flow, current_price, info)
        else:
            financial_ratios = pd.DataFrame()
            st.warning("Could not fetch current price to calculate all valuation ratios.")

        # Display latest ratios in a summary
        if not financial_ratios.empty:
            st.markdown("##### Latest Key Financial Ratios")
            latest_ratios = financial_ratios.iloc[0].dropna()
            
            # Group ratios by type
            profitability_ratios = latest_ratios[[col for col in latest_ratios.index if 'Profit Margin' in col or 'Return on' in col]]
            liquidity_ratios = latest_ratios[[col for col in latest_ratios.index if 'Ratio' in col and ('Current' in col or 'Quick' in col)]]
            solvency_ratios = latest_ratios[[col for col in latest_ratios.index if 'Debt-to-Equity' in col or 'Interest Coverage' in col]]
            efficiency_ratios = latest_ratios[[col for col in latest_ratios.index if 'Turnover' in col]]
            valuation_ratios = latest_ratios[[col for col in latest_ratios.index if 'P/E' in col or 'P/S' in col or 'EV/EBITDA' in col]]
            growth_ratios = latest_ratios[[col for col in latest_ratios.index if 'Growth' in col]]

            col_ratios1, col_ratios2, col_ratios3 = st.columns(3)
            with col_ratios1:
                st.markdown("**Profitability**")
                for ratio, value in profitability_ratios.items():
                    st.write(f"- {ratio}: `{value:.2f}%`")
                st.markdown("**Liquidity**")
                for ratio, value in liquidity_ratios.items():
                    st.write(f"- {ratio}: `{value:.2f}`")
            with col_ratios2:
                st.markdown("**Solvency/Leverage**")
                for ratio, value in solvency_ratios.items():
                    st.write(f"- {ratio}: `{value:.2f}`")
                st.markdown("**Efficiency**")
                for ratio, value in efficiency_ratios.items():
                    st.write(f"- {ratio}: `{value:.2f}`")
            with col_ratios3:
                st.markdown("**Valuation (Current)**")
                for ratio, value in valuation_ratios.items():
                    st.write(f"- {ratio}: `{value:.2f}`")
                st.markdown("**Growth**")
                for ratio, value in growth_ratios.items():
                    st.write(f"- {ratio}: `{value:.2f}%`")
            st.markdown("---")


        # Detailed Financial Statements & Ratios
        with st.expander("Detailed Financial Statements & Ratio Trends"):
            tab1, tab2, tab3, tab4 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow", "Ratio Trends"])

            with tab1:
                st.markdown("##### Quarterly Income Statement")
                if not income_stmt.empty:
                    st.dataframe(income_stmt.head(), use_container_width=True)
                    # Chart for key income statement items
                    inc_stmt_chart_data = income_stmt[['Total Revenue', 'Gross Profit', 'Net Income']].dropna()
                    if not inc_stmt_chart_data.empty:
                        st.plotly_chart(plot_historical_data(inc_stmt_chart_data, "Quarterly Revenue, Gross Profit, Net Income", "Amount"), use_container_width=True)
                else:
                    st.info("No income statement data available.")

            with tab2:
                st.markdown("##### Quarterly Balance Sheet")
                if not balance_sheet.empty:
                    st.dataframe(balance_sheet.head(), use_container_width=True)
                    # Chart for key balance sheet items
                    bal_sheet_chart_data = balance_sheet[['Total Assets', 'Total Liabilities', 'Stockholders Equity']].dropna()
                    if not bal_sheet_chart_data.empty:
                        st.plotly_chart(plot_historical_data(bal_sheet_chart_data, "Quarterly Assets, Liabilities, Equity", "Amount"), use_container_width=True)
                else:
                    st.info("No balance sheet data available.")

            with tab3:
                st.markdown("##### Quarterly Cash Flow Statement")
                if not cash_flow.empty:
                    st.dataframe(cash_flow.head(), use_container_width=True)
                    # Chart for key cash flow items
                    cf_chart_data = cash_flow[['Total Cash From Operating Activities', 'Total Cash From Investing Activities', 'Total Cash From Financing Activities', 'Change In Cash']].dropna()
                    if not cf_chart_data.empty:
                        st.plotly_chart(plot_historical_data(cf_chart_data, "Quarterly Cash Flow Activities", "Amount"), use_container_width=True)
                else:
                    st.info("No cash flow data available.")

            with tab4:
                st.markdown("##### Key Ratio Trends Over Time")
                if not financial_ratios.empty:
                    st.dataframe(financial_ratios, use_container_width=True)
                    
                    st.markdown("**Profitability Ratios**")
                    profit_ratio_cols = [col for col in financial_ratios.columns if 'Profit Margin' in col or 'Return on' in col]
                    if profit_ratio_cols:
                        st.plotly_chart(plot_historical_data(financial_ratios[profit_ratio_cols], "Profitability Ratios", "%"), use_container_width=True)
                    
                    st.markdown("**Liquidity & Solvency Ratios**")
                    liq_solv_ratio_cols = [col for col in financial_ratios.columns if 'Ratio' in col and not ('P/E' in col or 'P/S' in col or 'EV/EBITDA' in col)]
                    if liq_solv_ratio_cols:
                        st.plotly_chart(plot_historical_data(financial_ratios[liq_solv_ratio_cols], "Liquidity & Solvency Ratios", "Ratio"), use_container_width=True)
                    
                    st.markdown("**Growth Ratios**")
                    growth_ratio_cols = [col for col in financial_ratios.columns if 'Growth' in col]
                    if growth_ratio_cols:
                        st.plotly_chart(plot_historical_data(financial_ratios[growth_ratio_cols], "Growth Ratios", "%"), use_container_width=True)
                else:
                    st.info("No financial ratio data to display trends.")
        
        st.markdown("---")

        # --- Section 3: Market Dependencies ---
        st.subheader("3. Market Dependencies")

        col3_1, col3_2 = st.columns(2)
        with col3_1:
            st.markdown("##### Market Performance")
            if not history.empty:
                fig = px.line(history, x=history.index, y='Close', title=f"{ticker_input} Historical Close Price (5 Years)")
                fig.update_layout(xaxis_rangeslider_visible=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No historical price data available.")
        
        with col3_2:
            st.markdown("##### Investor Sentiment & Dividend Policy")
            if not recommendations.empty:
                st.write("**Analyst Ratings:**")
                st.dataframe(recommendations.head(5), use_container_width=True)
            else:
                st.info("No recent analyst recommendations available via yfinance.")
            
            st.write("**Dividend Policy:**")
            dividend_yield = info.get('dividendYield', 'N/A')
            if dividend_yield != 'N/A':
                st.write(f"- Dividend Yield: `{dividend_yield:.2%}`")
            else:
                st.write("- Dividend Yield: `N/A`")
            
            if not dividends.empty:
                st.write("- Has paid dividends historically.")
                fig_div = px.bar(dividends.reset_index(), x='Date', y='Dividends', title="Historical Dividends Paid")
                st.plotly_chart(fig_div, use_container_width=True)
            else:
                st.write("- No historical dividend payments found.")
            
            # Placeholder for correlation with indices, news sentiment, social media buzz
            st.write(f"")
            st.info("""
            **Overall Market Performance & Investor Sentiment:**
            A full analysis would involve calculating correlation with major indices (e.g., S&P 500, Nasdaq Composite),
            analyzing recent news sentiment using NLP techniques, and monitoring social media buzz.
            (Data for these aspects would require additional APIs and processing.)
            """)

        st.markdown("---")

        # --- Section 4: Sector Connections ---
        st.subheader("4. Sector Connections")
        st.write(f"**Industry Classification:** The company belongs to the **{info.get('sector', 'N/A')}** sector, specifically the **{info.get('industry', 'N/A')}** industry.")
        
        st.markdown("##### Sector Trends & Supply Chain")
        st.info(f"""
        **Broader Industry Trends:** For a company in the **{info.get('industry', 'N/A')}** industry, key trends to consider include:
        *   **Technological Advancements:** How innovations (e.g., AI, automation, new materials) are impacting production, product development, and competitive landscape.
        *   **Regulatory Changes:** New government policies, environmental regulations, or industry-specific compliance requirements.
        *   **Consumer Preferences:** Shifting tastes, demand for sustainability, or changes in purchasing power.
        *   **Supply Chain Dynamics:** Geopolitical stability affecting material sourcing, logistics costs, and labor availability.

        **Supply Chain Dependencies:** Identifying key suppliers and their financial health is crucial. For instance, a tech company might depend on specific semiconductor manufacturers, or a retail company on a global network of logistics providers.
        
        **Customer Base:** Analyzing customer concentration (e.g., reliance on a few large clients) and their economic sensitivity. Is the product/service discretionary or essential?
        (A detailed analysis requires industry reports and company-specific disclosures beyond standard financial data.)
        """)
        st.markdown("---")

        # --- Section 5: Competitor Relationships ---
        st.subheader("5. Competitor Relationships")
        st.markdown("##### Competitive Landscape")
        st.info(f"""
        **Direct Competitors:** Companies offering similar products/services in the same market (e.g., Apple vs. Samsung, Coca-Cola vs. Pepsi).
        **Indirect Competitors:** Companies vying for the same customer wallet, even if their products are different (e.g., streaming services vs. movie theaters).
        
        **Competitive Advantages/Disadvantages:**
        *   **Moat:** What gives the company a sustainable advantage (e.g., brand, patents, network effects, cost leadership)?
        *   **Brand Strength:** How recognizable and trusted is the brand?
        *   **Innovation:** R&D investment, new product pipeline, ability to adapt.
        *   **Cost Structure:** Is the company a low-cost producer or a premium provider?

        **Market Share:** Understanding the company's position relative to its competitors in key markets.
        (This section typically requires market research reports, industry news, and competitor financial analysis.)
        """)
        st.markdown("---")

        # --- Section 6: Economic Factors ---
        st.subheader("6. Economic Factors")
        st.markdown("##### Macroeconomic & Regulatory Environment")
        st.info("""
        **Macroeconomic Indicators:**
        *   **GDP Growth:** Impact on overall consumer and business spending.
        *   **Inflation Rates:** Affects cost of goods, pricing power, and consumer spending.
        *   **Interest Rate Policies (Monetary Policy):** Influences borrowing costs, capital expenditure, and valuation multiples (especially for growth stocks).
        *   **Unemployment Rates:** Indicates consumer confidence and spending capacity.

        **Consumer Spending:** Differentiating between discretionary (e.g., luxury goods, entertainment) and non-discretionary (e.g., food, utilities) spending patterns helps understand resilience during economic downturns.

        **Global Economic Conditions:** Geopolitical events (e.g., trade wars, regional conflicts), international trade relations, and currency fluctuations (for multinational corporations) can significantly impact performance.

        **Regulatory Environment:** Government policies, taxes, tariffs, environmental regulations, and industry-specific rules can create opportunities or impose significant costs and restrictions.
        (A complete analysis here would integrate data from economic indicators, central bank reports, and geopolitical analyses.)
        """)

        st.markdown("---")
        st.success("Analysis complete!")

    elif analyze_button:
        st.error(f"Could not retrieve data for ticker: **{ticker_input}**. Please check the ticker symbol and try again.")
else:
    st.info("Please enter a stock ticker in the sidebar and click 'Analyze Stock' to begin.")

st.sidebar.markdown("---")
st.sidebar.markdown("Developed by a Senior Python Developer")