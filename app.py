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

# Set Streamlit page configuration
st.set_page_config(
    page_title="CSCO Financial Ecosystem Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Full Analysis Text (as provided by the user) ---
ANALYSIS_TEXT = """
Let's dive into a comprehensive financial analysis of Cisco Systems, Inc. (CSCO).

## Financial Ecosystem Analysis of Cisco Systems, Inc. (CSCO)

Cisco Systems, Inc. (CSCO) is a multinational technology conglomerate that designs, manufactures, and sells networking hardware, telecommunications equipment, and other high-technology services and products. Its business model is deeply intertwined with the global technology landscape, enterprise spending, and the ongoing digital transformation.

### 1. Key Financial Relationships & Performance Metrics:

*   **Revenue Growth & Diversification:**
    *   **Historical Trends:** Cisco has demonstrated consistent revenue generation, though growth rates can fluctuate with the IT spending cycles. Historically, it was heavily reliant on hardware (routers, switches), but has been strategically shifting towards software and services.
    *   **Subscription Revenue:** A critical metric is the growth of its **Software & Services revenue**. This recurring revenue stream provides greater predictability and higher gross margins compared to hardware. The transition to a "subscriptions-led" business model is a key focus.
    *   **Product Mix:** Analyzing the performance of different product segments (e.g., Enterprise Networking, Collaboration, Security, Data Center) is crucial to understand growth drivers and potential headwinds.
*   **Profitability & Margins:**
    *   **Gross Margins:** Generally strong, especially in software and services. Hardware margins are more competitive. The shift towards higher-margin software is a positive trend.
    *   **Operating Margins:** Reflect operational efficiency. Investments in R&D and sales & marketing are significant. Examining trends in these expenses relative to revenue is important.
    *   **Net Income & EPS:** Core profitability metrics. Analysis of trends and any impact from acquisitions or restructuring is key.
*   **Balance Sheet Strength:**
    *   **Cash & Equivalents:** Cisco typically holds substantial cash reserves, providing flexibility for acquisitions, R&D, share buybacks, and dividends.
    *   **Debt Levels:** Historically, Cisco has managed its debt conservatively. A low debt-to-equity ratio indicates financial stability.
    *   **Working Capital Management:** Efficiency in managing inventory and receivables is important, particularly for a hardware-heavy business.
*   **Cash Flow Generation:**
    *   **Operating Cash Flow:** A very strong indicator of Cisco's ability to generate cash from its core operations. Consistent and growing operating cash flow is a sign of financial health.
    *   **Free Cash Flow (FCF):** Cash available after capital expenditures. This is crucial for dividends, share repurchases, and strategic investments. Cisco has a strong track record of FCF generation.
*   **Shareholder Returns:**
    *   **Dividends:** Cisco is a dividend-paying stock and has a history of dividend growth, making it attractive to income-seeking investors.
    *   **Share Buybacks:** The company regularly engages in share repurchases, which can boost EPS and return capital to shareholders.

### 2. Market Dependencies:

*   **Global IT Spending:** Cisco's fortunes are directly tied to the overall health of the global IT spending market. This includes enterprise hardware, software, and services. Economic downturns or slowdowns in IT investment will negatively impact Cisco.
*   **Enterprise Capital Expenditure (CapEx):** Businesses are the primary customers for Cisco. Their willingness and ability to invest in network infrastructure, data centers, and collaboration tools are paramount.
*   **Digital Transformation & Cloud Adoption:** The ongoing shift towards digital services and cloud computing creates both opportunities and challenges. Cisco benefits from the infrastructure build-out required for these transformations but also faces competition from cloud-native providers.
*   **Globalization & Emerging Markets:** Economic and political stability in key global markets influences demand for Cisco's products and services. Emerging markets represent significant growth potential.
*   **Supply Chain Dynamics:** As a hardware manufacturer, Cisco is susceptible to supply chain disruptions (e.g., chip shortages), which can affect production volumes and costs.

### 3. Sector Connections:

*   **Networking Hardware:** Cisco is a dominant player in this sector, but it's a mature market with intense competition.
*   **Telecommunications Equipment:** Cisco plays a role here, particularly with its service provider offerings.
*   **Software & Cloud Services:** This is where Cisco is increasingly focusing, competing with software giants and cloud providers.
*   **Cybersecurity:** A growing and critical area. Cisco has made significant acquisitions and investments in this space.
*   **Collaboration Tools:** With the rise of remote work, the demand for unified communications and collaboration solutions (e.g., Webex) has increased.

### 4. Competitor Relationships:

Cisco operates in a highly competitive landscape. Key competitors vary by product segment:

*   **Networking Hardware:**
    *   **Arista Networks (ANET):** A strong competitor, particularly in high-performance data center networking.
    *   **Juniper Networks (JNPR):** A long-standing competitor in enterprise and service provider networking.
    *   **Hewlett Packard Enterprise (HPE) / Aruba Networks:** Competes in enterprise networking solutions.
*   **Software & Cloud:**
    *   **Microsoft (MSFT):** For collaboration (Teams vs. Webex) and increasingly in hybrid cloud solutions.
    *   **Amazon (AMZN) / Amazon Web Services (AWS):** For cloud infrastructure and services.
    *   **Google (GOOGL) / Google Cloud:** Similar to AWS.
    *   **VMware (now part of Broadcom - AVGO):** In virtualization and hybrid cloud.
*   **Cybersecurity:**
    *   **Palo Alto Networks (PANW):** A major player in firewalls and security platforms.
    *   **Fortinet (FTNT):** Another significant cybersecurity competitor.
    *   **CrowdStrike (CRWD):** In endpoint security.
    *   **Zscaler (ZS):** In cloud security.
*   **Collaboration:**
    *   **Zoom Video Communications (ZM):** A direct competitor to Webex.
    *   **Microsoft (MSFT):** Teams.

Cisco's strategy often involves acquiring companies to gain market share or technological capabilities, making M&A activity a key dynamic in its competitive ecosystem.

### 5. Economic Factors Impacting CSCO:

*   **Interest Rates:** Higher interest rates can increase the cost of capital for businesses, potentially leading to reduced IT spending and impacting Cisco's ability to finance acquisitions.
*   **Inflation:** Rising inflation can lead to higher input costs for hardware manufacturing and increase operating expenses, potentially impacting margins if not passed on to customers.
*   **Economic Growth & Recessions:** Strong economic growth generally correlates with increased IT investment. Recessions often lead to budget cuts and delayed projects, negatively affecting demand.
*   **Currency Fluctuations:** As a global company, currency exchange rate movements can impact its reported revenue and profitability when translated into USD.
*   **Geopolitical Stability:** Trade wars, political tensions, and international conflicts can disrupt global supply chains, impact international sales, and create uncertainty for businesses.
*   **Technological Advancements:** Rapid innovation in areas like AI, 5G, and edge computing creates both opportunities for Cisco to offer new solutions and threats from new entrants or disruptive technologies.
*   **Regulatory Environment:** Regulations related to data privacy, cybersecurity, antitrust, and international trade can impact Cisco's operations and market access.

### Conclusion:

Cisco Systems (CSCO) operates within a dynamic and complex financial ecosystem. Its financial health is closely linked to global economic conditions and enterprise IT spending. The company's strategic pivot towards software and recurring revenue models is crucial for future growth and margin expansion, but it also introduces it to new competitive pressures from software and cloud giants. Understanding the interplay between its financial performance, market dependencies, competitor landscape, and broader economic forces is essential for a comprehensive analysis of CSCO's stock. Investors should monitor its progress in transitioning to a software-led business, its ability to innovate and adapt to new technologies, and its resilience in the face of economic headwinds.

---

Summary (company in one line)
- Cisco Systems (CSCO) is a dominant, cash-generative networking-hardware company that has been shifting its mix toward software, subscriptions and security — a business exposed to enterprise, service-provider and public-sector IT/capex cycles, with strong recurring revenue and a capital-return focus (dividends + buybacks).

Note on currency and data
- Analysis based on facts and structural relationships known through June 2024. I do not have live price/quarterly numbers; any valuation or ratio references below are qualitative or directional. Check the latest 10-Q/earnings release for up-to-date metrics.

1) Business / revenue structure and key financial relationships
- Revenue mix: historically dominated by hardware (switches, routers, optics) with increasing contributions from software (subscriptions, licenses), security, and services. The trend toward higher-margin recurring revenue improves revenue visibility and supports multiple expansion.
- Gross margin and operating margin profile: hardware sales have lower margins than software/subscription and services; a shift to software tends to lift operating margins over time if hardware declines are offset.
- Cash flow: strong operating cash flow and free cash flow are structural strengths. This funds dividends, buybacks and acquisitions. FCF stability is aided by recurring revenue and large enterprise/customer contracts.
- Capital allocation: conservative balance sheet (investment-grade) with ongoing dividend and substantial buyback programs. M&A used strategically to acquire software/security capabilities.
- Booking metrics: bookings, backlog, deferred revenue and subscription renewal rates are important leading indicators of revenue and cash flows.

2) Product / segment drivers and their financial effects
- Campus/enterprise switching (Catalyst line) and wireless (including Aruba overlap via competition): tied to corporate LAN/Wi‑Fi refresh cycles and office reopening trends.
- Data center switching & routing (Nexus, UCS relationships): driven by cloud, hyper-scale/data center expansions and AI/ML workloads; optics and high-speed switches are higher ASP items that materially affect revenue and gross margin.
- Service provider / carrier routing: tied to telecom spend, 5G rollouts and edge infrastructure spending.
- Security and software (CX, Secure Access, Secure Firewall, SD-WAN, Intent-Based Networking): subscription revenue increases recurring revenue and improves gross margins. Growth here is critical for valuation as the market values recurring software more highly than hardware.
- Collaboration and Webex: competes with software providers; growth stabilizes recurring revenue but has stiff competition affecting pricing/ARPU.
- Channel & partners: Cisco sells heavily through an indirect channel (distributors, VARs, managed service providers). Channel inventory levels affect near-term revenue lumpyness.

3) Key competitors and relationships
- Arista Networks: primary competitor in cloud/data-center switching (high-speed Ethernet). Arista competes on performance and software-driven architectures.
- Juniper Networks: competitor across routing, switching and network OS; strong in service provider markets and software (Contrail).
- HPE/Aruba: strong in enterprise wireless/LAN and switching in SMB and enterprise markets.
- Extreme Networks, Huawei, Nokia (and Ericsson in carrier space): varying degrees of competition globally; Huawei remains a low-cost competitor in many non-US markets.
- Security peers: Palo Alto Networks, Fortinet, Check Point — compete in firewall, secure access and NGFW markets where Cisco is pushing to grow its software/security business.
- Virtualization/SW-defined: VMware (NSX) historically overlaps in virtualization and SDN; public cloud providers (AWS, Microsoft, GCP) both compete and buy from Cisco.
- Semiconductor/optics suppliers: Broadcom, Marvell, Intel, and others supply key ASICs/optical components. These suppliers are crucial to product roadmaps; pricing/availability directly impact margins and time-to-market.

4) Customers & channel dynamics
- Customer base: large enterprises, service providers/carriers, public sector/government and SMBs (via channels). Large carriers and cloud providers are meaningful customers but also strategic partners/competitors in some areas.
- Channel inventory and purchasing patterns: Cisco’s revenue can be lumpy due to channel stocking/unsticking and customer capex cycles. Watch channel inventory and distributor order trends in quarterly commentary.
- Geographical exposure: large share of revenue from Americas, EMEA, APAC — China exposure is material enough to be affected by US-China tensions and export controls.

5) Macro & regulatory dependencies
- Enterprise IT capex cycle: global GDP growth, corporate IT budgets and macro uncertainty (recession risk) directly influence hardware refresh and network upgrade spending.
- Interest rates: higher rates raise discount rates (lowering multiples) and can lead to reduced enterprise capex; they also increase borrowing costs for customers.
- Trade policy & export controls: US export restrictions to China (semiconductors/network equipment) can materially constrain sales and product functionality in China; compliance/regulatory risks exist.
- Supply chain/semiconductor cycle: shortages or price increases in ASICs, optics and other components affect product availability, ASPs and margins.
- Currency: FX fluctuations affect reported revenue and margins.
- Government/telco stimulus (5G, broadband spending): public programs for broadband/5G can be tailwinds.

6) Valuation and investor-relevant metrics to monitor
- Recurring revenue percentage and growth rate (subscriptions & services): rising recurring revenue typically supports re-rating.
- Software ARR / subscription bookings and renewal rates: ARR growth and churn are key to long-term cash flow stability.
- Book-to-bill and order trends: leading indicators of near-term revenue.
- Gross margin & operating margin trajectory: measure impact of software mix and cost control.
- Free cash flow and cash/debt balances: liquidity and ability to maintain dividends/buybacks and M&A capacity.
- R&D and SG&A trends: investment in software/security vs. cost discipline.
- Dividend coverage (FCF per share vs dividend) and buyback pace.
- Customer concentration / geographic revenue by region (especially China).

7) Strategic opportunities, catalysts
- Transition to software/subscription model: higher-margin, predictable revenue could drive multiple expansion if growth is demonstrated.
- Security and observability: acquisitions and internal growth can accelerate higher-margin recurring revenue.
- Cloud, data center and AI networking demand: growth in high-speed switching and optics for AI clusters is a potential revenue and ASP tailwind.
- 5G and edge computing: network modernization for telcos and private 5G deployments creates opportunities.
- Channel transformation and managed services growth: growth of Cisco+ and partner-managed offerings could increase sticky revenue.

8) Key risks and downside drivers
- Hardware commoditization and pricing pressure: reduced ASPs and margin compression.
- Aggressive competition (Arista, Juniper, HPE, cloud providers) leading to share loss or lower pricing.
- Macro downturn triggering capex cuts across enterprise and carriers.
- Export controls, geopolitical tensions and supply chain disruptions harming revenue in key markets (China).
- Execution risk in software transition: failing to grow ARR or integrate M&A.
- Customer consolidation toward cloud providers that bypass traditional network hardware vendors.
- Regulatory or legal risks (antitrust, IP litigation) and cybersecurity breaches that damage reputation.

9) Sector/market interconnections to watch
- Semiconductors & optics makers (Broadcom, Marvell) — cost/availability and potential supplier concentration.
- Cloud providers (AWS, Azure, GCP) — both customers and competitors; their on-prem offerings and white-box networking trends matter.
- Cybersecurity market dynamics — willingness of customers to consolidate security vendors or buy best-of-breed.
- Telecom capex cycles and government stimulus for broadband/5G.

10) Practical monitoring checklist (what to watch each quarter)
- Software & subscription revenue growth and ARR figures.
- Book-to-bill ratio, backlog and channel inventory commentary.
- Gross margin and operating margin trends (are margins improving as software mix grows?).
- Free cash flow, cash balance and net debt, and size of buyback/dividend programs.
- Large enterprise or carrier wins/losses and commentary on China exposure.
- R&D spend relative to revenue (deployment of software/security roadmap).
- Macro indicators: enterprise IT spend guidance, telco capex commentary, interest rates, and semiconductor lead times.
- Competitor earnings and product cycle announcements (Arista, Juniper, Palo Alto, Fortinet).

11) Scenario thinking (examples)
- Bull case: successful transition to >50% recurring revenue over time, strong ARR growth, expanding margins, continued FCF generation and multiple expansion due to software-like growth profile; data-center/AI optics demand accelerates revenue.
- Base case: modest software growth offsets hardware cyclicality, stable dividend and buybacks continue, slow single-digit revenue growth and steady margins.
- Bear case: macro-driven capex cuts and increased competition lead to hardware margin erosion, software growth disappoints, revenue declines and multiple contraction.

Bottom line
- Cisco is structurally advantaged by market leadership, a wide product portfolio, strong cash generation, and a large partner/channel ecosystem. The critical financial and strategic hinge points for future valuation are (1) the pace and profitability of the software/subscription transition, (2) data-center/AI optics and high-speed networking demand, and (3) exposure to macro/telco cycles and geopolitical constraints (notably China/export controls). Monitor ARR, bookings, margin trends, FCF and channel inventory as the most informative metrics for near-term and structural health.

If you want, I can:
- Pull the latest quarterly figures (revenue by segment, ARR, margins, FCF) if you give me a specific date or the latest report to reference.
- Produce a competitor peer-comps table with current multiples (P/E, EV/EBITDA) if you provide current market data or let me fetch it.

---

Of course. As a financial analysis expert, here is a comprehensive ecosystem analysis for **Cisco Systems, Inc. (CSCO)**.

### **1. Core Business & Financial Profile**
Cisco is the global leader in networking hardware, software, and services. Its core revenue drivers are:
*   **Infrastructure Platforms:** Switches, routers, wireless, and data center networking (comprising ~55% of revenue). This is the legacy cash cow.
*   **Applications & Security:** Collaboration (Webex), cybersecurity, and observability software (comprising ~30% of revenue). This is the strategic growth vector.
*   **Services:** Technical support and advisory services (comprising ~15% of revenue). This provides high-margin, recurring revenue.

**Key Financial Characteristics:** Mature, cash-rich, with a strong balance sheet. It has transitioned from pure hardware to a **software and subscription-based model** (Annual Recurring Revenue, or ARR, is a critical metric). Its generous dividend (current yield ~3.3%) and consistent share buybacks make it a "value" and "income" stock.

---

### **2. Key Market Dependencies & Sector Connections**
CSCO's performance is tied to several overarching market trends:

*   **Enterprise & Cloud Capital Expenditure (CapEx):** Cisco's fortunes rise and fall with the IT spending budgets of large corporations, governments, and service providers. Economic slowdowns that cause CapEx tightening are a direct headwind.
*   **Digital Transformation & Hybrid Work:** The permanent shift to hybrid work models drives demand for secure, agile networking (SD-WAN, SASE) and collaboration tools. This is a structural tailwind.
*   **Public Cloud vs. On-Premise (The "Cloud Dilemma"):** While cloud adoption (AWS, Azure, Google Cloud) initially threatened Cisco's on-premise hardware sales, Cisco has pivoted. It now provides networking for cloud data centers (with competitors like Arista) and *connects* enterprises to the cloud. Its strategy is "hybrid cloud."
*   **Cybersecurity Spending:** As a top player in network security (firewalls, zero-trust), Cisco benefits from the non-discretionary, ever-growing global cybersecurity market.
*   **Service Provider 5G Rollouts:** Investments in 5G infrastructure by telecom carriers drive demand for Cisco's routing and optical networking products.

---

### **3. Competitor Relationships (The Competitive Ecosystem)**
Cisco operates in a fiercely competitive landscape across its segments:

*   **Networking Hardware:**
    *   **Arista Networks (ANET):** The primary disruptor in high-speed data center switching, leveraging software-defined networking. A major threat in the core cloud provider space.
    *   **Juniper Networks (JNPR):** A direct, long-standing competitor in enterprise and service provider routing/switching.
    *   **Hewlett Packard Enterprise (HPE) / Aruba:** Strong competitor in enterprise wireless and campus networking.
    *   **Broadcom (AVGO) / Intel (INTC):** As chip suppliers, but also competitors in some merchant silicon.

*   **Security:**
    *   **Palo Alto Networks (PANW):** The pure-play leader in next-gen firewalls and security platforms, often out-innovating Cisco.
    *   **Fortinet (FTNT):** A strong competitor in unified threat management (UTM) and SD-WAN, known for cost-effectiveness.
    *   **CrowdStrike (CRWD), Zscaler (ZS):** Leaders in cloud-native security (endpoint, zero-trust network access), areas where Cisco is playing catch-up.

*   **Collaboration & Software:**
    *   **Microsoft (MSFT) Teams:** The dominant competitor to Webex, leveraging its ubiquitous Office 365 ecosystem.
    *   **Zoom Video Communications (ZM):** A pioneer in user-friendly video conferencing that took significant market share.
    *   **Software-Defined Networking (SDN):** Competes with VMware (now Broadcom) and a host of open-source and cloud-native software players.

**Cisco's M&A Strategy:** It has historically used its massive cash reserves to acquire growth and innovation (e.g., Splunk for observability/AI, Duo for zero-trust security), integrating them into its ecosystem.

---

### **4. Economic & Macroeconomic Factors**
*   **Interest Rates & Valuation:** As a mature, dividend-paying stock, CSCO is sensitive to interest rates. Higher rates make its yield less attractive relative to bonds, often putting pressure on its share price.
*   **Global Economic Health:** A global recession would lead to delayed or reduced enterprise IT spending, directly impacting Cisco's top line. It is a cyclical stock in this regard.
*   **Supply Chain & Geopolitics:** As a hardware manufacturer, Cisco is exposed to semiconductor shortages, logistics costs, and tariffs. Geopolitical tensions (e.g., US-China relations) affect its sales in key markets and its complex global supply chain.
*   **Foreign Exchange (FX):** With over 50% of revenue from outside the Americas, a strong US dollar negatively impacts reported earnings.

---

### **5. Forward-Looking Catalysts & Risks**
**Catalysts (Upside):**
1.  **Successful Integration of Splunk:** This $28B acquisition is transformative, giving Cisco unparalleled visibility into network and security data, enabling AI-driven insights.
2.  **Acceleration of Subscription Mix:** Higher software/subscription revenue improves margins, predictability, and valuation multiples.
3.  **AI Networking Demand:** The AI/ML boom requires massive, high-performance backend networks in data centers. Cisco's **Ethernet-based** strategy (competing with NVIDIA's InfiniBand) could see a major growth cycle.
4.  **Security Consolidation:** Enterprises prefer fewer security vendors. Cisco's integrated "security cloud" platform could gain share.

**Risks (Downside):**
1.  **Execution in a Shifting Market:** Failure to transition fast enough from hardware to software, or to fend off cloud-native competitors.
2.  **Increased Competition:** Relentless pressure from best-of-breed players like Arista, Palo Alto, and Microsoft in their respective domains.
3.  **Macroeconomic Slowdown:** A prolonged downturn in enterprise IT spending.
4.  **Integration Risk:** Large acquisitions (like Splunk) carry significant execution and cultural integration risks.

### **Conclusion: The Financial Ecosystem Summary**
**CSCO is a bellwether for global enterprise IT spending.** Its ecosystem is defined by the tension between its legacy, cash-generating hardware dominance and its strategic push into higher-growth, software-defined networking, security, and observability. Its stock performance is a function of:
*   **Macro Conditions** (IT CapEx cycles, interest rates),
*   **Competitive Execution** against more agile pure-plays,
*   **Successful Business Model Transition** to software/subscriptions, and
*   **Strategic Acquisitions** that plug innovation gaps.

It is no longer a high-growth tech stock but a **mature, financially stable company** navigating a pivotal transformation. Investors value it for its defensive qualities, strong cash flow, and shareholder returns, while watching closely for signs of durable growth in its software-defined future.
"""


def parse_analysis(text):
    """
    Parses the financial analysis text into a structured dictionary.
    Prioritizes the structured "expert analysis" for key metrics and lists.
    """
    sections = {}

    # --- Extract overarching summaries and notes ---
    summary_match = re.search(r"Summary \(company in one line\)\n- (.*)", text)
    sections["Summary (one line)"] = summary_match.group(1).strip() if summary_match else "N/A"

    note_match = re.search(r"Note on currency and data\n- (.*)", text, re.DOTALL)
    sections["Note on currency and data"] = note_match.group(1).strip() if note_match else "N/A"

    # --- Extract the "expert analysis" section (starts with "Of course. As a financial analysis expert...") ---
    expert_analysis_start_marker = "Of course. As a financial analysis expert,"
    expert_analysis_full_match = re.search(re.escape(expert_analysis_start_marker) + r"(.*)", text, re.DOTALL)

    if expert_analysis_full_match:
        expert_text = expert_analysis_full_match.group(1).strip()

        # Core Business & Financial Profile
        core_business_match = re.search(r"### \*\*1\. Core Business & Financial Profile\*\*(.*?)(?=\n### |\Z)", expert_text, re.DOTALL)
        if core_business_match:
            core_business_content = core_business_match.group(1).strip()
            sections["Core Business & Financial Profile"] = core_business_content

            # Revenue Mix from the expert analysis (e.g., ~55%)
            revenue_mix_pattern = r"\*   \*\*(.*?):\*\* .*?\(comprising ~(\d+)% of revenue\)"
            revenue_mix_data = re.findall(revenue_mix_pattern, core_business_content)
            sections["Revenue Mix"] = [{"segment": s, "percentage": int(p)} for s, p in revenue_mix_data]

            # Key Financial Characteristics
            key_financial_chars_match = re.search(r"^\*\*Key Financial Characteristics:\*\* (.*)", core_business_content, re.MULTILINE)
            sections["Key Financial Characteristics"] = key_financial_chars_match.group(1).strip() if key_financial_chars_match else "N/A"
            
        # Key Market Dependencies & Sector Connections
        market_deps_match = re.search(r"### \*\*2\. Key Market Dependencies & Sector Connections\*\*(.*?)(?=\n### |\Z)", expert_text, re.DOTALL)
        sections["Key Market Dependencies & Sector Connections"] = market_deps_match.group(1).strip() if market_deps_match else "N/A"

        # Competitor Relationships
        competitor_relationships_match = re.search(r"### \*\*3\. Competitor Relationships \(The Competitive Ecosystem\)\*\*(.*?)(?=\n### |\Z)", expert_text, re.DOTALL)
        if competitor_relationships_match:
            comp_content = competitor_relationships_match.group(1).strip()
            sections["Competitor Relationships (Expert)"] = comp_content

            # Structured Competitors from expert section
            structured_competitors = []
            segment_pattern = r"\*+\s*\*\*(.*?):\*\*\n((?:(?:\s+\*+)\s*\*+.*?\s*)+)"
            segments = re.findall(segment_pattern, comp_content)
            for segment_name, competitors_block in segments:
                # Corrected regex for competitor description, removing spurious `\*\*`
                competitors = re.findall(r"\*+\s*\*\*(.*?)\s*\(.*?\):\s*(.*)", competitors_block)
                for comp_name, comp_desc in competitors:
                    structured_competitors.append({
                        "Segment": segment_name.strip(),
                        "Competitor": comp_name.strip(),
                        "Description": comp_desc.strip()
                    })
            sections["Structured Competitors"] = structured_competitors


        # Economic & Macroeconomic Factors
        economic_factors_match = re.search(r"### \*\*4\. Economic & Macroeconomic Factors\*\*(.*?)(?=\n### |\Z)", expert_text, re.DOTALL)
        sections["Economic & Macroeconomic Factors (Expert)"] = economic_factors_match.group(1).strip() if economic_factors_match else "N/A"

        # Forward-Looking Catalysts & Risks
        catalysts_risks_match = re.search(r"### \*\*5\. Forward-Looking Catalysts & Risks\*\*(.*?)(?=\n### |\Z)", expert_text, re.DOTALL)
        if catalysts_risks_match:
            catalysts_risks_content = catalysts_risks_match.group(1).strip()
            
            catalysts_match = re.search(r"\*\*Catalysts \(Upside\):\*\*(.*?)(?=\n\*\*Risks \(Downside\):|\Z)", catalysts_risks_content, re.DOTALL)
            sections["Catalysts (Expert)"] = [item.strip() for item in catalysts_match.group(1).strip().split('\n') if item.strip()] if catalysts_match else []
            
            risks_match = re.search(r"\*\*Risks \(Downside\):\*\*(.*)", catalysts_risks_content, re.DOTALL)
            sections["Risks (Expert)"] = [item.strip() for item in risks_match.group(1).strip().split('\n') if item.strip()] if risks_match else []

        # Conclusion from the expert analysis
        expert_conclusion_match = re.search(r"### \*\*Conclusion: The Financial Ecosystem Summary\*\*(.*)", expert_text, re.DOTALL)
        sections["Expert Conclusion"] = expert_conclusion_match.group(1).strip() if expert_conclusion_match else "N/A"


    # --- Extract the detailed numbered sections (1) Business / revenue structure... etc.) ---
    # These sections start after the first '---' and before the 'Of course...' part
    detailed_sections_start = text.find("1) Business / revenue structure and key financial relationships")
    detailed_sections_end = text.find(expert_analysis_start_marker)
    
    if detailed_sections_start != -1 and detailed_sections_end != -1:
        detailed_text_block = text[detailed_sections_start:detailed_sections_end].strip()
        
        # Mapping for the numbered sections
        sections_map = {
            r"1\) Business / revenue structure and key financial relationships": "Business / Revenue Structure & Key Financial Relationships",
            r"2\) Product / segment drivers and their financial effects": "Product / Segment Drivers & Financial Effects",
            r"3\) Key competitors and relationships": "Key Competitors and Relationships (Detailed)",
            r"4\) Customers & channel dynamics": "Customers & Channel Dynamics",
            r"5\) Macro & regulatory dependencies": "Macro & Regulatory Dependencies",
            r"6\) Valuation and investor-relevant metrics to monitor": "Valuation & Investor Metrics",
            r"7\) Strategic opportunities, catalysts": "Strategic Opportunities / Catalysts (Detailed)",
            r"8\) Key risks and downside drivers": "Key Risks & Downside Drivers (Detailed)",
            r"9\) Sector/market interconnections to watch": "Sector/Market Interconnections",
            r"10\) Practical monitoring checklist \(what to watch each quarter\)": "Practical Monitoring Checklist",
            r"11\) Scenario thinking \(examples\)": "Scenario Thinking",
            r"Bottom line": "Bottom Line (Detailed)" 
        }
        
        # Regex to split content by these numbered headers
        # Use re.split with a lookahead assertion to keep the delimiter in the result
        section_splits = re.split(r"(?=\d+\)\s|Bottom line)", detailed_text_block)

        current_title_key = None
        for part in section_splits:
            part = part.strip()
            if not part:
                continue

            found_header = False
            for pattern, title in sections_map.items():
                if re.match(pattern, part):
                    current_title_key = title
                    # Remove the header line from the content
                    content = re.sub(pattern, "", part, count=1).strip()
                    sections[current_title_key] = content
                    found_header = True
                    break
            
            # Special case for "Bottom line" at the end of this block
            if not found_header and part.startswith("Bottom line"):
                 sections["Bottom Line (Detailed)"] = re.sub(r"Bottom line", "", part, count=1).strip()

        # Extract explicit key financial metrics from "Business / Revenue Structure & Key Financial Relationships"
        if "Business / Revenue Structure & Key Financial Relationships" in sections:
            metrics_text = sections["Business / Revenue Structure & Key Financial Relationships"]
            detailed_key_metrics = []
            
            # Patterns for bullet points (e.g., - Revenue mix: ...)
            metric_items = re.findall(r"^- (.*?):(.*)", metrics_text, re.MULTILINE)

            for metric_name, description in metric_items:
                detailed_key_metrics.append({
                    "Metric Category": "Business/Revenue Structure",
                    "Metric": metric_name.strip(),
                    "Description": description.strip()
                })
            sections["Extracted Key Metrics (Detailed)"] = detailed_key_metrics
            
        # Additional metrics from "6) Valuation and investor-relevant metrics to monitor"
        if "Valuation & Investor Metrics" in sections:
            val_metrics_text = sections["Valuation & Investor Metrics"]
            val_metric_items = re.findall(r"^- (.*?):(.*)", val_metrics_text, re.MULTILINE)
            if "Extracted Key Metrics (Detailed)" not in sections:
                sections["Extracted Key Metrics (Detailed)"] = []
            for metric, desc in val_metric_items:
                 sections["Extracted Key Metrics (Detailed)"].append({
                    "Metric Category": "Valuation & Investor",
                    "Metric": metric.strip(),
                    "Description": desc.strip()
                })

    return sections


# --- Streamlit App ---
def main():
    st.title("📈 Financial Ecosystem Analysis: Cisco Systems, Inc. (CSCO)")
    st.markdown("A comprehensive analysis of Cisco's financial health, market dependencies, and strategic outlook.")

    parsed_data = parse_analysis(ANALYSIS_TEXT)

    # --- Initial Summary and Note ---
    st.subheader("Company Snapshot")
    st.markdown(f"**{parsed_data.get('Summary (one line)', 'N/A')}**")
    st.info(f"**Note on Currency & Data:** {parsed_data.get('Note on currency and data', 'N/A')}")

    st.markdown("---")

    # --- Core Business & Financial Profile (from expert analysis) ---
    st.header("🔍 Core Business & Financial Profile")
    if "Core Business & Financial Profile" in parsed_data:
        # Split to separate the initial narrative from the Key Financial Characteristics bullet
        core_business_narrative = parsed_data["Core Business & Financial Profile"].split('**Key Financial Characteristics:**')[0].strip()
        st.markdown(core_business_narrative)
    
    # Key Financial Characteristics
    if "Key Financial Characteristics" in parsed_data:
        st.markdown(f"**Key Financial Characteristics:** {parsed_data['Key Financial Characteristics']}")

    # Revenue Mix Chart
    if "Revenue Mix" in parsed_data and parsed_data["Revenue Mix"]:
        st.subheader("📊 Revenue Mix")
        df_revenue_mix = pd.DataFrame(parsed_data["Revenue Mix"])
        
        chart = alt.Chart(df_revenue_mix).mark_bar().encode(
            x=alt.X("percentage", type="quantitative", title="Percentage (%)", axis=alt.Axis(format=".0f")),
            y=alt.Y("segment", type="nominal", title="Revenue Segment", sort="-x"),
            tooltip=["segment", "percentage"]
        ).properties(
            title="Cisco's Core Revenue Drivers (Approximate Mix)"
        )
        st.altair_chart(chart, use_container_width=True)
    
    st.markdown("---")

    # --- Key Financial Relationships & Performance Metrics (from detailed section) ---
    st.header("💰 Key Financial Relationships & Performance Metrics")
    if "Extracted Key Metrics (Detailed)" in parsed_data and parsed_data["Extracted Key Metrics (Detailed)"]:
        df_metrics = pd.DataFrame(parsed_data["Extracted Key Metrics (Detailed)"])
        df_metrics.index = df_metrics.index + 1 # 1-based indexing for display
        st.dataframe(df_metrics, use_container_width=True)
    
    with st.expander("Show Full Business / Revenue Structure & Key Financial Relationships"):
        st.markdown(parsed_data.get("Business / Revenue Structure & Key Financial Relationships", "No detailed text available."))

    st.markdown("---")

    # --- Market Dependencies & Sector Connections ---
    st.header("🌐 Market Dependencies & Sector Connections")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Market Dependencies")
        if "Key Market Dependencies & Sector Connections" in parsed_data:
            # Extract bullet points from the expert summary for concise display
            market_deps_text = parsed_data["Key Market Dependencies & Sector Connections"]
            market_deps_bullet_points = re.findall(r"\*   \*\*(.*?)\*\*: (.*)", market_deps_text)
            if market_deps_bullet_points:
                for dep, desc in market_deps_bullet_points:
                    st.markdown(f"- **{dep.strip()}:** {desc.strip()}")
            else: 
                 st.markdown(parsed_data.get("Market Dependencies (Detailed)", "No market dependencies text available."))

    with col2:
        st.subheader("Sector Connections")
        if "Sector Connections (Detailed)" in parsed_data:
            st.markdown(parsed_data["Sector Connections (Detailed)"])
    st.markdown("---")

    # --- Competitor Relationships ---
    st.header("🤝 Competitor Relationships")
    st.markdown("Cisco operates in a fiercely competitive landscape across its segments.")

    if "Structured Competitors" in parsed_data and parsed_data["Structured Competitors"]:
        df_competitors = pd.DataFrame(parsed_data["Structured Competitors"])
        df_competitors.index = df_competitors.index + 1
        st.dataframe(df_competitors, use_container_width=True)

    with st.expander("View More Competitors & Detailed Relationships"):
        st.markdown(parsed_data.get("Key Competitors and Relationships (Detailed)", "No detailed text available."))

    st.markdown("---")

    # --- Economic & Macroeconomic Factors ---
    st.header("🌍 Economic & Macroeconomic Factors")
    if "Economic & Macroeconomic Factors (Expert)" in parsed_data:
        st.markdown(parsed_data["Economic & Macroeconomic Factors (Expert)"])
    else:
        st.markdown(parsed_data.get("Macro & Regulatory Dependencies", "No detailed economic factors available."))
    st.markdown("---")

    # --- Forward-Looking Catalysts & Risks ---
    st.header("🎯 Forward-Looking Catalysts & Risks")
    col_catalysts, col_risks = st.columns(2)

    with col_catalysts:
        st.subheader("🚀 Catalysts (Upside)")
        if "Catalysts (Expert)" in parsed_data and parsed_data["Catalysts (Expert)"]:
            for i, catalyst in enumerate(parsed_data["Catalysts (Expert)"]):
                st.markdown(f"{i+1}. {catalyst}")
        else:
            st.markdown(parsed_data.get("Strategic Opportunities / Catalysts (Detailed)", "No specific catalysts identified."))

    with col_risks:
        st.subheader("🚧 Risks (Downside)")
        if "Risks (Expert)" in parsed_data and parsed_data["Risks (Expert)"]:
            for i, risk in enumerate(parsed_data["Risks (Expert)"]):
                st.markdown(f"{i+1}. {risk}")
        else:
            st.markdown(parsed_data.get("Key Risks & Downside Drivers (Detailed)", "No specific risks identified."))
    st.markdown("---")
    
    # --- Other Detailed Sections ---
    st.header("📋 Additional Detailed Analysis Areas")

    if "Product / Segment Drivers & Financial Effects" in parsed_data:
        with st.expander("Product / Segment Drivers & Financial Effects"):
            st.markdown(parsed_data["Product / Segment Drivers & Financial Effects"])

    if "Customers & Channel Dynamics" in parsed_data:
        with st.expander("Customers & Channel Dynamics"):
            st.markdown(parsed_data["Customers & Channel Dynamics"])

    if "Sector/Market Interconnections" in parsed_data:
        with st.expander("Sector/Market Interconnections to Watch"):
            st.markdown(parsed_data["Sector/Market Interconnections"])

    if "Practical Monitoring Checklist" in parsed_data:
        with st.expander("Practical Monitoring Checklist (What to Watch Each Quarter)"):
            st.markdown(parsed_data["Practical Monitoring Checklist"])

    if "Scenario Thinking" in parsed_data:
        with st.expander("Scenario Thinking (Examples)"):
            st.markdown(parsed_data["Scenario Thinking"])
    st.markdown("---")

    # --- Overall Conclusion ---
    st.header("✔️ Overall Conclusion & Bottom Line")
    if "Expert Conclusion" in parsed_data:
        st.markdown(parsed_data["Expert Conclusion"])
    else: 
        st.markdown(parsed_data.get("Bottom Line Summary", "No overall conclusion available."))
        st.markdown(parsed_data.get("Bottom Line (Detailed)", ""))

    st.markdown("""
        ---
        _Analysis based on the provided text. For up-to-date metrics, always consult the latest official financial reports._
    """)

if __name__ == "__main__":
    main()