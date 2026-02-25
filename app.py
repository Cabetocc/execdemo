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
import plotly.express as px
import re

# --- App Configuration ---
st.set_page_config(page_title="AstraZeneca (AZN) Financial Ecosystem Analysis", layout="wide")

# --- Helper Functions ---
def extract_key_metrics(text):
    """Extracts key financial metrics using regex, if present."""
    metrics = {}
    # Example: Search for "Gross Profit Margin: ~80%" or "R&D Investment: ~20-25% of revenue"
    # This is a basic example, more sophisticated NLP could be used for broader extraction
    patterns = {
        "Gross Margin": r"Gross Margin:.*?([\d\.\%]+)",
        "R&D Investment": r"R&D Investment:.*?([\d\.\%\s]+)",
        "Revenue Concentration": r"Revenue concentration.*?([\w\s]+$)",
        "Operating Cash Flow": r"Strong Operating Cash Flow",
        "Dividend Policy": r"Dividend Policy:.*?([\w\s]+)",
        "M&A Activity": r"M&A Activity:.*?([\w\s]+)",
        "Alexion Acquisition": r"Alexion Acquisition:.*?([\w\s]+)$",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            value = match.group(1).strip()
            # Clean up common extractions
            if "of revenue" in value:
                value = value.replace("of revenue", "").strip()
            if "%" in value and not value.startswith("%"):
                value = value.replace("%", "").strip()
            metrics[key] = value
    return metrics

def create_section_header(title):
    """Creates a formatted section header."""
    st.header(title)
    st.markdown("---")

def add_chart(data, x_col, y_col, title, chart_type="bar"):
    """Adds a Plotly chart to the Streamlit app."""
    if data is None or data.empty:
        st.warning(f"No data available to create '{title}' chart.")
        return

    try:
        if chart_type == "bar":
            fig = px.bar(data, x=x_col, y=y_col, title=title, labels={x_col: x_col, y_col: y_col})
        elif chart_type == "line":
            fig = px.line(data, x=x_col, y=y_col, title=title, markers=True, labels={x_col: x_col, y_col: y_col})
        elif chart_type == "pie":
            fig = px.pie(data, names=x_col, values=y_col, title=title)
        else:
            st.error(f"Unsupported chart type: {chart_type}")
            return

        fig.update_layout(
            title_x=0.5,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating chart '{title}': {e}")

# --- Main App Logic ---
def app():
    st.title("AstraZeneca (AZN) Financial Ecosystem Analysis")

    analysis_text = """
### **Comprehensive Financial Ecosystem Analysis: AstraZeneca PLC (AZN)**

AstraZeneca (AZN) is a global biopharmaceutical company headquartered in Cambridge, UK, with a primary listing on the London Stock Exchange and a secondary listing on NASDAQ. It focuses on the discovery, development, and commercialization of prescription medicines, primarily in oncology, cardiovascular, renal & metabolism (CVRM), respiratory & immunology, and rare diseases.

---

### **1. Key Financial Relationships & Metrics**

**Revenue Drivers:**
- **Blockbuster Drugs:** Key products like Tagrisso (oncology), Farxiga (diabetes/CVRM), and Imfinzi (oncology) drive a significant portion of revenue. Farxiga, for example, has shown robust growth due to expanded indications (heart failure, CKD).
- **Geographic Mix:** Strong presence in **Emerging Markets** (especially China) and the **US**, with Europe also contributing substantially. Currency fluctuations (USD/GBP/EUR) impact reported revenues.
- **COVID-19 Vaccine:** While Vaxzevria sales have declined, it previously provided a revenue boost and expanded the company’s global footprint.

**Profitability & Margins:**
- **Gross Margin:** Typically high (~80%) due to the proprietary nature of pharmaceuticals, but can be pressured by product mix, generics competition, and pricing negotiations.
- **R&D Investment:** AZN reinvests heavily in R&D (~20-25% of revenue) to fuel its pipeline, impacting short-term earnings but critical for long-term growth.
- **Operating Leverage:** As products scale, margins can expand, but ongoing investment in launches and pipeline limits near-term margin expansion.

**Cash Flow & Capital Allocation:**
- **Strong Operating Cash Flow:** Supports dividend payments, share buybacks, and business development.
- **Dividend Policy:** Known for a progressive dividend policy, appealing to income-focused investors.
- **M&A Activity:** Strategic acquisitions (e.g., Alexion in 2021 for $39B) enhance therapeutic reach (rare diseases) but increase leverage and integration complexity.

---

### **2. Market Dependencies & Risks**

**Regulatory Environment:**
- **FDA (US), EMA (EU), NMPA (China):** Drug approvals, label expansions, and safety monitoring are critical. Regulatory setbacks can significantly impact stock performance.
- **Pricing & Reimbursement:** Increasing pressure from governments and payers, especially in the US (Medicare drug price negotiation under the Inflation Reduction Act) and Europe, can affect pricing power.

**Patent Expirations:**
- **Key Patents:** Loss of exclusivity (LOE) for major drugs (e.g., Nexium, Crestor in past years) leads to generic competition and revenue erosion. Ongoing pipeline innovation is essential to offset this.

**Clinical Trial Outcomes:**
- **Pipeline Success/Failure:** Positive Phase III data (e.g., recent successes in oncology) can drive stock upside, while failures lead to sharp declines. The market closely monitors trial readouts.

---

### **3. Sector Connections & Competitor Relationships**

**Therapeutic Area Competition:**
- **Oncology:** Competes with **Merck (MRK)** (Keytruda), **Bristol-Myers Squibb (BMY)** (Opdivo), **Roche (RHHBY)**, and **Pfizer (PFE)**. AZN’s focus on targeted therapies (e.g., Tagrisso for EGFR-mutated NSCLC) creates both competition and collaboration opportunities.
- **CVRM & Diabetes:** Faces **Novo Nordisk (NVO)** and **Eli Lilly (LLY)** in diabetes/Obesity, and **Novartis (NVS)** in cardiovascular. Farxiga competes with Jardiance (Boehringer Ingelheim/Eli Lilly) in heart failure/CKD.
- **Respiratory:** Competes with **GSK** and **Sanofi** in asthma/COPD.
- **Rare Diseases (post-Alexion):** Competes with **Roche, Takeda, and Biogen** in complement-mediated diseases.

**Collaborations & Partnerships:**
- **Daiichi Sankyo:** Landmark partnership for Enhertu (HER2-targeting ADC) in oncology, with significant revenue-sharing.
- **Oxford University:** COVID-19 vaccine collaboration.
- **Small Biotech Alliances:** Frequent partnerships to access innovative early-stage assets (e.g., with Ionis Pharmaceuticals in CVRM).

---

### **4. Economic & Macroeconomic Factors**

**Global Economic Health:**
- **Recession Resilience:** Pharmaceuticals are generally defensive, but economic downturns can pressure healthcare budgets and affect drug pricing/access.
- **Inflation:** Impacts manufacturing costs, R&D expenses, and supply chain logistics. AZN’s pricing power can partially offset this.

**Currency Exchange Rates:**
- As a UK-domiciled company reporting in USD, **GBP/USD fluctuations** significantly impact translated revenues and earnings. A weaker GBP boosts reported results from international sales.

**Interest Rates:**
- Higher rates increase the cost of debt, affecting AZN’s financing costs for M&A and capital projects. They also impact valuation multiples for growth stocks, including biopharma.

**Geopolitical Factors:**
- **US-China Tensions:** AZN’s significant sales in China (~13% of revenue) could be affected by trade policies or IP disputes.
- **Brexit:** Ongoing regulatory divergence between the UK and EU may create operational complexities.

---

### **5. ESG & Societal Factors**

**Environmental:** Focus on reducing carbon footprint and sustainable manufacturing.
**Social:** Drug pricing ethics, access to medicines in low-income countries, and diversity in clinical trials.
**Governance:** Strong board oversight, but executive compensation and M&A decisions (like Alexion’s premium) are scrutinized.

---

### **6. Stock Performance Drivers**

- **Earnings Reports:** Quarterly revenue/earnings beats or misses, especially guidance updates.
- **Pipeline Milestones:** Clinical trial results, regulatory submissions, and approvals.
- **M&A Rumors/Deals:** Speculation or announcements of acquisitions.
- **Macro Sentiment:** Sector rotation (into/out of healthcare), interest rate expectations, and currency moves.

---

### **Conclusion**

AstraZeneca operates in a complex ecosystem where **innovation (R&D productivity), regulatory navigation, and competitive dynamics** are paramount. Its transition to a biopharma leader with a robust oncology and CVRM portfolio, supplemented by strategic M&A (Alexion), positions it for growth, but not without risks. Investors must monitor:
1. **Pipeline execution** and clinical trial outcomes.
2. **Pricing pressures** from US and international payers.
3. **Currency and macroeconomic headwinds**.
4. **Competitive threats** in key therapeutic areas.

AZN’s defensive qualities (dividend, essential medicines) provide stability, while its growth pipeline offers upside, making it a **core holding in global healthcare portfolios**, albeit with sector-specific volatility.
"""

    st.markdown(analysis_text)

    # --- Extract and Display Key Metrics ---
    st.sidebar.title("Key Metrics Extracted")
    extracted_metrics = extract_key_metrics(analysis_text)

    if extracted_metrics:
        for key, value in extracted_metrics.items():
            st.sidebar.metric(label=key, value=value)
    else:
        st.sidebar.warning("No specific financial metrics automatically extracted.")

    # --- Visualizations ---
    st.header("Visualizations")
    st.markdown("Visualizing key aspects of AstraZeneca's financial ecosystem.")

    # Example DataFrames (replace with actual data if available)
    # Data for illustrative purposes, based on analysis text context
    revenue_drivers_data = pd.DataFrame({
        'Therapeutic Area': ['Oncology', 'CVRM', 'Rare Diseases (Alexion)', 'Respiratory', 'Vaccines'],
        'Approximate % of Revenue (Illustrative)': [40, 30, 15, 10, 5] # Hypothetical percentages
    })

    competitor_focus_data = pd.DataFrame({
        'Competitor': ['Merck (MRK)', 'Bristol-Myers Squibb (BMY)', 'Roche (RHHBY)', 'Pfizer (PFE)', 'Novo Nordisk (NVO)', 'Eli Lilly (LLY)'],
        'Therapeutic Area Focus': ['Oncology', 'Oncology', 'Oncology/Diagnostics', 'Oncology/Vaccines', 'Diabetes/Obesity', 'Diabetes/Obesity/CNS'],
        'Competition Type': ['Head-to-Head (Oncology)', 'Head-to-Head (Oncology)', 'Head-to-Head (Oncology)', 'Head-to-Head (Oncology)', 'Head-to-Head (CVRM)', 'Head-to-Head (CVRM)']
    })

    market_dependency_data = pd.DataFrame({
        'Market': ['US', 'Emerging Markets', 'Europe', 'China'],
        'Importance': ['High', 'High', 'Medium', 'High'],
        'Revenue Share (Illustrative)': [40, 25, 20, 15] # Hypothetical percentages
    })

    economic_factors_data = pd.DataFrame({
        'Economic Factor': ['Global Economic Health', 'Inflation', 'Currency Exchange Rates', 'Interest Rates', 'Geopolitical Stability'],
        'Impact on AZN': ['Defensive but budget pressure', 'Increases costs, potential price pass-through', 'Translation gains/losses', 'Higher financing costs, valuation impact', 'Supply chain & market access risks']
    })

    # Chart 1: Revenue Drivers by Therapeutic Area
    if not revenue_drivers_data.empty:
        add_chart(revenue_drivers_data, x_col='Therapeutic Area', y_col='Approximate % of Revenue (Illustrative)', title="Illustrative Revenue Drivers by Therapeutic Area", chart_type="pie")

    # Chart 2: Key Competitors and their Focus
    if not competitor_focus_data.empty:
        add_chart(competitor_focus_data, x_col='Competitor', y_col='Therapeutic Area Focus', title="Illustrative Key Competitor Focus Areas", chart_type="bar") # Can be adapted for more detail

    # Chart 3: Market Dependencies
    if not market_dependency_data.empty:
        add_chart(market_dependency_data, x_col='Market', y_col='Revenue Share (Illustrative)', title="Illustrative Geographic Revenue Share", chart_type="bar")

    # Chart 4: Economic Factors Impact
    if not economic_factors_data.empty:
        # Creating a simple visual for economic factors, as direct plotting might be complex
        st.subheader("Impact of Economic Factors")
        for index, row in economic_factors_data.iterrows():
            st.markdown(f"- **{row['Economic Factor']}**: {row['Impact on AZN']}")


    st.header("Detailed Sections")

    # Section 1: Key Financial Relationships & Metrics
    create_section_header("1. Key Financial Relationships & Metrics")
    st.markdown("""
    **Revenue Drivers:**
    - **Blockbuster Drugs:** Key products like Tagrisso (oncology), Farxiga (diabetes/CVRM), and Imfinzi (oncology) drive a significant portion of revenue. Farxiga, for example, has shown robust growth due to expanded indications (heart failure, CKD).
    - **Geographic Mix:** Strong presence in **Emerging Markets** (especially China) and the **US**, with Europe also contributing substantially. Currency fluctuations (USD/GBP/EUR) impact reported revenues.
    - **COVID-19 Vaccine:** While Vaxzevria sales have declined, it previously provided a revenue boost and expanded the company’s global footprint.

    **Profitability & Margins:**
    - **Gross Margin:** Typically high (~80%) due to the proprietary nature of pharmaceuticals, but can be pressured by product mix, generics competition, and pricing negotiations.
    - **R&D Investment:** AZN reinvests heavily in R&D (~20-25% of revenue) to fuel its pipeline, impacting short-term earnings but critical for long-term growth.
    - **Operating Leverage:** As products scale, margins can expand, but ongoing investment in launches and pipeline limits near-term margin expansion.

    **Cash Flow & Capital Allocation:**
    - **Strong Operating Cash Flow:** Supports dividend payments, share buybacks, and business development.
    - **Dividend Policy:** Known for a progressive dividend policy, appealing to income-focused investors.
    - **M&A Activity:** Strategic acquisitions (e.g., Alexion in 2021 for $39B) enhance therapeutic reach (rare diseases) but increase leverage and integration complexity.
    """)

    # Section 2: Market Dependencies & Risks
    create_section_header("2. Market Dependencies & Risks")
    st.markdown("""
    **Regulatory Environment:**
    - **FDA (US), EMA (EU), NMPA (China):** Drug approvals, label expansions, and safety monitoring are critical. Regulatory setbacks can significantly impact stock performance.
    - **Pricing & Reimbursement:** Increasing pressure from governments and payers, especially in the US (Medicare drug price negotiation under the Inflation Reduction Act) and Europe, can affect pricing power.

    **Patent Expirations:**
    - **Key Patents:** Loss of exclusivity (LOE) for major drugs (e.g., Nexium, Crestor in past years) leads to generic competition and revenue erosion. Ongoing pipeline innovation is essential to offset this.

    **Clinical Trial Outcomes:**
    - **Pipeline Success/Failure:** Positive Phase III data (e.g., recent successes in oncology) can drive stock upside, while failures lead to sharp declines. The market closely monitors trial readouts.
    """)

    # Section 3: Sector Connections & Competitor Relationships
    create_section_header("3. Sector Connections & Competitor Relationships")
    st.markdown("""
    **Therapeutic Area Competition:**
    - **Oncology:** Competes with **Merck (MRK)** (Keytruda), **Bristol-Myers Squibb (BMY)** (Opdivo), **Roche (RHHBY)**, and **Pfizer (PFE)**. AZN’s focus on targeted therapies (e.g., Tagrisso for EGFR-mutated NSCLC) creates both competition and collaboration opportunities.
    - **CVRM & Diabetes:** Faces **Novo Nordisk (NVO)** and **Eli Lilly (LLY)** in diabetes/Obesity, and **Novartis (NVS)** in cardiovascular. Farxiga competes with Jardiance (Boehringer Ingelheim/Eli Lilly) in heart failure/CKD.
    - **Respiratory:** Competes with **GSK** and **Sanofi** in asthma/COPD.
    - **Rare Diseases (post-Alexion):** Competes with **Roche, Takeda, and Biogen** in complement-mediated diseases.

    **Collaborations & Partnerships:**
    - **Daiichi Sankyo:** Landmark partnership for Enhertu (HER2-targeting ADC) in oncology, with significant revenue-sharing.
    - **Oxford University:** COVID-19 vaccine collaboration.
    - **Small Biotech Alliances:** Frequent partnerships to access innovative early-stage assets (e.g., with Ionis Pharmaceuticals in CVRM).
    """)

    # Section 4: Economic & Macroeconomic Factors
    create_section_header("4. Economic & Macroeconomic Factors")
    st.markdown("""
    **Global Economic Health:**
    - **Recession Resilience:** Pharmaceuticals are generally defensive, but economic downturns can pressure healthcare budgets and affect drug pricing/access.
    - **Inflation:** Impacts manufacturing costs, R&D expenses, and supply chain logistics. AZN’s pricing power can partially offset this.

    **Currency Exchange Rates:**
    - As a UK-domiciled company reporting in USD, **GBP/USD fluctuations** significantly impact translated revenues and earnings. A weaker GBP boosts reported results from international sales.

    **Interest Rates:**
    - Higher rates increase the cost of debt, affecting AZN’s financing costs for M&A and capital projects. They also impact valuation multiples for growth stocks, including biopharma.

    **Geopolitical Factors:**
    - **US-China Tensions:** AZN’s significant sales in China (~13% of revenue) could be affected by trade policies or IP disputes.
    - **Brexit:** Ongoing regulatory divergence between the UK and EU may create operational complexities.
    """)

    # Section 5: ESG & Societal Factors
    create_section_header("5. ESG & Societal Factors")
    st.markdown("""
    **Environmental:** Focus on reducing carbon footprint and sustainable manufacturing.
    **Social:** Drug pricing ethics, access to medicines in low-income countries, and diversity in clinical trials.
    **Governance:** Strong board oversight, but executive compensation and M&A decisions (like Alexion’s premium) are scrutinized.
    """)

    # Section 6: Stock Performance Drivers
    create_section_header("6. Stock Performance Drivers")
    st.markdown("""
    - **Earnings Reports:** Quarterly revenue/earnings beats or misses, especially guidance updates.
    - **Pipeline Milestones:** Clinical trial results, regulatory submissions, and approvals.
    - **M&A Rumors/Deals:** Speculation or announcements of acquisitions.
    - **Macro Sentiment:** Sector rotation (into/out of healthcare), interest rate expectations, and currency moves.
    """)

    st.header("Conclusion")
    st.markdown("""
    AstraZeneca operates in a complex ecosystem where **innovation (R&D productivity), regulatory navigation, and competitive dynamics** are paramount. Its transition to a biopharma leader with a robust oncology and CVRM portfolio, supplemented by strategic M&A (Alexion), positions it for growth, but not without risks. Investors must monitor:
    1. **Pipeline execution** and clinical trial outcomes.
    2. **Pricing pressures** from US and international payers.
    3. **Currency and macroeconomic headwinds**.
    4. **Competitive threats** in key therapeutic areas.

    AZN’s defensive qualities (dividend, essential medicines) provide stability, while its growth pipeline offers upside, making it a **core holding in global healthcare portfolios**, albeit with sector-specific volatility.
    """)

if __name__ == "__main__":
    app()