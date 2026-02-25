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

# Set Streamlit page configuration
st.set_page_config(
    layout="wide",
    page_title="AstraZeneca (AZN) Financial Ecosystem Analysis",
    page_icon="💊"
)

# --- Content for sections ---

def intro_content():
    st.write(f"""
    This app provides a comprehensive financial ecosystem analysis of AstraZeneca (AZN), a prominent global biopharmaceutical company.
    The analysis delves into AZN's internal financial drivers, market dependencies, sector connections, competitive landscape,
    and external economic factors, based on the provided qualitative financial overview.
    """)

def company_overview_content():
    st.subheader("Company Overview")
    st.markdown("""
    AstraZeneca (AZN) is a global, science-led biopharmaceutical company focused on the discovery, development, manufacturing,
    and commercialization of prescription medicines. Its primary therapeutic areas include **oncology, cardiovascular, renal & metabolism (CVRM),
    respiratory & immunology, and rare diseases** (largely via the Alexion acquisition).

    It is dual-listed (primary market exposure to Europe and the U.S.), reports in USD, and sells drugs globally through a mix of direct sales, partners, and collaborators.
    Headquartered in Cambridge, UK. Key products include Tagrisso (oncology), Farxiga (diabetes/heart failure), and COVID-19 vaccine Vaxzevria.
    """)

def financial_drivers_content():
    st.subheader("Financial Drivers & Relationships")
    st.markdown("""
    AZN's financial performance is shaped by a complex interplay of internal and external factors:
    - **Revenue Streams:** Primarily driven by sales of prescription drugs, with blockbuster drugs in oncology (e.g., Imfinzi, Tagrisso), CVRM (e.g., Farxiga), and respiratory (e.g., Symbicort) being key.
    - **Cost of Goods Sold (COGS):** Manufacturing costs, raw materials, and packaging directly impact profitability.
    - **Research & Development (R&D) Expenses:** A significant portion of expenditure dedicated to new drug discovery and development, crucial for future growth but a substantial ongoing cost.
    - **Sales, General, and Administrative (SG&A) Expenses:** Encompasses marketing, sales force, and corporate overhead.
    - **Gross Profit & Operating Profit Margins:** Indicators of pricing power and operational efficiency.
    - **Net Profit & Earnings Per Share (EPS):** The bottom line for investor returns.
    - **Debt Levels & Interest Expense:** Impact profitability and financial flexibility.
    - **Cash Flow from Operations (CFO) & Free Cash Flow (FCF):** Essential for funding R&D, dividends, and acquisitions, and cash available for debt repayment or share buybacks.
    - **Dividend Payout Ratio:** Important for income-seeking investors.
    - **Capital Allocation:** Decisions on R&D, acquisitions, dividends, or share buybacks significantly influence financial trajectory.
    """)

    st.markdown("---")
    st.markdown("#### Illustrative Financial Mix (Dummy Data)")
    st.info("The charts below use *dummy data* to illustrate the conceptual proportions mentioned in the analysis, not actual AstraZeneca financial figures.")

    col1, col2 = st.columns(2)

    with col1:
        st.write("##### Revenue Mix by Therapeutic Area")
        revenue_data = {
            'Therapeutic Area': ['Oncology', 'CVRM', 'Rare Diseases', 'Respiratory & Immunology', 'Other'],
            'Revenue Share (%)': [40, 25, 15, 10, 10]
        }
        df_revenue = pd.DataFrame(revenue_data)

        chart_revenue = alt.Chart(df_revenue).mark_arc(outerRadius=120).encode(
            theta=alt.Theta(field="Revenue Share (%)", type="quantitative"),
            color=alt.Color(field="Therapeutic Area", type="nominal", title="Area"),
            order=alt.Order("Revenue Share (%)", sort="descending"),
            tooltip=["Therapeutic Area", "Revenue Share (%)"]
        ).properties(
            title="Illustrative Revenue Mix"
        )
        st.altair_chart(chart_revenue, use_container_width=True)

    with col2:
        st.write("##### Illustrative Expense Allocation")
        expense_data = {
            'Expense Category': ['R&D', 'COGS', 'SG&A', 'Other Operating Expenses', 'Net Profit/Margin'],
            'Share (%)': [20, 30, 25, 10, 15] # Illustrative, not actual AZN
        }
        df_expense = pd.DataFrame(expense_data)

        chart_expense = alt.Chart(df_expense).mark_arc(outerRadius=120).encode(
            theta=alt.Theta(field="Share (%)", type="quantitative"),
            color=alt.Color(field="Expense Category", type="nominal", title="Category"),
            order=alt.Order("Share (%)", sort="descending"),
            tooltip=["Expense Category", "Share (%)"]
        ).properties(
            title="Illustrative Expense Allocation"
        )
        st.altair_chart(chart_expense, use_container_width=True)

def therapeutic_assets_content():
    st.subheader("Key Therapeutic Assets and their Strategic Roles")
    st.markdown("""
    AstraZeneca's portfolio is strategically diversified across high-growth and high-value therapeutic areas:
    - **Oncology portfolio:** Core growth engine (immune-oncology agents, targeted therapies like Tagrisso, Imfinzi, Enhertu). Often command premium pricing but face intense competition and high trial-readout dependency.
    - **CVRM/diabetes drugs:** Major growth area with expanding indications (heart failure, CKD) that drive durable sales across large patient populations (e.g., Farxiga).
    - **Rare diseases (Alexion products):** High Average Selling Prices (ASPs), lower patient counts, but revenue stability while patents/exclusivity hold.
    - **Respiratory & Immunology:** Symbicort and newer biologics.

    Many of AstraZeneca’s major drugs are co-developed or marketed under collaboration agreements, shaping revenue recognition, margins, and future upside.
    """)

def relationships_content():
    st.subheader("Market, Partner, and Sector Connections")

    st.markdown("#### Market Dependencies")
    st.markdown("""
    - **Global Healthcare Demand:** Tied to population growth, aging demographics, and rising disposable incomes.
    - **Reimbursement Policies & Payer Landscape:** Government and private health insurance policies, drug pricing regulations. Favorable policies are essential for market access.
    - **Patent Expirations & Generic/Biosimilar Competition:** Can significantly erode revenue and profitability.
    - **New Drug Launches & Product Pipeline Success:** Primary driver of growth; clinical trial failures impact future revenue.
    - **Global Economic Conditions:** Pharmaceuticals are relatively recession-resistant, but downturns can impact healthcare spending.
    - **Foreign Exchange Rates:** Fluctuations significantly affect reported financial results due to global operations.
    """)

    st.markdown("#### Partner, Collaborator, and Supply Relationships")
    st.markdown("""
    - **Co-development partners:** Alliances with companies like Daiichi Sankyo and Merck/MSD share clinical costs, development risk, and future revenue/royalty exposure.
    - **Contract Manufacturers (CMOs):** Outsourcing portions of manufacturing depends on CMO relationships, quality inspections, and capacity.
    - **Contract Research Organizations (CROs):** Clinical trials rely on CROs for execution; delays impact timelines and cash burn.
    - **Payers and PBMs:** Influence formulary placement and net pricing in markets like the U.S. and Europe.
    """)

    st.markdown("#### Sector Connections")
    st.markdown("""
    - **Pharmaceutical & Biotechnology Industry:** Performance is intrinsically linked to broader industry trends.
    - **Healthcare Services & Providers:** Demand for drugs is driven by needs of hospitals, clinics, and providers.
    - **Medical Device Manufacturers:** Potential synergies or indirect competition.
    - **Life Sciences & Research Institutions:** Collaboration and licensing agreements are crucial for early-stage discovery.
    """)

    st.markdown("---")
    st.markdown("#### Illustrative R&D Pipeline Progression (Dummy Data)")
    st.info("This chart uses *dummy data* to conceptually visualize the stages of drug development and the decreasing number of candidates as they progress through trials.")

    pipeline_data = {
        'Stage': ['Discovery/Pre-Clinical', 'Phase I', 'Phase II', 'Phase III', 'Regulatory Review', 'Marketed'],
        'Number of Programs (Illustrative)': [100, 40, 20, 10, 5, 3] # Fictional numbers
    }
    df_pipeline = pd.DataFrame(pipeline_data)

    chart_pipeline = alt.Chart(df_pipeline).mark_bar().encode(
        x=alt.X('Number of Programs (Illustrative)', title='Number of Programs'),
        y=alt.Y('Stage', sort='-x', title='Development Stage'),
        tooltip=['Stage', 'Number of Programs (Illustrative)']
    ).properties(
        title='Conceptual Drug Pipeline Progression'
    )
    st.altair_chart(chart_pipeline, use_container_width=True)


def competitor_landscape_content():
    st.subheader("Competitor Landscape and Interactions")
    st.markdown("""
    AZN operates in a highly competitive landscape. Key competitors include:
    - **Major Pharmaceutical Companies:** Pfizer, Roche, Novartis, Merck & Co., Bristol Myers Squibb, Eli Lilly, Sanofi, Johnson & Johnson, Takeda Pharmaceutical.
    - **Biotechnology Companies:** Smaller, specialized biotech firms with innovative pipelines in specific therapeutic areas.
    """)
    st.markdown("#### Competitive Dynamics:")
    st.markdown("""
    - **Therapeutic Area Overlap:** Competitors often target the same disease areas, leading to direct competition for market share.
    - **R&D Race:** Constant vying to be first to market with innovative treatments.
    - **Pricing & Market Access:** Competition influences pricing strategies and ability to secure favorable market access.
    - **Mergers & Acquisitions (M&A):** Industry is characterized by significant M&A activity to acquire assets or consolidate positions.
    - **Biosimilar Competition:** Emergence of biosimilars intensifies competition as patents expire.
    """)
    st.markdown("#### Direct Competitors by Area (Examples):")
    st.markdown("""
    - **Oncology:** Merck (Keytruda), Bristol-Myers Squibb (Opdivo/Yervoy), Roche/Genentech (multiple oncology franchises).
    - **CVRM/Diabetes:** Eli Lilly, Novo Nordisk (GLP-1 and other metabolic drugs), Boehringer Ingelheim / Lilly (SGLT2 competitor Jardiance/empagliflozin).
    - **Rare diseases:** Sanofi, Roche and specialty biotechs.
    """)


def external_factors_content():
    st.subheader("Regulatory, Economic & Macro Factors")

    st.markdown("#### Regulatory, Reimbursement and Legal Dependencies")
    st.markdown("""
    - **Regulatory Approvals:** FDA/EMA/PMDA approvals, label expansions, and safety findings are binary catalysts.
    - **Reimbursement Negotiations & Pricing Controls:** Determine net realized prices in major markets (U.S., EU, China, Japan, UK). Policy changes (e.g., U.S. Medicare negotiation) are material risk factors.
    - **Patent Litigation & Exclusivity:** Outcomes of patent challenges affect future revenue streams.
    - **Safety Events:** Black-box warnings or manufacturing compliance failures can trigger recalls and lost revenue.
    """)

    st.markdown("#### Macroeconomic and Market Dependencies")
    st.markdown("""
    - **Currency Exposure:** As a global company reporting in USD with material European and emerging-market revenue, FX movements (USD, GBP, EUR, CNY) change reported revenue and margins.
    - **Interest Rates & Discount Rates:** Higher rates increase borrowing costs and discount applied to pipeline NPV, potentially reducing equity valuations.
    - **Inflation & Input Costs:** Higher manufacturing, labor, and logistics costs compress margins unless offset by pricing power or higher sales volumes.
    - **Geopolitical Stability:** Political instability can disrupt supply chains, impact regulatory processes, and affect market access.
    - **Government Healthcare Policies & Regulations:** Changes in drug pricing regulations and intellectual property laws profoundly impact profitability.
    - **Global GDP Growth:** Correlates with increased healthcare spending.
    - **Trade Policies & Tariffs:** Affect the cost of importing raw materials or exporting finished goods.
    """)

def swot_content():
    st.subheader("SWOT Summary")

    # Create a DataFrame for SWOT for better presentation
    swot_data = {
        'Category': ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'],
        'Points': [
            ["Leading oncology portfolio", "Robust pipeline", "Strong emerging market presence", "Strong R&D engine"],
            ["Dependence on a few blockbuster drugs", "High R&D failure risk", "Pricing pressures", "High fixed R&D and SG&A"],
            ["Expansion in rare diseases", "Digital health integration", "mRNA platform development", "Growing global healthcare demand"],
            ["Drug pricing reforms (e.g., U.S. Medicare negotiation)", "Generic/biosimilar competition", "Clinical trial setbacks", "Patent expirations", "FX volatility"]
        ]
    }
    df_swot = pd.DataFrame(swot_data)

    st.table(df_swot.set_index('Category'))

    st.markdown("---")
    st.info("The SWOT analysis provides a qualitative overview of internal and external factors impacting AstraZeneca.")


def metrics_risks_content():
    st.subheader("Key Financial KPIs & Risks")

    st.markdown("#### Financial KPIs and Metrics to Monitor")
    st.markdown("""
    - **% revenue by product** and top-5 product concentration (exposure risk).
    - **Growth rates** of core franchises (oncology, CVRM, rare disease).
    - **R&D expense** and R&D/sales ratio (productivity and burn).
    - **Gross margin** and margin by geography/product (impact of royalties & partnerships).
    - **Free cash flow** and operating cash conversion (ability to fund dividends, buybacks, or M&A).
    - **Net debt/EBITDA** and interest coverage (balance sheet flexibility for acquisitions).
    - **Pipeline milestones calendar:** Expected Phase III readouts, regulatory decision dates, and patent expiry cliffs.
    - **Litigation and contingent liabilities** disclosures.
    """)

    st.markdown("#### Key Risks")
    st.markdown("""
    - **Clinical trial failures or safety issues** (binary downside events).
    - **Pricing and reimbursement reforms** reducing realized prices for major drugs.
    - **Patent expirations** and biosimilar/generic entry eroding revenue.
    - **Partner disputes or failed collaborations** that reduce expected upside.
    - **Manufacturing or supply-chain disruptions** that limit product availability.
    - **FX volatility** and macroeconomic shocks reducing purchasing power and reimbursement generosity in key markets.
    """)

def investment_considerations_content():
    st.subheader("Investment Considerations & Catalysts")

    st.markdown("#### Investment Considerations")
    st.markdown("""
    - **Growth Catalysts:** Pipeline milestones (e.g., datopotamab deruxtecan in lung cancer), geographic expansion in Asia.
    - **Risks:** Pipeline delays, adverse regulatory decisions, loss of exclusivity for key drugs post-2030.
    - **Valuation:** Trades at a premium to some peers due to growth profile and pipeline potential. Metrics to watch: P/E relative to sector, EV/EBITDA, and free cash flow yield.
    """)

    st.markdown("#### Key Catalysts to Watch (Near-Term)")
    st.markdown("""
    - Upcoming **quarterly earnings** and management guidance.
    - **Pipeline milestone calendar** (FDA/EMA submission/decision dates, Phase III readouts).
    - Major **competitor trial readouts** (head-to-head or competing mechanisms).
    - **Regulatory and HTA decisions** in the U.S., UK (NICE), EU and China.
    - **Currency moves** and macro data affecting revenue recognition and margins.
    - **M&A announcements** (bolt-on acquisitions to fill pipeline gaps) and strategic partnerships.
    - **Policy developments** (U.S. drug pricing legislation, EU price referencing decisions).
    """)

def conclusion_content():
    st.subheader("Conclusion: Net of Everything")
    st.markdown("""
    AstraZeneca’s stock is driven by a combination of:
    1.  The performance of a **concentrated set of high-value drugs** (oncology and CVRM are primary).
    2.  The success of a **high-investment R&D engine** and its pipeline readouts.
    3.  The outcomes of **partnership agreements** and royalty structures.
    4.  **Regulatory and reimbursement developments** in large markets.
    5.  **Macro factors** (FX, interest rates, supply chain).

    **Upside** comes from successful trial outcomes, label expansions, and favorable reimbursement.
    **Downside** can be abrupt from trial failures, patent loss, or policy-driven price reductions.

    Effective analysis requires product-level forecasting, careful tracking of partner economics, and monitoring of regulatory/policy calendars.
    AZN is a well-diversified biopharma leader with a strong oncology focus and a promising pipeline. Its financial health is robust, but it faces
    sector-wide challenges like pricing pressures and R&D risks.
    """)

# --- Main App Structure ---
st.title("💊 AstraZeneca (AZN) Financial Ecosystem Analysis")
st.markdown("---")

# Sidebar for navigation
st.sidebar.header("Navigation")
sections = {
    "Introduction": intro_content,
    "Company Overview": company_overview_content,
    "Financial Drivers & Relationships": financial_drivers_content,
    "Key Therapeutic Assets": therapeutic_assets_content,
    "Market, Partner & Sector Connections": relationships_content,
    "Competitor Landscape": competitor_landscape_content,
    "Regulatory, Economic & Macro Factors": external_factors_content,
    "SWOT Summary": swot_content,
    "Key Financial KPIs & Risks": metrics_risks_content,
    "Investment Considerations & Catalysts": investment_considerations_content,
    "Conclusion": conclusion_content,
}

# Display sidebar navigation links
for section_title, _ in sections.items():
    # Use st.markdown with an anchor tag to create clickable links for scrolling
    st.sidebar.markdown(f"[{section_title}](#{section_title.lower().replace(' ', '-')})")

st.write("Scroll down or use the sidebar for detailed sections.")
st.markdown("---")

# Main content display
st.container()
with st.container():
    st.markdown("<a name='introduction'></a>", unsafe_allow_html=True)
    intro_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='company-overview'></a>", unsafe_allow_html=True)
    company_overview_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='financial-drivers-&-relationships'></a>", unsafe_allow_html=True)
    financial_drivers_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='key-therapeutic-assets'></a>", unsafe_allow_html=True)
    therapeutic_assets_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='market,-partner-&-sector-connections'></a>", unsafe_allow_html=True)
    relationships_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='competitor-landscape'></a>", unsafe_allow_html=True)
    competitor_landscape_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='regulatory,-economic-&-macro-factors'></a>", unsafe_allow_html=True)
    external_factors_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='swot-summary'></a>", unsafe_allow_html=True)
    swot_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='key-financial-kpis-&-risks'></a>", unsafe_allow_html=True)
    metrics_risks_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='investment-considerations-&-catalysts'></a>", unsafe_allow_html=True)
    investment_considerations_content()
    st.markdown("---")

st.container()
with st.container():
    st.markdown("<a name='conclusion'></a>", unsafe_allow_html=True)
    conclusion_content()
    st.markdown("---")


# Footer
st.markdown("---")
st.markdown("##### *Disclaimer: This analysis is based on provided text and uses illustrative dummy data for charts. It is not financial advice.*")