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
import re # For extracting data from text

# --- Configuration ---
st.set_page_config(layout="wide", page_title="AZN Financial Analysis Dashboard", page_icon="📈")

# --- Raw Analysis Text (for easy reference and parsing) ---
# This variable stores the complete analysis text provided.
# It's kept here for context, but parsed content is used for display.
analysis_text = """
## AZN: A Deep Dive into AstraZeneca's Prospects and Industry Landscape

**AstraZeneca (AZN)**, a global biopharmaceutical giant, operates within the dynamic and highly competitive healthcare sector. This analysis will provide a forward-looking perspective on AZN's performance, its competitive positioning, and the external factors influencing its trajectory over the next 3-6 months.

---

### Fundamental Evaluation: Near-Term Outlook and Catalysts

AstraZeneca has demonstrated robust performance recently, driven by its strong oncology portfolio, the continued success of its COVID-19 vaccine and antibody treatments (though with diminishing contributions from the latter), and growth in its respiratory and cardiovascular segments. We anticipate this momentum to largely continue in the next 3-6 months, albeit with some nuances.

**Key Performance Indicators & Projections (Next 3-6 Months):**

*   **Revenue Growth:** We expect continued single-digit to low-double-digit percentage revenue growth. The oncology segment, particularly with new drug approvals and label expansions, will remain a primary driver. The cardiovascular, renal, and metabolism (CVRM) portfolio should also contribute steadily. The timing and ramp-up of new launches will be crucial to achieving the higher end of this range.
*   **Margins:** Gross margins are expected to remain strong, reflecting the premium pricing power of innovative pharmaceuticals. However, operating margins might see some pressure due to increased R&D spending on pipeline advancement and higher marketing and selling expenses associated with new product launches and expanded global reach. We anticipate operating margins to remain in the mid-to-high 20s.
*   **Profitability:** Earnings per share (EPS) are projected to grow, mirroring revenue trends but potentially moderated by increased investment. The company's strategic acquisitions and divestitures could also play a role in EPS trajectory.

**Key Catalysts (Next 3-6 Months):**

1.  **New Drug Approvals & Label Expansions:** This is a perennial catalyst for AZN. We will be closely watching for regulatory decisions on key pipeline assets, particularly in oncology (e.g., Enhertu's potential in new indications, Lynparza's continued expansion) and potentially in areas like immunology or rare diseases. Positive approvals and label expansions significantly de-risk pipeline assets and unlock new market opportunities.
2.  **Phase 3 Data Readouts and Regulatory Filings:** Positive results from late-stage clinical trials can significantly de-risk pipeline assets and signal future growth drivers. Conversely, disappointing data can create headwinds. We are monitoring several key Phase 3 programs that could have significant implications.
3.  **Surgical Robotics Integration & Performance (MedImmune):** While not a direct drug catalyst, the successful integration and commercialization of the recently acquired IVI Biologics assets (assuming this refers to the acquisition of IVI Biologics by AZN, which is correct) and continued progress with their biologics manufacturing capabilities will be important for long-term pipeline support and cost efficiency.

---

### Peer Benchmarking: AZN vs. Competitors

AstraZeneca operates in a highly competitive landscape. Here's a comparative snapshot against its key peers:

| Metric             | AstraZeneca (AZN) | Pfizer (PFE) | Novartis (NVS) | Roche (RHHBY) |
| :----------------- | :---------------- | :----------- | :------------- | :------------ |
| **P/E Ratio (TTM)** | ~19-21x           | ~12-14x      | ~15-17x        | ~18-20x       |
| **YoY Revenue Growth (LTM)** | ~5-8%             | ~0-2%        | ~2-4%          | ~3-5%         |
| **Market Share (Global Pharma)** | ~3-4%             | ~5-6%        | ~4-5%          | ~5-6%         |
| **R&D as % of Revenue** | ~20-23%           | ~12-15%      | ~14-17%        | ~16-19%       |
| **Oncology Revenue Contribution** | High              | Moderate     | Moderate       | High          |

*Note: Metrics are estimates and can fluctuate based on reporting periods and market conditions. P/E ratios are forward-looking multiples that consider expected earnings. YoY Revenue Growth is based on trailing twelve months (LTM) performance. Market Share is a broad estimate for the global pharmaceutical market.*

**Analysis:**

*   **Valuation:** AZN generally trades at a premium P/E relative to some peers like Pfizer, likely reflecting its stronger recent growth trajectory and a more robust pipeline. Novartis and Roche trade in a similar range.
*   **Growth:** AZN's revenue growth has been more consistent and robust than Pfizer and Novartis recently, driven by its strong product portfolio, particularly in oncology. Roche also exhibits steady growth, often fueled by its diagnostics division alongside pharmaceuticals.
*   **Market Share:** AZN holds a significant but not dominant market share, competing fiercely across multiple therapeutic areas.
*   **R&D Investment:** AZN maintains a high level of R&D investment, crucial for sustaining its innovation-driven business model and filling its pipeline for future growth.

---

### Adjacent Industry Analysis: Upstream & Downstream Impacts

Understanding the broader ecosystem is critical. For AZN, two key adjacent industries provide valuable insights:

1.  **Biotech & Pharmaceutical Services (Upstream):** This includes Contract Research Organizations (CROs), Contract Development and Manufacturing Organizations (CDMOs), and raw material suppliers (e.g., active pharmaceutical ingredients - APIs, excipients).
    *   **Current Sentiment:** **Tailwind.** The demand for outsourced R&D and manufacturing services remains strong as biopharma companies, including AZN, look to accelerate drug development and manage complex supply chains. We are seeing a healthy pipeline of early-stage drug candidates being advanced by smaller biotechs, which drives demand for CRO/CDMO services. Supply chain resilience remains a focus, but major disruptions are less prevalent than a year ago.
    *   **Impact on AZN:** This sector's health generally supports AZN's ability to efficiently conduct clinical trials and manufacture its products. Favorable pricing and capacity from CDMOs can positively impact cost of goods sold (COGS) and accelerate R&D timelines.

2.  **Healthcare Payers & Providers (Downstream):** This encompasses insurance companies, government health programs (e.g., Medicare, Medicaid), hospitals, and physician networks.
    *   **Current Sentiment:** **Mixed, leaning towards Headwind.** Payer consolidation and increasing pressure on drug pricing from governments and insurance providers remain significant concerns. However, the shift towards value-based care and outcomes-based reimbursement models could benefit innovative therapies with demonstrable efficacy and cost-effectiveness. Geopolitical factors and inflation can also impact healthcare spending.
    *   **Impact on AZN:** Pricing and reimbursement negotiations are crucial. The ability to demonstrate the economic value of AZN's new therapies will be paramount for market access and sustained revenue growth. Stricter formulary controls and reimbursement hurdles could slow down the adoption of new drugs, impacting near-term sales.

---

### Risk Assessment: Bull & Bear Cases for the Upcoming Quarter

**Bull Case:**

*   **Stronger-than-expected drug launch uptake:** Key new product launches exceed initial sales expectations due to superior clinical data, effective marketing, and favorable market access.
*   **Positive regulatory decisions:** Multiple significant drug approvals or label expansions for pipeline assets receive expedited or favorable regulatory clearance, de-risking future revenue streams.
*   **Robust clinical trial data:** Positive Phase 3 data readouts for promising pipeline candidates are announced, significantly boosting investor confidence in future growth.
*   **Favorable geopolitical/macroeconomic shifts:** A reduction in global inflation or more stable economic conditions could lead to increased healthcare spending and less pressure on drug pricing.

**Bear Case:**

*   **Clinical trial setbacks or regulatory rejections:** A key pipeline drug fails to meet efficacy endpoints in Phase 3 trials or faces a regulatory rejection, significantly impacting future growth prospects.
*   **Increased pricing pressure and payer pushback:** Major payers (governments or large insurance companies) implement stricter reimbursement policies or demand significant price concessions for AZN's key drugs.
*   **Competitive challenges intensify:** A competitor launches a highly effective new therapy that rapidly gains market share, eroding AZN's position in a key therapeutic area.
*   **Supply chain disruptions or manufacturing issues:** Unexpected production problems or raw material shortages lead to product shortages or increased manufacturing costs.

---

**Conclusion:**

AstraZeneca remains a well-positioned player in the biopharmaceutical industry, underpinned by a strong oncology franchise and a promising pipeline. The next 3-6 months will be characterized by the execution of new drug launches, progress in clinical development, and ongoing navigation of the complex payer landscape. While potential headwinds from pricing pressures and competitive dynamics exist, the company's innovation engine and strategic focus offer a compelling outlook. Investors should closely monitor regulatory announcements, clinical trial results, and the commercial performance of recently approved therapies.

---

Company overview
- Ticker/company: AZN — AstraZeneca plc. Primary industry: global pharmaceutical / biopharmaceutical company with major franchises in oncology, cardiovascular/metabolic/renal (CVRM), respiratory, and immunology; significant presence in oncology biologics, small-molecule drugs, and large-scale global commercialization.
- Core commercial drivers (mid‑2024 context): oncology (Imfinzi, Tagrisso exposure through EGFR franchise/related portfolio elements and partnered assets), SGLT2 class leader Farxiga (dapagliflozin) driving growth in diabetes, heart failure and chronic kidney disease indications, and a broad late‑stage pipeline supported by partnerships (e.g., collaborations with Daiichi Sankyo, MSD/Merck and others).

3–6 month outlook (near term)
- Expected financial/operating direction: Over the next 3–6 months AstraZeneca is likely to show continued top‑line growth driven primarily by the ongoing uptake of Farxiga in expanded cardiometabolic and renal indications and continued momentum in key oncology products and partnered medicines. Given the company’s scale and diversified portfolio, cash flow and margins should remain resilient absent any major one‑off charges.
- Key fundamentals and drivers:
  - Revenue trajectory: Mid‑single to high‑single digit organic revenue growth is a reasonable baseline expectation in the absence of large M&A or major regulatory shock, assuming continued uptake of SGLT2 and oncology volumes.
  - Margins/cash flows: Operating margins should remain healthy, supported by high-margin biologics and mature franchises; R&D spending will remain substantial but is skewed toward high‑value oncology and CVRM programs.
  - Balance sheet/FX: AstraZeneca’s balance sheet is strong relative to peers; nevertheless, reported results can show FX volatility (sterling/euro vs. USD) and interest‑rate driven discounting can affect investor sentiment toward long‑dated R&D prospects.
- Macroeconomic and policy influences:
  - Pricing and reimbursement headwinds remain a risk in major markets. Continued cost‑containment efforts (Europe) and U.S. policy developments (expanded Medicare negotiation timelines/coverage decisions) could influence outlook for specific high‑revenue drugs.
  - A mild global growth slowdown would likely have limited immediate impact on demand for AstraZeneca’s chronic and oncology therapies but could affect elective procedures and some uptake dynamics.
- Company‑specific catalysts and timing:
  - Upcoming regulatory decisions or late‑stage trial readouts (oncology and CVRM indications) are the main event risks/opportunities in the 3–6 month window. Positive readouts or label expansions (e.g., new Farxiga indications, positive oncology trial data) would be direct upside catalysts; disappointing data or regulatory setbacks would be material negatives.
  - Business development activity (partnerships, bolt‑on M&A) could also move sentiment if disclosed.
Overall near‑term view: cautiously constructive. AstraZeneca’s underlying commercial momentum and deep pipeline give it a reasonable probability of modest outperformance versus the broad market over the next few months, conditional on trial readouts and no major adverse regulatory surprises.

Competitive comparison (selected peers: Pfizer, Roche, Novartis)
- Pfizer (PFE)
  - Strengths: Enormous scale, strong vaccine and novel platform capability (mRNA), diversified commercial base, strong near‑term cash generation from vaccines and antiviral sales when relevant.
  - Weaknesses vs AZN: Pfizer has less exposure to the high‑growth SGLT2/heart‑failure space and weaker oncology franchise depth relative to AstraZeneca’s focused oncology pipeline; Pfizer’s pipeline has improved post‑2020 but AstraZeneca is more oncology‑centric.
  - Relative position: Pfizer is more platform/diversified and event‑driven (vaccines/antivirals), whereas AZN has steadier growth from durable specialty franchises.
- Roche (ROG / RHHBY)
  - Strengths: Best‑in‑class oncology portfolio and diagnostics integration, very high margins, deep biologics expertise and stable cash flows from oncology blockbusters.
  - Weaknesses vs AZN: Roche’s growth is heavily dependent on oncology and diagnostics; it is less exposed to the cardiometabolic SGLT2 opportunity that is a major growth engine for AstraZeneca.
  - Relative position: Roche is a premium margin, innovation‑heavy comparator in oncology and companion diagnostics; AstraZeneca competes strongly on late‑stage oncology assets but offers broader exposure to CVRM growth.
- Novartis (NVS)
  - Strengths: Broad therapeutic mix, strong in ophthalmology and gene/cell therapy investments, disciplined cost base.
  - Weaknesses vs AZN: Novartis is less centered on oncology immunotherapy biology and less exposed to SGLT2 expansion; its growth profile differs and can be more tied to lifecycle management and generics/biologics management.
  - Relative position: Novartis is a diversified pharma with complementary strengths; AstraZeneca’s near‑term growth profile is arguably stronger because of Farxiga and oncology momentum.
Summary of relative strengths/weaknesses for AZN
- Strengths: Faster near‑term commercial growth from SGLT2 and oncology; deep late‑stage pipeline and meaningful partnerships; robust cash generation; established global commercial footprint.
- Weaknesses: Exposure to regulatory/pricing risk in major markets; clinical trial binary risks in oncology; some legacy franchises maturing which require offsetting pipeline success.

Adjacent industries and transmission channels
- Diagnostics and precision medicine: Companion diagnostics and molecular testing directly influence uptake of targeted oncology treatments (testing → patient identification → prescription volumes). Growth in diagnostics expands addressable patient populations for AZ oncology drugs.
- Contract manufacturing and CDMOs: Supply continuity and launch timing depend on CDMO capacity for biologics and ADCs. Manufacturing constraints or quality issues at suppliers can delay launches or limit volumes.
- Payers/insurers and health policy: Payer coverage decisions, HTA outcomes and reimbursement negotiations (especially in the U.S. and EU) are direct transmission channels for revenue. Policies such as Medicare price negotiation or national cost‑effectiveness rules materially affect margins on high‑priced specialty drugs.
- Guideline committees and medical societies: Updates to clinical practice guidelines (cardiology, nephrology, oncology) materially affect uptake speeds for Farxiga and other drugs; favorable guideline changes can accelerate adoption.
- Biotechnology/technology ecosystem: Advances in ADCs, bispecifics, and gene‑editing technologies shape competition and partner opportunities; AZ’s collaborations position it to capture some of these gains but also require scientific execution.
- Macro supply chain (APIs, logistics): Geopolitical disruptions or commodity inflation can increase COGS and affect margins; AZ’s scale mitigates but does not eliminate these risks.

Key risks and opportunities
- Opportunities
  - Indication expansion for Farxiga (HF, CKD, earlier diabetes prevention) → durable revenue upside and higher share of wallet in CVRM.
  - Positive late‑stage oncology readouts or new approvals (including ADCs and immuno-oncology combinations) → meaningful upward re-rating potential.
  - Strategic partnerships or bolt-on M&A to shore up pipeline or fill capability gaps.
- Risks
  - Clinical trial failures or disappointing regulatory outcomes in key late-stage programs, particularly oncology (binary events with outsized impact).
  - Policy/regulatory pricing pressure (U.S. drug pricing reforms, EU cost containment, tender dynamics) that reduce realized prices or delay launches.
  - Competitive displacement from other oncology entrants, biosimilars, or class rivals (SGLT2 competitors expanding label sets).
  - FX volatility and macro slowdown that indirectly depress growth or complicate forecasting.
  - Manufacturing or supply disruptions for key biologics/ADC products.

Summary judgment
AstraZeneca enters the 3–6 month horizon with a favorable fundamental setup: diversified, high‑growth drivers in both cardiometabolic (Farxiga) and oncology, a deep late‑stage pipeline and solid balance sheet. Near‑term performance will be shaped by clinical/regulatory readouts, reimbursement developments, and the macro environment. Relative to peers, AZN combines stronger near‑term organic growth potential than some large diversified peers (because of SGLT2 and oncology momentum) but also faces the typical binary trial/regulatory risks of an innovation‑heavy company. For stakeholders, the most consequential near‑term monitorables are upcoming trial readouts and regulatory filings, payer coverage/HTA developments in key markets, and any material guidance updates from management. This is a balanced constructive view conditional on continued successful clinical execution and manageable policy headwinds.

---

# **Company Analysis: AstraZeneca PLC (AZN)**

## **1. Market Sentiment & Expectations (Next 3-6 Months)**

Overall sentiment for AstraZeneca is cautiously optimistic, with a strong emphasis on its robust pipeline offsetting near-term challenges.

*   **Bullish Perspectives:**
    *   **Pipeline Powerhouse:** The dominant theme is excitement around the company's deep and diverse late-stage pipeline. Analysts frequently cite upcoming Phase III data readouts and regulatory submissions as key catalysts. Morgan Stanley notes AZN has one of the "most attractive pipelines in pharma," with significant potential in oncology, rare diseases, and cardiometabolic areas.
    *   **Beyond COVID-19:** The company has successfully decoupled its growth story from its COVID-19 vaccine/Vyndaqel. Strong double-digit revenue growth (ex-COVID) in recent quarters is seen as sustainable, driven by core blockbusters like Tagrisso (cancer), Farxiga (diabetes/heart failure), and newer launches such as Ultomiris, Enhertu (with Daiichi Sankyo), and Calquence.
    *   **Upward Revisions:** Several analysts (e.g., from Barclays, Jefferies) have recently raised their price targets, citing better-than-expected Q1 2024 performance and confidence in management's guidance for high single-digit to low double-digit percentage revenue growth through 2026.

*   **Bearish/Cautious Perspectives:**
    *   **China Pricing Pressure:** A recurring concern is the ongoing impact of volume-based procurement (VBP) policies in China, which exert significant price pressure on mature drugs. While AZN's diversified portfolio mitigates this, it remains a headwind for certain segments of its business in a key market.
    *   **Pipeline Execution Risk:** The bullish thesis is heavily dependent on successful clinical trial outcomes and regulatory approvals. Any significant setbacks in key pipeline assets (e.g., datopotamab deruxtecan in lung cancer) could negatively impact the stock.
    *   **Competitive Intensity:** In core areas like oncology (PD-(L)1 inhibitors, ADC therapies) and diabetes, competition is fierce. The ability of drugs like Enhertu and Farxiga to maintain growth against existing and new rivals is closely watched.

**Summary:** The consensus expects steady, pipeline-driven growth. The stock is often viewed as a "defensive growth" pick in pharma, with near-term performance hinging on clinical catalysts rather than broad economic cycles.

## **2. Competitive Positioning (vs. Key Pharma Peers)**

AstraZeneca competes primarily with other global pharmaceutical giants like **Roche, Merck & Co. (MSD), Pfizer, Novartis, and Johnson & Johnson.**

*   **Strengths (Relative to Peers):**
    *   **Oncology Leadership:** A top-tier oncology franchise, particularly in targeted therapies (Tagrisso) and through its groundbreaking ADC collaboration on **Enhertu**, where it leads in breast and gastric cancers and is expanding into lung cancer.
    *   **High-Growth Core:** Exceptional growth from its "CVRM" (Cardiovascular, Renal & Metabolism) unit, led by **Farxiga** (an SGLT2 inhibitor), which has become a standard-of-care in heart failure and chronic kidney disease, giving it a durable advantage.
    *   **Strategic R&D Focus:** A disciplined R&D strategy focused on high-science areas (oncology, biopharmaceuticals, rare diseases) with clear biological pathways, which has improved R&D productivity.

*   **Weaknesses (Relative to Peers):**
    *   **Limited Diversification:** Compared to peers like **Johnson & Johnson** (with its massive MedTech and Consumer divisions) or **Novartis** (with a strong generics arm in Sandoz, now spun off), AZN is a more pure-play innovative pharma company. This can lead to higher volatility if pipeline events disappoint.
    *   **Late to Immuno-Oncology:** While it has caught up, AZN's own PD-L1 inhibitor, **Imfinzi**, entered the market later than Keytruda (Merck) and Opdivo (BMS), ceding first-mover advantage in some major indications.

*   **Opportunities:**
    *   **Rare Disease Expansion:** The acquisition of Alexion provided a leading rare disease platform. Integrating this and expanding the pipeline (e.g., Ultomiris) into new indications is a major growth vector.
    *   **Geographic Expansion:** Continued penetration in emerging markets, especially beyond China (e.g., Latin America, Middle East), leveraging its established commercial footprint.

*   **Threats:**
    *   **Patent Expiries:** Like all large pharma, it faces future patent cliffs. Key drugs like Tagrisso (2028-2032, varies by region) and Farxiga (mid-2030s) will eventually face generic/biosimilar competition, though the timeline provides a long runway.
    *   **Pricing & Access Scrutiny:** Intense global pressure on drug pricing and access, particularly in the US (IRA drug price negotiations) and Europe.

## **3. Adjacent Industry Impact**

Several adjacent industries significantly influence AstraZeneca's performance:

*   **Biotechnology & Drug Discovery:** AZN's success is deeply intertwined with the biotech sector.
    *   **Positive Impact:** Its aggressive business development strategy relies on partnerships and acquisitions (e.g., Daiichi Sankyo for ADCs, Fusion Pharma for radioconjugates) to in-validate cutting-edge science. A vibrant biotech innovation ecosystem is a direct feedstock for its pipeline.
    *   **Negative Impact:** High valuations in biotech can make acquisitions more expensive. Also, competition from agile, science-focused biotechs forces continuous innovation.

*   **Healthcare Technology & Data Science:**
    *   **Positive Impact:** Utilization of **AI and real-world data (RWD)** accelerates drug discovery (target identification), improves clinical trial design (patient recruitment), and supports value demonstrations to payers. AZN is actively investing in this space.
    *   **Impact:** Advances in **diagnostics**, particularly in oncology (companion diagnostics, liquid biopsies), are critical for the targeted therapies AZN develops. More precise diagnostics expand the addressable market for its drugs.

*   **Supply Chain & Manufacturing:**
    *   **Negative Impact:** Global supply chain complexities and geopolitical tensions can affect the cost and reliability of sourcing raw materials and manufacturing complex biologics and ADCs. The industry learned this acutely during the pandemic.

*   **Policy & Regulatory Environment:**
    *   **Negative Impact:** The most direct adjacent "industry" is government policy. The US **Inflation Reduction Act (IRA)** directly impacts AZN by subjecting key drugs like Farxiga to Medicare price negotiations, potentially affecting long-term revenue projections in its largest market. Changes in trade policies or IP protections in key markets also pose risks.

**Conclusion:** AstraZeneca is positioned as a growth-oriented pharmaceutical leader with a highly regarded pipeline that is expected to drive performance over the next 6-12 months. Its main challenges are external (policy, pricing) and execution-based (pipeline results), while its competitive strengths in oncology and CVRM provide a solid foundation. Its performance is increasingly dependent on successful navigation of the biotechnology and health-tech landscapes.
"""

# --- Data Extraction and Processing for Charts ---

# Function to extract numeric mid-points from text ranges (e.g., "19-21x" -> 20.0, "5-8%" -> 6.5)
def extract_midpoint_from_range(text):
    # Regex to find numbers or number ranges like '19-21', '5-8', '20-23'
    # Handles optional '~' prefix and 'x' or '%' suffix
    match = re.search(r'~?(\d+\.?\d*)(?:-(\d+\.?\d*))?', text)
    if match:
        lower = float(match.group(1))
        upper = float(match.group(2)) if match.group(2) else lower
        return (lower + upper) / 2 # Return midpoint for visualization
    return None # If no numerical range or single number found


# Peer Benchmarking Raw Data
peer_data = {
    "Metric": ["P/E Ratio (TTM)", "YoY Revenue Growth (LTM)", "Market Share (Global Pharma)", "R&D as % of Revenue", "Oncology Revenue Contribution"],
    "AstraZeneca (AZN)": ["~19-21x", "~5-8%", "~3-4%", "~20-23%", "High"],
    "Pfizer (PFE)": ["~12-14x", "~0-2%", "~5-6%", "~12-15%", "Moderate"],
    "Novartis (NVS)": ["~15-17x", "~2-4%", "~4-5%", "~14-17%", "Moderate"],
    "Roche (RHHBY)": ["~18-20x", "~3-5%", "~5-6%", "~16-19%", "High"]
}
df_peers_raw = pd.DataFrame(peer_data).set_index("Metric")

# Create a chartable DataFrame by converting text ranges to numerical midpoints
df_peers_chartable = df_peers_raw.copy()
for col in df_peers_chartable.columns:
    # Only apply to metrics that have numerical ranges
    df_peers_chartable[col] = df_peers_chartable[col].apply(
        lambda x: extract_midpoint_from_range(x) if isinstance(x, str) and ('x' in x or '%' in x) else x
    )

# Melt the DataFrame for Altair charting - only include numerical metrics
chart_metrics = ["P/E Ratio (TTM)", "YoY Revenue Growth (LTM)", "R&D as % of Revenue"]
df_peers_melted = df_peers_chartable.loc[chart_metrics].reset_index().melt(
    id_vars="Metric", var_name="Company", value_name="Value"
)

# --- Streamlit App Layout ---

st.title("📈 AstraZeneca (AZN) Financial Analysis Dashboard")
st.markdown("A deep dive into AZN's prospects, competitive positioning, and industry landscape over the next 3-6 months.")
st.markdown("---")

# --- Key Metrics and Company Overview ---
st.header("Company Overview & Key Financial Projections (Next 3-6 Months)")
overview_col1, overview_col2 = st.columns([1, 2])

with overview_col1:
    st.subheader("AstraZeneca PLC (AZN)")
    st.markdown("""
    **Primary Industry:** Global pharmaceutical / biopharmaceutical company.
    **Major Franchises:** Oncology, Cardiovascular/Metabolic/Renal (CVRM), Respiratory, Immunology.
    **Key Focus:** Oncology biologics, small-molecule drugs, and global commercialization.
    """)
    st.info("Overall near-term view: **Cautiously Constructive**")

with overview_col2:
    st.subheader("Near-Term Financial Outlook")
    st.markdown("""
    *   **Revenue Growth:** Expected continued **single-digit to low-double-digit percentage** growth, driven by oncology and CVRM.
    *   **Gross Margins:** Expected to remain strong due to premium pricing.
    *   **Operating Margins:** Anticipated in the **mid-to-high 20s**, with potential pressure from increased R&D and marketing investments.
    *   **Profitability (EPS):** Projected to grow, possibly moderated by increased strategic investments.
    *   **Balance Sheet:** Strong relative to peers; however, subject to FX volatility.
    """)

st.markdown("---")

# --- Key Catalysts ---
st.header("Key Catalysts (Next 3-6 Months)")
st.markdown("""
*   **New Drug Approvals & Label Expansions:** Watch for regulatory decisions on key pipeline assets in oncology (e.g., Enhertu, Lynparza) and other areas. Positive outcomes de-risk pipeline assets and open new market opportunities.
*   **Phase 3 Data Readouts and Regulatory Filings:** Favorable late-stage clinical trial results are crucial indicators of future growth drivers.
*   **Surgical Robotics Integration & Performance:** Successful integration and commercialization of recently acquired assets (e.g., IVI Biologics) for long-term pipeline support and operational efficiency.
""")
st.markdown("---")

# --- Peer Benchmarking ---
st.header("Peer Benchmarking: AZN vs. Competitors")
st.markdown("A comparative snapshot against key global pharmaceutical peers.")

st.subheader("Comparative Metrics Table")
st.dataframe(df_peers_raw, use_container_width=True)

st.subheader("Key Performance Indicators Comparison (Mid-point Estimates for Visualization)")

# Create charts for selected numerical metrics
chart_cols = st.columns(3)

for i, metric in enumerate(chart_metrics):
    with chart_cols[i]:
        st.markdown(f"**{metric}**")
        chart_data = df_peers_melted[df_peers_melted['Metric'] == metric]
        
        # Define chart properties based on metric
        y_axis_label = metric.replace(" (TTM)", "").replace(" (LTM)", "")
        tooltip_format = ".1f"
        suffix = "x" if "P/E Ratio" in metric else "%"

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Company:N', sort=alt.EncodingSortField(field="Value", op="average", order='descending'), title=None),
            y=alt.Y('Value:Q', title=f'{y_axis_label} {suffix}'),
            color=alt.condition(
                alt.datum.Company == 'AstraZeneca (AZN)',
                alt.value('#63B02A'),  # AZN color: a distinctive green
                alt.value('#4682B4')    # Other companies color: steelblue
            ),
            tooltip=[
                alt.Tooltip('Company:N'),
                alt.Tooltip('Value:Q', title=y_axis_label, format=tooltip_format, suffix=suffix)
            ]
        ).properties(
            title=None,
            height=300
        ).interactive() # Make charts interactive for zooming/panning
        st.altair_chart(chart, use_container_width=True)

st.markdown("""
**Analysis of Peer Benchmarking:**
*   **Valuation (P/E Ratio):** AstraZeneca generally trades at a premium P/E, likely reflecting its robust growth trajectory and promising pipeline compared to some peers like Pfizer.
*   **Growth (YoY Revenue):** AZN has shown more consistent and stronger revenue growth recently, largely driven by its oncology and CVRM portfolios.
*   **R&D Investment:** AZN maintains a high commitment to R&D, essential for its innovation-driven business model and future pipeline development.
""")
st.markdown("---")

# --- Adjacent Industry Analysis (Upstream & Downstream) ---
st.header("Adjacent Industry Analysis: Upstream & Downstream Impacts")

adj_col1, adj_col2 = st.columns(2)

with adj_col1:
    st.subheader("1. Biotech & Pharmaceutical Services (Upstream)")
    st.markdown("Includes Contract Research Organizations (CROs), Contract Development and Manufacturing Organizations (CDMOs), and raw material suppliers.")
    st.markdown("**Current Sentiment:** 🟢 **Tailwind**")
    st.markdown("""
    A strong demand for outsourced R&D and manufacturing services directly supports AZN's ability to efficiently conduct clinical trials and scale production. This environment can positively impact cost efficiencies and accelerate R&D timelines.
    """)

with adj_col2:
    st.subheader("2. Healthcare Payers & Providers (Downstream)")
    st.markdown("Encompasses insurance companies, government health programs (e.g., Medicare), hospitals, and physician networks.")
    st.markdown("**Current Sentiment:** 🟡 **Mixed, leaning towards Headwind**")
    st.markdown("""
    Payer consolidation and increasing pressure on drug pricing from governments and insurers remain significant concerns. For AZN, demonstrating the clear economic and clinical value of its innovative therapies is paramount for market access and sustained revenue growth amidst tighter reimbursement controls.
    """)
st.markdown("---")

# --- Risk Assessment ---
st.header("Risk Assessment: Bull & Bear Cases for the Upcoming Quarter")
risk_col1, risk_col2 = st.columns(2)

with risk_col1:
    st.subheader("🐂 Bull Case: Potential Upsides")
    st.success("""
    *   **Stronger-than-expected drug launch uptake:** Key new product launches significantly exceed initial sales forecasts due to superior clinical data, effective marketing, and favorable market access.
    *   **Positive regulatory decisions:** Multiple significant drug approvals or label expansions for pipeline assets receive expedited or favorable regulatory clearance, de-risking future revenue streams.
    *   **Robust clinical trial data:** Announcement of positive Phase 3 data readouts for promising pipeline candidates, boosting investor confidence in future growth.
    *   **Favorable macroeconomic shifts:** A reduction in global inflation or more stable economic conditions leading to increased healthcare spending and reduced pressure on drug pricing.
    """)

with risk_col2:
    st.subheader("🐻 Bear Case: Potential Downsides")
    st.error("""
    *   **Clinical trial setbacks or regulatory rejections:** A key pipeline drug fails to meet efficacy endpoints in Phase 3 trials or faces a regulatory rejection, significantly impacting future growth prospects.
    *   **Increased pricing pressure and payer pushback:** Major payers implement stricter reimbursement policies or demand significant price concessions for AZN's key drugs (e.g., U.S. IRA impact).
    *   **Competitive challenges intensify:** A competitor launches a highly effective new therapy that rapidly gains market share, eroding AZN's position in a key therapeutic area.
    *   **Supply chain disruptions or manufacturing issues:** Unexpected production problems or raw material shortages leading to product shortages or increased manufacturing costs.
    """)
st.markdown("---")

# --- Market Sentiment & Expectations ---
st.header("Market Sentiment & Expectations (Next 3-6 Months)")
st.markdown("The overall market sentiment for AstraZeneca is **cautiously optimistic**, heavily influenced by its robust pipeline and strategic execution.")

sentiment_col1, sentiment_col2 = st.columns(2)

with sentiment_col1:
    st.subheader("Bullish Perspectives 🟢")
    st.markdown("""
    *   **Pipeline Powerhouse:** Analysts frequently highlight AZN's deep and diverse late-stage pipeline, particularly in oncology, rare diseases, and cardiometabolic areas, as a key future growth driver.
    *   **Sustainable Growth:** The company has successfully diversified its growth beyond COVID-19 related products, demonstrating strong and sustainable double-digit revenue growth in its core franchises.
    *   **Analyst Upgrades:** Several analysts have recently raised price targets, reflecting confidence in management's guidance and better-than-expected financial performance.
    """)

with sentiment_col2:
    st.subheader("Bearish/Cautious Perspectives 🟠")
    st.markdown("""
    *   **China Pricing Pressure:** Ongoing impact from volume-based procurement (VBP) policies in China could be a headwind for certain mature drugs.
    *   **Pipeline Execution Risk:** The optimistic outlook is heavily reliant on successful clinical trial outcomes and timely regulatory approvals. Any setbacks could negatively impact the stock.
    *   **Intense Competition:** Fierce competition in key therapeutic areas like oncology and diabetes requires continuous innovation and strong commercial execution to maintain market share.
    """)
st.markdown("---")

# --- Competitive Positioning (SWOT-like) ---
st.header("Competitive Positioning: Strengths, Weaknesses, Opportunities, Threats")

comp_col1, comp_col2 = st.columns(2)

with comp_col1:
    with st.expander("💪 **Strengths (Relative to Peers)**", expanded=True):
        st.markdown("""
        *   **Oncology Leadership:** A top-tier oncology franchise, particularly in targeted therapies (e.g., Tagrisso) and its innovative ADC collaboration on Enhertu.
        *   **High-Growth CVRM Core:** Exceptional growth from its Cardiovascular, Renal & Metabolism (CVRM) unit, led by Farxiga, establishing it as a standard-of-care in multiple indications.
        *   **Strategic R&D Focus:** A disciplined R&D strategy concentrated on high-science areas with clear biological pathways, enhancing R&D productivity.
        """)
    with st.expander("🎯 **Opportunities**", expanded=True):
        st.markdown("""
        *   **Rare Disease Expansion:** Significant growth potential through integrating Alexion's rare disease platform and expanding pipeline assets like Ultomiris into new indications.
        *   **Geographic Expansion:** Continued penetration into emerging markets beyond China, leveraging its established global commercial footprint.
        """)

with comp_col2:
    with st.expander("📉 **Weaknesses (Relative to Peers)**", expanded=True):
        st.markdown("""
        *   **Limited Diversification:** Compared to highly diversified peers (e.g., J&J), AZN is more of a pure-play innovative pharma company, potentially leading to higher stock volatility if pipeline events disappoint.
        *   **Late to Immuno-Oncology:** While a strong player, AZN's PD-L1 inhibitor, Imfinzi, entered the market later than some key competitors, ceding initial first-mover advantage.
        """)
    with st.expander("⚠️ **Threats**", expanded=True):
        st.markdown("""
        *   **Patent Expiries:** Like all large pharmaceutical companies, AZN faces future patent cliffs for key revenue-generating drugs, which will eventually introduce generic/biosimilar competition.
        *   **Pricing & Access Scrutiny:** Intense global pressure on drug pricing and access, especially in major markets like the U.S. (e.g., Inflation Reduction Act) and Europe, could impact future revenue and margins.
        """)
st.markdown("---")

# --- Deeper Dive into Broader Adjacent Industry Impact ---
st.header("Deeper Dive: Broader Adjacent Industry Impacts")
st.markdown("Exploring how various external industries and factors intricately influence AstraZeneca's performance:")

st.expander_biotech_tech = st.expander("🔬 **Biotechnology, Health Tech & Data Science Ecosystem**", expanded=False)
with st.expander_biotech_tech:
    st.markdown("""
    *   **Positive Impact:** AZN's success is deeply intertwined with the biotech sector; strategic partnerships (e.g., Daiichi Sankyo for ADCs) and acquisitions feed its pipeline. Adoption of **AI and real-world data (RWD)** accelerates drug discovery, improves clinical trial design, and strengthens value propositions to payers. Advances in **diagnostics** (companion diagnostics, liquid biopsies) are critical for targeted therapies.
    *   **Negative Impact:** High valuations in the biotech space can make acquisitions more expensive. Rapid innovation from agile biotechs and tech companies necessitates continuous R&D investment and competitive pressure.
    """)

st.expander_supply_chain_macro = st.expander("🏭 **Global Supply Chain & Macroeconomic Factors**", expanded=False)
with st.expander_supply_chain_macro:
    st.markdown("""
    *   **Negative Impact:** Global supply chain complexities, geopolitical tensions, and commodity inflation can directly affect the cost and reliability of sourcing raw materials (APIs) and manufacturing complex biologics/ADCs, impacting COGS and margins. Macroeconomic slowdowns can indirectly affect elective procedures or overall healthcare spending.
    """)

st.expander_policy_regulatory = st.expander("🏛️ **Policy, Regulatory & Reimbursement Environment**", expanded=False)
with st.expander_policy_regulatory:
    st.markdown("""
    *   **Negative Impact:** Government policy, particularly the U.S. **Inflation Reduction Act (IRA)**, poses a direct threat by subjecting key drugs (like Farxiga) to Medicare price negotiations. Changes in trade policies, intellectual property (IP) protections, Health Technology Assessment (HTA) outcomes, and payer coverage decisions in key markets materially affect market access, pricing, and revenue potential for high-priced specialty drugs.
    *   **Positive Impact:** Favorable updates to clinical practice guidelines (e.g., cardiology, nephrology, oncology medical societies) can accelerate the adoption of AZN's therapies.
    """)

st.markdown("---")

# --- Overall Conclusion ---
st.header("Overall Summary Judgment")
st.markdown("""
AstraZeneca enters the 3–6 month horizon with a fundamentally favorable setup, characterized by diversified, high-growth drivers in both its cardiometabolic (Farxiga) and oncology franchises, a deep late-stage pipeline, and a solid balance sheet. Near-term performance will be primarily shaped by successful clinical/regulatory readouts, favorable reimbursement developments, and the broader macroeconomic environment.

Relative to its peers, AZN exhibits stronger near-term organic growth potential due to its SGLT2 and oncology momentum. However, like any innovation-heavy biopharma company, it faces inherent binary trial and regulatory risks. For stakeholders, close monitoring of upcoming trial data, regulatory filings, payer coverage decisions in key markets, and any material updates from management will be crucial to assessing its trajectory. The overall view remains **balanced and constructively optimistic**, contingent on continued successful clinical execution and manageable policy headwinds.
""")

st.markdown("---")
st.info("Disclaimer: This analysis is for informational purposes only and should not be considered financial advice. Please consult a qualified financial professional before making investment decisions.")