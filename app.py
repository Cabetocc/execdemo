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
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import textwrap

# --- Page Configuration ---
st.set_page_config(
    page_title="IBM Financial Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Helper Functions ---

def wrap_text(text, width=50):
    """Wraps text to a specified width for better display in Streamlit."""
    return textwrap.fill(text, width=width)

def format_currency(value):
    """Formats numbers into a readable currency string."""
    if abs(value) >= 1e9:
        return f"${value / 1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value / 1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value / 1e3:.2f}K"
    return f"${value:.2f}"

def format_growth(value):
    """Formats numbers into a readable percentage string."""
    return f"{value:.2f}%"

def create_revenue_chart(data):
    """Creates a bar chart for revenue breakdown."""
    fig = go.Figure(data=[
        go.Bar(name='Revenue (2023)', x=data['Segment'], y=data['Revenue_Billions'],
               marker_color=data['Color'])
    ])

    fig.update_layout(
        title_text='IBM Revenue Breakdown by Segment (2023)',
        xaxis_title='Segment',
        yaxis_title='Revenue (Billions USD)',
        legend_title='Segment',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        hovermode='x unified'
    )
    return fig

def create_profitability_chart(data):
    """Creates a line chart for profitability metrics."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['Year'], y=data['Gross_Margin'], mode='lines+markers', name='Gross Margin (%)',
        line=dict(color='cyan', width=2), marker=dict(color='cyan')
    ))
    fig.add_trace(go.Scatter(
        x=data['Year'], y=data['Operating_Margin'], mode='lines+markers', name='Operating Margin (%)',
        line=dict(color='magenta', width=2), marker=dict(color='magenta')
    ))

    fig.update_layout(
        title_text='IBM Profitability Trends (Gross & Operating Margins)',
        xaxis_title='Year',
        yaxis_title='Margin (%)',
        legend_title='Metric',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    return fig

def create_cashflow_chart(data):
    """Creates a bar chart for cash flow metrics."""
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Operating Cash Flow', 'Free Cash Flow'))

    fig.add_trace(go.Bar(
        name='Operating Cash Flow (Billions USD)',
        x=data['Year'], y=data['Operating_Cash_Flow_Billions'],
        marker_color='teal'
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        name='Free Cash Flow (Billions USD)',
        x=data['Year'], y=data['Free_Cash_Flow_Billions'],
        marker_color='gold'
    ), row=1, col=2)

    fig.update_layout(
        title_text='IBM Cash Flow Generation',
        yaxis1_title='Billions USD',
        yaxis2_title='Billions USD',
        legend_title='Metric',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=450 # Adjust height for better readability
    )
    return fig

def create_shareholder_return_chart(data):
    """Creates a bar chart for shareholder returns."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Dividends Paid (Billions USD)',
        x=data['Year'], y=data['Dividends_Paid_Billions'],
        marker_color='forestgreen'
    ))
    fig.add_trace(go.Bar(
        name='Share Buybacks (Billions USD)',
        x=data['Year'], y=data['Share_Buybacks_Billions'],
        marker_color='indianred'
    ))

    fig.update_layout(
        title_text='IBM Shareholder Returns',
        xaxis_title='Year',
        yaxis_title='Billions USD',
        legend_title='Activity',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    return fig

# --- Sample Data (Replace with actual fetched data if available) ---
# This data is illustrative and based on the analysis provided.
# In a real application, this would come from APIs like Yahoo Finance, financial data providers, etc.

# Revenue Data
revenue_data_2023 = pd.DataFrame({
    'Segment': [
        'Cloud & Cognitive Software',
        'Consulting',
        'Infrastructure',
        'Financing'
    ],
    'Revenue_Billions': [45.7, 36.7, 25.0, 3.2],
    'Color': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] # Consistent colors
})
revenue_data_2023['Revenue_Billions'] = revenue_data_2023['Revenue_Billions'].astype(float)
revenue_data_2023['Revenue_Billions_Formatted'] = revenue_data_2023['Revenue_Billions'].apply(format_currency)

# Profitability Data
profitability_data = pd.DataFrame({
    'Year': [2021, 2022, 2023],
    'Gross_Margin': [52.3, 53.2, 55.9],
    'Operating_Margin': [12.0, 13.9, 15.3]
})
profitability_data['Gross_Margin_Formatted'] = profitability_data['Gross_Margin'].apply(format_growth)
profitability_data['Operating_Margin_Formatted'] = profitability_data['Operating_Margin'].apply(format_growth)


# Cash Flow Data
cashflow_data = pd.DataFrame({
    'Year': [2021, 2022, 2023],
    'Operating_Cash_Flow_Billions': [13.4, 12.0, 14.2],
    'Free_Cash_Flow_Billions': [11.4, 9.3, 11.2]
})
cashflow_data['Operating_Cash_Flow_Billions_Formatted'] = cashflow_data['Operating_Cash_Flow_Billions'].apply(format_currency)
cashflow_data['Free_Cash_Flow_Billions_Formatted'] = cashflow_data['Free_Cash_Flow_Billions'].apply(format_currency)


# Shareholder Returns Data
shareholder_data = pd.DataFrame({
    'Year': [2021, 2022, 2023],
    'Dividends_Paid_Billions': [6.5, 6.7, 7.1],
    'Share_Buybacks_Billions': [3.0, 2.0, 1.5] # Example figures
})
shareholder_data['Dividends_Paid_Billions_Formatted'] = shareholder_data['Dividends_Paid_Billions'].apply(format_currency)
shareholder_data['Share_Buybacks_Billions_Formatted'] = shareholder_data['Share_Buybacks_Billions'].apply(format_currency)

# Key Metrics Summary
key_metrics_data = {
    "Market Cap": "$150B",
    "Revenue (2023)": "$93.1B",
    "Net Income (2023)": "$7.5B",
    "EPS (2023)": "$8.23",
    "Operating Cash Flow (2023)": "$14.2B",
    "Free Cash Flow (2023)": "$11.2B",
    "Debt to Equity Ratio": "1.4x", # Illustrative
    "Dividend Yield": "4.0%",
    "P/E Ratio": "18.2x", # Illustrative
}

# --- Sidebar ---
st.sidebar.title("IBM Financial Analysis")
st.sidebar.markdown("---")
st.sidebar.header("Sections")
st.sidebar.markdown("[1. Overview](#overview)")
st.sidebar.markdown("[2. Key Financial Metrics](#key-financial-metrics)")
st.sidebar.markdown("[3. Revenue & Business Segments](#revenue--business-segments)")
st.sidebar.markdown("[4. Profitability Analysis](#profitability-analysis)")
st.sidebar.markdown("[5. Cash Flow Generation](#cash-flow-generation)")
st.sidebar.markdown("[6. Shareholder Returns](#shareholder-returns)")
st.sidebar.markdown("[7. Market Dependencies & Sector Connections](#market-dependencies--sector-connections)")
st.sidebar.markdown("[8. Competitor Landscape](#competitor-landscape)")
st.sidebar.markdown("[9. Economic Factors & Risks](#economic-factors--risks)")
st.sidebar.markdown("[10. Conclusion & Outlook](#conclusion--outlook)")

st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info(
    "This app provides a financial analysis of IBM (International Business Machines Corporation) "
    "based on the provided text. It aims to extract key metrics, visualize performance, "
    "and summarize important aspects of its business ecosystem. "
    "Please note that the data presented here is illustrative and for demonstration purposes."
)

# --- Main Content ---

st.title("IBM (International Business Machines Corporation) - Financial Analysis")
st.markdown("---")

# --- Overview Section ---
st.header("1. Overview")
st.markdown(wrap_text(
    "IBM is a mature technology and consulting company with a long history. Its strategic focus has shifted "
    "towards **hybrid cloud, Artificial Intelligence (AI), and enterprise software/services**. "
    "Key business segments include Cloud & Cognitive Software, Consulting, and Infrastructure. "
    "The company aims to leverage its acquisition of Red Hat to lead in the hybrid cloud market."
))
st.markdown("---")

# --- Key Financial Metrics Section ---
st.header("2. Key Financial Metrics")
st.markdown("Below is a summary of IBM's key financial metrics (illustrative data).")

# Display key metrics in a structured way
cols = st.columns(3)
for i, (metric, value) in enumerate(key_metrics_data.items()):
    with cols[i % 3]:
        st.metric(label=metric, value=value)

st.markdown("---")

# --- Revenue & Business Segments Section ---
st.header("3. Revenue & Business Segments")
st.markdown(wrap_text(
    "IBM's revenue is diversified across several segments, with a strategic push towards higher-margin "
    "software and consulting services. Recurring revenue from software subscriptions is a key focus for "
    "stability and predictability. The shift post-Red Hat acquisition has significantly boosted its hybrid cloud and "
    "open-source footprint."
))

# Create and display revenue chart
revenue_fig = create_revenue_chart(revenue_data_2023)
st.plotly_chart(revenue_fig, use_container_width=True)

st.markdown("#### Revenue Breakdown Highlights (Illustrative 2023 Data):")
for index, row in revenue_data_2023.iterrows():
    st.markdown(f"- **{row['Segment']}**: {row['Revenue_Billions_Formatted']} (Approx. {row['Revenue_Billions']/revenue_data_2023['Revenue_Billions'].sum()*100:.1f}%)")

st.markdown("---")

# --- Profitability Analysis Section ---
st.header("4. Profitability Analysis")
st.markdown(wrap_text(
    "IBM's profitability is closely watched, with analysts focusing on gross and operating margins across its segments. "
    "The increasing contribution of high-margin software and consulting, along with operational efficiencies, "
    "has been a driver for improved profitability."
))

# Create and display profitability chart
profitability_fig = create_profitability_chart(profitability_data)
st.plotly_chart(profitability_fig, use_container_width=True)

st.markdown("#### Profitability Trend Insights:")
for index, row in profitability_data.iterrows():
    st.markdown(f"- **{row['Year']}**: Gross Margin: {row['Gross_Margin_Formatted']}, Operating Margin: {row['Operating_Margin_Formatted']}")

st.markdown("---")

# --- Cash Flow Generation Section ---
st.header("5. Cash Flow Generation")
st.markdown(wrap_text(
    "IBM is known for its strong cash flow generation, a critical component for funding its operations, "
    "dividends, share buybacks, and strategic investments. Free Cash Flow (FCF) is a key metric "
    "indicating cash available after capital expenditures."
))

# Create and display cash flow chart
cashflow_fig = create_cashflow_chart(cashflow_data)
st.plotly_chart(cashflow_fig, use_container_width=True)

st.markdown("#### Cash Flow Highlights:")
for index, row in cashflow_data.iterrows():
    st.markdown(f"- **{row['Year']}**: Operating Cash Flow: {row['Operating_Cash_Flow_Billions_Formatted']}, Free Cash Flow: {row['Free_Cash_Flow_Billions_Formatted']}")

st.markdown("---")

# --- Shareholder Returns Section ---
st.header("6. Shareholder Returns")
st.markdown(wrap_text(
    "IBM has a long history of returning capital to shareholders through consistent dividends and share buybacks. "
    "Its status as a 'dividend aristocrat' underscores its commitment to income-focused investors."
))

# Create and display shareholder returns chart
shareholder_fig = create_shareholder_return_chart(shareholder_data)
st.plotly_chart(shareholder_fig, use_container_width=True)

st.markdown("#### Shareholder Return Highlights:")
for index, row in shareholder_data.iterrows():
    st.markdown(f"- **{row['Year']}**: Dividends Paid: {row['Dividends_Paid_Billions_Formatted']}, Share Buybacks: {row['Share_Buybacks_Billions_Formatted']}")

st.markdown("---")

# --- Market Dependencies & Sector Connections Section ---
st.header("7. Market Dependencies & Sector Connections")
st.markdown(wrap_text(
    "IBM's business is deeply influenced by enterprise IT spending cycles, the pace of digital transformation, "
    "and the adoption of hybrid cloud and AI technologies. It operates within sectors like Software, IT Consulting, "
    "and Infrastructure, facing competition from major tech players."
))
st.markdown("Key dependencies include:")
st.markdown("- **Enterprise IT Spending**: Directly impacts demand for IBM's solutions.")
st.markdown("- **Hybrid Cloud & AI Adoption**: Primary growth drivers for its strategic pivot.")
st.markdown("- **Digital Transformation Trends**: Fuels demand for consulting and modernization services.")
st.markdown("- **Regulated Industries**: IBM targets sectors like financial services and healthcare, where its trust and hybrid cloud focus are advantageous.")
st.markdown("---")

# --- Competitor Landscape Section ---
st.header("8. Competitor Landscape")
st.markdown(wrap_text(
    "IBM faces a diverse set of competitors. In cloud and AI, it competes with hyperscalers like AWS, Microsoft Azure, "
    "and Google Cloud, though its hybrid approach offers differentiation. In consulting, it contends with firms "
    "like Accenture and Deloitte. Specialized competition exists in software (Microsoft, Oracle, SAP) and infrastructure (HPE, Dell)."
))
st.markdown("Key competitor categories:")
st.markdown("- **Hyperscalers**: AWS, Microsoft Azure, Google Cloud (indirect competition for cloud workloads).")
st.markdown("- **Enterprise Software & AI**: Microsoft, Oracle, SAP, Salesforce.")
st.markdown("- **IT Services & Consulting**: Accenture, Deloitte, Capgemini, Cognizant.")
st.markdown("- **Infrastructure**: HPE, Dell Technologies.")
st.markdown("The Red Hat acquisition enhances its position in open-source and hybrid cloud platforms.")
st.markdown("---")

# --- Economic Factors & Risks Section ---
st.header("9. Economic Factors & Risks")
st.markdown(wrap_text(
    "IBM's performance is sensitive to macroeconomic conditions. Global economic growth, interest rates, "
    "inflation, and geopolitical stability can significantly impact enterprise spending, borrowing costs, "
    "and supply chains. Regulatory changes related to data privacy and sovereignty also play a crucial role."
))
st.markdown("Key factors and risks:")
st.markdown("- **Macroeconomic Headwinds**: Slowdowns can affect IT budgets and project timelines.")
st.markdown("- **Interest Rate Sensitivity**: Impacts borrowing costs and client financing.")
st.markdown("- **Currency Fluctuations**: As a global company, FX rates affect reported earnings.")
st.markdown("- **Geopolitical Instability & Trade Policies**: Can disrupt operations and international sales.")
st.markdown("- **Regulatory Landscape**: Data privacy, sovereignty, and compliance requirements.")
st.markdown("- **Competitive Pressure**: Intense competition from hyperscalers and other tech giants.")
st.markdown("- **Execution Risk**: Successfully executing its hybrid cloud and AI strategy is paramount.")
st.markdown("---")

# --- Conclusion & Outlook Section ---
st.header("10. Conclusion & Outlook")
st.markdown(wrap_text(
    "IBM is navigating a complex transition, aiming to re-establish growth through its hybrid cloud and AI strategy. "
    "Its financial strength, characterized by robust cash flow and consistent shareholder returns, provides a solid foundation. "
    "Success hinges on its ability to capture the enterprise AI market, drive adoption of its Red Hat-based solutions, "
    "and manage the decline of legacy businesses effectively. While facing significant competition and macroeconomic uncertainties, "
    "IBM's focus on hybrid cloud, enterprise trust, and AI integration positions it for continued relevance in the evolving tech landscape."
))
st.markdown("---")

st.markdown("<p style='text-align: center; color: gray;'>© 2023 IBM Financial Analysis App | Data is illustrative and for educational purposes only.</p>", unsafe_allow_html=True)