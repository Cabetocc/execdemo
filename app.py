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
import re

# Set Streamlit page configuration for a wider layout and custom title/icon
st.set_page_config(layout="wide", page_title="Nokia (NOK) Financial Ecosystem Analysis", page_icon="📈")

# --- Raw Financial Analysis Text ---
# This variable holds the entire financial analysis provided by the user.
# It is embedded directly into the app for completeness and easy execution.
ANALYSIS_TEXT = """
Let's dive into a comprehensive financial ecosystem analysis of Nokia (NOK). As a global leader in network infrastructure and technology, Nokia operates within a dynamic and interconnected landscape.

## Nokia (NOK): A Financial Ecosystem Analysis

Nokia's stock (NOK) is influenced by a complex web of financial relationships, market dependencies, sector connections, competitor dynamics, and broader economic factors. Here's a breakdown:

### 1. Key Financial Relationships and Metrics
*   **Revenue Streams:** Nokia's revenue is primarily derived from:
    *   **Network Infrastructure:** This is their core business, encompassing mobile networks (5G, 4G), fixed networks, and IP networks. Sales here are project-based and often involve long-term contracts with telecom operators.
    *   **Nokia Technologies:** This segment includes their patent licensing business, which is a significant and relatively high-margin revenue source.
    *   **Nokia Enterprise:** This segment focuses on providing network solutions to non-telecom enterprises, such as industrial IoT, smart cities, and government sectors.
*   **Profitability & Margins:**
    *   **Gross Margins:** Driven by R&D intensity and competitive pricing in the network infrastructure segment. Patent licensing (Nokia Technologies) generally offers higher gross margins.
    *   **Operating Margins:** Sensitive to R&D spending, sales, general, and administrative expenses, and the overall demand for network equipment.
    *   **Net Income:** Influenced by operating performance, interest expenses, and taxes.
*   **Capital Structure:**
    *   **Debt:** Nokia maintains a certain level of debt to finance its operations, R&D, and potential acquisitions. Its ability to manage debt is crucial for financial stability.
    *   **Equity:** The market capitalization of NOK reflects investor sentiment and the company's perceived future earnings potential.
*   **Cash Flow:**
    *   **Operating Cash Flow:** Essential for funding R&D, capital expenditures, and debt repayment. It can be lumpy due to project-based revenue.
    *   **Free Cash Flow:** Indicates the cash available after capital expenditures, a key metric for evaluating financial health and shareholder returns.
*   **R&D Investment:** Nokia invests heavily in research and development to stay competitive in the fast-evolving technology sector, especially with 5G and future network generations. This is a significant cost but crucial for long-term survival and growth.
*   **Dividend Policy:** While Nokia has paid dividends in the past, its current policy is subject to its financial performance and strategic priorities. Investors closely watch for dividend announcements.

### 2. Market Dependencies
*   **Telecommunications Operator Spending:** Nokia's primary customers are mobile and fixed network operators worldwide. Their capital expenditure (CapEx) budgets, driven by network upgrades (e.g., 5G rollout, fiber expansion), technology evolution, and customer demand, directly impact Nokia's sales.
*   **Global Economic Growth & Consumer Demand:** Indirectly, economic growth fuels consumer demand for mobile data and services, which in turn drives telecom operators' need for network expansion and upgrades.
*   **Government Policies & Regulations:** Spectrum allocation, net neutrality rules, and national security concerns can influence telecom operator spending patterns and the types of vendors they can use.
*   **Technology Adoption Rates:** The speed at which new technologies like 5G, IoT, and AI are adopted by consumers and enterprises dictates the demand for Nokia's solutions.
*   **Supply Chain Stability:** Like all hardware manufacturers, Nokia is dependent on the stability and availability of components from its suppliers. Geopolitical events and trade disputes can disrupt this.

### 3. Sector Connections
*   **Telecommunications Equipment Sector:** Nokia is a direct player in this sector. Its performance is intertwined with the overall health and trends of this industry.
*   **Semiconductor Sector:** Nokia relies on advanced chips and components from semiconductor manufacturers. Disruptions or price changes in this sector can impact Nokia's costs and product availability.
*   **Software & Services Sector:** As networks become more software-defined, Nokia's integration of software and services with its hardware offerings is crucial. Its success depends on its ability to deliver robust software solutions.
*   **Cloud Computing Sector:** The convergence of telecom networks and cloud infrastructure presents both opportunities and dependencies for Nokia as it integrates its solutions with cloud platforms.
*   **Cybersecurity Sector:** Network security is paramount. Nokia's solutions must be secure, and the company may also partner with or acquire cybersecurity firms to enhance its offerings.

### 4. Competitor Relationships

Nokia operates in a highly competitive landscape. Its key competitors include:

*   **Ericsson (ERIC):** A direct and major competitor, especially in mobile network infrastructure. They vie for the same large operator contracts.
*   **Huawei (Private):** Despite geopolitical challenges, Huawei remains a significant competitor, particularly in emerging markets.
*   **Samsung (005930.KS):** Increasingly a strong player in mobile network equipment, particularly with its 5G solutions.
*   **Cisco Systems (CSCO):** A dominant player in enterprise networking and IP routing, areas where Nokia also competes.
*   **Juniper Networks (JNPR):** Another key competitor in routing and switching.
*   **ZTE (0763.HK):** A Chinese competitor that also competes for global network contracts.

The competitive dynamics are characterized by:
*   **Price Wars:** Intense competition can lead to pricing pressure, impacting margins.
*   **Technological Innovation:** Companies constantly race to develop and deploy the next generation of network technology.
*   **Geopolitical Influence:** Government policies and trade restrictions can significantly impact market access and competitive positioning (especially for Huawei).
*   **Acquisition/Partnership Activity:** Companies may merge, acquire others, or form strategic alliances to gain market share or technological advantages.

### 5. Economic Factors
*   **Global Interest Rates:** Higher interest rates increase Nokia's cost of borrowing and can also impact the CapEx budgets of telecom operators if they have to borrow more for their investments.
*   **Inflation:** Can increase Nokia's raw material costs, labor expenses, and potentially affect its pricing power.
*   **Foreign Exchange Rates:** As a global company, Nokia's reported earnings are subject to fluctuations in currency exchange rates.
*   **Geopolitical Stability:** Conflicts, trade wars, and political instability can disrupt supply chains, impact international sales, and lead to shifts in government spending on critical infrastructure.
*   **Technological Disruption:** Emergence of new communication paradigms or significant breakthroughs in areas like quantum computing could alter the long-term demand for current network infrastructure.
*   **Economic Recessions:** During economic downturns, telecom operators may scale back their CapEx spending, directly impacting Nokia's revenue.

### Conclusion: Nokia's Financial Ecosystem

Nokia's financial health is intricately linked to the global telecommunications industry's investment cycles, driven by the relentless demand for faster, more reliable, and ubiquitous connectivity. Its success hinges on its ability to innovate rapidly, manage its extensive supply chain, navigate complex geopolitical landscapes, and secure long-term contracts with major telecom operators. The patent licensing arm provides a valuable, more stable revenue stream, while the enterprise segment offers diversification.

Investors in NOK should closely monitor:

*   **Telecom operator CapEx trends.**
*   **The pace of 5G and future network deployments.**
*   **Nokia's R&D pipeline and technological leadership.**
*   **Competitive pressures and pricing dynamics.**
*   **Geopolitical developments impacting global trade and infrastructure security.**
*   **The performance of its Nokia Technologies segment.**

By understanding these interconnected elements, one can gain a more holistic view of Nokia's financial ecosystem and its potential future trajectory.

---

Below is a structured, comprehensive analysis of NOK (Nokia Corporation) and the financial ecosystem that determines its performance. I cover Nokia’s business model and revenue drivers, key financial relationships and sensitivities, market and sector linkages, principal competitors, macro and geopolitical factors, principal risks and catalysts, and the financial/operational metrics investors should monitor.

1) Business model and revenue mix (high level)
- Core activities: telecommunications network equipment (RAN, core networks), optical and fixed networks, software and cloud infrastructure for operators, services (integration/managed services), and technology licensing (Nokia Technologies / patents).
- Revenue characteristics: mix of multi‑year equipment contracts (lumpy, high ticket), recurring software/subscription and services revenue (higher margin and more predictable), and licensing/royalty income (variable but high-margin).
- Segment margin profile: hardware/equipment (RAN, optical) typically lower margin and capital-intensive; software, services and licensing generally higher margin and steadier cash flow.

2) Key financial relationships and sensitivities
- Telco capex cycles: Nokia revenue and order flow are strongly correlated with global carrier CAPEX for 4G/5G rollouts, upgrades (NSA → SA), fiber/backhaul and core replacements. A slowdown in carrier spending directly hits orders and near-term revenue.
- Large customers concentration: a handful of major carriers (global Tier‑1 operators) account for a meaningful share of orders; wins/losses or contract timing with several large customers can materially impact quarterly results.
- Backlog and book‑to‑bill: order backlog gives visibility; book‑to‑to-bill is a critical indicator of demand momentum.
- Supply chain inputs: dependence on semiconductor and optical components. Chip shortages, single‑source supplier issues, or lead‑time spikes affect delivery timing and costs.
- Currency exposure: revenues and costs denominated across euros, dollars, other currencies — FX movements affect reported sales and margins.
- Working capital and cash conversion: large contracts drive receivables and inventory swings; management of working capital impacts free cash flow.
- Debt and interest rates: Nokia’s financing costs and valuation are sensitive to interest rates and credit market conditions (affects net interest expense and debt refinancing).

3) Market and sector connections
- Telecom equipment sector: Nokia sits in the global telecom infrastructure market alongside Ericsson, Huawei, Samsung, ZTE, etc. Trends in 5G deployment, private networks, Open RAN, and fiber/higher‑speed optical networks directly affect Nokia.
- Optical and IP transport: strong link to data growth and operators upgrading backbone capacity — competitors in this vertical include Ciena, Infinera, Cisco, Fujitsu.
- Cloud and edge ecosystems: partnerships with hyperscalers and cloud providers for network cloudification, MEC (multi‑access edge computing), vRAN deployments; demand for cloud-native software and orchestration platforms ties Nokia to cloud ecosystem trends.
- Enterprise/industrial IoT: private 5G, Industry 4.0, smart factories, and critical infrastructure projects create growth opportunities outside traditional carrier customers.
- Semiconductor industry: advances in RF front‑ends, ASICs, FPGAs and system on chips influence product roadmaps and costs. Supply tightness or new chip offerings can be limiting or enabling.

4) Principal competitors and how they shape Nokia’s market
- Ericsson: closest direct competitor in RAN and core networks in many regions — price competition and feature parity battles. Ericsson’s contract wins/losses and pricing strategy heavily influence Nokia.
- Huawei: largest global market share in many regions; subject to bans and restrictions in several Western markets. Where Huawei is restricted, Nokia benefits; where Huawei competes freely, price and volume pressure intensify.
- Samsung: competitor in RAN and 5G in some markets; strong where it has operator relationships and price advantage.
- Ciena / Infinera / Cisco / Fujitsu: main rivals in optical transport and IP routing for backhaul/core networks.
- Smaller/adjacent: Juniper, Ribbon, NEC, ZTE (regionally), and emerging Open RAN specialists (Mavenir, Altiostar, Parallel Wireless) which can disrupt traditional RAN supply chains.

5) Geopolitical and regulatory factors
- Security/sovereignty policies: bans or restrictions on Huawei/ZTE in the US, parts of Europe, Australia and elsewhere create openings for Nokia (and Ericsson). Conversely, relaxation of bans or Huawei regaining ground would be negative.
- Export controls and sanctions: Russia, China policies, export licensing for sensitive telecom tech can affect market access and revenue.
- Government subsidies and industrial policy: EU digital sovereignty programs, US CHIPS/Infrastructure funding, and national 5G subsidies can accelerate deals and shift competitive dynamics.
- Trade tensions and tariffs: affect supply chains, component sourcing costs, and local footprint decisions.

6) Economic and macro drivers
- Global GDP and telecom operator revenue growth: operator profitability and ARPU influence their ability to invest in networks.
- Inflation and input costs: higher materials/transport costs compress margins if not passed to customers.
- Interest rates: influence cost of debt and the discount rate investors use to value future cash flows.
- Capex cycles: replacement cycles for RAN and fiber infrastructure drive multi-year waves of spending.

7) Strategic/technology trends that are tailwinds or headwinds
- Tailwinds:
  - Continued 5G deployments and migration to standalone 5G (SA).
  - Fiberization and optical upgrades driven by data traffic growth.
  - Open RAN adoption — if Nokia can lead or adapt, opportunity to win modular contracts; but Open RAN also enables new competitors, creating mixed impact.
  - Private 5G and enterprise deployments.
  - Growth of cloud-native network functions and software subscriptions.
  - Regulatory restrictions on Chinese vendors benefiting Nokia in certain markets.
- Headwinds:
  - Aggressive price competition and margin erosion (especially if Huawei competes).
  - Slow carrier CAPEX in a macro slowdown.
  - Delays in contract awards or multiyear project postponements.
  - Supply chain disruptions and component cost inflation.
  - Rapid tech shifts that favor nimbler, software-first competitors.

8) Financial metrics and KPIs to monitor (what investors should watch)
- Order intake and backlog (bookings, book-to-bill): forward revenue visibility.
- Revenue by segment and geography: RAN vs. optical vs. software/services vs. licensing; exposure to key markets (North America, Europe, APAC).
- Gross margin and operating margin trends: product mix and pricing pressure effects.
- Free cash flow and cash conversion: working capital swings from large projects.
- Net debt / leverage metrics and interest expense: balance sheet strength.
- R&D as % of sales: investment level required to maintain competitive position.
- Licensing revenues and unusually large one-off settlements or disputes.
- Major contract awards / customer wins and timing of deliveries.
- Management guidance and changes to long-range targets.

9) Key risks
- Competitive pricing undercutting margins.
- Failure to win or execute large contracts.
- Concentration risk from a few large customers.
- Geopolitical exclusions or sanctions that close markets or complicate supply chains.
- Patent litigation or unfavorable licensing rulings.
- Technology disruption from Open RAN or non‑traditional vendors that reduce incumbents’ share.

10) Valuation and investment catalysts (how value could be realized)
- Catalysts that could re-rate the stock:
  - Consistent growth in software and services revenue (higher margin recurring revenue).
  - Significant contract wins with Tier‑1 carriers (especially in North America and Europe).
  - Positive impacts from government subsidy programs or exclusion of Huawei in new countries.
  - Improving free cash flow and deleveraging the balance sheet.
  - Successful commercialization of new products (cloud-native core, vRAN, optical platforms).
- Bear case scenario drivers:
  - Prolonged CAPEX weakness, significant market share loss, sustained margin compression, or costly patent/legal outcomes.

11) Practical monitoring checklist for ongoing tracking
- Quarterly earnings: watch order intake, backlog, guidance, segment margins.
- Press releases: large contract awards, partnership announcements (hyperscalers, governments), and Open RAN activity.
- Competitor news: Ericsson/Huawei contract awards and pricing trends.
- Macro indicators: carrier CAPEX announcements, government funding programs, semiconductor supply developments.
- Regulatory actions: bans, security reviews, and sanctions that affect market access.

Summary
Nokia’s fortunes are driven by telecom carrier CAPEX cycles, market share wins/losses in 5G and optical, its ability to grow higher‑margin software and services, and geopolitical/regulatory shifts that reallocate market share among vendors. Key risks are pricing pressure, supply chain constraints, and lumpy contract timing; key opportunities are Open RAN (if monetized), fiber/optical upgrades, private 5G, and any regulatory moves that restrict Huawei. From a financial-investment standpoint, focus on order intake/book‑to‑bill, margin trajectory (especially software mix), free cash flow conversion, and management guidance around large contract execution.

If you want, I can:
- Pull the latest financial metrics (revenue, margins, debt, cash) and compare Nokia to Ericsson, Huawei (estimates), and Ciena; or
- Build bull/baseline/bear scenario projections for revenue and free cash flow over the next 3 years based on assumed market share and capex scenarios. Which would you prefer?

---

### **Comprehensive Financial Analysis: Nokia Corporation (NOK)**

#### **1. Company Overview**
Nokia Corporation (NOK) is a Finnish multinational telecommunications, information technology, and consumer electronics company. Historically known for mobile phones, Nokia has transformed into a **networking and telecommunications infrastructure leader**, focusing on 5G, cloud networking, and software-defined networks. It operates through four segments:  
- **Mobile Networks** (5G, radio access)  
- **Network Infrastructure** (fixed networks, IP routing)  
- **Cloud and Network Services** (core networks, cloud solutions)  
- **Nokia Technologies** (licensing, R&D).

---

#### **2. Key Financial Relationships**
- **Revenue Streams**: Heavily dependent on capital expenditure cycles of telecom operators (e.g., AT&T, Verizon, Vodafone). 5G rollout drives equipment sales.  
- **Profitability**: Margins are influenced by R&D spending (~14% of revenue) and competitive pricing in network hardware.  
- **Balance Sheet**: Strong liquidity (€8.9B cash & equivalents as of 2023), but carries debt (€5.6B). Dividend was reinstated in 2023 after a hiatus.  
- **Geographic Exposure**: ~30% revenue from North America, ~20% from Europe. Emerging markets (Asia, Africa) offer growth but higher volatility.

---

#### **3. Market Dependencies**
- **Telecom Capex Cycles**: NOK’s performance is tied to global telecom infrastructure spending. Economic slowdowns may delay 5G investments.  
- **Technology Adoption**: Demand for 5G standalone networks, edge computing, and fiber broadband directly impacts orders.  
- **Regulation**: Spectrum auctions, cybersecurity policies (e.g., EU regulations), and trade restrictions (e.g., China-West tensions) affect operations.  
- **Supply Chain**: Relies on semiconductors, optical components. Disruptions (e.g., chip shortages) can delay deliveries.

---

#### **4. Sector Connections & Competitor Relationships**
- **Primary Competitors**:  
  - **Ericsson (ERIC)**: Direct rival in radio access networks. Market share battles in 5G contracts (e.g., recent AT&T deal lost to ERIC).  
  - **Huawei**: Dominant in China and emerging markets; geopolitical pressures have opened opportunities in Western markets.  
  - **Cisco (CSCO)**: Competes in IP routing and enterprise networks.  
  - **Samsung**: Emerging in 5G infrastructure, especially in North America.  
- **Partnerships**: Collaborates with **Microsoft Azure**, **Amazon Web Services** for cloud solutions, and **Qualcomm** for chipset design.  
- **Customer Base**: Major telecom operators (e.g., T-Mobile, Deutsche Telekom) and enterprises adopting private 5G networks.

---

#### **5. Economic & Macro Factors**
- **Interest Rates**: High rates increase borrowing costs for telecom clients, potentially slowing capex. NOK’s debt servicing costs also rise.  
- **Inflation**: Increases component and logistics costs, squeezing margins if not passed to customers.  
- **Currency Fluctuations**: As a global company, NOK faces EUR/USD exchange rate risks (reported in EUR).  
- **Geopolitical Risks**: US-China tensions impact supply chains and market access (e.g., restrictions on Huawei benefit NOK but raise trade uncertainty).  
- **Sustainability Trends**: Demand for energy-efficient networks drives R&D in "green" telecom solutions.

---

#### **6. Stock Performance Drivers**
- **Catalysts**:  
  - Major 5G contract wins (especially with operators in India, US, Europe).  
  - Growth in high-margin software/services (e.g., SaaS offerings).  
  - Patent licensing revenue (Nokia’s portfolio includes over 20,000 patents).  
- **Risks**:  
  - Market share loss to Ericsson or Samsung.  
  - Slowdown in 5G adoption post-initial rollout.  
  - Integration challenges from acquisitions (e.g., Alcatel-Lucent).

---

#### **7. Valuation & Outlook**
- **Trading Metrics**: P/E ~7x (as of 2024), below sector average, reflecting market skepticism about growth sustainability.  
- **Dividend Yield**: ~3.5%, appealing to income investors.  
- **Growth Strategy**: Focus on expanding in enterprise networks, IoT, and cloud-native software.  
- **ESG Factors**: Strong ESG ratings due to circular economy initiatives and net-zero targets.

---

#### **8. Investment Considerations**
- **Bull Case**: Accelerated 5G/6G deployment, margin expansion in software, and geopolitical tailwinds from Huawei restrictions.  
- **Bear Case**: Intense price competition, capex cuts by telecoms in a recession, and failure to innovate in cloud networking.  
- **Monitoring Points**: Quarterly order book growth, patent litigation outcomes, and management’s margin guidance.

Nokia’s transformation from a handset maker to a B2B infrastructure player has stabilized its business, but it remains cyclical and competitive. Success hinges on executing its technology roadmap and capturing higher-margin software opportunities while navigating a complex geopolitical landscape.
"""

# Function to parse the analysis text into sections based on the latest, most structured analysis
def parse_analysis_text(text):
    sections = {}
    # Find the start of the last comprehensive analysis, which uses '####' for sections
    last_analysis_start_idx = text.rfind("### **Comprehensive Financial Analysis: Nokia Corporation (NOK)**")
    
    if last_analysis_start_idx != -1:
        text_to_parse = text[last_analysis_start_idx:]
    else:
        # Fallback if the specific header isn't found, try to parse the whole text
        text_to_parse = text

    # Regex to split by '#### N. Section Title' and capture title and content
    # It captures the title (Group 1) and content (Group 2) up to the next '####' or end of string
    pattern = r'#### (\d+\.\s*.*?)\n(.*?)(?=\n#### \d+\.|\Z)'
    matches = re.findall(pattern, text_to_parse, re.DOTALL)

    for title, content in matches:
        sections[title.strip()] = content.strip()
            
    # If no '####' sections found, try parsing the first analysis style ('### N. Section Title')
    if not sections:
        pattern = r'### (\d+\.\s*.*?)\n(.*?)(?=\n### \d+\.|\Z)'
        matches = re.findall(pattern, text, re.DOTALL)
        for title, content in matches:
            sections[title.strip()] = content.strip()
    
    # If still no sections, try the numbered list style ('N) Section Title')
    if not sections:
        pattern = r'\n(\d+\)\s*.*?)\n(.*?)(?=\n\d+\)|\Z)'
        matches = re.findall(pattern, text, re.DOTALL)
        for title, content in matches:
            sections[title.strip()] = content.strip()

    # As a last resort, if no clear sections are found, put the entire text into one section
    if not sections:
        sections["Full Analysis"] = text.strip()

    return sections

# Function to extract key numerical/factual metrics from the entire text
def extract_key_metrics(full_text):
    metrics = {
        "R&D Investment (% of Revenue)": "N/A",
        "Cash & Equivalents (2023)": "N/A",
        "Debt (2023)": "N/A",
        "P/E Ratio (2024)": "N/A",
        "Dividend Yield": "N/A",
        "Geographic Revenue (North America)": "N/A",
        "Geographic Revenue (Europe)": "N/A",
        "Patents Held": "N/A",
        "Dividend Policy": "N/A"
    }

    # R&D Investment (% of Revenue)
    rd_match = re.search(r'R&D spending \((~?\d+\%?) of revenue\)', full_text)
    if rd_match:
        metrics["R&D Investment (% of Revenue)"] = rd_match.group(1)
    else: # Fallback to another mention if first pattern fails
        rd_match = re.search(r'R&D Investment:.*?invests heavily.*?This is a significant cost', full_text, re.DOTALL)
        if rd_match:
            metrics["R&D Investment (% of Revenue)"] = "Heavy & Crucial"
        
    # Cash & Equivalents
    cash_match = re.search(r'Strong liquidity \(€([\d\.]+)B cash & equivalents as of (\d{4})\)', full_text)
    if cash_match:
        metrics["Cash & Equivalents (2023)"] = f"€{cash_match.group(1)} Billion (as of {cash_match.group(2)})"
    
    # Debt
    debt_match = re.search(r'carries debt \(€([\d\.]+)B\)', full_text)
    if debt_match:
        metrics["Debt (2023)"] = f"€{debt_match.group(1)} Billion"

    # P/E Ratio
    pe_match = re.search(r'P/E (~?\d+x) \(as of (\d{4})\)', full_text)
    if pe_match:
        metrics["P/E Ratio (2024)"] = f"{pe_match.group(1)} (as of {pe_match.group(2)})"

    # Dividend Yield
    div_yield_match = re.search(r'Dividend Yield: (~?\d+\.\d+\%)', full_text)
    if div_yield_match:
        metrics["Dividend Yield"] = div_yield_match.group(1)
        
    # Dividend Policy
    div_policy_match = re.search(r'Dividend was reinstated in (\d{4})', full_text)
    if div_policy_match:
        metrics["Dividend Policy"] = f"Reinstated {div_policy_match.group(1)}"
    else: # Fallback to general statement
        div_policy_match = re.search(r'While Nokia has paid dividends in the past, its current policy is subject to its financial performance and strategic priorities.', full_text)
        if div_policy_match and metrics["Dividend Policy"] == "N/A":
            metrics["Dividend Policy"] = "Subject to Performance"

    # Geographic Revenue (North America)
    na_rev_match = re.search(r'~?(\d+\%) revenue from North America', full_text)
    if na_rev_match:
        metrics["Geographic Revenue (North America)"] = na_rev_match.group(1)

    # Geographic Revenue (Europe)
    eu_rev_match = re.search(r'~?(\d+\%) from Europe', full_text)
    if eu_rev_match:
        metrics["Geographic Revenue (Europe)"] = eu_rev_match.group(1)

    # Patents Held
    patents_match = re.search(r'over ([\d,]+) patents', full_text)
    if patents_match:
        metrics["Patents Held"] = f"{patents_match.group(1)} Patents"
        
    return metrics


# --- Streamlit Application Layout ---

st.title("📈 Nokia (NOK) Financial Ecosystem Analysis")
st.markdown("A comprehensive breakdown of Nokia's financial landscape, market dynamics, and strategic outlook, based on the provided analysis text.")

# Parse the main analysis text and extract key metrics
parsed_sections = parse_analysis_text(ANALYSIS_TEXT)
key_metrics = extract_key_metrics(ANALYSIS_TEXT) # Pass full text for comprehensive metric extraction

# --- Key Metrics Section ---
st.header("📊 Key Metrics & Financial Snapshot")

# Define the order of metrics to display and their default values
metrics_display_order = [
    ("P/E Ratio (2024)", "N/A"),
    ("Dividend Yield", "N/A"),
    ("Dividend Policy", "N/A"),
    ("Cash & Equivalents (2023)", "N/A"),
    ("Debt (2023)", "N/A"),
    ("R&D Investment (% of Revenue)", "N/A"),
    ("Patents Held", "N/A"),
    ("Geographic Revenue (North America)", "N/A"),
    ("Geographic Revenue (Europe)", "N/A")
]

# Create columns for metric display
cols = st.columns(4) 

# Display metrics dynamically
for i, (label, default_value) in enumerate(metrics_display_order):
    col_idx = i % 4
    cols[col_idx].metric(label, key_metrics.get(label, default_value))
    
st.markdown("---") # Separator for visual clarity

# --- Tabs for Detailed Analysis Sections ---
# Define a preferred order for tabs for better readability
preferred_tab_order = [
    "1. Company Overview", 
    "2. Key Financial Relationships", 
    "3. Market Dependencies",
    "4. Sector Connections & Competitor Relationships", 
    "5. Economic & Macro Factors",
    "6. Stock Performance Drivers", 
    "7. Valuation & Outlook", 
    "8. Investment Considerations"
]

# Sort the parsed section titles according to the preferred order
sorted_tab_titles = [title for title in preferred_tab_order if title in parsed_sections]
# Add any remaining parsed sections that were not in the preferred order
for title in parsed_sections:
    if title not in sorted_tab_titles:
        sorted_tab_titles.append(title)

# Create Streamlit tabs for each section
tabs = st.tabs(sorted_tab_titles)

for i, title in enumerate(sorted_tab_titles):
    with tabs[i]:
        st.subheader(title)
        st.markdown(parsed_sections[title])

        # --- Charts (Illustrative Data) ---
        # Add specific charts based on the content of each section where meaningful
        if title == "1. Company Overview":
            st.markdown("#### Nokia's Business Segments (Illustrative Revenue Share)")
            # Illustrative pie chart showing revenue distribution across segments
            revenue_streams_data = pd.DataFrame({
                'Segment': ['Mobile Networks', 'Network Infrastructure', 'Cloud and Network Services', 'Nokia Technologies'],
                'Revenue Share': [35, 30, 20, 15] # Assumed percentages based on text description
            })
            chart_revenue_streams = alt.Chart(revenue_streams_data).mark_arc(outerRadius=120).encode(
                theta=alt.Theta(field="Revenue Share", type="quantitative"),
                color=alt.Color(field="Segment", type="nominal", title="Segment"),
                order=alt.Order("Revenue Share", sort="descending"),
                tooltip=["Segment", alt.Tooltip("Revenue Share", format=".1f")]
            ).properties(
                title="Illustrative Revenue Segment Distribution"
            )
            st.altair_chart(chart_revenue_streams, use_container_width=True)

        elif title == "2. Key Financial Relationships":
            # R&D Investment Chart
            st.markdown("#### R&D Investment Over Time (Conceptual)")
            # Attempt to parse R&D percentage, default to 14.0 if extraction fails
            rd_val_str = key_metrics.get("R&D Investment (% of Revenue)", "14%").replace('~', '').replace('%', '')
            rd_val = float(rd_val_str) if rd_val_str.replace('.', '', 1).isdigit() else 14.0
            
            # Illustrative data for R&D over a few years, showing consistency around the extracted value
            rd_data = pd.DataFrame({
                'Year': [2021, 2022, 2023, 2024],
                'R&D_as_percent_revenue': [rd_val - 0.5, rd_val + 0.2, rd_val, rd_val - 0.3] 
            })
            chart_rd = alt.Chart(rd_data).mark_line(point=True).encode(
                x=alt.X('Year:O', axis=alt.Axis(title="Year")),
                y=alt.Y('R&D_as_percent_revenue', title="R&D as % of Revenue", scale=alt.Scale(domain=[max(0, rd_val - 5), rd_val + 5])),
                tooltip=['Year', alt.Tooltip('R&D_as_percent_revenue', format=".1f")]
            ).properties(
                title=f"Conceptual R&D Investment ({rd_val:.1f}% average)"
            )
            st.altair_chart(chart_rd, use_container_width=True)

            # Geographic Revenue Breakdown Chart
            st.markdown("#### Geographic Revenue Breakdown (Illustrative)")
            # Attempt to parse geographic revenue percentages, default if extraction fails
            na_percent_str = key_metrics.get("Geographic Revenue (North America)", "30%").replace('~', '').replace('%', '')
            eu_percent_str = key_metrics.get("Geographic Revenue (Europe)", "20%").replace('~', '').replace('%', '')
            
            na_percent = float(na_percent_str) if na_percent_str.replace('.', '', 1).isdigit() else 30.0
            eu_percent = float(eu_percent_str) if eu_percent_str.replace('.', '', 1).isdigit() else 20.0
            other_percent = 100 - na_percent - eu_percent # Calculate remaining for "Other"
            
            geo_data = pd.DataFrame({
                'Region': ['North America', 'Europe', 'Asia, Africa & Other'],
                'Revenue Share': [na_percent, eu_percent, other_percent]
            })
            chart_geo = alt.Chart(geo_data).mark_arc(outerRadius=120).encode(
                theta=alt.Theta(field="Revenue Share", type="quantitative"),
                color=alt.Color(field="Region", type="nominal", title="Region"),
                order=alt.Order("Revenue Share", sort="descending"),
                tooltip=["Region", alt.Tooltip("Revenue Share", format=".1f")]
            ).properties(
                title="Geographic Revenue Distribution (Illustrative)"
            )
            st.altair_chart(chart_geo, use_container_width=True)

        elif title == "4. Sector Connections & Competitor Relationships":
            st.markdown("#### Key Competitors Landscape (Illustrative Strength)")
            # Bar chart showing illustrative strength/presence of key competitors
            competitor_data = pd.DataFrame({
                'Competitor': ['Ericsson (ERIC)', 'Huawei (Private)', 'Samsung', 'Cisco Systems (CSCO)', 'Juniper Networks (JNPR)', 'ZTE'],
                'Strength': [90, 85, 70, 60, 40, 50] # Illustrative strength score out of 100
            })
            chart_competitors = alt.Chart(competitor_data).mark_bar().encode(
                x=alt.X('Competitor:N', sort='-y', axis=alt.Axis(title="Competitor")),
                y=alt.Y('Strength:Q', title="Illustrative Market Presence/Strength"),
                tooltip=['Competitor', 'Strength']
            ).properties(
                title="Illustrative Competitor Presence"
            )
            st.altair_chart(chart_competitors, use_container_width=True)

        elif title == "6. Stock Performance Drivers" or title == "8. Investment Considerations":
            st.markdown("#### Investment Scenario Outlook (Conceptual)")
            # Bar chart for conceptual investment scenarios (Bull, Bear, Base Case)
            scenario_data = pd.DataFrame({
                'Scenario': ['Bull Case', 'Bear Case', 'Base Case'],
                'Outlook': [80, 20, 50] # Illustrative outlook score out of 100
            })
            chart_scenario = alt.Chart(scenario_data).mark_bar().encode(
                x=alt.X('Scenario:N', axis=alt.Axis(title="Scenario")),
                y=alt.Y('Outlook:Q', title="Conceptual Outlook Score"),
                color=alt.Color('Scenario', scale=alt.Scale(range=['#4CAF50', '#F44336', '#FFEB3B'])), # Green, Red, Yellow for scenarios
                tooltip=['Scenario', 'Outlook']
            ).properties(
                title="Conceptual Investment Scenario Outlook"
            )
            st.altair_chart(chart_scenario, use_container_width=True)
            
st.markdown("---") # Final separator
st.info("Disclaimer: This analysis is based on the provided text and aims to present the information in a structured, visual manner. All numerical data, especially for charts, are illustrative based on descriptive text and not real-time financial figures.")