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
import re

# --- Configuration ---
st.set_page_config(layout="wide", page_title="Nokia (NOK) Financial Analysis")

# --- Original Analysis Text ---
# The complete financial analysis text is embedded here.
analysis_text = """
Let's dive into a comprehensive financial analysis of Nokia (NOK).

**I. Company Overview and Business Segments**

Nokia is a Finnish multinational telecommunications, information technology, and consumer electronics company headquartered in Espoo, Finland. Its primary business revolves around providing network infrastructure and services to telecom operators and enterprises. The company has undergone significant strategic shifts over the years, moving away from its consumer mobile phone business (which was sold to Microsoft in 2014 and later licensed to HMD Global) to focus on B2B (business-to-business) solutions.

Nokia's core business segments typically include:

*   **Network Infrastructure:** This is the largest segment and encompasses:
    *   **Mobile Networks:** Providing 5G, 4G, and older radio access network (RAN) solutions, as well as core network equipment.
    *   **Fixed Networks:** Offering broadband access (fiber optics), IP routing, and optical networking solutions.
    *   **Cloud and Network Services:** Delivering software, AI, and analytics solutions for network management and optimization.
*   **Nokia Technologies:** This segment focuses on patent licensing (including its vast intellectual property portfolio in mobile communication technologies) and intellectual property development.
*   **Nokia Enterprise:** This segment targets non-telecom operators, offering connectivity solutions for industries like manufacturing, transportation, and energy.

**II. Key Financial Relationships and Metrics Analysis**

To understand Nokia's financial health and performance, we'll examine several key financial relationships:

*   **Revenue Growth:** Nokia's revenue has been influenced by the cyclical nature of telecom capital expenditures, the transition to 5G, and competitive pressures. Investors will look for consistent or accelerating revenue growth, particularly in its core Network Infrastructure segment.
*   **Profitability:**
    *   **Gross Profit Margin:** Indicates efficiency in producing its network equipment and services. Improvements here suggest better cost management or pricing power.
    *   **Operating Profit Margin (EBIT Margin):** Shows profitability from core operations. Volatility can arise from R&D investments, restructuring costs, or competitive pricing.
    *   **Net Profit Margin:** The bottom line, reflecting overall profitability after all expenses, interest, and taxes.
    *   **EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization):** A useful metric for comparing profitability across companies and understanding operational cash flow generation potential.
*   **Balance Sheet Strength:**
    *   **Debt-to-Equity Ratio:** Measures financial leverage. A high ratio can indicate higher risk, while a low ratio suggests financial stability. Nokia has historically managed its debt levels, but significant acquisitions or market downturns can impact this.
    *   **Current Ratio and Quick Ratio:** Assess short-term liquidity, indicating the company's ability to meet its immediate obligations.
    *   **Cash Flow from Operations:** Crucial for funding R&D, capital expenditures, and dividends (if applicable). Strong positive cash flow is a sign of a healthy business.
    *   **Free Cash Flow (FCF):** Cash flow available after capital expenditures. This is a key indicator of a company's ability to return value to shareholders or reinvest in the business.
*   **Valuation Metrics:**
    *   **Price-to-Earnings (P/E) Ratio:** Compares Nokia's stock price to its earnings per share. A high P/E might suggest investor optimism or overvaluation, while a low P/E could indicate undervaluation or underlying concerns.
    *   **Price-to-Sales (P/S) Ratio:** Useful for companies with inconsistent earnings. It indicates how much investors are willing to pay for each dollar of sales.
    *   **Enterprise Value to EBITDA (EV/EBITDA):** A common valuation metric in the telecom infrastructure space, providing a more comprehensive view than P/E by including debt and cash.
    *   **Dividend Yield (if applicable):** While Nokia has historically paid dividends, its policy can change. Investors consider this for income generation.

**III. Market Dependencies and Sector Connections**

Nokia operates within a highly dynamic and interconnected ecosystem:

*   **Telecommunications Operators (Telcos):** This is Nokia's primary customer base (e.g., AT&T, Verizon, Vodafone, Deutsche Telekom). Their capital expenditure cycles, investment decisions in new network technologies (like 5G and fiber), and regulatory environments directly impact Nokia's sales.
*   **5G Rollout:** The global deployment of 5G technology is a major driver for Nokia. The pace of this rollout, including government initiatives and operator investment, significantly influences demand for Nokia's RAN, core network, and fiber solutions.
*   **Broadband Expansion:** The increasing demand for high-speed internet, especially in residential and enterprise settings, fuels demand for Nokia's fixed network products.
*   **Cloud and Software Services:** As telcos embrace virtualization and cloud-native architectures, demand for Nokia's software, AI, and analytics solutions grows. This also links Nokia to the broader cloud computing and enterprise software markets.
*   **Semiconductor and Component Suppliers:** Nokia relies on a complex supply chain for essential components like chips. Disruptions in this supply chain (e.g., chip shortages) can impact production and profitability.
*   **Content Providers and OTT Services:** While not direct customers, the growth of streaming services and online content drives demand for greater network capacity, indirectly benefiting Nokia.

**IV. Competitor Relationships**

The telecommunications infrastructure market is highly competitive. Nokia's main rivals include:

*   **Ericsson (ERIC):** A direct competitor across most of Nokia's product lines, particularly in mobile networks and managed services.
*   **Huawei (HWP):** A dominant player globally, though its market share in certain Western markets has been impacted by geopolitical concerns and sanctions. Huawei remains a formidable competitor in many regions.
*   **ZTE (0763.HK):** Another Chinese competitor, offering a broad range of telecom equipment.
*   **Samsung (005930.KS):** Increasingly a significant player in the 5G RAN market, challenging established players.
*   **Cisco Systems (CSCO):** A strong competitor in the IP routing and optical networking space, especially for enterprise and service provider backhaul.
*   **Juniper Networks (JNPR):** Another key player in routing and switching.
*   **Alcatel-Lucent (now part of Nokia):** Historically a major competitor, its acquisition by Nokia consolidated the market.

Nokia's success depends on its ability to innovate, maintain competitive pricing, build strong customer relationships, and navigate complex geopolitical landscapes that can favor or hinder specific competitors.

**V. Economic Factors Impacting Nokia**

Several macroeconomic and geopolitical factors can influence Nokia's performance:

*   **Global Economic Growth:** A strong global economy generally leads to increased demand for telecommunications services, driving telco investment and thus Nokia's sales. Economic downturns can lead to reduced CapEx by operators.
*   **Interest Rates:** Higher interest rates can increase the cost of capital for both Nokia and its customers, potentially slowing down investment decisions.
*   **Inflation:** Rising input costs (labor, raw materials, components) due to inflation can pressure Nokia's profit margins if it cannot pass these costs on to its customers.
*   **Currency Fluctuations:** As a Finnish company with global operations, Nokia is exposed to currency risks. For example, a strong Euro can make its products more expensive for customers using other currencies, impacting sales volume and profitability.
*   **Government Policies and Regulations:**
    *   **Spectrum Auctions:** Government decisions on allocating radio spectrum for 5G and future technologies directly impact the urgency and scale of operator investments.
    *   **Geopolitical Tensions and Trade Policies:** Restrictions or bans on specific vendors (like Huawei) can create opportunities for Nokia in some markets but can also lead to retaliatory measures or supply chain disruptions. Government support for domestic technology also plays a role.
    *   **National Security Concerns:** In some countries, concerns about the security of network infrastructure can influence vendor selection, leading to increased scrutiny and potential shifts in market share.
*   **Technological Disruption:** Rapid advancements in areas like AI, quantum computing, and new communication protocols could necessitate significant R&D investments and strategic shifts.
*   **Capital Expenditure Cycles of Telcos:** The telecommunications industry is characterized by large, cyclical capital expenditures as operators upgrade their networks. Nokia's performance is heavily tied to these cycles.

**VI. SWOT Analysis (Summary of Strengths, Weaknesses, Opportunities, Threats)**

*   **Strengths:**
    *   Strong patent portfolio and IP leadership.
    *   Established customer relationships with major telcos.
    *   Comprehensive product and service offering across mobile and fixed networks.
    *   Global presence and service capabilities.
    *   Experience and expertise in network technologies.
*   **Weaknesses:**
    *   Profitability has been inconsistent in the past due to restructuring and competition.
    *   Reliance on large, cyclical telco CapEx.
    *   Intense competition, particularly from Huawei.
    *   Potential challenges in adapting quickly to new market trends or technological shifts.
*   **Opportunities:**
    *   Continued global 5G and future 6G network deployments.
    *   Growth in enterprise private networks.
    *   Expansion of broadband access (fiber, fixed wireless access).
    *   Increasing demand for network software, AI, and cloud solutions.
    *   Potential market share gains from competitor restrictions.
*   **Threats:**
    *   Intensifying price competition.
    *   Geopolitical risks and trade wars impacting market access.
    *   Rapid technological obsolescence requiring constant R&D.
    *   Supply chain disruptions.
    *   Potential for regulatory changes impacting network deployment or vendor choices.

**Conclusion**

Nokia operates in a crucial but highly competitive and evolving sector. Its financial ecosystem is tightly linked to the capital expenditure cycles of telecommunications operators, the pace of 5G and broadband deployments, and global economic and geopolitical conditions. While Nokia has strengths in its technological capabilities and customer base, it faces significant challenges from intense competition and the need for continuous innovation. Investors scrutinize its revenue growth, profitability, and cash flow generation, while also considering the broader market dynamics, its competitive positioning, and the impact of economic and political forces. The company's ability to successfully navigate these factors will determine its future financial performance and shareholder value.

---

Below is a structured, comprehensive view of Nokia (ticker: NOK) and the financial ecosystem that drives its business and stock performance. I cover business structure and revenue drivers, supplier/customer relationships, competitive landscape, sector and technology dependencies, macro & regulatory influences, key financial/operational metrics to watch, and principal risks and opportunities.

1) Business overview — revenue streams and segments
- Core businesses: Networks (radio access, IP/optical, core, and associated services & software) is the largest revenue source; Nokia Technologies (patent licensing, IP, and some tech products) provides recurring but lumpy licensing income; Cloud & Network Services, and enterprise/private networks are other growth areas.
- Revenue mix matters: hardware (RAN, optical) tends to be cyclical and lower margin; software/services and licensing are higher margin and more recurring. Shift toward software and services improves margin profile over time but requires execution.

2) Customers and demand drivers
- Primary customers: global mobile network operators (MNOs) — e.g., AT&T, Verizon, T‑Mobile, Vodafone, Deutsche Telekom, China Mobile, BT — plus some large enterprises and governments for private networks and critical infrastructure.
- Demand cycles: carrier CAPEX cycles (driven by spectrum auctions, 4G/5G/6G rollouts, and refresh cycles) are the primary driver of bookings and revenue. Operator profitability/ARPU and their willingness to invest materially affect Nokia’s near-term performance.
- Government and public-sector contracts: security-conscious nations (U.S., EU members) pick vendors based on policy considerations; Nokia benefits from “trusted vendor” procurement in Western markets.

3) Suppliers and supply-chain dependencies
- Semiconductor suppliers: Nokia relies on third-party chips (baseband, RF components, switching/optical ASICs) from firms like Qualcomm, Broadcom, Marvell and fab capacity from TSMC/Intel/Samsung Foundry. Global chip availability and pricing affect deliveries and margins.
- Optical and passive component supply chains (coherent optics, transceivers) are critical; component shortages or single-source constraints can delay rollouts.
- Manufacturing and logistics: Nokia outsources components and some manufacturing, making it sensitive to global supply-chain disruptions, container freight costs, and geopolitical export controls.

4) Competitive landscape
- Direct public competitors: Ericsson (ERIC) — closest peer in global RAN and services; Ciena (CIEN) and Juniper/Cisco (CI/Cisco) — compete in optical/IP routing and service provider domains.
- Private/low-cost competitors: Huawei and ZTE dominate many emerging markets on price and vertical integration (Huawei especially); restrictions on Huawei in the U.S./parts of Europe create opportunities for Nokia and Ericsson.
- New/Open-RAN entrants: Mavenir, Rakuten Symphony, Altiostar and other software-focused vendors challenge traditional vendors in O-RAN and virtualized RAN deployments.
- Cloud players: hyperscalers (AWS, Google Cloud, Microsoft) and cloud-native networking software vendors are increasingly relevant for core/cloudification and edge computing partnerships.
- Competitive dynamics: price competition in mature markets, technological differentiation (energy efficiency, throughput, software features), and services execution determine market share.

5) Technology & sector dependencies
- 5G rollout: major growth driver. RAN, transport (IP/optical), core network virtualization, and managed services are tied to the pace of carrier 5G deployments, densification, and shift to cloud-native cores.
- Open RAN movement: a structural trend that can lower barriers for new entrants and change vendor economics. Nokia participates in O-RAN but must balance revenue/profitability trade-offs vs traditional RAN.
- Software/cloud transformation: transition to software-defined networking, virtualization and cloud-native architectures shifts revenue from hardware to subscription/software & services.
- Edge computing, private networks, and industrial IoT: potential growth opportunities, particularly with enterprise and industrial customers.
- Patent/IP (Nokia Technologies): 5G/4G patent portfolio generates licensing revenue; patents are strategic assets and provide recurring cash flow but are subject to disputes and renewals.

6) Macroeconomic, regulatory & geopolitical factors
- Geopolitics & security policy: bans/restrictions on Huawei in Western markets are tailwinds. Export controls, trade tensions (US-China/EU-China), and sanctions can both help (by excluding rivals) and hurt (restricting supply sources).
- Government subsidies and industrial policy: EU funding initiatives for secure networks and national subsidies for 5G can accelerate Nokia’s opportunities in Europe; CHIPS Act and related incentives may help semiconductors but changing supply incentives also affect component sourcing.
- Interest rates & macro environment: higher interest rates increase discounting of future cash flows and pressure highly cyclical capex-dependent stocks. Carrier CAPEX can be delayed in periods of weak demand or macro uncertainty.
- Currency exposure: Nokia reports in EUR but generates material revenue in USD and other currencies; FX moves affect reported revenue and margins.
- Inflation and operator economics: operator willingness to invest depends on ARPU trends, inflation, and competitive pressure in consumer markets.

7) Financial/operational metrics and relationships to monitor
- Bookings / order intake and backlog: leading indicators of future revenue.
- Book-to-bill ratio: shows demand vs delivery capacity.
- Gross margin by segment: hardware vs software/services yields different margins; watch margin trends as mix shifts.
- Services & software revenue percentage: higher mix implies more predictable, higher-margin revenue.
- Nokia Technologies/licensing revenue and stability: licensing is lumpy but high-margin; contract renewals and settlements are material.
- Operating margin, adjusted EBIT, free cash flow conversion: cash generation is vital for R&D, dividends, buybacks, and deleveraging.
- Net debt / liquidity: cyclical downturns can pressure companies with high leverage.
- R&D spend and CapEx: critical for long-term competitiveness in RAN, optical, and 6G research (including Bell Labs legacy).
- Major contract wins/losses and pilot-to-commercial conversion (especially for Open RAN deployments).
- Legal/IP outcomes: licensing disputes or settlements can materially swing Technology segment cashflows.

8) Valuation/market relationships
- Peer comparables: Ericsson, Ciena, Cisco, Juniper, and selected semiconductor suppliers. NOK’s multiples will be influenced by margin trends, growth visibility, and the split between one-time vs recurring revenues.
- Sensitivity to sector rotation: Nokia tends to move with telecom equipment peers and the broader tech/hardware group; also sensitive to interest-rate changes because of cyclical nature.

9) Key opportunities
- Faster 5G rollouts and network densification (small cells, mid-band mmWave) in Europe/North America.
- Displacement of Huawei in Western-aligned and allied countries.
- Growth in software, cloud, managed services, and private networks.
- Open RAN adoption at scale (if Nokia can capture meaningful share via virtualized offerings and ecosystem partnerships).
- Licensing and patent monetization, including new 5G/6G IP.

10) Principal risks
- Intensifying price competition (especially from Huawei/ZTE where allowed), which can compress margins.
- Delays or cutbacks in carrier CAPEX due to macro weakness or poor operator economics.
- Supply-chain disruptions and semiconductor shortages or price inflation.
- Execution risk on software transition and integrating acquisitions.
- Regulatory and geopolitical shifts (e.g., sudden policy reversals or new export controls) that could restrict markets or inputs.
- Lumpy licensing revenue and legal outcomes affecting cash flow predictability.

11) Practical monitoring checklist for investors
- Quarterly/annual filings: bookings, backlog, segment revenue (Networks vs Technologies), gross margins, operating cash flow, net debt.
- Major contract announcements (wins with tier-1 carriers) and geographic mix of those wins.
- Progress and wins in Open RAN and cloud-native core deployments.
- Patent licensing deal updates and material settlements.
- R&D spend trajectory and CapEx guidance.
- Analyst guidance vs bookings and book-to-bill trends.
- Macro indicators: carrier capex guidance, spectrum auctions scheduled in major markets, regulatory headwinds/benefits in EU/US/Asia.
- Competitor earnings/capital deployment — particularly Ericsson and Ciena — for relative performance and pricing trends.

Summary
Nokia’s performance is driven by global carrier CAPEX cycles, competitive dynamics between Ericsson/Huawei/Samsung and emerging Open RAN vendors, semiconductor and component supply conditions, and regulatory/geopolitical shifts that reshape market access. The company’s long-term path depends on its ability to increase higher-margin software and services revenue, convert RAN technology wins into scale (including Open RAN), and protect/monetize its IP portfolio — all while managing execution, supply-chain and pricing pressures. For investment decisions, focus on bookings/book-to-bill, margin mix evolution, free cash flow and licensing trends, and major contract pipelines as the principal leading indicators.

If you’d like, I can:
- Pull together a comparable peer set and a tailored set of KPIs to track weekly/quarterly,
- Draft an investor monitoring dashboard of the 8–10 most actionable metrics,
- Or analyze a recent quarterly report (you can paste the key numbers) and map them into the framework above.

---

**Stock Analysis: Nokia Corporation (NOK)**  

---

### **1. Company Overview**
- **Ticker:** NOK (NYSE, Helsinki, Frankfurt)  
- **Headquarters:** Espoo, Finland  
- **Sector:** Technology / Communication Equipment  
- **Industry:** Networking & Telecommunications  
- **Key Business Segments:**  
  - **Network Infrastructure** (Mobile Networks, Fixed Networks, IP/Optical Networks, Submarine Networks)  
  - **Mobile Networks** (5G equipment, radio access networks)  
  - **Cloud and Network Services** (Core network software, cloud solutions)  
  - **Nokia Technologies** (Licensing of intellectual property, patents)  

---

### **2. Key Financial Relationships**
- **Revenue Streams:** Heavily dependent on capital expenditure cycles of telecom operators (e.g., AT&T, Verizon, Vodafone).  
- **Profitability Drivers:**  
  - **Gross Margins:** Higher in IP/Optical Networks and Nokia Technologies (licensing).  
  - **Operating Leverage:** Fixed-cost base in R&D and manufacturing; profitability improves with higher sales volume.  
- **Balance Sheet Strength:**  
  - Strong cash position (€4.3 billion as of Q3 2023) with manageable debt.  
  - Investments in R&D (~13% of revenue) critical for maintaining technological edge.  
  - **Dividend Policy:** Reinstated dividend in 2023 after suspension during restructuring.  

---

### **3. Market Dependencies**
- **5G Rollout Cycle:** Growth tied to global 5G infrastructure deployment, especially in North America, Europe, and Asia.  
- **Telecom Operator Spending:** Sensitivity to economic cycles; operators may delay capex in downturns.  
- **Geopolitical Factors:**  
  - Trade restrictions (e.g., China-West tensions) impact supply chains and market access.  
  - European Union policies promoting “Open RAN” (open radio access networks) could alter competitive dynamics.  
- **Currency Risk:** Revenue in USD, EUR, and other currencies; EUR appreciation can negatively impact reported earnings.  

---

### **4. Sector Connections**
- **Telecom Equipment Industry:** Oligopolistic structure with **Ericsson (ERIC)**, **Huawei**, **ZTE**, and **Cisco (CSCO)** as key players.  
- **Supply Chain:** Relies on semiconductor suppliers (e.g., Broadcom, Intel) and contract manufacturers.  
- **End-Market Links:**  
  - **Enterprise Networks:** Growth in private 5G networks for industries (manufacturing, logistics).  
  - **Government & Defense:** Secure communications infrastructure.  

---

### **5. Competitor Relationships**
- **Direct Competitors:**  
  - **Ericsson (ERIC):** Similar portfolio; intense competition in 5G radio access networks.  
  - **Huawei:** Dominant in China and emerging markets; excluded from many Western markets due to security concerns (benefits NOK and ERIC).  
  - **Cisco (CSCO):** Competes in IP routing and optical networks.  
- **Competitive Advantages:**  
  - Strong patent portfolio (~20,000 patent families, including foundational 5G patents).  
  - End-to-end portfolio (from radio to core networks).  
- **Weaknesses:** Lower scale vs. Huawei; slower growth in some emerging markets.  

---

### **6. Economic Factors**
- **Macroeconomic Sensitivity:**  
  - High interest rates increase financing costs for telecom operators, potentially delaying 5G investments.  
  - Inflation impacts component costs and logistics.  
- **Regulatory Environment:**  
  - Spectrum allocation policies by governments drive operator investment.  
  - National security regulations (e.g., bans on Huawei) create opportunities in Western markets.  
- **Technology Shifts:**  
  - Transition to cloud-native, software-defined networks requires ongoing R&D.  
  - Growth in IoT, edge computing, and AI-driven networks could provide new revenue streams.  

---

### **7. Financial Ecosystem Summary**
Nokia operates in a **cyclical, capital-intensive industry** with high strategic importance to national telecom infrastructure. Its financial health is tied to:  
1. **Global 5G Capex Cycles** – Peaks and troughs in operator spending.  
2. **Geopolitical Realignments** – Western shift away from Huawei.  
3. **R&D Efficiency** – Ability to innovate while maintaining margins.  
4. **Patent Monetization** – High-margin licensing revenue providing stability.  

**Risks:**  
- Market share loss to Ericsson or new Open RAN entrants.  
- Prolonged telecom capex slowdown.  
- Supply chain disruptions (semiconductors, logistics).  

**Opportunities:**  
- Increased 5G adoption in India, Southeast Asia, and Africa.  
- Expansion into enterprise private networks.  
- Licensing revenue from 5G patents in automotive, IoT.  

---

### **8. Investment Considerations**
- **Valuation:** Often trades at lower P/E vs. software-centric tech due to lower growth outlook and hardware margins.  
- **Catalysts:**  
  - New 5G contract wins in key markets (e.g., India, Europe).  
  - Margin expansion from cost-cutting and product mix shift to software.  
  - Patent licensing renewals (e.g., with smartphone makers).  
- **ESG Factors:** Strong focus on sustainability (energy-efficient networks, circular economy initiatives).  

---

**Conclusion:** Nokia’s stock performance is a function of **telecom capex cycles, competitive dynamics vs. Ericsson/Huawei, and execution in transitioning to higher-margin software and services**. Monitoring quarterly order books, geopolitical developments, and 5G rollout timelines is essential for forecasting its financial trajectory.
"""


def parse_analysis_text(text):
    """
    Parses the full analysis text into a dictionary of sections.
    Handles Roman numeral headings, numbered list headings, and distinct conclusions.
    """
    sections = {}

    # Split into three main blocks based on "---" separators
    blocks = re.split(r'\n---\n', text)

    # Block 1: Initial Comprehensive Financial Analysis (Roman numerals)
    if len(blocks) > 0:
        main_analysis_text = blocks[0].strip()
        # Regex to split by "**I. Title**" like headings
        main_sections_raw = re.split(r'(\n\*\*I{1,3}\. [A-Za-z\s&-]+\*\*)\n', main_analysis_text, flags=re.MULTILINE)
        
        # The first part before the first Roman numeral heading is an introduction
        if main_sections_raw and main_sections_raw[0].strip():
            sections['Introduction'] = main_sections_raw[0].strip()
        
        # Process Roman numeral sections
        for i in range(1, len(main_sections_raw), 2):
            title = main_sections_raw[i].strip().replace('**', '')
            content = main_sections_raw[i+1].strip()
            sections[title] = content
        
        # Explicitly handle the "Conclusion" from this first block if it wasn't caught by generic Roman numeral parsing
        # The regex looks for "**Conclusion**\n" followed by content, up to the next block or next Roman numeral
        first_conclusion_match = re.search(r'\n\*\*Conclusion\*\*\n(.*?)(?=\n\*\*I{1,3}\.|$)', main_analysis_text, re.DOTALL)
        if first_conclusion_match:
            # Check if it was already caught by Roman numeral parsing (if a generic "**Conclusion**" was present)
            if "Conclusion" in sections:
                sections["Conclusion of Initial Analysis"] = sections.pop("Conclusion") # Rename it
            else:
                sections["Conclusion of Initial Analysis"] = first_conclusion_match.group(1).strip()
        elif "Conclusion" in sections: # If it was a generic 'Conclusion' from the splitting and not explicitly handled above
            sections['Conclusion of Initial Analysis'] = sections.pop('Conclusion')


    # Block 2: Structured, Comprehensive View (Numbered points like "1) Business overview")
    if len(blocks) > 1:
        structured_view_text = blocks[1].strip()
        
        # The text before "1) Business overview" serves as an introduction to this section
        intro_match = re.match(r'(.*?)\n1\) Business overview', structured_view_text, re.DOTALL)
        if intro_match:
            sections['Structured Ecosystem View Introduction'] = intro_match.group(1).strip()
        
        # Regex to split by "1) Title" like headings
        structured_sections_raw = re.split(r'(\n\d+\) [A-Za-z\s&\-,\/—]+)\n', structured_view_text, flags=re.MULTILINE)
        
        for i in range(1, len(structured_sections_raw), 2):
            title = structured_sections_raw[i].strip()
            content = structured_sections_raw[i+1].strip()
            sections[f"Structured View: {title}"] = content
        
        # Extract the Summary from this block
        summary_match = re.search(r'\nSummary\n(.*?)(?=\nIf you’d like|$)', structured_view_text, re.DOTALL)
        if summary_match:
            sections['Summary of Ecosystem View'] = summary_match.group(1).strip()

    # Block 3: Stock Analysis (Numbered hash headings like "### 1. Company Overview")
    if len(blocks) > 2:
        stock_analysis_text = blocks[2].strip()
        # The initial part might contain a small intro or just the "Stock Analysis: Nokia Corporation (NOK)"
        intro_part = stock_analysis_text.split('\n### 1. Company Overview')[0].strip()
        if intro_part and intro_part != "**Stock Analysis: Nokia Corporation (NOK)**": # Avoid adding just the title again
             sections['Stock Analysis Overview'] = intro_part
        
        # Regex to split by "### 1. Title" like headings
        stock_analysis_sections_raw = re.split(r'(\n### \d+\. [A-Za-z\s&-:]+)\n', stock_analysis_text, flags=re.MULTILINE)
        
        for i in range(1, len(stock_analysis_sections_raw), 2):
            title = stock_analysis_sections_raw[i].strip().replace('### ', '')
            content = stock_analysis_sections_raw[i+1].strip()
            sections[f"Stock Analysis: {title}"] = content
        
        # Extract the final "Conclusion" from the very end of the text
        final_conclusion_match = re.search(r'\n\*\*Conclusion:\*\*(.*?)$', stock_analysis_text, re.DOTALL)
        if final_conclusion_match:
            sections['Final Investment Conclusion'] = final_conclusion_match.group(1).strip()

    return sections

parsed_sections = parse_analysis_text(analysis_text)


# --- Dummy Data Generation for Charts (Illustrative, not real Nokia data) ---
years = pd.to_datetime([f'{2018+i}-01-01' for i in range(7)]) # 7 years of data

df_revenue = pd.DataFrame({
    'Year': years,
    'Revenue (B€)': [23.3, 23.1, 21.9, 22.2, 24.9, 23.6, 25.1] # Cyclical but some growth, reflecting text
})

df_margins = pd.DataFrame({
    'Year': years,
    'Gross Profit Margin (%)': [35, 36, 34, 37, 39, 38, 40],
    'Operating Profit Margin (%)': [6, 7, 4, 8, 10, 9, 11],
    'Net Profit Margin (%)': [2, 3, 1, 5, 7, 6, 8]
})

df_capex_rd = pd.DataFrame({
    'Year': years,
    'R&D Spend (B€)': [4.5, 4.3, 4.2, 4.5, 4.8, 4.7, 4.9], # Stable/increasing R&D
    'Capital Expenditures (B€)': [1.5, 1.4, 1.3, 1.6, 1.8, 1.7, 1.9] # Reflecting CapEx needs
})

df_debt_equity = pd.DataFrame({
    'Year': years,
    'Debt-to-Equity Ratio': [0.55, 0.50, 0.48, 0.45, 0.40, 0.38, 0.35] # Illustrative improvement/stability
})

df_cash_flow = pd.DataFrame({
    'Year': years,
    'Cash Flow from Operations (B€)': [3.0, 3.2, 2.8, 3.5, 3.8, 3.6, 4.0],
    'Free Cash Flow (B€)': [1.5, 1.8, 1.5, 2.0, 2.2, 2.0, 2.5] # Strong positive cash flow
})

# Conceptual market share for competitors based on qualitative description
df_market_share = pd.DataFrame({
    'Competitor': ['Huawei', 'Ericsson', 'Nokia', 'Samsung', 'ZTE', 'Cisco', 'Juniper', 'Others'],
    'Estimated Market Share (%)': [28, 24, 18, 10, 8, 6, 3, 3] # Fictional distribution, broader competition
})


# --- Streamlit App Layout ---

st.title("Nokia (NOK) Financial Analysis & Ecosystem Deep Dive")
st.markdown("---")

# Sidebar for navigation
st.sidebar.header("Analysis Sections")
page_options = list(parsed_sections.keys())
selected_page = st.sidebar.radio("Navigate to:", page_options)

# Main content area
st.header(selected_page)
st.markdown(parsed_sections[selected_page])

# --- Add Charts where meaningful based on selected section ---
if "Key Financial Relationships and Metrics Analysis" in selected_page or \
   "Financial/operational metrics and relationships to monitor" in selected_page or \
   "Key Financial Relationships" in selected_page:
    st.subheader("Key Financial Trends (Illustrative)")

    col1, col2 = st.columns(2)
    with col1:
        st.write("### Revenue Growth")
        fig_revenue = px.line(df_revenue, x='Year', y='Revenue (B€)', title='Illustrative Annual Revenue', markers=True)
        fig_revenue.update_layout(yaxis_title="Revenue in Billions of Euros")
        st.plotly_chart(fig_revenue, use_container_width=True)
        st.caption("Illustrative data reflecting cyclical nature and potential for growth mentioned in the analysis.")

    with col2:
        st.write("### Profitability Margins")
        fig_margins = px.line(df_margins, x='Year', y=['Gross Profit Margin (%)', 'Operating Profit Margin (%)', 'Net Profit Margin (%)'], 
                              title='Illustrative Profitability Margins', markers=True)
        fig_margins.update_layout(yaxis_title="Margin Percentage (%)")
        st.plotly_chart(fig_margins, use_container_width=True)
        st.caption("Illustrative data showing potential trends for gross, operating, and net profit margins (inconsistent/volatile as per text).")

    col3, col4 = st.columns(2)
    with col3:
        st.write("### Cash Flow Generation")
        fig_cash_flow = px.bar(df_cash_flow, x='Year', y=['Cash Flow from Operations (B€)', 'Free Cash Flow (B€)'], 
                               title='Illustrative Cash Flow Trends', barmode='group')
        fig_cash_flow.update_layout(yaxis_title="Cash Flow in Billions of Euros")
        st.plotly_chart(fig_cash_flow, use_container_width=True)
        st.caption("Illustrative data showing positive operational and free cash flow generation, crucial for funding R&D, CapEx, and dividends.")

    with col4:
        st.write("### Debt-to-Equity Ratio")
        fig_debt_equity = px.line(df_debt_equity, x='Year', y='Debt-to-Equity Ratio', 
                                  title='Illustrative Debt-to-Equity Ratio', markers=True)
        fig_debt_equity.update_layout(yaxis_title="Ratio")
        st.plotly_chart(fig_debt_equity, use_container_width=True)
        st.caption("Illustrative data showing Nokia's historical management or improving debt levels.")

    st.subheader("Key Metrics Extracted (as mentioned in the analysis):")
    st.markdown(
        """
        **Performance & Profitability:**
        -   **Revenue Growth:** Consistency and acceleration, especially in Network Infrastructure.
        -   **Gross Profit Margin:** Efficiency in production, cost management, pricing power.
        -   **Operating Profit Margin (EBIT Margin):** Profitability from core operations, reflecting R&D and competitive pressures.
        -   **Net Profit Margin:** Overall profitability after all expenses.
        -   **EBITDA:** Useful for comparing operational cash flow generation.
        -   **Bookings / Order Intake and Backlog:** Leading indicators of future revenue.
        -   **Book-to-bill ratio:** Shows demand versus delivery capacity.
        -   **Services & software revenue percentage:** Indicates shift towards higher-margin, more predictable revenue.
        -   **Nokia Technologies/licensing revenue:** High-margin but potentially lumpy income.

        **Balance Sheet & Liquidity:**
        -   **Debt-to-Equity Ratio:** Financial leverage and stability.
        -   **Current Ratio and Quick Ratio:** Short-term liquidity to meet immediate obligations.
        -   **Net Debt / Liquidity:** Overall financial health and capacity.

        **Cash Flow:**
        -   **Cash Flow from Operations:** Crucial for funding R&D, capital expenditures, and dividends.
        -   **Free Cash Flow (FCF):** Cash available for shareholders or reinvestment after CapEx.

        **Valuation:**
        -   **Price-to-Earnings (P/E) Ratio:** Stock price relative to earnings per share.
        -   **Price-to-Sales (P/S) Ratio:** Useful for companies with inconsistent earnings.
        -   **Enterprise Value to EBITDA (EV/EBITDA):** Comprehensive valuation in telecom infrastructure, including debt and cash.
        -   **Dividend Yield:** Income generation for investors.

        **Investment & Operational:**
        -   **R&D Spend and CapEx:** Critical for long-term competitiveness and technology leadership.
        -   **Major contract wins/losses:** Indicators of market traction and competitive success.
        -   **Legal/IP outcomes:** Can significantly impact Nokia Technologies' cash flows.
        """
    )

elif "Competitor Relationships" in selected_page or \
     "Competitive landscape" in selected_page:
    st.subheader("Illustrative Competitive Landscape")
    st.markdown("The telecommunications infrastructure market is highly competitive with several key players mentioned:")
    
    fig_competitors = px.pie(df_market_share, values='Estimated Market Share (%)', names='Competitor', 
                             title='Illustrative Global Telecom Equipment Market Share')
    fig_competitors.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_competitors, use_container_width=True)
    st.caption("This chart is purely illustrative and does not represent actual market share data. It aims to visualize the competitive distribution described in the analysis, where Huawei and Ericsson are key rivals, and Nokia is a significant player alongside others.")
    
    st.markdown("""
    **Key Competitors Mentioned:**
    *   **Ericsson (ERIC):** A direct competitor across most of Nokia's product lines, particularly in mobile networks and managed services.
    *   **Huawei (HWP):** A dominant player globally, though its market share in certain Western markets has been impacted by geopolitical concerns and sanctions.
    *   **ZTE (0763.HK):** Another Chinese competitor, offering a broad range of telecom equipment.
    *   **Samsung (005930.KS):** Increasingly a significant player in the 5G RAN market.
    *   **Cisco Systems (CSCO):** A strong competitor in the IP routing and optical networking space, especially for enterprise and service provider backhaul.
    *   **Juniper Networks (JNPR):** Another key player in routing and switching.
    *   **New/Open-RAN Entrants:** Mavenir, Rakuten Symphony, Altiostar, and other software-focused vendors are challenging traditional players in O-RAN and virtualized RAN deployments.
    """)

elif "SWOT Analysis" in selected_page:
    st.subheader("Nokia's SWOT Analysis")
    
    # Extract SWOT elements from the text for display using regex
    swot_text = parsed_sections[selected_page]
    
    # Using regex to capture content between headings
    strengths_match = re.search(r'\*\*Strengths:\*\*(.*?)(?=\n\*\*Weaknesses:|$)', swot_text, re.DOTALL)
    weaknesses_match = re.search(r'\*\*Weaknesses:\*\*(.*?)(?=\n\*\*Opportunities:|$)', swot_text, re.DOTALL)
    opportunities_match = re.search(r'\*\*Opportunities:\*\*(.*?)(?=\n\*\*Threats:|$)', swot_text, re.DOTALL)
    threats_match = re.search(r'\*\*Threats:\*\*(.*?)$', swot_text, re.DOTALL) # Threats is usually the last one

    # Helper function to clean and split into list items
    def clean_swot_list(match):
        if match:
            # Get the captured group and split by '\n*' for bullet points, then strip whitespace
            return [item.strip() for item in match.group(1).split('\n*') if item.strip()]
        return []

    strengths_list = clean_swot_list(strengths_match)
    weaknesses_list = clean_swot_list(weaknesses_match)
    opportunities_list = clean_swot_list(opportunities_match)
    threats_list = clean_swot_list(threats_match)

    col_s, col_w = st.columns(2)
    with col_s:
        st.success("### Strengths")
        for item in strengths_list:
            st.markdown(f"- {item}")
    with col_w:
        st.warning("### Weaknesses")
        for item in weaknesses_list:
            st.markdown(f"- {item}")
    
    col_o, col_t = st.columns(2)
    with col_o:
        st.info("### Opportunities")
        for item in opportunities_list:
            st.markdown(f"- {item}")
    with col_t:
        st.error("### Threats")
        for item in threats_list:
            st.markdown(f"- {item}")
    
    st.markdown("---")
    st.markdown("R&D Spend (mentioned as ~13% of revenue in 'Stock Analysis: 2. Key Financial Relationships') is critical for maintaining technological edge and addressing market dynamics.")
    fig_rd_spend = px.area(df_capex_rd, x='Year', y='R&D Spend (B€)', title='Illustrative R&D Spend Over Time', markers=True)
    fig_rd_spend.update_layout(yaxis_title="R&D Spend in Billions of Euros")
    st.plotly_chart(fig_rd_spend, use_container_width=True)
    st.caption("Illustrative R&D spend, crucial for innovation and adapting to technological shifts (e.g., 6G, AI, quantum computing).")


elif "Conclusion" in selected_page: # Catches both "Conclusion of Initial Analysis" and "Final Investment Conclusion"
    st.subheader("Key Investment Considerations")
    st.markdown(parsed_sections[selected_page])
    st.markdown("---")
    
    if "Final Investment Conclusion" in selected_page:
        st.subheader("Practical Monitoring Checklist for Investors (Highlights):")
        st.markdown(
            """
            -   **Quarterly/Annual Filings:** Scrutinize bookings, backlog, segment revenue (Networks vs Technologies), gross margins, operating cash flow, and net debt.
            -   **Major Contract Announcements:** Pay attention to new wins with tier-1 carriers and the geographic distribution of these contracts.
            -   **Technology Progress:** Monitor advancements and commercial wins in Open RAN and cloud-native core deployments.
            -   **IP/Legal Updates:** Track patent licensing deal updates and material legal settlements, which can impact high-margin revenue.
            -   **Macro Indicators:** Observe carrier Capital Expenditure (CapEx) guidance, scheduled spectrum auctions in major markets, and regulatory headwinds/benefits in key regions (EU/US/Asia).
            -   **Competitor Earnings:** Analyze the financial performance of key competitors like Ericsson and Ciena for insights into relative market share and pricing trends.
            -   **R&D Spend Trajectory:** Evaluate the evolution of R&D investment and CapEx guidance, as these are vital for long-term competitiveness.
            """
        )

st.markdown("---")
st.sidebar.markdown("---")
st.sidebar.info("Analysis of Nokia (NOK) based on provided financial text. All charts use illustrative data.")