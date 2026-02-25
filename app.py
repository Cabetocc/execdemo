Here's the complete Streamlit application (`app.py`) for analyzing Moderna's financial outlook, focusing on key metrics, summaries, and meaningful visualizations derived from the provided text.

```python
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
import plotly.graph_objects as go
import re

# Set page config for a clean and wide layout
st.set_page_config(
    page_title="MRNA Financial Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# This is a financial analysis app for Moderna (MRNA)."
    }
)

# --- Raw Analysis Text ---
# (Pasting the provided analysis text here)
analysis_text = """
## MRNA: Navigating a Post-Pandemic Landscape - A Research Update

**Company:** Moderna, Inc. (MRNA)
**Date:** October 26, 2023
**Analyst:** [Your Name/Team Name]

**Executive Summary:**

Moderna, Inc. (MRNA) is at a critical inflection point as it transitions from a pandemic-centric revenue driver to a diversified mRNA platform company. While the substantial COVID-19 vaccine revenue has diminished, the company's pipeline of vaccines and therapeutics for other diseases presents significant long-term potential. Our near-term outlook for MRNA is cautious but optimistic, driven by the upcoming flu season, potential regulatory approvals for its RSV vaccine, and continued progress in its oncology and rare disease programs. However, the competitive landscape is intensifying, and the dependence on timely regulatory approvals and successful commercialization remains a key risk.

---

### Fundamental Evaluation:

**Recent Performance & Near-Term Outlook (Next 3-6 Months):**

Moderna's recent performance has been heavily influenced by the decline in COVID-19 vaccine sales as pandemic urgency subsided and vaccination rates normalized. While this has led to a significant drop in revenue and profitability compared to the peak pandemic years, it was an anticipated outcome. The company has been strategically investing in its pipeline and manufacturing capabilities to build a sustainable business beyond COVID-19.

For the next 3-6 months (late 2023 through early 2024), we anticipate the following:

*   **Revenue Stabilization with Seasonal Boost:** We expect revenue to stabilize and potentially see a modest increase driven by the annual influenza vaccine market. While MRNA's flu vaccine (mRNA-1010) is still in development and facing strong competition, any positive clinical data or early market traction could be a catalyst. The primary revenue driver will likely remain its COVID-19 vaccine Spikevax, with sales expected to be significantly lower than peak but still contributing.
*   **Gross Margin Pressure:** Gross margins may continue to face some pressure due to the lower sales volumes and the need to manage inventory for a more diversified product portfolio. However, as manufacturing scales and becomes more efficient, there's potential for margin improvement over the longer term.
*   **Continued R&D Investment:** MRNA will continue to invest heavily in its R&D pipeline, particularly in oncology, rare diseases, and other infectious diseases. This will weigh on near-term profitability but is crucial for long-term growth.
*   **Focus on RSV Vaccine Commercialization:** A key area to watch is the commercialization strategy and initial uptake of its respiratory syncytial virus (RSV) vaccine (mRESVIA). Successful market penetration here would be a significant de-risking event and a strong validation of its platform.

**Key Catalysts for the Next 3-6 Months:**

1.  **RSV Vaccine (mRESVIA) Regulatory Approval and Early Commercial Performance:** The potential for FDA approval of mRESVIA for the prevention of RSV-associated lower respiratory tract disease in older adults is a major near-term catalyst. Early sales figures and physician adoption post-launch will be closely scrutinized and could significantly impact sentiment and revenue projections.
2.  **Positive Data Readouts from Key Pipeline Programs:** Updates on clinical trials for its mRNA-1010 (influenza vaccine), mRNA-4157/V940 (personalized mRNA cancer vaccine in combination with KEYTRUDA), and other programs in infectious diseases and rare genetic disorders can drive significant stock movement. Positive Phase 2 or Phase 3 data would validate the company's diversification strategy.
3.  **Strategic Partnerships and Collaborations:** Announcements of new or expanded partnerships with pharmaceutical giants for co-development or co-commercialization of pipeline assets can signal strong external validation and provide valuable non-dilutive capital, de-risking the development process.

---

### Peer Benchmarking:

| Metric                | Moderna, Inc. (MRNA) | Pfizer Inc. (PFE) | BioNTech SE (BNTX) | Novavax, Inc. (NVAX) |
| :-------------------- | :------------------- | :---------------- | :----------------- | :------------------- |
| **P/E Ratio (TTM)**   | ~7.5 (Highly Volatile due to COVID-19 earnings) | ~12.8             | N/A (Negative)     | N/A (Negative)       |
| **YoY Revenue Growth**| Declining (driven by COVID-19 normalization) | Declining (driven by COVID-19 normalization) | Declining (driven by COVID-19 normalization) | Declining (driven by COVID-19 normalization) |
| **Market Share (COVID-19 Vaccine)** | Significant, but declining from peak | Dominant (with BioNTech), but declining from peak | Significant (with Pfizer), but declining from peak | Negligible (compared to mRNA competitors) |
| **Pipeline Stage (Key Focus)** | Diverse (RSV, Flu, Oncology, Rare Diseases) | Diverse (Oncology, Vaccines, Inflammation) | Oncology, Infectious Diseases | Protein-based Vaccines (COVID-19, Flu) |
| **Recent Stock Performance (YTD)** | [Insert YTD Performance] | [Insert YTD Performance] | [Insert YTD Performance] | [Insert YTD Performance] |

*Note: P/E ratios for companies heavily influenced by COVID-19 vaccine sales can be highly volatile and may not be representative of future earnings power. YoY revenue growth for all players in this space is currently negative due to normalization post-pandemic. Market share data is estimated and can fluctuate.*

**Analysis:**

*   **Valuation:** MRNA's P/E ratio is currently low, reflecting the significant drop in earnings from its COVID-19 peak. This could make it appear attractive on a historical basis, but it's crucial to look beyond the COVID-19 windfall. PFE, being a much larger and more diversified pharmaceutical company, trades at a more traditional pharmaceutical multiple. BNTX and NVAX, while also in the vaccine space, have faced significant challenges and have negative earnings, making P/E comparisons difficult.
*   **Revenue Growth:** All major vaccine players are experiencing revenue declines from their COVID-19 highs. The key differentiator will be their ability to pivot and establish new growth drivers. MRNA's success hinges on its pipeline, especially the RSV vaccine.
*   **Market Share:** While MRNA has a strong presence in the COVID-19 vaccine market, the overall market size is shrinking. Its ability to gain significant market share in new therapeutic areas like RSV and oncology will be critical. Pfizer/BioNTech remain dominant in COVID-19 and are formidable competitors across various fronts. Novavax has struggled to gain meaningful traction.

---

### Adjacent Industry Analysis:

**Upstream: Raw Material & Manufacturing Equipment Suppliers:**

*   **Industry:** Specialty chemicals, lipid synthesis, contract manufacturing organizations (CMOs) specializing in nucleic acid production.
*   **Current Status:** The supply chain for raw materials used in mRNA vaccine production (e.g., specialized lipids, nucleotides) has generally normalized after initial pandemic-related stresses. Manufacturers have scaled up capacity. However, lead times for specialized equipment, like bioreactors and purification systems, can still be a factor, particularly for new builds or expansions.
*   **Tailwinds/Headwinds:**
    *   **Tailwind:** Improved availability and competitive pricing for key raw materials due to scaled production. MRNA's established manufacturing processes also provide some stability.
    *   **Headwind:** Potential for increased input costs due to global inflation and energy prices, which could slightly impact gross margins if not fully passed on. For smaller players like Novavax, securing manufacturing capacity and raw materials at competitive rates can be a more significant hurdle.

**Downstream: Healthcare Providers (Hospitals, Clinics) & Pharmacies:**

*   **Industry:** Healthcare delivery systems, retail pharmacies, government health programs, private insurers.
*   **Current Status:** Healthcare providers and payers are increasingly focused on cost-effectiveness and demonstrating the value of new therapies. The shift from pandemic emergency to routine healthcare requires robust clinical data, clear reimbursement pathways, and effective market access strategies. The flu season and the introduction of new vaccines for vulnerable populations (like the elderly for RSV) are key demand drivers.
*   **Tailwinds/Headwinds:**
    *   **Tailwind:** The aging global population creates a growing demand for vaccines and treatments for age-related diseases like RSV. Healthcare systems are also becoming more amenable to integrating mRNA technology into their established vaccination schedules if clinical and economic benefits are proven.
    *   **Headwind:** **Reimbursement and Market Access:** Gaining favorable reimbursement from governments and private insurers is crucial for commercial success, especially for newer vaccines and therapies in competitive markets. This process can be lengthy and challenging. **Physician and Patient Adoption:** Educating physicians and gaining patient trust in new mRNA-based treatments beyond COVID-19 will take time and significant marketing effort. The flu vaccine market, in particular, is highly competitive with established players.

---

### Risk Assessment:

**Bear Case (Upcoming Quarter):**

*   **Disappointing RSV Vaccine Launch:** Lower-than-expected uptake for mRESVIA due to physician hesitancy, payer restrictions, or competitive pressure from existing protein-based RSV vaccines (if approved imminently) could significantly temper near-term revenue expectations and investor sentiment.
*   **Negative or Ambiguous Clinical Trial Data:** Adverse events or lack of efficacy in ongoing Phase 3 trials for other key pipeline candidates (e.g., flu vaccine, oncology) could lead to significant pipeline delays and a valuation reset.
*   **Intensified Competition and Pricing Pressure:** Competitors might launch superior or more competitively priced vaccines or therapies, eroding MRNA's potential market share in key areas.
*   **Supply Chain Disruptions or Manufacturing Issues:** Unforeseen problems in manufacturing scale-up or securing critical raw materials could delay product launches and impact revenue targets.

**Bull Case (Upcoming Quarter):**

*   **Strong RSV Vaccine Approval and Robust Initial Sales:** A timely and broad approval for mRESVIA, coupled with strong initial physician and patient uptake, would validate MRNA's platform and provide a significant revenue stream beyond COVID-19.
*   **Positive Clinical Data Readouts:** Compelling Phase 3 data for the influenza vaccine (mRNA-1010) or significant progress in the personalized cancer vaccine (mRNA-4157/V940) program, especially if it shows synergy with other therapies, could unlock substantial future value.
*   **Successful Strategic Partnership:** Securing a high-profile partnership for a key pipeline asset with a major pharmaceutical company would provide capital, de-risk development, and offer strong external validation.
*   **Government Procurement and Public Health Initiatives:** Increased government orders for COVID-19 boosters or proactive initiatives to support the adoption of new vaccines (like RSV) could provide unexpected revenue boosts.

---

**Conclusion:**

Moderna is navigating a complex transition period. The company's innovative mRNA platform holds immense promise for transforming the treatment landscape across various diseases. While the pandemic-driven revenue surge has passed, the success of its next-generation vaccines and therapeutics, particularly the RSV vaccine, will be crucial for its future. Investors should closely monitor regulatory approvals, clinical trial results, and commercial execution in the coming quarters. We remain cautiously optimistic about MRNA's long-term prospects, but near-term volatility is expected as the company proves its diversified pipeline.

---

Company overview
- Company: Moderna, Inc. (ticker: MRNA).
- Primary industry: Biotechnology / commercial vaccines and mRNA-based therapeutics (platform developer and manufacturer of mRNA vaccines and therapeutics; leading commercial product historically the COVID‑19 mRNA vaccine).
- Business model highlights: platform-driven R&D across infectious disease vaccines, seasonal/respiratory vaccines, oncology and rare disease programs; manufacturing scale-up and CDMO-like capabilities; revenue mix shifting from pandemic-driven COVID sales toward a more diversified product and partnership pipeline.

3–6 month outlook (Mar–Aug 2026)
Base-case tone: cautious, mixed
- Revenue trajectory: Near-term topline performance will remain sensitive to seasonal and government-driven vaccine demand (COVID-19 boosters, influenza and any new respiratory vaccine programs). If no major new product launches or large public procurement contracts materialize in the next 3–6 months, comparable revenues are likely to be muted versus the pandemic peak and could be lumpy quarter-to-quarter as legacy COVID contracts roll off.
- Margins and profitability: Gross margins and operating profitability will continue to reflect a transition: higher R&D and commercialization spend for multiple late‑stage programs offsetting lower COVID volume. Expect margin pressure versus peak-pandemic levels until new products scale or volume-based cost improvements materialize.
- Pipeline catalysts and clinical readouts: The company’s short-term stock performance will be sensitive to near-term clinical/regulatory milestones (e.g., RSV/seasonal vaccine trial readouts, late‑stage data or filings for other vaccine candidates, or any major partnership/contract announcements). Positive readouts or procurement agreements would be material upside; negative or delayed outcomes would be meaningful downside.
- Macroeconomic and policy context: Public health budgets, government procurement cycles, and payer willingness to pay will be the dominant macro drivers for near-term demand. General macro conditions (growth, health budgets) are less directly cyclical for vaccines than for elective therapeutics but still important for procurement size and timing.
- Guidance and market sentiment: Expect guidance to be cautious and conditional—management will likely emphasize pipeline potential and cost discipline while acknowledging revenue normalization from pandemic highs.

Scenario summary (3–6 months)
- Upside scenario: one or more favorable regulatory/clinical readouts or large public procurement deals (national booster campaigns or stockpile purchases) drive better-than-expected revenue and improved market sentiment.
- Base scenario: continued revenue normalization, modest margin compression as R&D continues, and stock volatility keyed to pipeline newsflow.
- Downside scenario: weak seasonal uptake, competitive displacement (e.g., cheaper or more convenient vaccines), or delayed trial readouts lead to further revenue shortfalls and downward revisions.

Competitive comparison (2–4 key peers)
1) Pfizer (PFE)
- Strengths relative to Moderna: broader commercial infrastructure and diversified revenue base beyond vaccines (large pharmaceutical business), deeper payer relationships, strong global sales/marketing and manufacturing footprint; existing COVID-19 booster product (co-developed) gives immediate commercial clout.
- Weaknesses relative to Moderna: legacy biologics pipeline is large but not specifically focused on mRNA innovation; slower platform iteration compared with pure‑play mRNA firms.
- Implication: Pfizer is a formidable commercial competitor for market access and procurement deals; Moderna competes more on platform agility and next‑generation mRNA products.

2) BioNTech (BNTX)
- Strengths: mRNA-native competitor focused on infectious disease and oncology; strong scientific expertise in individualized cancer immunotherapy; partnership with Pfizer provides global commercial scale for infectious-disease vaccines.
- Weaknesses: smaller standalone commercial footprint and manufacturing scale than Pfizer; relies on partners for some commercial execution.
- Implication: BioNTech is a direct platform peer—competitive in mRNA innovation and oncology—but Moderna’s vertically integrated manufacturing and earlier commercial vaccine experience give it advantages in scale-up and supply.

3) GSK / Sanofi (select legacy vaccine players)
- Strengths: deep experience in traditional vaccines, well‑established relationships with public health agencies, broad manufacturing networks and vaccine category expertise (e.g., RSV). They can compete on pricing, adjuvant technologies, and established procurement channels.
- Weaknesses: not native mRNA innovators (though many legacy players are partnering with mRNA companies); slower to iterate new platform features.
- Implication: Legacy vaccine makers remain strong competitors for public tenders and high‑volume seasonal markets; Moderna must demonstrate clinical and cost advantages to displace them.

Relative strengths and weaknesses (Moderna)
- Strengths: leading mRNA platform, rapid design-to-clinic timelines, prior large-scale commercial manufacturing experience, pipeline breadth across infectious disease and oncology.
- Weaknesses: revenue volatility tied to pandemic-era product rolloff, concentration risk if new products don’t scale, pricing pressure from governments and competitors, substantial ongoing R&D spend.

Adjacent industries and transmission channels
- Contract development and manufacturing organizations (CDMOs): Capacity and costs at CMOs and raw-material suppliers (lipid nanoparticle components, nucleotides, specialty reagents) directly affect Moderna’s production timing, COGS and ability to meet large procurement contracts. Any bottleneck increases delivery risk and can raise unit costs.
- Public health procurement and government budgets: Decisions by ministries of health and agencies (procurement timing, stockpiling policies, reimbursement rules) are the main demand driver for vaccines—changes here have immediate revenue effects.
- Diagnostics & surveillance: Improved respiratory disease surveillance and diagnostics can increase targeted vaccine uptake (e.g., targeted booster campaigns) and improve product-market fit; conversely, lower perceived disease risk can depress uptake.
- Competing vaccine technologies (protein/adjuvant vaccines, viral vectors): Efficacy or pricing advantages from non-mRNA vaccines can reduce Moderna’s addressable market in some segments.
- Oncology and personalized medicine ecosystems: Success in oncology programs (neoantigen vaccines, combinations with checkpoint inhibitors) would open high-margin markets and new revenue streams, but these markets also require partnerships with pharma, payers and clinical adoption pathways.

Key risks and opportunities
Risks
- Commercial: Continued post‑pandemic demand decline for COVID boosters and delayed traction for new respiratory vaccines or seasonal launches.
- Competitive: Aggressive pricing and procurement wins by Pfizer/BioNTech or traditional vaccine makers, and faster launches of rival products.
- Clinical/development: Late‑stage trial failures or regulatory delays in key pipeline programs (RSV, CMV, flu, oncology).
- Manufacturing & supply chain: LNP or other raw-material shortages or manufacturing quality issues slowing deliveries.
- Reputational/policy: Public vaccine hesitancy, adverse safety signals (even if rare) or restrictive public procurement policies.

Opportunities
- New product approvals and procurement deals (RSV, seasonal influenza, CMV, combination vaccines) could materially restore growth and margins.
- Platform leverage: licensing, partnerships, and non-infectious disease applications (oncology, rare diseases) could diversify revenue and raise long‑term valuations.
- Manufacturing scale and cost reductions: improved yield and scale economies could raise gross margins.
- Strategic collaborations with large pharma or governments for stockpiles and seasonal programs.

Summary judgment
- Over the next 3–6 months, Moderna’s near‑term commercial performance is likely to remain transitional: the company faces ongoing revenue normalization from pandemic highs, margin pressure from continued R&D investment, and high sensitivity to pipeline readouts and public procurement cycles. Absent near-term regulatory wins or large contract awards, results will likely be uneven and sentiment-driven.
- Competitive position: Moderna retains a leading scientific and platform position in mRNA technology and valuable manufacturing know‑how, giving it an edge in rapid product development and potential new markets. However, it faces fierce competition from Pfizer/BioNTech (particularly on global commercial reach and procurement relationships) and established vaccine companies for seasonal and public‑health markets.
- Investment/strategic implication (non‑advice): Watch the upcoming 1–2 quarters for clinical readouts, contract announcements, and management guidance revisions—these items will be the main drivers of performance and provide clearer evidence whether Moderna’s next wave of products can replace lost COVID-era revenue.

Key items to monitor in the next 3–6 months
- Timing and outcomes of any late‑stage clinical readouts or regulatory filings (respiratory programs, CMV, oncology combos).
- New procurement/volume purchase agreements with governments or large institutional buyers.
- Quarterly revenue guidance and margin trends, and commentary on manufacturing capacity and COGS.
- Any material partnerships or licensing deals that de‑risk commercialization pathways.

(Analysis presented for informational purposes and not investment advice.)

---

# **Analysis of Moderna, Inc. (MRNA)**

## **1. Market Sentiment & Expectations (Last 3–6 Months)**

*   **Predominantly Cautious to Bearish:** Sentiment has shifted significantly from the pandemic highs. The primary focus is on the company's challenging transition from a "COVID-19 company" to a diversified commercial biotech.
*   **Key Bullish Themes:**
    *   **Pipeline Progress:** Positive data readouts for pipeline assets, particularly the **mRNA-1345 RSV vaccine** (competing with GSK's Arexvy and Pfizer's Abrysvo), are seen as the most critical near-term catalyst. Approval and successful commercialization are viewed as essential for revenue diversification.
    *   **Long-term Platform Validation:** Investors with a long-term view believe in the potential of the mRNA platform beyond infectious diseases, especially in **oncology (personalized cancer vaccines)** and **rare diseases**. Positive Phase 2 data for its personalized cancer vaccine (mRNA-4157) with Merck's Keytruda has generated optimism about a future blockbuster.
    *   **Cost Control:** Management's commitment to significant cost-cutting and a return to breakeven by 2026 is viewed positively as a necessary step.
*   **Key Bearish Themes & Concerns:**
    *   **"COVID Cliff":** The dramatic decline in Spikevax sales is the overwhelming narrative. With COVID vaccine demand becoming seasonal and commoditized, forecasting future revenue is highly uncertain. Q4 2023 and early 2024 earnings reports highlighted this steep decline.
    *   **Commercial Execution Questions:** As a first-time commercial company outside of pandemic conditions, Moderna faces skepticism about its ability to market and sell non-COVID products (like the RSV vaccine) effectively against established pharma giants.
    *   **Cash Burn & Profitability:** The company is currently operating at a loss as R&D investments remain high while COVID revenue plummets. The path to sustained profitability is a major concern for analysts.
    *   **Stock Performance:** The stock has significantly underperformed the broader market (e.g., SPY) and biotech indices (e.g., XBI) over the past year, reflecting these headwinds.

## **2. Competitive Positioning (Infectious Disease & Oncology)**

*   **Strengths:**
    *   **Technology Leadership:** Still considered a leader in mRNA technology with a robust patent estate and extensive manufacturing experience.
    *   **Speed & Agility:** The mRNA platform allows for rapid development and iteration, a proven advantage in responding to viral variants.
    *   **Strong Balance Sheet:** Despite cash burn, the company entered 2024 with over $12 billion in cash and investments, providing a long runway to fund pipeline development.
    *   **Key Partnerships:** The high-profile collaboration with **Merck in oncology** is a major strategic asset and validation.
*   **Weaknesses:**
    *   **Over-reliance on One Product:** Historic and near-term financial health remains heavily tied to a single product (Spikevax) in a declining market.
    *   **Limited Commercial Infrastructure:** Lacks the large, established sales forces and deep provider relationships of competitors like **Pfizer, GSK, and Sanofi**.
    *   **Pipeline Maturity:** While promising, most non-COVID pipeline assets are in mid-to-late-stage development, meaning significant revenue is years away.
*   **Opportunities:**
    *   **Successful RSV Launch:** Capturing meaningful market share in the ~$10+ billion RSV vaccine market would be a transformative success and prove its commercial capabilities.
    *   **Pipeline Catalysts:** Positive data in 2024/2025 for flu (combination vaccines), latent virus vaccines (CMV, EBV), and oncology could re-rate the stock.
    *   **Platform Expansion:** Success in new therapeutic areas (cardiovascular, autoimmune) would dramatically expand total addressable market.
*   **Threats:**
    *   **Intense Competition:** In RSV: GSK and Pfizer are entrenched. In Flu: Sanofi and GSK dominate. In COVID: Pfizer/BioNTech and Novavax compete on price. In Oncology: Numerous modalities (cell therapy, targeted therapies) are competing.
    *   **Pricing & Reimbursement Pressure:** Payers are exerting more pressure on vaccine pricing, especially in a commoditized COVID market.
    *   **Patent Litigation:** Ongoing mRNA patent disputes (e.g., with Pfizer/BioNTech) create a potential financial and operational overhang.

## **3. Adjacent Industry Impact**

*   **Public Health Policy & Government Procurement:**
    *   The shift of COVID vaccines to the **commercial market** in the U.S. has disrupted sales models, introduced pricing complexity, and created near-term demand uncertainty. This transition, dictated by government health policy, is a direct and material negative impact.
    *   **Recommendations** from bodies like the CDC's Advisory Committee on Immunization Practices (ACIP) on seasonal COVID and RSV vaccines directly drive demand.
*   **General Biotech Funding Environment:**
    *   The broader biotech sector has faced a prolonged period of tight capital markets and high interest rates. This negatively impacts sentiment for all pre-profitability biotechs like Moderna, making investors less tolerant of cash burn and demanding clearer near-term paths to profitability.
*   **Consumer Health Sentiment & Vaccine Hesitancy:**
    *   Trends in public trust in vaccines and public health institutions, influenced by political and social discourse, can affect uptake rates for all of Moderna's products, not just COVID vaccines.
*   **Supply Chain & Logistics:**
    *   While Moderna has built significant internal capacity, the broader biopharma supply chain for raw materials (nucleotides, lipids) and vial/filling capacity can influence cost and production timelines. Stabilization here is a positive.
*   **Artificial Intelligence (AI) in Drug Discovery:**
    *   Moderna has heavily invested in digital and AI tools to accelerate mRNA design and biomarker discovery. Advances in this adjacent tech sector are a **net positive**, potentially increasing R&D efficiency and success rates. Moderna often highlights its "Digital Biotech" strategy in this context.

**Conclusion:** Moderna is at a critical inflection point. The market is discounting its past COVID success and is intensely focused on its ability to execute a difficult transition. The near-term (next 12-18 months) outlook is dominated by the commercial launch of its RSV vaccine and the continued management of the COVID revenue decline. Long-term sentiment hinges on clinical pipeline success, particularly in oncology. The stock is currently priced for significant uncertainty, with high risk but also high potential reward if its non-COVID pipeline delivers.
"""

# --- Helper Functions for Parsing ---

def extract_header_info(text):
    """Extracts company, ticker, date, and analyst from the first block."""
    company_match = re.search(r"\*\*Company:\*\*\s*(.+?)\s*\((MRNA)\)", text)
    date_match = re.search(r"\*\*Date:\*\*\s*(.+)", text)
    analyst_match = re.search(r"\*\*Analyst:\*\*\s*(.+)", text)

    return {
        "Company": company_match.group(1) if company_match else "N/A",
        "Ticker": company_match.group(2) if company_match else "N/A",
        "Date": date_match.group(1) if date_match else "N/A",
        "Analyst": analyst_match.group(1) if analyst_match else "N/A",
    }

def extract_section(text, section_header, next_section_header=None):
    """
    Extracts content between a given section header and the next one (or end of text).
    Handles potential markdown headers within the content.
    """
    section_header_escaped = re.escape(section_header)
    
    if next_section_header:
        next_section_header_escaped = re.escape(next_section_header)
        pattern = rf"{section_header_escaped}(.*?)(?=\s*{next_section_header_escaped}|$)"
    else:
        pattern = rf"{section_header_escaped}(.*)"
        
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        content = match.group(1).strip()
        # Remove the section header itself from the content for a cleaner output
        content = re.sub(rf"^{re.escape(section_header)}\s*\n*", "", content, flags=re.IGNORECASE)
        # Remove any leading markdown headers (#, ##, ###) if they accidentally got included
        content = re.sub(r"^(#+)\s*", "", content, flags=re.MULTILINE)
        return content
    return "N/A"

def parse_peer_benchmarking_table(text):
    """Parses the markdown table for peer benchmarking into a pandas DataFrame."""
    table_match = re.search(r"\| Metric\s*\|.+\n\|\s*:---\s*\|.+\n((\|.+\|.+\|.+\|.+\|.+\n)+)", text)
    if table_match:
        table_string = table_match.group(0)
        lines = table_string.strip().split('\n')
        
        # Extract header, clean it
        header = [h.strip() for h in lines[0].split('|') if h.strip()]
        
        # Extract data rows, clean them
        data_rows = []
        for line in lines[2:]: # Skip header and separator line
            row = [item.strip() for item in line.split('|') if item.strip()]
            if row: 
                data_rows.append(row)
        
        if data_rows and header:
            df = pd.DataFrame(data_rows, columns=header)
            df = df.set_index("Metric")
            return df
    return pd.DataFrame()

# --- Main App Logic ---

# Split the analysis into the three main blocks based on "---" separators
analysis_blocks = analysis_text.split("---")

# Assign blocks to variables
block1_text = analysis_blocks[0] if len(analysis_blocks) > 0 else ""
block2_text = analysis_blocks[1] if len(analysis_blocks) > 1 else ""
block3_text = analysis_blocks[2] if len(analysis_blocks) > 2 else ""

# Extract header information
header_info = extract_header_info(block1_text)

# --- Streamlit UI ---

st.title(f"📈 Moderna, Inc. ({header_info['Ticker']}) - Financial Analysis")
st.markdown(f"**Date:** {header_info['Date']} | **Analyst:** {header_info['Analyst']}")
st.markdown("---")

# --- Key Metrics Snapshot ---
st.header("✨ Key Metrics & Snapshot")
col1, col2, col3, col4 = st.columns(4)

# Extract P/E for MRNA from the table
peer_df = parse_peer_benchmarking_table(block1_text)
mrna_pe_str = peer_df.loc["P/E Ratio (TTM)", "Moderna, Inc. (MRNA)"] if not peer_df.empty else "N/A"
mrna_pe_num = None
if isinstance(mrna_pe_str, str) and 'N/A' not in mrna_pe_str:
    try:
        mrna_pe_num = float(re.sub(r'[~()]', '', mrna_pe_str.split(' ')[0]))
    except ValueError:
        pass

# Extract cash position from block 3
cash_match = re.search(r"over \$(\d+\.?\d*)\s*billion in cash and investments", block3_text)
cash_position = float(cash_match.group(1)) if cash_match else "N/A"

with col1:
    st.metric("Company", header_info['Company'])
with col2:
    st.metric("P/E Ratio (TTM)", mrna_pe_str)
with col3:
    st.metric("Cash & Investments (Early 2024)", f"${cash_position:.1f} Billion" if isinstance(cash_position, float) else cash_position)
with col4:
    st.metric("Market Sentiment", "Cautious to Bearish")

st.markdown("---")

# --- Executive Summary ---
st.header("📄 Executive Summary")
executive_summary = extract_section(block1_text, "**Executive Summary:**", "---")
st.markdown(executive_summary)

st.markdown("---")

# --- Visualizations Section ---
st.header("📊 Key Visualizations")

# P/E Ratio Comparison
st.subheader("Peer Valuation: P/E Ratio (TTM)")
if not peer_df.empty:
    pe_data = peer_df.loc["P/E Ratio (TTM)"].copy()
    pe_chart_list = []
    
    for company, pe_str in pe_data.items():
        if 'N/A' not in pe_str:
            try:
                # Remove non-numeric characters except '.' and '-'
                numeric_pe = re.sub(r'[^\d.-]', '', pe_str.split(' ')[0])
                pe_chart_list.append({"Company": company.replace("Moderna, Inc. (MRNA)", "MRNA").replace("Pfizer Inc. (PFE)", "PFE").replace("BioNTech SE (BNTX)", "BNTX").replace("Novavax, Inc. (NVAX)", "NVAX"),
                                      "P/E Ratio": float(numeric_pe)})
            except ValueError:
                continue # Skip if conversion fails
        
    if pe_chart_list:
        pe_chart_df = pd.DataFrame(pe_chart_list)
        fig_pe = px.bar(pe_chart_df, x="Company", y="P/E Ratio", 
                        title="Peer P/E Ratio (TTM) Comparison",
                        labels={"P/E Ratio": "P/E Ratio (TTM)"},
                        color="Company",
                        color_discrete_map={"MRNA": "#636EFA", "PFE": "#EF553B", "BNTX": "#00CC96", "NVAX": "#AB63FA"})
        fig_pe.update_layout(showlegend=False)
        st.plotly_chart(fig_pe, use_container_width=True)
    else:
        st.warning("Could not extract P/E ratios for visualization.")
else:
    st.warning("Peer benchmarking data not available for P/E chart.")

col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    st.subheader("Conceptual Revenue Trajectory")
    # This is a conceptual chart based on "declining from peak" and "stabilizing" narrative
    revenue_data = {
        'Period': ['Peak Pandemic (2021-22)', 'Post-Pandemic Decline (2023)', 'Stabilization/Future Growth (2024+)'],
        'Revenue Level (Index)': [100, 40, 50] # Relative index
    }
    revenue_df = pd.DataFrame(revenue_data)
    fig_revenue = px.line(revenue_df, x='Period', y='Revenue Level (Index)', 
                          title='MRNA Conceptual Revenue Trajectory',
                          labels={'Revenue Level (Index)': 'Relative Revenue Level'},
                          markers=True, line_shape="spline",
                          color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig_revenue.update_yaxes(range=[0, 110])
    st.plotly_chart(fig_revenue, use_container_width=True)

with col_viz2:
    st.subheader("COVID-19 Vaccine Market Share (Conceptual)")
    # Conceptual market share based on text descriptions "Dominant", "Significant", "Negligible"
    market_share_data = {
        "Company": ["Pfizer/BioNTech", "Moderna", "Novavax"],
        "Share_Conceptual": [50, 35, 15] # Estimated relative shares
    }
    market_share_df = pd.DataFrame(market_share_data)
    fig_market_share = px.bar(market_share_df, x="Company", y="Share_Conceptual",
                              title="Conceptual COVID-19 Vaccine Market Share",
                              labels={"Share_Conceptual": "Relative Market Share (%)"},
                              color="Company",
                              color_discrete_map={"Pfizer/BioNTech": "#636EFA", "Moderna": "#EF553B", "Novavax": "#B6E880"})
    fig_market_share.update_yaxes(range=[0, 60])
    st.plotly_chart(fig_market_share, use_container_width=True)

# Pipeline Focus Visualization
st.subheader("MRNA Pipeline Focus Areas")
pipeline_focus_text_all = analysis_text # Search across all blocks
pipeline_areas = {
    "RSV": len(re.findall(r"RSV vaccine|mRESVIA|respiratory syncytial virus", pipeline_focus_text_all, re.IGNORECASE)),
    "Influenza (Flu)": len(re.findall(r"flu vaccine|influenza vaccine|mRNA-1010", pipeline_focus_text_all, re.IGNORECASE)),
    "Oncology (Cancer)": len(re.findall(r"oncology|cancer vaccine|mRNA-4157|V940|Keytruda", pipeline_focus_text_all, re.IGNORECASE)),
    "Rare Diseases": len(re.findall(r"rare diseases|rare genetic disorders", pipeline_focus_text_all, re.IGNORECASE)),
    "CMV": len(re.findall(r"CMV", pipeline_focus_text_all, re.IGNORECASE)), # Cytomegalovirus
    "Other Infectious Diseases": len(re.findall(r"infectious disease", pipeline_focus_text_all, re.IGNORECASE)) + len(re.findall(r"latent virus vaccines|EBV", pipeline_focus_text_all, re.IGNORECASE)),
    "COVID-19": len(re.findall(r"COVID-19 vaccine|Spikevax", pipeline_focus_text_all, re.IGNORECASE)) # Still mentioned as a driver/past driver
}

# Adjust "Other Infectious Diseases" to not double count explicit ones
explicit_infectious = pipeline_areas["RSV"] + pipeline_areas["Influenza (Flu)"] + pipeline_areas["CMV"] + pipeline_areas["COVID-19"]
if pipeline_areas["Other Infectious Diseases"] > explicit_infectious:
    pipeline_areas["Other Infectious Diseases"] -= explicit_infectious
else:
    pipeline_areas["Other Infectious Diseases"] = 0 # Avoid negative values

# Filter out zero values and create DataFrame
pipeline_chart_data = {k: v for k, v in pipeline_areas.items() if v > 0}
if pipeline_chart_data:
    pipeline_df = pd.DataFrame(list(pipeline_chart_data.items()), columns=['Area', 'Mentions'])
    fig_pipeline = px.pie(pipeline_df, values='Mentions', names='Area', 
                          title='MRNA Pipeline Focus Areas by Mention Frequency',
                          hole=0.4,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pipeline.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pipeline, use_container_width=True)
else:
    st.info("Could not extract specific pipeline focus areas for visualization.")

st.markdown("---")

# --- Sections and Summaries (Expanders for Cleanliness) ---

st.header("📖 In-Depth Analysis Sections")

# --- Block 1: Initial Research Update ---
st.subheader("Part 1: Research Update (Oct 2023)")
with st.expander("Fundamental Evaluation"):
    st.markdown(extract_section(block1_text, "### Fundamental Evaluation:", "### Peer Benchmarking:"))

with st.expander("Peer Benchmarking Table & Analysis"):
    st.markdown(extract_section(block1_text, "### Peer Benchmarking:", "### Adjacent Industry Analysis:")) # Capture text above table too
    if not peer_df.empty:
        st.dataframe(peer_df)

with st.expander("Adjacent Industry Analysis"):
    st.markdown(extract_section(block1_text, "### Adjacent Industry Analysis:", "### Risk Assessment:"))

with st.expander("Risk Assessment (Upcoming Quarter)"):
    risk_assessment_content = extract_section(block1_text, "### Risk Assessment:", "**Conclusion:**")
    st.markdown(risk_assessment_content)

    # Risk vs Opportunity Balance Visualization
    bear_case_list = re.findall(r"^\*\s*.+\n?", extract_section(risk_assessment_content, "**Bear Case (Upcoming Quarter):**", "**Bull Case (Upcoming Quarter):**"), re.MULTILINE)
    bull_case_list = re.findall(r"^\*\s*.+\n?", extract_section(risk_assessment_content, "**Bull Case (Upcoming Quarter):**", r"^\S"), re.MULTILINE) # Match until next non-whitespace char

    bear_count = len(bear_case_list)
    bull_count = len(bull_case_list)
    
    risk_opportunity_df = pd.DataFrame({
        "Category": ["Bear Case (Near-term)", "Bull Case (Near-term)"],
        "Count": [-bear_count, bull_count] # Negative for risks, positive for opportunities
    })

    fig_risk_opportunity = px.bar(risk_opportunity_df, y="Category", x="Count", 
                                  title="Risk vs. Opportunity Balance (Upcoming Quarter)",
                                  color="Count",
                                  color_continuous_scale=[(0, "red"), (0.5, "lightgrey"), (1, "green")],
                                  labels={"Count": "Weighted Impact (Conceptual)"},
                                  orientation="h")
    fig_risk_opportunity.update_layout(xaxis_title="Number of Points (Negative: Risk, Positive: Opportunity)")
    st.plotly_chart(fig_risk_opportunity, use_container_width=True)

with st.expander("Conclusion (Part 1 Analysis)"):
    st.markdown(extract_section(block1_text, "**Conclusion:**", "---"))

st.markdown("---")

# --- Block 2: Detailed Company Overview, Outlook, Competitive, Risks/Opportunities ---
st.subheader("Part 2: Company Outlook & Competitive Landscape (Supplemental)")
with st.expander("Company Overview"):
    st.markdown(extract_section(block2_text, "Company overview", "3–6 month outlook (Mar–Aug 2026)"))

with st.expander("3–6 Month Outlook (Mar–Aug 2026)"):
    st.markdown(extract_section(block2_text, "3–6 month outlook (Mar–Aug 2026)", "Scenario summary (3–6 months)"))
    st.markdown("### Scenario Summary (3–6 months)")
    st.markdown(extract_section(block2_text, "Scenario summary (3–6 months)", "Competitive comparison (2–4 key peers)"))

with st.expander("Competitive Comparison (2-4 Key Peers)"):
    st.markdown(extract_section(block2_text, "Competitive comparison (2–4 key peers)", "Relative strengths and weaknesses (Moderna)"))

with st.expander("Relative Strengths and Weaknesses (Moderna)"):
    st.markdown(extract_section(block2_text, "Relative strengths and weaknesses (Moderna)", "Adjacent industries and transmission channels"))

with st.expander("Adjacent Industries and Transmission Channels"):
    st.markdown(extract_section(block2_text, "Adjacent industries and transmission channels", "Key risks and opportunities"))

with st.expander("Key Risks and Opportunities (General)"):
    general_risks_ops = extract_section(block2_text, "Key risks and opportunities", "Summary judgment")
    st.markdown(general_risks_ops)

    # General Risk vs Opportunity Balance Visualization
    risks_general_list = re.findall(r"^\*\s*.+\n?", extract_section(general_risks_ops, "Risks", "Opportunities"), re.MULTILINE)
    opportunities_general_list = re.findall(r"^\*\s*.+\n?", extract_section(general_risks_ops, "Opportunities"), re.MULTILINE)
    
    risks_general_count = len(risks_general_list)
    opportunities_general_count = len(opportunities_general_list)

    general_risk_opportunity_df = pd.DataFrame({
        "Category": ["General Risks", "General Opportunities"],
        "Count": [-risks_general_count, opportunities_general_count]
    })

    fig_general_risk_opportunity = px.bar(general_risk_opportunity_df, y="Category", x="Count", 
                                          title="General Risk vs. Opportunity Balance",
                                          color="Count",
                                          color_continuous_scale=[(0, "red"), (0.5, "lightgrey"), (1, "green")],
                                          labels={"Count": "Number of Points"},
                                          orientation="h")
    fig_general_risk_opportunity.update_layout(xaxis_title="Number of Points (Negative: Risk, Positive: Opportunity)")
    st.plotly_chart(fig_general_risk_opportunity, use_container_width=True)

with st.expander("Summary Judgment"):
    st.markdown(extract_section(block2_text, "Summary judgment", "Key items to monitor in the next 3–6 months"))

with st.expander("Key Items to Monitor in the Next 3–6 Months"):
    st.markdown(extract_section(block2_text, "Key items to monitor in the next 3–6 months", r"\(Analysis presented for informational purposes and not investment advice.\)"))

st.markdown("---")

# --- Block 3: Market Sentiment & Expectations ---
st.subheader("Part 3: Market Sentiment & Strategic Positioning (Summary)")
with st.expander("Market Sentiment & Expectations (Last 3–6 Months)"):
    sentiment_content = extract_section(block3_text, "## \*\*1. Market Sentiment & Expectations (Last 3–6 Months)\*\*", "## \*\*2. Competitive Positioning (Infectious Disease & Oncology)\*\*")
    st.markdown(sentiment_content)
    
    # Market Sentiment Gauge (Conceptual)
    st.subheader("Overall Market Sentiment (Conceptual)")
    
    sentiment_score = -0.6 # -1 (Bearish) to 1 (Bullish) - Reflects "Predominantly Cautious to Bearish"

    fig_sentiment = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Market Sentiment"},
        gauge = {'axis': {'range': [-1, 1], 'tickvals': [-1, 0, 1], 'ticktext': ['Bearish', 'Neutral', 'Bullish']},
                 'bar': {'color': "#636EFA"},
                 'steps': [
                     {'range': [-1, -0.3], 'color': "lightcoral"},
                     {'range': [-0.3, 0.3], 'color': "lightgray"},
                     {'range': [0.3, 1], 'color': "lightgreen"}],
                 'threshold': {
                     'line': {'color': "darkblue", 'width': 4},
                     'thickness': 0.75,
                     'value': sentiment_score
                     }
                }))
    fig_sentiment.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig_sentiment, use_container_width=True)


with st.expander("Competitive Positioning (Infectious Disease & Oncology)"):
    st.markdown(extract_section(block3_text, "## \*\*2. Competitive Positioning (Infectious Disease & Oncology)\*\*", "## \*\*3. Adjacent Industry Impact\*\*"))

with st.expander("Adjacent Industry Impact"):
    st.markdown(extract_section(block3_text, "## \*\*3. Adjacent Industry Impact\*\*", "**Conclusion:** Moderna is at a critical inflection point."))

with st.expander("Overall Conclusion (Part 3 Analysis)"):
    st.markdown(extract_section(block3_text, "**Conclusion:** Moderna is at a critical inflection point."))

st.markdown("---")
st.info("Disclaimer: This analysis is presented for informational purposes only and is not investment advice.")