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
import altair as alt

# --- Helper function for creating bar charts for peer comparison ---
def create_metrics_bar_chart(df, value_col, title, y_axis_label, highlight_company="AstraZeneca (AZN)"):
    """
    Creates a bar chart for peer metrics, highlighting a specific company.
    
    Args:
        df (pd.DataFrame): DataFrame containing company metrics.
        value_col (str): The column name representing the metric value.
        title (str): The title of the chart.
        y_axis_label (str): The label for the y-axis.
        highlight_company (str, optional): The name of the company to highlight.
                                           Defaults to "AstraZeneca (AZN)".
    Returns:
        alt.Chart: An Altair bar chart object.
    """
    # Ensure 'Company' column is nominal for correct sorting/labeling
    df['Company'] = df['Company'].astype(str)
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Company:N', 
                sort=alt.EncodingSortField(field=value_col, op="average", order='descending'), 
                title='Company'),
        y=alt.Y(value_col, title=y_axis_label),
        color=alt.condition(
            alt.datum['Company'] == highlight_company,
            alt.value('orange'), # Color for AstraZeneca
            alt.value('steelblue') # Color for others
        ),
        tooltip=['Company', alt.Tooltip(value_col, format='.1f')]
    ).properties(
        title=title
    ).interactive()
    return chart

# --- Streamlit App Configuration ---
st.set_page_config(layout="wide", page_title="AstraZeneca (AZN) Financial Analysis", icon="🔬")

st.title("🔬 AstraZeneca (AZN) - Forward-Looking Financial Analysis")
st.markdown("---")

st.subheader("Senior Equity Research Analyst View")

# --- Key Metrics Extraction & Display ---
st.header("📊 Key Metrics & Snapshot")
st.markdown("A quick overview of AstraZeneca's essential financial and operational indicators.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Ticker", value="AZN")
with col2:
    st.metric(label="Sector", value="Pharmaceuticals & Biotechnology")
with col3:
    # Extracted directly from text, approximate value
    st.metric(label="Market Cap", value="~$200 Billion") 
with col4:
    # Extracted directly from text
    st.metric(label="Q1 2024 Revenue Growth (ex-COVID)", value="19%", delta="Positive momentum")

st.markdown("### Growth & Financials (Estimates)")
col_a, col_b, col_c = st.columns(3)
with col_a:
    # Extracted from text
    st.metric(label="Expected Near-Term Revenue Growth", value="Mid-to-High Single Digits")
with col_b:
    # Extracted from text
    st.metric(label="Q1 2024 Core EPS Guidance", value="Raised", delta="Strong management confidence")
with col_c:
    # Extracted from text
    st.metric(label="Operating Margins", value="Healthy & Stable", delta="Potential for slight improvement")

st.markdown("---")

# --- Sections and Summaries: Fundamental Evaluation ---
st.header("📜 Fundamental Evaluation & Outlook")
st.markdown("AstraZeneca's robust performance is driven by its strong oncology portfolio, rapidly growing respiratory, and cardiovascular franchises.")

with st.expander("Next 3-6 Months Outlook"):
    st.markdown("""
    We anticipate continued strong performance for AZN in the near term. The company is well-positioned to benefit from ongoing demand for its established products and the incremental contributions from recent launches and pipeline advancements. We expect revenue growth to remain in the mid-to-high single digits, driven by a combination of volume increases and favorable pricing, particularly in the US and emerging markets. Margins should remain stable, with potential for slight improvement as the company continues to optimize its operational efficiency.
    """)

with st.expander("Key Catalysts (Next 3-6 Months)"):
    st.markdown("""
    1.  **Continued Momentum in Oncology:** Sustained strong sales of blockbuster cancer drugs like Tagrisso and Imfinzi. Positive data readouts from ongoing clinical trials for these drugs, potentially expanding their indications, could provide significant upward revisions to our forecasts.
    2.  **Growth in Cardiovascular, Renal & Metabolism (CVRM) and Respiratory & Immunology (R&I):** Increasing adoption of Farxiga (for diabetes, heart failure, and chronic kidney disease) and Lynparza (in oncology). We will be closely monitoring sales figures and market penetration for these drugs, as well as any new approvals or label expansions.
    3.  **Pipeline Advancements & Strategic Partnerships:** Any positive updates from Phase III trial readouts or regulatory submissions for its novel pipeline candidates (e.g., in Alzheimer's, rare diseases) could be a significant catalyst. Furthermore, strategic partnerships or acquisitions that bolster its R&D capabilities or market access will be closely watched.
    """)

st.markdown("---")

# --- Peer Benchmarking and Visualizations ---
st.header("⚖️ Peer Benchmarking")
st.markdown("A comparison of AstraZeneca against its key competitors across various financial metrics.")

# Data for Peer Benchmarking Table (Midpoints of ranges from text for simplicity)
peer_data = {
    "Metric": ["AstraZeneca (AZN)", "Eli Lilly and Company (LLY)", "Roche Holding AG (RHHBY)", "Novartis AG (NVS)"],
    "P/E Ratio (TTM)": [22.5, 75.0, 20.0, 17.5],
    "YoY Revenue Growth (%)": [6.5, 22.5, 4.0, 3.0], 
    "Market Share (Global Pharma %)": [3.5, 2.5, 4.5, 3.5], 
    "Gross Margin (%)": [77.5, 72.5, 82.5, 77.5], 
    "R&D as % of Sales (%)": [19.0, 27.5, 16.5, 13.5] 
}
peer_df = pd.DataFrame(peer_data).set_index("Metric")
st.dataframe(peer_df, use_container_width=True)

st.markdown("### Visualizing Peer Metrics")
st.info("AstraZeneca (AZN) is highlighted in **orange** for easy comparison across the charts below.")

# Reshape DataFrame for Altair charting
chart_data = peer_df.reset_index().rename(columns={"Metric": "Company"})

# Create individual charts for each metric
metrics_to_chart = [
    {"col": "P/E Ratio (TTM)", "label": "P/E Ratio"},
    {"col": "YoY Revenue Growth (%)", "label": "YoY Revenue Growth (%)"},
    {"col": "Market Share (Global Pharma %)", "label": "Global Pharma Market Share (%)"},
    {"col": "Gross Margin (%)", "label": "Gross Margin (%)"},
    {"col": "R&D as % of Sales (%)", "label": "R&D as % of Sales (%)"}
]

for metric_info in metrics_to_chart:
    st.subheader(f"{metric_info['label']} Comparison")
    chart = create_metrics_bar_chart(chart_data, metric_info['col'], 
                                     f'{metric_info["label"]} Across Key Peers', metric_info['label'])
    st.altair_chart(chart, use_container_width=True)
    st.markdown("---")


# --- Adjacent Industry Analysis ---
st.header("🌍 Adjacent Industry Analysis")
st.markdown("Understanding how upstream and downstream industries influence AstraZeneca's performance.")

with st.expander("Upstream: Biotechnology & Contract Research/Manufacturing Organizations (CROs/CDMOs)"):
    st.subheader("Current Tailwinds (Positive Influences):")
    st.info("""
    *   **Biotech Innovation:** Improved funding environment and advances in gene editing, AI-driven drug discovery, and novel therapeutic modalities provide a rich pipeline for collaborations and acquisitions.
    *   **CRO/CDMO Demand:** Strong demand indicates a healthy overall drug development pipeline, which benefits companies like AZN that utilize these partners for clinical trials and manufacturing.
    """)
    st.subheader("Potential Headwinds (Negative Influences):")
    st.warning("""
    *   **Supply Chain Disruptions:** Potential for disruptions for specialized reagents or raw materials could impact development timelines.
    *   **Cost & Competition:** Increased competition for top-tier CRO/CDMO talent and capacity could lead to higher costs.
    """)

with st.expander("Downstream: Healthcare Providers (Hospitals, Clinics) & Payers (Insurance Companies)"):
    st.subheader("Current Tailwinds (Positive Influences):")
    st.info("""
    *   **Global Healthcare Expenditure:** Increasing global healthcare expenditure and an aging population continue to drive demand for pharmaceuticals.
    *   **Value-Based Care:** Payers increasingly focus on value-based care, favoring well-established drugs with strong clinical outcomes and cost-effectiveness (e.g., Farxiga).
    *   **Normalization of Healthcare Access:** Post-pandemic normalization means patients are more readily accessing healthcare, leading to higher utilization of prescription drugs.
    """)
    st.subheader("Potential Headwinds (Negative Influences):")
    st.warning("""
    *   **Drug Pricing Pressure:** Pressure from governments and private payers remains a constant challenge.
    *   **Reimbursement Policies:** Stricter reimbursement policies, formulary restrictions, and the rise of value-based contracting could impact pricing power and market access.
    *   **Healthcare System Constraints:** Physician burnout and hospital capacity constraints could indirectly affect prescription volumes.
    """)

st.markdown("---")

# --- Risk Assessment ---
st.header("⚠️ Risk Assessment")
st.markdown("A balanced view of potential near-term scenarios for AstraZeneca.")

col_bull, col_bear = st.columns(2)

with col_bull:
    st.subheader("🐂 Bull Case (Upcoming Quarter)")
    st.success("""
    *   **Strong Beat on Earnings & Positive Guidance:** AZN delivers EPS and revenue figures significantly above consensus, driven by exceptional performance of key growth drivers (Tagrisso, Imfinzi, Farxiga).
    *   **Positive Pipeline Updates & Regulatory Approvals:** Positive interim data from crucial Phase 3 trials, or a surprise early approval for a significant pipeline candidate, validating long-term growth strategy.
    *   **Favorable Regulatory Environment & Payer Relations:** Signs of a more stable pricing environment in key markets or favorable formulary decisions for new indications of existing drugs.
    """)

with col_bear:
    st.subheader("🐻 Bear Case (Upcoming Quarter)")
    st.error("""
    *   **Disappointing Clinical Trial Data:** A significant setback in a late-stage clinical trial for a key pipeline asset could lead to substantial negative revision of growth prospects.
    *   **Intensified Competition & Pricing Pressure:** Unexpectedly strong competitive launches or aggressive pricing actions by payers (e.g., US Medicare drug price negotiations) could erode market share and margins.
    *   **Supply Chain or Manufacturing Issues:** Unforeseen production problems or critical raw material shortages for a blockbuster drug, impacting sales and investor confidence.
    """)

st.markdown("---")

# --- Detailed Company Overview and Competitive Comparison ---
st.header("📋 Detailed Company Overview & Competitive Analysis")

with st.expander("Company Overview"):
    st.markdown("""
    **Ticker/company:** AZN — AstraZeneca PLC.
    **Primary industry:** Global biopharmaceuticals (prescription pharmaceuticals and biologics, with major franchises in oncology, cardiovascular/renal/metabolism (CVRM), respiratory, and rare diseases). AstraZeneca is a research-led, large-cap pharma with a portfolio that blends marketed growth drugs (notably oncology and SGLT2 agents) and a broad late-stage pipeline.
    """)

with st.expander("3–6 Month Outlook (Detailed)"):
    st.markdown("""
    **Expected topline and earnings trajectory:** Over the next 3–6 months, performance is likely to be driven primarily by (i) the trajectory of sales for its core growth medicines (oncology portfolio, SGLT2 agents such as Farxiga/dapagliflozin), (ii) quarterly reported results and updated management guidance, and (iii) FX translation effects. Absent an unexpected major regulatory setback, the company is positioned to deliver continued revenue growth at a mid-to-high single-digit to low double-digit percentage pace versus mature-pharma peers, supported by oncology and CVRM product momentum. Margin performance should remain relatively resilient because of high-margin biologic/oncology mix, but earnings per share will remain sensitive to R&D spend, business development activity, and currency moves.
    **Key macro influences:** Global macro conditions — growth in major markets, payer budget pressures, and inflation/interest-rate impacts — will matter. Moderate economic growth and continued pressure on healthcare budgets in some countries could intensify reimbursement scrutiny and slow volume/price growth in select markets. Conversely, secular demand for cancer and cardio-renal medicines is structurally inelastic, supporting resilience.
    **Industry dynamics:** The oncology market remains a high-growth, competitive arena with frequent label expansions and combination regimens. SGLT2s and other cardio-renal agents continue to see guideline adoption, which supports durable demand. However, increasing competition from other pharma players and biosimilars/generics for older molecules is a continuing constraint.
    """)
    st.subheader("Company-Specific Catalysts & Risks (Detailed):")
    col_cat_det, col_risks_det = st.columns(2)
    with col_cat_det:
        st.success("""
        **Catalysts:** Upcoming quarterly results and any announced label expansions or regulatory approvals for late-stage assets (e.g., additional indications for approved oncology or cardio-renal agents), positive Phase III readouts or accelerated approvals, and strategic partnerships or targeted M&A could all provide upside over the next few months.
        """)
    with col_risks_det:
        st.error("""
        **Risks:** Adverse clinical data or regulatory setbacks for key pipeline programs, intensified price/regulatory actions in major markets, manufacturing or supply disruptions, material legal/settlement outcomes, and unfavorable FX moves represent the principal near-term downside risks.
        """)

st.subheader("Competitive Comparison (Detailed Analysis vs. Select Peers)")

# Specific competitive comparison details from the text
competitors_detailed = {
    "Pfizer (PFE)": {
        "Strengths vs AZN": "Extremely large commercial scale, strong cash flow generation, and highly diversified portfolio including vaccines, established primary care/oncology assets, and broad manufacturing capacity. Faster capacity to absorb late-stage setbacks and pursue bolt-on M&A. Typically more exposed to vaccine/covid-era revenue fluctuations (depending on the cycle).",
        "Weaknesses vs AZN": "Pfizer’s growth profile has been more episodic (vaccine-driven waves) while AstraZeneca has more sustained organic growth in oncology and SGLT2s. Pfizer faces large near-term patent cliffs and more cyclical revenue sources.",
        "Relative Assessment": "Pfizer offers scale and balance-sheet optionality; AstraZeneca offers steadier growth driven by therapeutic-area momentum."
    },
    "Roche (RHHBY / ROG.SW)": {
        "Strengths vs AZN": "Leading diagnostics-therapeutics integration and a deep, profitable oncology franchise with strong margins and an established personalized medicine position. Roche’s diagnostics business provides valuable demand-signal lead indicators for therapeutic uptake.",
        "Weaknesses vs AZN": "Roche’s growth has in some periods been more modest than AZN’s higher-growth oncology + CVRM mix; Roche may be slightly less aggressive commercially in select geographies.",
        "Relative Assessment": "Roche is a diagnostic-enabled oncology leader with superior margin profile; AstraZeneca is faster-growing from new indications and a broader commercial push in cardio-renal."
    },
    "Novartis (NVS)": {
        "Strengths vs AZN": "Diversified exposure including innovative medicines and generics (Sandoz), and a strong presence in cell- and gene-therapy areas. Novartis has meaningful scale in established therapeutic areas and targeted innovation.",
        "Weaknesses vs AZN": "Novartis’ diversified business dilutes the high-margin growth mix that AstraZeneca currently benefits from in oncology and SGLT2s.",
        "Relative Assessment": "Novartis combines diversification and innovation; AstraZeneca offers a clearer growth story concentrated around a few high-growth franchises."
    }
}

for comp, details in competitors_detailed.items():
    with st.expander(f"vs. {comp}"):
        st.markdown(f"**Strengths vs AZN:** {details['Strengths vs AZN']}")
        st.markdown(f"**Weaknesses vs AZN:** {details['Weaknesses vs AZN']}")
        st.markdown(f"**Relative Assessment:** {details['Relative Assessment']}")

st.markdown("---")

# --- Market Sentiment & Expectations (Next 6-12 Months) ---
st.header("📈 Market Sentiment & Expectations (Next 6-12 Months)")
st.markdown("The prevailing market sentiment for AstraZeneca is **cautiously optimistic to bullish**, driven by its strong oncology and biopharmaceutical pipeline, though tempered by competitive pressures.")

col_bull_drivers, col_bear_concerns = st.columns(2)

with col_bull_drivers:
    st.subheader("Bullish Drivers:")
    st.success("""
    *   **Pipeline Strength & Launches:** Analysts consistently highlight an "industry-leading pipeline" with successful launches like Tagrisso, Enhertu, and Farxiga delivering sustained double-digit revenue growth.
    *   **Beyond COVID-19:** Growth story successfully decoupled from its COVID-19 vaccine/Vaxzevria and antibody therapy (Q1 2024 total revenue up 19% excluding COVID-19 medicines).
    *   **Upgraded Guidance:** In its Q1 2024 report, AZN raised its full-year 2024 core EPS guidance, signaling strong management confidence.
    """)

with col_bear_concerns:
    st.subheader("Bearish Concerns & Risks:")
    st.warning("""
    *   **China Pricing Pressure:** Recurring theme of exposure to ongoing price cuts in China's volume-based procurement schemes, acting as a headwind for some mature products.
    *   **Intense Competition:** Fierce competitive landscape in key areas like oncology (e.g., Tagrisso faces emerging competition) and diabetes. Requires continuous high R&D spending.
    *   **Acquisition Integration:** Recent strategic acquisitions (Fusion Pharmaceuticals, Amolyt Pharma) carry execution and integration risks.
    """)

st.markdown("### Recent Key Acquisitions")
acquisitions_df = pd.DataFrame({
    'Acquisition': ['Fusion Pharmaceuticals', 'Amolyt Pharma'],
    'Value (Billion USD)': [1.2, 2.0] # Values extracted from text
})

acquisition_chart = alt.Chart(acquisitions_df).mark_bar().encode(
    x=alt.X('Acquisition:N', sort=None, title='Acquisition Target'),
    y=alt.Y('Value (Billion USD):Q', title='Value (Billion USD)'),
    tooltip=['Acquisition', 'Value (Billion USD)']
).properties(
    title='Recent Key Acquisitions by AstraZeneca (Value)'
).interactive()
st.altair_chart(acquisition_chart, use_container_width=True)


st.markdown("---")

# --- Overall Conclusion ---
st.header("🎯 Summary Judgment & Conclusion")
st.markdown("""
AstraZeneca is positioned as a high-growth pharmaceutical leader with a de-risked post-COVID profile. Its success hinges on executing its robust oncology and biopharma pipeline, navigating pricing pressures, and leveraging innovations from adjacent biotech and tech sectors. The primary investment thesis revolves around its industry-leading R&D productivity translating into sustained revenue growth.
""")

st.info("""
**Disclaimer:** This assessment is evidence-based and forward-looking, not investment advice.
""")