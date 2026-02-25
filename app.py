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

ticker = st.text_input("Enter stock ticker", value="?").upper().strip()
generate = st.button("Generate")

if st.button("Generate"):
    payload = {"ticker": ticker}
    try:
        r = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        st.write("Status:", r.status_code)
        st.code(r.text[:1000])
        r.raise_for_status()
    except Exception as e:
        st.error(f"Webhook call failed: {e}")

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

            if updated == before:
                status.warning("Still processing. Please wait a bit longer and press Generate again (or refresh).")

        st.rerun()


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def create_app():
    st.set_page_config(
        page_title="IBM Financial Ecosystem Analysis",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🌐 IBM (IBM): A Financial Ecosystem Analysis")
    st.markdown(
        """
        This application breaks down the financial ecosystem of IBM (International Business Machines Corporation)
        based on the provided qualitative analysis. While the original text doesn't contain specific numerical data,
        this app visualizes key relationships using illustrative, synthetic data to reflect the described trends and proportions.
        """
    )

    st.info(
        "**Note:** All charts and numerical data presented are **illustrative and synthetic**, "
        "designed to visualize the qualitative relationships described in the provided text. "
        "They do not represent actual IBM financial data."
    )

    # --- Section 1: Key Financial Relationships ---
    st.header("1. Key Financial Relationships")

    with st.expander("Read full analysis of Key Financial Relationships"):
        st.markdown(
            """
            IBM's financial health is driven by several core relationships within its business segments and its overall financial structure.

            *   **Revenue Diversification:** IBM's revenue streams are segmented into Software, Consulting, Infrastructure, and Financing.
                The strength and growth of its **Software** and **Consulting** segments are paramount for driving overall revenue growth and improving profitability.
            *   **Profitability and Margins:** Software and Consulting generally boast higher gross margins than Infrastructure. IBM's strategic shift aims to improve and stabilize overall profit margins.
            *   **Cash Flow Generation:** IBM has historically been a strong Operating Cash Flow (OCF) generator. Strong Free Cash Flow (FCF) is critical for dividends, share buybacks, and strategic acquisitions.
            *   **Debt Structure and Leverage:** IBM carries significant debt. Managing debt levels and maintaining a strong credit rating is crucial.
            *   **Capital Allocation:** Balance between dividend payouts, buybacks, and strategic investments significantly impacts shareholder value.
            """
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Diversification (Illustrative)")
        # Synthetic data for Revenue Diversification
        revenue_data = {
            'Segment': ['Software', 'Consulting', 'Infrastructure', 'Financing'],
            'Revenue Share (%)': [35, 30, 25, 10]
        }
        df_revenue = pd.DataFrame(revenue_data)

        fig_revenue = px.pie(
            df_revenue,
            values='Revenue Share (%)',
            names='Segment',
            title='Illustrative Revenue Share by Segment',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_revenue.update_traces(textposition='inside', textinfo='percent+label')
        fig_revenue.update_layout(showlegend=True)
        st.plotly_chart(fig_revenue, use_container_width=True)

    with col2:
        st.subheader("Gross Margins by Segment (Illustrative)")
        # Synthetic data for Gross Margins
        margin_data = {
            'Segment': ['Software', 'Consulting', 'Infrastructure'],
            'Gross Margin (%)': [75, 60, 40] # Software > Consulting > Infrastructure
        }
        df_margin = pd.DataFrame(margin_data)

        fig_margin = px.bar(
            df_margin,
            x='Segment',
            y='Gross Margin (%)',
            title='Illustrative Gross Margins by Segment',
            color='Segment',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_margin.update_yaxes(range=[0, 100], ticksuffix="%")
        st.plotly_chart(fig_margin, use_container_width=True)

    st.subheader("Cash Flow Generation (Illustrative)")
    # Synthetic data for Cash Flow
    cash_flow_data = {
        'Year': [2021, 2022, 2023],
        'Operating Cash Flow (Billions USD)': [12, 13, 14],
        'Free Cash Flow (Billions USD)': [9, 10, 11]
    }
    df_cash_flow = pd.DataFrame(cash_flow_data)

    fig_cash_flow = px.line(
        df_cash_flow,
        x='Year',
        y=['Operating Cash Flow (Billions USD)', 'Free Cash Flow (Billions USD)'],
        title='Illustrative Operating vs. Free Cash Flow',
        markers=True,
        line_shape='spline',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig_cash_flow.update_yaxes(title_text="Billions USD")
    fig_cash_flow.update_xaxes(dtick="1")
    st.plotly_chart(fig_cash_flow, use_container_width=True)


    # --- Section 2: Market Dependencies & Strategic Focus ---
    st.header("2. Market Dependencies & Strategic Focus")

    with st.expander("Read full analysis of Market Dependencies"):
        st.markdown(
            """
            IBM operates in markets with specific dependencies:

            *   **Cloud Computing Market:** Its future is intrinsically linked to hybrid cloud solutions.
            *   **Artificial Intelligence (AI) & Machine Learning (ML) Market:** AI is a core pillar of IBM's strategy.
            *   **Enterprise IT Spending:** Directly impacts IBM's top line.
            *   **Digital Transformation Market:** Businesses undergoing constant digital transformation.
            *   **Cybersecurity Market:** Increasing threat landscape drives demand for solutions.
            """
        )

    # Synthetic data for Strategic Focus Areas
    focus_areas_data = {
        'Focus Area': ['Hybrid Cloud Adoption', 'AI & ML Market', 'Digital Transformation', 'Cybersecurity', 'Enterprise IT Spending'],
        'Strategic Importance': [5, 5, 4, 3, 5] # Scale of 1-5
    }
    df_focus = pd.DataFrame(focus_areas_data)

    fig_focus = px.bar(
        df_focus,
        x='Strategic Importance',
        y='Focus Area',
        orientation='h',
        title='IBM\'s Illustrative Strategic Focus Areas (Importance Scale 1-5)',
        color='Strategic Importance',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig_focus.update_xaxes(range=[0, 5.5], tickvals=[1, 2, 3, 4, 5])
    st.plotly_chart(fig_focus, use_container_width=True)


    # --- Section 3: Sector Connections & Competitor Relationships ---
    st.header("3. Sector Connections & Competitor Relationships")

    with st.expander("Read full analysis of Sector Connections & Competitor Relationships"):
        st.markdown(
            """
            IBM straddles multiple technology and service sectors:
            *   **Software Sector:** Enterprise software, cloud platforms, data analytics, AI.
            *   **IT Services & Consulting Sector:** Competing with major consulting firms.
            *   **Hardware & Infrastructure Sector:** Mainframes, servers.
            *   **Cloud Computing Sector:** Hybrid cloud offerings.
            *   **Financial Technology (FinTech) Sector:** Solutions for financial institutions.

            IBM faces intense competition across its diverse business lines from:
            *   **Cloud & Software Competitors:** AWS, Microsoft Azure, GCP, Oracle, SAP.
            *   **Consulting Competitors:** Deloitte, PwC, Accenture, Capgemini.
            *   **Infrastructure Competitors:** Dell Technologies, HP Enterprise.
            """
        )

    st.subheader("Competitive Landscape (Illustrative Categorization)")
    competitors_data = {
        'Category': [
            'Major Cloud Providers', 'Enterprise Software', 'IT Services & Consulting',
            'Infrastructure Hardware', 'AI/Analytics Specialists'
        ],
        'IBM Competitors': [
            'AWS, Azure, GCP', 'Oracle, SAP, Microsoft', 'Accenture, Deloitte, Capgemini',
            'Dell, HPE', 'Specialized AI firms'
        ]
    }
    df_competitors = pd.DataFrame(competitors_data)

    fig_competitors = go.Figure(data=[go.Table(
        header=dict(values=list(df_competitors.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_competitors['Category'], df_competitors['IBM Competitors']],
                   fill_color='lavender',
                   align='left'))
    ])
    fig_competitors.update_layout(title_text="Illustrative IBM Competitors by Category")
    st.plotly_chart(fig_competitors, use_container_width=True)


    # --- Section 4: Economic Factors Impacting IBM ---
    st.header("4. Economic Factors Impacting IBM")

    with st.expander("Read full analysis of Economic Factors"):
        st.markdown(
            """
            IBM's performance is sensitive to broader economic trends:

            *   **Global Economic Growth:** Strong growth increases enterprise IT spending; recessions lead to budget cuts.
            *   **Interest Rates:** Higher rates increase borrowing costs for IBM and influence investor demand.
            *   **Inflation:** Can increase operating costs but also potentially passed on to customers.
            *   **Geopolitical Stability:** Disrupts supply chains, affects international sales, increases uncertainty.
            *   **Technological Disruption:** Rapid pace of change (e.g., generative AI) presents both opportunities and threats.
            *   **Regulatory Environment:** Data privacy, antitrust scrutiny, cybersecurity mandates impact operations.
            *   **Currency Fluctuations:** Affects reported earnings for a global company.
            """
        )
    st.markdown(
        """
        These factors are predominantly qualitative. Instead of a chart, here's a summary of their potential impact:
        *   **Positive Impact:** Strong global economic growth, stable interest rates, effective management of inflation,
            geopolitical stability, successful adaptation to technological disruption, favorable regulatory environment,
            and stable currency exchange rates.
        *   **Negative Impact:** Economic slowdowns/recessions, rising interest rates, high inflation, geopolitical
            instability, failure to adapt to technological shifts, stringent or unfavorable regulations, and adverse
            currency fluctuations.
        """
    )


    # --- Section 5: Conclusion & Key Metrics to Monitor ---
    st.header("5. Conclusion & Key Metrics to Monitor")

    with st.expander("Read full Conclusion"):
        st.markdown(
            """
            IBM operates within a dynamic and competitive financial ecosystem. Its strategic pivot towards hybrid cloud and AI
            aims to reposition it for future growth in higher-margin, recurring revenue businesses.
            Its financial success is dependent on its ability to:
            *   Execute its hybrid cloud strategy effectively.
            *   Drive innovation and adoption of its AI solutions.
            *   Maintain strong customer relationships and secure large enterprise contracts.
            *   Manage its debt and generate consistent free cash flow.
            *   Adapt to evolving economic conditions and technological disruptions.
            """
        )

    st.subheader("Key Metrics to Monitor (Illustrative Trends)")
    metrics_data = {
        'Metric': [
            'Revenue Growth by Segment (Software/Red Hat)',
            'Cloud/Hybrid Revenue Growth',
            'Gross Margin & Operating Margin Trends',
            'Free Cash Flow (FCF)',
            'Net Debt & Interest Coverage Ratio',
            'Dividend Payout Ratio vs FCF',
            'Major New Customer Wins/Renewals'
        ],
        'Illustrative Trend': [
            'Improving', 'Accelerating', 'Stable to Improving',
            'Stable to Improving', 'Stable', 'Stable', 'Consistent'
        ],
        'Why it Matters': [
            'Indicates success of strategic pivot',
            'Core to future growth engine',
            'Reflects higher-value business mix',
            'Funds dividends, buybacks, M&A',
            'Indicates financial health & flexibility',
            'Ensures dividend sustainability',
            'Signals market traction & demand'
        ]
    }
    df_metrics = pd.DataFrame(metrics_data)

    fig_metrics = go.Figure(data=[go.Table(
        header=dict(values=list(df_metrics.columns),
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[df_metrics['Metric'], df_metrics['Illustrative Trend'], df_metrics['Why it Matters']],
                   fill_color='aliceblue',
                   align='left',
                   height=30))
    ])
    fig_metrics.update_layout(title_text="Key Metrics for Investors/Analysts to Monitor")
    st.plotly_chart(fig_metrics, use_container_width=True)

    st.markdown("---")
    st.markdown(
        "**Disclaimer:** This app is for educational and illustrative purposes only and should not be considered "
        "financial advice. Please consult with a qualified financial professional for actual investment decisions."
    )

if __name__ == '__main__':
    create_app()
