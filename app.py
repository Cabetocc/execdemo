import streamlit as st



def _safe_text(x):
    return str(x or '')

def _safe_strip(x):
    return _safe_text(x).strip()

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

            if updated == before:
                status.warning("Still processing. Please wait a bit longer and press Generate again (or refresh).")

        st.rerun()


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# Set Streamlit page configuration
st.set_page_config(
    page_title="AstraZeneca (AZN) Financial Ecosystem Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# The financial analysis text
ANALYSIS_TEXT = """
Let's break down the financial ecosystem of **AstraZeneca PLC (AZN)**. As a major global pharmaceutical company, its ecosystem is complex and influenced by a wide range of factors.

## AstraZeneca PLC (AZN): Financial Ecosystem Analysis

**I. Key Financial Relationships & Metrics:**

*   **Revenue Drivers:** AstraZeneca's revenue is primarily driven by its innovative pharmaceuticals and biologics across several key therapeutic areas:
    *   **Oncology:** This is a significant growth engine, with blockbuster drugs like Tagrisso, Imfinzi, and Lynparza.
    *   **Cardiovascular, Renal & Metabolism (CVRM):** Drugs like Farxiga are crucial here.
    *   **Respiratory & Immunology:** Symbicort and biologics like Tezspire are important.
    *   **Vaccines & Immune Therapies:** While the COVID-19 vaccine Vaxzevria had a significant impact, its contribution is now declining.
*   **Profitability & Margins:**
    *   **Gross Margins:** Pharmaceutical companies generally enjoy high gross margins due to the intellectual property and R&D investment embedded in their products. AZN's gross margins are typically strong.
    *   **Operating Margins:** These are influenced by R&D expenditure, sales and marketing costs, and general administrative expenses. AZN's focus on R&D is a key driver of its operating expenses.
    *   **Net Margins:** Affected by interest expenses, taxes, and other non-operating items.
*   **Research & Development (R&D) Investment:** This is the lifeblood of a pharmaceutical company. AZN invests heavily in R&D to develop new drugs and expand the indications of existing ones. This is a significant cost but crucial for future revenue growth and market position.
*   **Debt & Leverage:** While AZN is a large, established company, it may utilize debt for acquisitions, R&D funding, or to manage its capital structure. Analysts will examine its debt-to-equity ratio and interest coverage to assess financial risk.
*   **Cash Flow:**
    *   **Operating Cash Flow:** A critical indicator of the company's ability to generate cash from its core business. Strong operating cash flow is essential for funding R&D, dividends, and potential acquisitions.
    *   **Free Cash Flow (FCF):** Operating cash flow minus capital expenditures. This represents cash available for debt repayment, dividends, share buybacks, and strategic investments.
*   **Dividend Payouts:** As a mature company, AZN typically pays dividends to its shareholders, making it attractive to income-focused investors. The sustainability and growth of these dividends are closely watched.
*   **Acquisitions & Divestitures:** AZN has a history of strategic acquisitions and divestitures to bolster its pipeline, enter new therapeutic areas, or shed non-core assets. These transactions can significantly impact its financial statements and future prospects.

**II. Market Dependencies:**

*   **Prescription Volumes & Patient Access:** The demand for AZN's drugs is directly tied to prescription volumes, which are influenced by physician prescribing habits, patient awareness, and disease prevalence.
*   **Reimbursement Policies & Payer Negotiations:** Pharmaceutical companies are heavily reliant on government and private insurers to reimburse for their drugs. Negotiations with payers, pricing pressures, and formulary decisions are critical.
*   **Global Economic Conditions:** While healthcare is relatively recession-resistant, economic downturns can impact government healthcare spending, individual disposable income for healthcare, and overall market demand.
*   **Regulatory Approvals & Market Exclusivity:** The ability to gain and maintain regulatory approval for new drugs and to protect them from generic competition through patent exclusivity is paramount. Delays or rejections can be devastating.
*   **Competition & Generic Erosion:** The threat of generic competition after patent expiry is a constant factor. The timing and impact of biosimilar/generic entry on revenue streams are closely monitored.
*   **Supply Chain & Manufacturing:** Disruptions in the global supply chain or manufacturing issues can impact product availability and revenue.

**III. Sector Connections:**

*   **Pharmaceutical & Biotechnology Sector:** AZN operates within this highly regulated and R&D-intensive sector. Its performance is often benchmarked against other large-cap pharmaceutical companies.
*   **Healthcare Sector:** More broadly, AZN is a component of the healthcare sector, which includes medical devices, healthcare providers, and health insurance.
*   **Emerging Markets Healthcare:** AZN has a significant presence in emerging markets, making it sensitive to the growth and healthcare infrastructure development in these regions.

**IV. Competitor Relationships:**

AZN competes with a vast array of global pharmaceutical giants and smaller biotech firms. Key competitors include:

*   **Oncology:**
    *   **Pfizer:** Competing with numerous oncology drugs.
    *   **Merck & Co. (MSD):** Strong in immuno-oncology (Keytruda).
    *   **Bristol Myers Squibb (BMS):** Also a major player in immuno-oncology.
    *   **Roche:** A dominant force in oncology with a strong pipeline.
    *   **Novartis:** Another diversified pharmaceutical giant with oncology offerings.
*   **Cardiovascular, Renal & Metabolism:**
    *   **Eli Lilly:** Strong presence with diabetes and obesity drugs.
    *   **Novo Nordisk:** A leader in diabetes and obesity.
    *   **Sanofi:** Offers competing products in these areas.
*   **Respiratory & Immunology:**
    *   **GSK (GlaxoSmithKline):** A significant competitor in respiratory and vaccines.
    *   **Sanofi:** Competes in immunology and respiratory.
    *   **AbbVie:** Strong in immunology.
*   **Emerging Players:** Numerous smaller biotech companies are developing innovative therapies that could disrupt specific therapeutic areas.

**V. Economic Factors:**

*   **Interest Rates:** Affect borrowing costs for R&D and acquisitions. Also influences the attractiveness of dividend yields relative to fixed income.
*   **Inflation:** Can impact R&D costs, manufacturing expenses, and potentially influence drug pricing strategies.
*   **Currency Exchange Rates:** As a global company, fluctuations in currency exchange rates can significantly impact reported revenues and profits. For example, a strong USD can make its European revenues less valuable in USD terms.
*   **Government Healthcare Spending Policies:** Austerity measures or changes in national health service priorities in major markets (e.g., the US, Europe, China) can directly affect demand and pricing.
*   **Geopolitical Stability:** Disruptions in key markets or supply chains due to geopolitical events can have an impact.
*   **Demographic Trends:** Aging populations in developed countries increase the demand for many of AZN's therapeutic areas, while growing middle classes in emerging markets present growth opportunities.
*   **Technological Advancements:** Breakthroughs in areas like AI for drug discovery or gene therapy can create both opportunities and threats for established players.

**VI. Key Strengths & Risks for AZN:**

*   **Strengths:**
    *   Strong R&D pipeline with promising assets.
    *   Leadership positions in key therapeutic areas (e.g., oncology, CVRM).
    *   Global diversification across developed and emerging markets.
    *   Established brand recognition and reputation.
    *   Solid financial footing with robust cash flow generation.
*   **Risks:**
    *   Patent expirations and generic competition.
    *   Clinical trial failures and regulatory hurdles.
    *   Pricing pressures from payers and governments.
    *   Intense competition from both large and small players.
    *   Execution risk on M&A strategies.
    *   Potential for unexpected side effects or safety concerns.

**In conclusion, AstraZeneca's financial ecosystem is a dynamic interplay of scientific innovation, market forces, regulatory landscapes, and global economic conditions. Its success hinges on its ability to continually develop and commercialize breakthrough medicines, navigate complex reimbursement environments, and effectively manage its global operations in the face of intense competition. Investors and analysts scrutinize these interconnected elements to assess the company's long-term viability and shareholder value potential.**

---

Below is a concise, structured analysis of AstraZeneca plc (ticker: AZN) and the financial/ecosystem forces that most materially affect its share price and long‑term outlook.

1) Business overview and revenue drivers
- Core therapeutic areas: oncology, cardiovascular/metabolic (CVMD), respiratory/immunology, rare diseases (Alexion acquisition), and other specialty medicines. Oncology and CV/metabolic are the primary growth engines; rare disease biologics (Soliris, Ultomiris) provide high margin, durable revenue.
- Revenue model: product sales (majority), collaboration/co‑promotion revenues, milestone and royalty income from partnerships, and service/CRO spend via outsourced R&D/manufacturing relationships.
- Pipeline orientation: heavy R&D investment focused on oncology (targeted therapies, immuno‑oncology, antibody‑drug conjugates), CV/metabolic (SGLT2 and other agents), and rare disease biologics. Pipeline progress and late‑stage readouts are major value drivers.

2) Key commercial products and dependencies (high level)
- Oncology: Tagrisso (osimertinib) — a key driver in targeted non‑small cell lung cancer (EGFR); Imfinzi (durvalumab) in immuno‑oncology — both subject to competition and label expansion opportunities.
- CV/metabolic: SGLT2 and other cardiorenal/metabolic franchises drive recurring growth and exposure to diabetes/heart‑failure markets.
- Rare disease: Soliris/Ultomiris (from Alexion acquisition) provide high‑margin, long‑duration sales but face biosimilar/market access and pricing scrutiny in some jurisdictions.
- Note: COVID vaccine (Vaxzevria) contributed in prior years but is not a core ongoing revenue growth engine.

3) Major partnerships and collaboration relationships
- Large co‑development/co‑commercial partnerships are central to revenue and pipeline economics:
  - PARP and olaparib (Lynparza) collaboration with MSD (Merck in the U.S.) — aligns oncology IP/revenue sharing.
  - ADC and HER2 collaborations (e.g., with Daiichi Sankyo) and other oncology alliances — provide access to complementary technology and indications.
  - Regional commercialization partnerships (historically with local players in China and elsewhere) to accelerate market entry.
- Contract manufacturing and R&D outsourcing: reliance on large CROs/CDMOs (e.g., Lonza, Catalent, other CMOs and CROs) for biologics/clinical trials creates operational dependencies and concentration risk.

4) Competitor set and market relationships
- Direct competitors by therapy area:
  - Oncology: Roche, Bristol‑Myers Squibb, Merck (Keytruda), Pfizer, Novartis and multiple oncology biotech players — competition on efficacy, combination regimens, and label expansion.
  - CV/Metabolic & Diabetes/Obesity: Novo Nordisk and Eli Lilly (GLP‑1 and multi‑agonists such as tirzepatide/novel agents) are reshaping metabolic/obesity markets and indirectly pressuring some diabetes drug economics; Pfizer and Novo also influence CV drug space.
  - Rare diseases/biologics: Alexion competes with other rare‑disease specialists (e.g., Regeneron, Sanofi, Novartis) and faces biosimilar entrants for older biologics.
- Competitive dynamics: trial readouts, head‑to‑head results, safety profiles, and payer willingness to reimburse combinations determine commercial success.

5) Financial relationships and capital structure implications
- Revenue concentration: significant exposure to mature products with patent timelines; recurring high‑margin biologic revenues from rare disease portfolio underpin cash flow.
- M&A and inorganic growth: the Alexion acquisition materially expanded the rare disease franchise and adjusted leverage and capital allocation priorities (R&D vs. dividends vs. buybacks).
- Cash flow profile: typically strong operational cash flow from biologics and established medicines funds R&D and shareholder returns; free cash flow volatility tied to product mix, milestone timing, and working capital.
- Dividend and returns: AstraZeneca targets shareholder returns but balances them with heavy R&D and strategic acquisitions; dividends are meaningful but the company tends to prioritize growth investments in many cycles.

6) Macro, regulatory and policy drivers
- Regulatory approvals and label expansions (FDA, EMA, NMPA) are binary catalysts that materially re‑rate the stock.
- Pricing and reimbursement: US policy (including Medicare negotiation timelines), international reference pricing, and payer cost‑containment pressure are persistent risks. The Inflation Reduction Act and similar policies increase uncertainty about future pricing for certain drugs.
- Patent expirations and generic/biosimilar entries: patent cliffs for key molecules, or successful biosimilar launches, can impair revenue trajectories; lifecycle management and new indications mitigate but do not eliminate the risk.
- Currency exposure: reporting currency and the split of global sales (large U.S. exposure) make FX movements (GBP/USD/EUR) relevant to reported results and EPS.
- Macro environment: global GDP growth, healthcare budgets, and demographic trends (aging populations) influence demand; higher interest rates raise discount rates applied by investors to long‑dated pipeline value.

7) Sector connections and supply chain ecosystem
- CRO/CDMO relationships: AstraZeneca is embedded with major CROs and CDMOs for trials and biologics manufacture; disruptions or capacity constraints at these partners can delay launches.
- Diagnostics and companion diagnostics: partnerships with diagnostic companies are critical in precision oncology (testing for EGFR, HER2, others) which impacts drug uptake.
- Biotech/academic collaborations: early discovery partnerships with biotechs and universities feed the pipeline and can produce milestone receipts or dilution if structured via equity.

8) Key risks
- Clinical trial failure or safety signals in late‑stage programs.
- Major competitor assets (e.g., Keytruda, Herceptin/Enhertu, GLP‑1 drugs) reducing expected market share.
- Pricing and reimbursement changes, especially large‑market policies (U.S. Medicare negotiation).
- Regulatory delays or unfavorable label decisions.
- Supply chain disruption for biologics components or manufacturing capacity constraints.
- Litigation and IP disputes (common in pharma).

9) Key catalysts and monitoring checklist (what investors should watch)
- Late‑stage (Phase III/registrational) oncology and CVMD trial readouts and regulatory filings.
- Quarterly sales trends by franchise (oncology growth vs. rare disease dynamics vs. diabetes/CV).
- Progress on label expansions and approvals across major markets (FDA, EMA, China NMPA).
- Patent expiry timelines and biosimilar entry risk for Soliris/other biologics.
- Updates on major collaborations and any milestone/royalty changes.
- Macro/regulatory developments: US drug pricing policies, EU pricing reforms, and reimbursement rulings in China.
- M&A activity or large licensing deals that materially change pipeline or financial leverage.
- FX movements and interest rate environment that affect valuation and reported earnings.

10) Investment implications (high level)
- Structural growth thesis: strong oncology and cardiorenal/metabolic franchises plus Alexion rare disease assets give AstraZeneca a balanced growth-and-margin profile, supported by a deep pipeline. This supports a premium to many peers in growth scenarios.
- Risk/return profile: high potential upside tied to pipeline successes and label expansions, but binary trial/regulatory events, pricing pressure, and biosimilar risk can create downside volatility.
- Valuation drivers: pipeline de‑risking, sustained commercial execution in U.S./China, and margin expansion on biologics sales will be the primary levers to justify higher multiples. Conversely, adverse policy moves or major competitive losses would compress multiples.

If you want, I can:
- produce a prioritized watchlist of 6–10 upcoming AstraZeneca clinical/regulatory milestones and their likely timing (based on public filings and trial registries),
- map the company’s revenue by franchise and geography using the latest financial statements (if you provide the most recent 10‑K/annual report or allow me to pull recent data),
- or compare AZN’s valuation and key financial ratios vs. a defined peer group (e.g., Roche, Pfizer, Novartis, Merck, BMS).

---

**Stock Ticker: AZN (AstraZeneca PLC)**

---

### **1. Company Overview**
AstraZeneca is a global biopharmaceutical company headquartered in Cambridge, UK. It focuses on the discovery, development, and commercialization of prescription medicines, primarily in oncology, cardiovascular, renal & metabolism, respiratory & immunology, and rare disease areas. Key products include Tagrisso (oncology), Farxiga (diabetes/heart failure), and COVID-19 vaccine Vaxzevria.

---

### **2. Key Financial Relationships**
- **Revenue Streams**: Heavily dependent on oncology drugs (~35% of total revenue), followed by cardiovascular/metabolism and respiratory drugs. Geographic diversification: U.S. (~45% of revenue), Europe, and emerging markets.
- **Profitability**: High R&D expenditure (~20–25% of revenue) impacts short-term margins but drives long-term growth via drug pipelines. Operating margins have improved due to cost efficiencies and patent-protected blockbuster drugs.
- **Debt & Liquidity**: Moderate debt levels post-acquisitions (e.g., Alexion in 2021), but strong cash flow from mature drugs supports debt servicing and shareholder returns.
- **Dividends**: Consistent dividend payer with gradual growth, appealing to income-focused investors.

---

### **3. Market Dependencies**
- **Regulatory Environment**: FDA (U.S.), EMA (Europe), and other health authorities’ approvals are critical for drug launches and label expansions.
- **Patent Expirations**: Key drugs face eventual patent cliffs (e.g., Nexium, Crestor in past years). Current focus on extending exclusivity through new indications or combination therapies.
- **Healthcare Policies**: Pricing pressures from U.S. Medicare negotiations (Inflation Reduction Act) and European cost-containment measures could impact future revenue.
- **Global Health Crises**: COVID-19 vaccine demand boosted revenue temporarily but is now declining; pandemic preparedness initiatives offer opportunities.

---

### **4. Sector Connections**
- **Pharmaceutical Industry**: Part of a competitive, innovation-driven sector with high barriers to entry. Trends include personalized medicine, biologics, and digital health integration.
- **Supply Chain**: Relies on active pharmaceutical ingredient (API) manufacturers, contract research organizations (CROs), and logistics partners. Geopolitical risks (e.g., China dependencies) may affect operations.
- **Biotech Partnerships**: Collaborations with biotech firms (e.g., Daiichi Sankyo for Enhertu) are crucial for pipeline expansion. M&A activity is common to acquire novel therapies.

---

### **5. Competitor Relationships**
- **Direct Competitors**: 
  - **Large Cap Pharma**: Pfizer (PFE), Merck (MRK), Roche (RHHBY), Novartis (NVS), Johnson & Johnson (JNJ).
  - **Oncology Focus**: Bristol-Myers Squibb (BMY), Gilead Sciences (GILD).
- **Competitive Advantages**: Strong oncology pipeline, geographic reach in emerging markets, and leadership in respiratory diseases.
- **Threats**: Intense competition in oncology (e.g., Keytruda from Merck) and diabetes (Jardiance from Eli Lilly). Biosimilars may erode sales of older biologics.

---

### **6. Economic Factors**
- **Macroeconomic Sensitivity**: Generally defensive; demand for medicines is relatively inelastic during recessions, but currency fluctuations (USD/GBP/EUR) impact reported earnings.
- **Interest Rates**: Higher rates increase borrowing costs for acquisitions and R&D financing, potentially affecting valuation multiples.
- **Inflation**: R&D and manufacturing costs may rise, though pricing power in patented drugs can offset pressures.
- **Emerging Markets Growth**: Rising healthcare access in China, Brazil, and other regions offers long-term growth tailwinds.

---

### **7. ESG & Regulatory Risks**
- **Environmental**: Commitment to net-zero emissions by 2025 influences operational costs and brand reputation.
- **Social**: Drug pricing scrutiny and access-to-medicine initiatives are key reputational risks.
- **Governance**: Compliance with anti-bribery laws (e.g., FCPA, UK Bribery Act) and clinical trial ethics is critical.

---

### **8. Investment Considerations**
- **Strengths**: Robust pipeline, strong oncology portfolio, growing emerging market presence.
- **Risks**: Patent expirations, regulatory hurdles, political drug pricing pressures, pipeline setbacks.
- **Valuation**: Trades at a premium to some peers due to growth prospects; metrics to watch: P/E, EV/EBITDA, and free cash flow yield.

---

### **Conclusion**
AstraZeneca operates in a complex ecosystem where innovation, regulatory navigation, and global market dynamics dictate performance. Its financial health is tied to successful drug launches and managing patent cliffs, while macroeconomic and sector-specific factors shape its risk-reward profile. Investors should monitor pipeline developments, competitive threats, and healthcare policy changes closely.
"""

# --- Utility Functions ---
def parse_analysis_text_into_sections(text):
    """
    Parses the analysis text into logical sections based on various heading patterns.
    Returns a dictionary of sections, the stock ticker, and distinct conclusion texts.
    """
    sections = {}
    ticker = "AZN"

    # Extract ticker
    ticker_match = re.search(r'Stock Ticker:\s*(AZN)\s+\(AstraZeneca PLC\)', text)
    if ticker_match:
        ticker = ticker_match.group(1)

    # Extract the distinct introduction and conclusion blocks
    global_intro_match = re.match(r'Let\'s break down the financial ecosystem of \*\*AstraZeneca PLC \(AZN\)\*\*. As a major global pharmaceutical company, its ecosystem is complex and influenced by a wide range of factors\.', text)
    global_intro = global_intro_match.group(0) if global_intro_match else text.split('## AstraZeneca PLC (AZN): Financial Ecosystem Analysis')[0].strip()

    first_analysis_conclusion_match = re.search(r'In conclusion, AstraZeneca\'s financial ecosystem is a dynamic interplay of scientific innovation, market forces, regulatory landscapes, and global economic conditions\. Its success hinges on its ability to continually develop and commercialize breakthrough medicines, navigate complex reimbursement environments, and effectively manage its global operations in the face of intense competition\. Investors and analysts scrutinize these interconnected elements to assess the company\'s long-term viability and shareholder value potential\.', text)
    first_analysis_conclusion = first_analysis_conclusion_match.group(0) if first_analysis_conclusion_match else ""

    final_conclusion_match = re.search(r'### \*\*Conclusion\*\*([\s\S]*)$', text)
    final_conclusion = final_conclusion_match.group(1).strip() if final_conclusion_match else ""

    # Define delimiters for the major blocks of analysis
    block1_delimiter = r'## AstraZeneca PLC \(AZN\): Financial Ecosystem Analysis'
    block2_delimiter = r'---\s*Below is a concise, structured analysis of AstraZeneca plc \(ticker: AZN\) and the financial/ecosystem forces that most materially affect its share price and long‑term outlook\.'
    block3_delimiter = r'---\s*\*\*Stock Ticker: AZN \(AstraZeneca PLC\)\*\*\s*---'

    # Split the main text into these blocks
    # Ensure regex patterns are properly escaped for re.split
    temp_blocks = re.split(f'({block1_delimiter}|{block2_delimiter}|{block3_delimiter})', text)
    
    # Reconstruct blocks with their delimiters as keys for easier processing
    full_blocks = {}
    current_key = "Global Introduction"
    for i, part in enumerate(temp_blocks):
        if re.match(block1_delimiter, part):
            current_key = "Detailed Ecosystem Analysis (AZN)"
            full_blocks[current_key] = ""
        elif re.match(block2_delimiter, part):
            current_key = "Concise Structured Analysis (AZN)"
            full_blocks[current_key] = ""
        elif re.match(block3_delimiter, part):
            current_key = "Company & Investment Overview (AZN)"
            full_blocks[current_key] = ""
        else:
            full_blocks[current_key] = full_blocks.get(current_key, "") + part
    
    # Process each major block
    for block_key, block_content in full_blocks.items():
        if block_key == "Global Introduction":
            if block_content.strip() and block_content.strip() != global_intro: # Only add if it's new content
                sections[block_key] = block_content.strip()
            continue # Already handled global_intro separately if needed
        
        # Remove the main conclusion if it's within the block content to prevent it being a sub-section
        block_content = _safe_text(block_content.replace(first_analysis_conclusion, "").replace(final_conclusion, "").strip())

        # Regex for different header types within blocks
        # Roman numerals (e.g., **I. Key Financial Relationships & Metrics:**)
        # Numbered list (e.g., 1) Business overview and revenue drivers)
        # Hash numbered (e.g., ### 1. Company Overview)
        header_pattern = re.compile(
            r'(^\*\*?[IVX]+\.\s.*?:?\*\*?$)|' # Roman numeral headers
            r'(^\d+\)\s.*?$)|' # Numbered list headers
            r'(^###\s*\d+\.\s.*?$)', # Hash numbered sections
            re.MULTILINE
        )

        sub_sections = re.split(header_pattern, block_content)
        
        # The first part before any header
        current_title_prefix = ""
        if "Detailed Ecosystem Analysis" in block_key: current_title_prefix = "" # No prefix for block 1's sub-sections
        elif "Concise Structured Analysis" in block_key: current_title_prefix = "Concise - "
        elif "Company & Investment Overview" in block_key: current_title_prefix = "Overview - "

        current_subsection_title = ""
        if sub_sections and sub_sections[0].strip():
            # If the block itself has content before its first sub-header
            # This is typically empty if split well, or an intro to the block
            pass 

        for i in range(1, len(sub_sections)):
            part = sub_sections[i]
            if part is None: continue # Skip empty groups from regex split

            # If it's a header
            if re.match(r'^\*\*?[IVX]+\.\s.*?:?\*\*?$', part) or \
               re.match(r'^\d+\)\s.*?$', part) or \
               re.match(r'^###\s*\d+\.\s.*?$', part):
                
                if current_subsection_title:
                    sections[current_title_prefix + _safe_strip(current_subsection_title)] = _safe_strip(sub_sections[i+1]) # Content is next part
                
                # Clean header text for dictionary key
                clean_header = re.sub(r'^\*\*?[IVX]+\.\s|\d+\)\s|^\#+\s|\*\*?:|\*\*$', '', part).strip()
                current_subsection_title = clean_header
            # else: content will be captured with the previous header
            # The way re.split works with capturing groups is: delimiter, content, delimiter, content...
            # so content is at index i+1 if part at index i is a delimiter.
        
        # Add the last subsection in the block
        if current_subsection_title:
             # Find the content for the last header
            last_content_start = block_content.find(_safe_text(sub_sections[-2])) + len(_safe_text(sub_sections[-2])) if len(sub_sections) > 1 else 0
            sections[current_title_prefix + _safe_strip(current_subsection_title)] = block_content[last_content_start:].strip()


    # Final cleanup of headers and sections, removing any empty or redundant
    final_sections = {}
    for title, content in sections.items():
        if content.strip() and title not in ["", "Stock Ticker: AZN (AstraZeneca PLC)"]: # Avoid empty sections
            final_sections[title.strip()] = content.strip()
    
    return final_sections, ticker, global_intro, first_analysis_conclusion, final_conclusion


def extract_key_metrics(text):
    """Extracts key numerical metrics described in the text."""
    metrics = []

    # R&D expenditure
    rd_match = re.search(r'R&D expenditure \((~?[\d–\-]+% of revenue)\)', text, re.IGNORECASE)
    if rd_match:
        metrics.append({"Metric": "R&D Expenditure", "Value": rd_match.group(1)})

    # Oncology revenue
    oncology_rev_match = re.search(r'oncology drugs \(~?([\d–\-]+% of total revenue)\)', text, re.IGNORECASE)
    if oncology_rev_match:
        metrics.append({"Metric": "Oncology Revenue", "Value": oncology_rev_match.group(1)})
    
    # US revenue
    us_rev_match = re.search(r'U\.S\. \((~?[\d–\-]+% of revenue)\)', text, re.IGNORECASE)
    if us_rev_match:
        metrics.append({"Metric": "U.S. Revenue Share", "Value": us_rev_match.group(1)})

    # Net-zero emissions target
    net_zero_match = re.search(r'net-zero emissions by (\d{4})', text, re.IGNORECASE)
    if net_zero_match:
        metrics.append({"Metric": "Net-zero Emissions Target", "Value": net_zero_match.group(1)})

    return pd.DataFrame(metrics) if metrics else None

# --- Chart Generation ---
def create_revenue_drivers_chart(data):
    """Generates a pie chart for revenue drivers based on mock data."""
    df_rev = pd.DataFrame(data)
    fig = px.pie(df_rev, values='Revenue Share', names='Therapeutic Area', 
                 title='Conceptual Revenue Drivers (Estimated)',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_geographic_revenue_chart(data):
    """Generates a pie chart for geographic revenue distribution."""
    df_geo = pd.DataFrame(data)
    fig = px.pie(df_geo, values='Revenue Share', names='Region', 
                 title='Conceptual Geographic Revenue Distribution (Estimated)',
                 color_discrete_sequence=px.colors.sequential.PuBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_rd_expenditure_gauge(value_str):
    """Generates a gauge chart for R&D expenditure."""
    # Attempt to parse the value string (e.g., "~20–25%")
    match = re.search(r'(\d+)-?(\d+)?%', value_str)
    if match:
        lower_bound = int(match.group(1))
        upper_bound = int(match.group(2)) if match.group(2) else lower_bound
        avg_value = (lower_bound + upper_bound) / 2
    else:
        avg_value = 22.5 # Default if parsing fails

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = avg_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "R&D Expenditure (% of Revenue)"},
        gauge = {'axis': {'range': [None, 50], 'ticksuffix': '%'},
                 'bar': {'color': "darkblue"},
                 'steps': [
                     {'range': [0, 15], 'color': "lightgray", 'name': 'Low'},
                     {'range': [15, 25], 'color': "gray", 'name': 'Moderate'},
                     {'range': [25, 50], 'color': "darkgray", 'name': 'High'}],
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': avg_value}}))
    return fig

# --- Main App Logic ---
def main():
    st.title("💊 AstraZeneca (AZN) Financial Ecosystem Deep Dive")
    st.markdown("A comprehensive analysis of AstraZeneca's financial landscape, market dependencies, and strategic positioning.")

    parsed_sections, ticker, global_intro, first_analysis_conclusion, final_conclusion = parse_analysis_text_into_sections(ANALYSIS_TEXT)

    st.sidebar.header("Navigation")
    section_titles = list(parsed_sections.keys())
    
    # Filter out empty or redundant sections (like those containing just '---' or specific internal notes)
    section_titles = [title for title in section_titles if title.strip() and not title.startswith('---') and not "if you want" in title.lower()]
    
    # Add conclusions explicitly to navigation if they were not part of the `sections` dict due to their extraction method
    if "Overall Conclusion" not in section_titles and final_conclusion:
         section_titles.append("Overall Conclusion")

    selected_section = st.sidebar.radio("Go to Section", section_titles)

    # Display Introduction
    st.header("📝 Introduction")
    st.markdown(global_intro)
    st.markdown(f"**Stock Ticker:** {ticker} (AstraZeneca PLC)")
    st.markdown("---")

    # Display Key Metrics
    st.header("📊 Key Financial Metrics Summary")
    key_metrics_df = extract_key_metrics(ANALYSIS_TEXT)
    if key_metrics_df is not None and not key_metrics_df.empty:
        st.dataframe(key_metrics_df, hide_index=True, use_container_width=True)
    else:
        st.info("No specific quantifiable metrics found in the text for direct extraction.")

    st.markdown("---")

    # --- Charts based on Text Descriptions (Mock Data) ---
    st.header("📈 Key Financial Visualizations (Conceptual)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Drivers")
        revenue_data = {
            'Therapeutic Area': ['Oncology', 'CVRM', 'Respiratory & Immunology', 'Rare Diseases', 'Vaccines & Immune Therapies', 'Other/Remaining'],
            'Revenue Share': [35, 20, 15, 15, 5, 10] # Based on ~35% for Oncology, others estimated. Vaccines declining.
        }
        st.plotly_chart(create_revenue_drivers_chart(revenue_data), use_container_width=True)

    with col2:
        st.subheader("Geographic Revenue Distribution")
        geographic_data = {
            'Region': ['U.S.', 'Europe', 'Emerging Markets', 'Other'],
            'Revenue Share': [45, 25, 20, 10] # Based on ~45% for U.S., others estimated
        }
        st.plotly_chart(create_geographic_revenue_chart(geographic_data), use_container_width=True)
    
    st.subheader("R&D Investment Level")
    # Get R&D value from extracted metrics for the gauge
    rd_exp_val = "22.5% of revenue" # Default
    if key_metrics_df is not None:
        rd_metric = key_metrics_df[key_metrics_df['Metric'] == 'R&D Expenditure']
        if not rd_metric.empty:
            rd_exp_val = rd_metric['Value'].iloc[0]

    st.plotly_chart(create_rd_expenditure_gauge(rd_exp_val), use_container_width=True)
    st.markdown("---")


    # Display the detailed sections
    st.header("Detailed Analysis Sections")
    for title in section_titles:
        # Skip the intro and conclusions as they are displayed separately
        if "Introduction" in title or "Conclusion" in title:
            continue
        
        content = parsed_sections.get(title, "Content not found for this section.")

        with st.expander(f"**{title}**"):
            st.markdown(content)
            
            # Add specific visualizations for certain sections if appropriate
            if "Competitor" in title:
                st.subheader("Key Competitors by Therapeutic Area")
                # Extract competitors and categories
                competitor_regex = r'\*\*(.*?):\*\*(.*?)(?=\*\*(?:Oncology|Cardiovascular, Renal & Metabolism|Respiratory & Immunology|Emerging Players)|$)'
                competitor_matches = re.findall(competitor_regex, content, re.DOTALL | re.IGNORECASE)

                competitor_data = []
                for area, competitors_str in competitor_matches:
                    competitors_list = [c.strip() for c in competitors_str.split('\n') if c.strip() and not c.strip().startswith('-')]
                    for comp in competitors_list:
                        if comp.startswith('-'):
                            comp = comp[1:].strip()
                        competitor_data.append({"Therapeutic Area": area.strip(), "Competitor": comp.split(':')[0].strip()})
                
                if competitor_data:
                    df_comp = pd.DataFrame(competitor_data)
                    st.dataframe(df_comp, hide_index=True, use_container_width=True)
                else:
                    st.info("No structured competitor data found for visualization.")
            
            if "Key Strengths & Risks" in title or "Key risks" in title:
                st.subheader("Strengths and Risks Summary")
                
                col_s, col_r = st.columns(2)
                
                strengths_match = re.search(r'\*\*Strengths:\*\*(.*?)(?=\*\*Risks:\*\*|$)', content, re.DOTALL)
                if strengths_match:
                    strengths_list = [s.strip() for s in strengths_match.group(1).split('\n*') if s.strip()]
                    with col_s:
                        st.success("✅ **Strengths**")
                        for s in strengths_list:
                            st.markdown(f"- {s.replace('*', '').strip()}")
                
                risks_match = re.search(r'\*\*Risks:\*\*(.*)', content, re.DOTALL)
                if risks_match:
                    risks_list = [r.strip() for r in risks_match.group(1).split('\n*') if r.strip()]
                    with col_r:
                        st.warning("⚠️ **Risks**")
                        for r in risks_list:
                            st.markdown(f"- {r.replace('*', '').strip()}")

    st.markdown("---")

    # Final Conclusion
    st.header("🏁 Overall Conclusion")
    # Display the main conclusion first, then the specific one if it's different.
    if final_conclusion:
        st.markdown(final_conclusion)
        if first_analysis_conclusion and first_analysis_conclusion != final_conclusion:
            st.markdown("---")
            st.subheader("Additional Concluding Thoughts")
            st.markdown(first_analysis_conclusion)
    elif first_analysis_conclusion:
        st.markdown(first_analysis_conclusion)
    else:
        st.info("No specific overall conclusion section found.")
    
    st.info("Note: All charts are conceptual and based on estimates/descriptions from the provided text, not real-time financial data.")


if __name__ == "__main__":
    main()