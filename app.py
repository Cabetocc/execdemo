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
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="IBM Financial Ecosystem Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Helper Functions ---
def format_currency(value):
    if pd.isna(value):
        return "N/A"
    try:
        return f"${value:,.0f}"
    except (ValueError, TypeError):
        return str(value)

def format_percentage(value):
    if pd.isna(value):
        return "N/A"
    try:
        return f"{value:.1f}%"
    except (ValueError, TypeError):
        return str(value)

def create_bar_chart(df, x_col, y_col, title, color_col=None, hover_data=None):
    if hover_data is None:
        hover_data = [x_col, y_col]
    fig = px.bar(df,
                 x=x_col,
                 y=y_col,
                 title=title,
                 color=color_col,
                 hover_data=hover_data,
                 labels={y_col: y_col.replace('_', ' ').title(), x_col: x_col.replace('_', ' ').title()},
                 template="plotly_white")
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20),
        legend_title_text=color_col.replace('_', ' ').title() if color_col else None
    )
    return fig

def create_pie_chart(df, names_col, values_col, title, hover_data=None):
    if hover_data is None:
        hover_data = [names_col, values_col]
    fig = px.pie(df,
                 names=names_col,
                 values=values_col,
                 title=title,
                 hover_data=hover_data,
                 hole=0.3,
                 template="plotly_white")
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20),
        legend_title_text=names_col.replace('_', ' ').title()
    )
    return fig

def format_metric_card(value, label, color="primary", prefix="$", suffix="%"):
    st.metric(label=label, value=f"{prefix}{value:,.0f}" if prefix == "$" else f"{value:.1f}{suffix}", delta=None)

# --- Data Simulation ---
# In a real app, this data would come from APIs (e.g., financial data providers)
# For demonstration, we use sample data reflecting the analysis.
data = {
    "segment": ["Software", "Consulting", "Infrastructure", "Financing"],
    "revenue_usd_billion": [40.0, 30.0, 22.0, 3.0],
    "gross_margin_pct": [80.0, 30.0, 45.0, 60.0],
    "operating_margin_pct": [25.0, 10.0, 15.0, 20.0],
    "recurring_revenue_pct": [75.0, 20.0, 10.0, 0.0]
}
df_segments = pd.DataFrame(data)
df_segments['revenue_usd_billion'] = df_segments['revenue_usd_billion'].astype(float)
df_segments['gross_margin_pct'] = df_segments['gross_margin_pct'].astype(float)
df_segments['operating_margin_pct'] = df_segments['operating_margin_pct'].astype(float)
df_segments['recurring_revenue_pct'] = df_segments['recurring_revenue_pct'].astype(float)

df_segments = df_segments.sort_values("revenue_usd_billion", ascending=False)

total_revenue = df_segments["revenue_usd_billion"].sum()
df_segments["revenue_share_pct"] = (df_segments["revenue_usd_billion"] / total_revenue) * 100

# Simulate Key Financials
key_financials_data = {
    "metric": ["Total Revenue", "Gross Profit", "Operating Income", "Net Income", "Free Cash Flow (FCF)"],
    "value_usd_billion": [95.0, 40.0, 15.0, 10.0, 18.0],
    "change_pct_yoy": [2.0, 5.0, 3.0, 4.0, 6.0] # Year-over-year change
}
df_financials = pd.DataFrame(key_financials_data)
df_financials["value_usd_billion"] = df_financials["value_usd_billion"].astype(float)
df_financials["change_pct_yoy"] = df_financials["change_pct_yoy"].astype(float)

# Simulate Capital Allocation
capital_allocation_data = {
    "category": ["Dividends", "Share Buybacks", "Acquisitions", "R&D"],
    "amount_usd_billion": [6.0, 5.0, 1.0, 8.0]
}
df_capital_allocation = pd.DataFrame(capital_allocation_data)

# Simulate Debt
debt_data = {
    "metric": ["Total Debt", "Net Debt / EBITDA"],
    "value": [50.0, 2.5] # Billion USD for Total Debt, ratio for Net Debt/EBITDA
}
df_debt = pd.DataFrame(debt_data)

# --- App Structure ---
st.title("IBM (International Business Machines Corporation) Financial Ecosystem Analysis")
st.markdown("""
This application provides an in-depth analysis of IBM's financial ecosystem, exploring its business model, market dependencies, competitive landscape, and key financial relationships.
The data presented here is illustrative, simulating the insights derived from a comprehensive financial analysis.
""")

# --- Sidebar ---
with st.sidebar:
    st.header("Analysis Sections")
    st.markdown("- [Key Metrics & Overview](#key-metrics--overview)")
    st.markdown("- [Revenue Streams & Profitability](#revenue-streams--profitability)")
    st.markdown("- [Capital Allocation & Balance Sheet](#capital-allocation--balance-sheet)")
    st.markdown("- [Market Dependencies & Economic Factors](#market-dependencies--economic-factors)")
    st.markdown("- [Sector Connections & Competitors](#sector-connections--competitors)")
    st.markdown("- [Strategic Partnerships & Ecosystem](#strategic-partnerships--ecosystem)")
    st.markdown("- [Key Risks & Catalysts](#key-risks--catalysts)")
    st.markdown("- [Summary](#summary)")

    st.markdown("---")
    st.header("Data Sources")
    st.markdown("This analysis is based on a simulated dataset that reflects typical financial reporting and strategic positioning of IBM. In a real-world scenario, this data would be sourced from official financial statements (10-K, 10-Q), investor relations reports, and reputable financial data providers.")

# --- Key Metrics & Overview ---
st.header("Key Metrics & Overview")
st.markdown("IBM is transforming its business model, focusing on hybrid cloud and AI. This section highlights its current financial health and strategic direction.")

# Metric Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    format_metric_card(df_financials.loc[df_financials['metric'] == 'Total Revenue', 'value_usd_billion'].iloc[0], "Total Revenue (USD Bn)", prefix="$")
with col2:
    format_metric_card(df_financials.loc[df_financials['metric'] == 'Free Cash Flow (FCF)', 'value_usd_billion'].iloc[0], "Free Cash Flow (USD Bn)", prefix="$")
with col3:
    format_metric_card(df_debt.loc[df_debt['metric'] == 'Net Debt / EBITDA', 'value'].iloc[0], "Net Debt / EBITDA", suffix="")
with col4:
    # Simulating a dividend yield for illustrative purposes
    avg_total_revenue = df_financials.loc[df_financials['metric'] == 'Total Revenue', 'value_usd_billion'].iloc[0]
    avg_dividends = df_capital_allocation.loc[df_capital_allocation['category'] == 'Dividends', 'amount_usd_billion'].iloc[0]
    dividend_yield = (avg_dividends / avg_total_revenue) * 100 if avg_total_revenue else 0
    format_metric_card(dividend_yield, "Dividend Yield", suffix="%")

st.markdown("---")

# --- Revenue Streams & Profitability ---
st.header("Revenue Streams & Profitability")
st.markdown("IBM's revenue is derived from several key segments, with a strategic emphasis on high-margin software and consulting services.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Segment")
    fig_revenue_bar = create_bar_chart(df_segments, "segment", "revenue_usd_billion", "Revenue by Segment (USD Billion)",
                                       color_col="segment",
                                       hover_data=["segment", "revenue_usd_billion", "revenue_share_pct"])
    st.plotly_chart(fig_revenue_bar, use_container_width=True)

    st.subheader("Recurring Revenue Contribution")
    fig_recurring_revenue = create_bar_chart(df_segments, "segment", "recurring_revenue_pct", "Recurring Revenue (%) by Segment",
                                            color_col="segment",
                                             hover_data=["segment", "recurring_revenue_pct"])
    st.plotly_chart(fig_recurring_revenue, use_container_width=True)


with col2:
    st.subheader("Revenue Share")
    fig_revenue_share = create_pie_chart(df_segments, "segment", "revenue_share_pct", "Revenue Share by Segment",
                                         hover_data=["segment", "revenue_share_pct", "revenue_usd_billion"])
    st.plotly_chart(fig_revenue_share, use_container_width=True)

    st.subheader("Profitability by Segment")
    fig_profitability = go.Figure()
    fig_profitability.add_trace(go.Bar(
        x=df_segments['segment'],
        y=df_segments['gross_margin_pct'],
        name='Gross Margin (%)',
        marker_color='rgb(55, 83, 109)',
        hovertemplate='<b>%{x}</b><br>Gross Margin: %{y:.1f}%<extra></extra>'
    ))
    fig_profitability.add_trace(go.Bar(
        x=df_segments['segment'],
        y=df_segments['operating_margin_pct'],
        name='Operating Margin (%)',
        marker_color='rgb(26, 118, 255)',
        hovertemplate='<b>%{x}</b><br>Operating Margin: %{y:.1f}%<extra></extra>'
    ))
    fig_profitability.update_layout(
        title_text="Segment Profitability (Gross & Operating Margins)",
        title_x=0.5,
        yaxis_title="Percentage (%)",
        xaxis_title="Segment",
        margin=dict(l=20, r=20, t=50, b=20),
        template="plotly_white",
        barmode='group'
    )
    st.plotly_chart(fig_profitability, use_container_width=True)

st.markdown("---")

# --- Capital Allocation & Balance Sheet ---
st.header("Capital Allocation & Balance Sheet")
st.markdown("IBM prioritizes returning value to shareholders through dividends and buybacks, supported by strong free cash flow generation. Its debt management is key to its financial stability.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Capital Allocation Priorities")
    fig_capital = px.pie(df_capital_allocation,
                         names='category',
                         values='amount_usd_billion',
                         title='Approximate Annual Capital Allocation (Illustrative)',
                         hole=0.3,
                         template="plotly_white")
    fig_capital.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20),
        legend_title_text='Allocation Category'
    )
    st.plotly_chart(fig_capital, use_container_width=True)

with col2:
    st.subheader("Balance Sheet Health")
    st.write("IBM's balance sheet is carefully managed, with a focus on deleveraging post-acquisitions and maintaining a strong credit profile.")
    debt_metric_col, debt_value_col = st.columns(2)
    with debt_metric_col:
        st.write("**Metric**")
        for index, row in df_debt.iterrows():
            st.write(row['metric'])
    with debt_value_col:
        st.write("**Value**")
        st.write(format_currency(df_debt.loc[df_debt['metric'] == 'Total Debt', 'value'].iloc[0]))
        st.write(f"{df_debt.loc[df_debt['metric'] == 'Net Debt / EBITDA', 'value'].iloc[0]:.1f}x")

    st.markdown("*Note: Total Debt is an illustrative billion USD figure; Net Debt/EBITDA is a key leverage ratio.*")


st.markdown("---")

# --- Market Dependencies & Economic Factors ---
st.header("Market Dependencies & Economic Factors")
st.markdown("IBM's performance is deeply intertwined with the broader economic environment and the technology spending patterns of large enterprises.")

st.subheader("Key Market Dependencies")
dependencies = [
    "Enterprise IT Spending Cycles",
    "Cloud Adoption & Hybrid-Cloud Maturity",
    "Digital Transformation Initiatives",
    "Artificial Intelligence (AI) Adoption",
    "Global Economic Growth",
    "Regulatory & Compliance Demands"
]
for dep in dependencies:
    st.markdown(f"- **{dep}:** IBM's revenue is directly influenced by companies' willingness and ability to invest in technology solutions.")

st.subheader("Economic Sensitivity")
st.markdown("""
- **Interest Rates:** IBM, as a dividend-paying stock, competes with fixed income. Higher rates can make its dividend less attractive. Its financing segment is also rate-sensitive.
- **Inflation:** Can impact operating costs but IBM's long-term contracts and pricing power in certain segments (e.g., software) can mitigate some effects.
- **Foreign Exchange (FX):** Significant international revenue means currency fluctuations can impact reported results. A strong USD generally reduces reported earnings.
- **Geopolitical Stability:** Global events can disrupt supply chains, affect market access, and influence corporate investment decisions.
""")

st.markdown("---")

# --- Sector Connections & Competitors ---
st.header("Sector Connections & Competitors")
st.markdown("IBM operates within the broad Technology sector, but its specific activities place it in direct competition and partnership with various industry players.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Primary Sector Focus")
    st.markdown("""
    - **Information Technology**
    - **Sub-sectors:**
        - IT Services & Consulting
        - Systems Software (Hybrid Cloud Platforms, AI, Data)
        - Enterprise Hardware & Infrastructure
    """)

with col2:
    st.subheader("Key Competitors & Ecosystem Players")
    st.markdown("""
    - **Hybrid Cloud & AI Platforms:** Microsoft (Azure), Amazon (AWS), Google Cloud (Alphabet). IBM differentiates with its hybrid-by-design approach via Red Hat.
    - **Enterprise Consulting & IT Services:** Accenture, Deloitte, Infosys, TCS.
    - **Enterprise Software:** Oracle, SAP, Salesforce (in specific areas).
    - **Infrastructure:** HPE, Dell (for non-mainframe hardware).
    - **Emerging:** Specialized AI firms, Quantum computing rivals.
    """)

st.markdown("---")

# --- Strategic Partnerships & Ecosystem ---
st.header("Strategic Partnerships & Ecosystem")
st.markdown("IBM's strategy heavily relies on its ability to integrate and collaborate within a complex technology ecosystem.")

st.subheader("Lynchpins of the Ecosystem")
st.markdown("""
- **Red Hat (OpenShift):** The core of IBM's hybrid cloud strategy. OpenShift acts as a common platform across on-premise and multiple public clouds (AWS, Azure, GCP), fostering collaboration with cloud providers.
- **System Integrators & VARs:** Crucial for reaching and servicing large enterprise clients.
- **Independent Software Vendors (ISVs):** IBM enables ISVs to deploy their applications on Red Hat OpenShift, expanding its software reach.
- **Academic & Government Labs:** Partnerships for cutting-edge research (AI, Quantum Computing).
""")

st.markdown("---")

# --- Key Risks & Catalysts ---
st.header("Key Risks & Catalysts")
st.markdown("Understanding the potential upside and downside factors is crucial for assessing IBM's future trajectory.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Potential Catalysts (Upside)")
    st.markdown("""
    - **Accelerated Hybrid Cloud Adoption:** Increased enterprise migration to hybrid cloud models where IBM/Red Hat is chosen as the primary platform.
    - **Growth in AI (watsonx):** Successful productization and adoption of IBM's AI platform, driving software revenue and high-margin consulting engagements.
    - **Strong FCF Generation & Capital Returns:** Continued robust free cash flow, enabling sustained dividend growth and share buybacks, appealing to value investors.
    - **Breakthroughs in Quantum Computing:** Commercial viability and adoption of quantum solutions, though a longer-term prospect.
    """)

with col2:
    st.subheader("Major Risks (Downside)")
    st.markdown("""
    - **Intense Competition:** Sustained pressure from hyperscale cloud providers (AWS, Azure, GCP) and agile software competitors.
    - **Execution Risk:** Failure to grow strategic software and consulting segments fast enough to offset declines in legacy businesses.
    - **Macroeconomic Slowdown:** A significant recession could reduce enterprise IT spending, impacting consulting and new software deals.
    - **Legacy Liabilities:** Management of pension obligations and other historical liabilities.
    - **Technological Disruption:** Rapid shifts in cloud architecture or AI paradigms that IBM fails to adapt to.
    """)

st.markdown("---")

# --- Summary ---
st.header("Summary of IBM's Financial Ecosystem")
st.markdown("""
IBM is a company in transition, leveraging its deep enterprise relationships and technological innovation to pivot towards a hybrid cloud and AI future. Its financial ecosystem is characterized by:

*   **Strategic Shift:** A clear focus on high-margin, recurring revenue from Software (driven by Red Hat) and Consulting, while managing the cyclicality of its Infrastructure segment.
*   **Cash Flow Powerhouse:** Consistent and strong Free Cash Flow generation is the bedrock of its financial strategy, enabling significant shareholder returns through dividends and buybacks.
*   **Value-Oriented Investor Profile:** IBM is primarily viewed as a value and income stock, appealing to investors seeking stability and yield, with a speculative growth component tied to its transformation.
*   **Complex Competitive Landscape:** Navigating intense competition from hyperscalers and established software giants, IBM differentiates through its hybrid-by-design approach and deep integration capabilities.
*   **Market Dependencies:** Heavily reliant on enterprise IT spending, which makes it sensitive to economic cycles, though less so than many other tech firms due to its mission-critical services.

Understanding these interconnected elements provides a holistic view of the forces shaping IBM's financial present and future.
""")

st.markdown("---")
st.markdown("Report generated by the IBM Financial Ecosystem Analyzer.")