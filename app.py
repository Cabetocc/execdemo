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
import re
import plotly.express as px

# The complete financial analysis text
ANALYSIS_TEXT = """
Let's dive into a comprehensive financial ecosystem analysis of IBM (International Business Machines Corporation).

## IBM (International Business Machines Corporation) Financial Ecosystem Analysis

IBM is a long-standing technology giant with a complex and evolving business model. Its financial ecosystem is shaped by a combination of internal strategic shifts, industry-wide trends, competitive pressures, and broader macroeconomic forces.

### 1. Key Financial Relationships (Internal & Operational)

*   **Revenue Streams:** IBM's revenue is diversified across several key segments:
    *   **Hybrid Cloud:** This is IBM's strategic focus and a significant growth driver, encompassing Red Hat, cloud platform services, and consulting.
    *   **Software:** Includes middleware, transaction processing software, and other enterprise software solutions.
    *   **Consulting:** Leverages IBM's expertise to help clients with digital transformation, cloud adoption, and business process re-engineering.
    *   **Infrastructure:** Includes mainframe systems, servers, and storage solutions, a more mature but still vital segment.
*   **Profitability & Margins:**
    *   **Gross Margins:** Vary significantly by segment. Software and consulting generally command higher gross margins than infrastructure.
    *   **Operating Margins:** Influenced by R&D expenses, sales & marketing, and general & administrative costs. IBM's focus on higher-margin software and cloud services aims to improve overall operating margins.
    *   **Net Income:** Affected by operational performance, interest expenses on debt, and taxes.
*   **Capital Allocation:**
    *   **R&D Investment:** Crucial for maintaining competitiveness in the rapidly evolving tech landscape, particularly in AI, quantum computing, and cloud technologies.
    *   **Acquisitions:** Strategic acquisitions, like Red Hat, have been pivotal in reshaping IBM's portfolio and driving its hybrid cloud strategy.
    *   **Share Buybacks & Dividends:** Historically, IBM has been a strong dividend payer, appealing to income-focused investors. While growth is the primary focus, capital returns remain a consideration.
*   **Debt and Leverage:** IBM carries a significant amount of debt. Its ability to manage this debt through consistent cash flow generation is critical for financial stability and investor confidence. The interest coverage ratio is a key metric to monitor.
*   **Cash Flow Generation:** IBM is known for its strong free cash flow generation, a testament to its established enterprise client base and diversified revenue. This cash flow is essential for funding R&D, acquisitions, and shareholder returns.

### 2. Market Dependencies

*   **Enterprise Spending Cycles:** IBM's revenue is highly dependent on the IT spending budgets of large enterprises. During economic downturns, these budgets can be cut, impacting IBM's sales. Conversely, in periods of economic growth and digital transformation initiatives, spending tends to increase.
*   **Digital Transformation:** The ongoing trend of businesses digitizing their operations and migrating to cloud environments is a primary market driver for IBM's hybrid cloud and consulting segments.
*   **AI and Automation Adoption:** The increasing adoption of Artificial Intelligence (AI) and automation technologies by businesses creates opportunities for IBM's software, consulting, and infrastructure solutions.
*   **Cloud Computing Adoption (Hybrid & Multi-Cloud):** While hyperscalers dominate public cloud, IBM's focus on hybrid and multi-cloud solutions caters to enterprises that require flexibility, data sovereignty, and integration with on-premises systems.
*   **Cybersecurity Needs:** As digital footprints expand, so do cybersecurity threats. This drives demand for IBM's security-related software and consulting services.

### 3. Sector Connections

*   **Technology Sector:** IBM is a foundational player in the broader technology sector, encompassing:
    *   **Software:** Competing with established players and cloud-native companies.
    *   **Cloud Computing:** Both public (indirectly) and private/hybrid cloud infrastructure and services.
    *   **IT Services & Consulting:** A major segment, interacting with clients across all industries.
    *   **Hardware:** Though its market share has shifted, it remains a player in enterprise servers and mainframes.
*   **Business Services Sector:** The consulting arm places IBM firmly within the business services sector, offering strategic and operational advice to other corporations.
*   **Telecommunications:** IBM's infrastructure and software solutions are vital for many telecommunications companies.
*   **Financial Services:** This is a major customer base for IBM, utilizing its technology for core banking, trading, and data analytics.

### 4. Competitor Relationships

IBM operates in a highly competitive landscape. Its key competitors vary by business segment:

*   **Hybrid Cloud:**
    *   **Microsoft (Azure):** Strong hybrid cloud offerings and a deep enterprise relationship.
    *   **Amazon Web Services (AWS):** Dominant in public cloud, but also offers hybrid solutions.
    *   **Google Cloud Platform (GCP):** Growing rapidly with strong AI and data analytics capabilities.
    *   **Oracle:** Offers cloud infrastructure and a strong software suite.
    *   **VMware:** A key player in virtualization and hybrid cloud management.
*   **Software:**
    *   **Microsoft (Office, Dynamics, Azure services):** Direct competitor in many enterprise software categories.
    *   **SAP:** Dominant in enterprise resource planning (ERP) and business intelligence.
    *   **Oracle:** Strong in database and enterprise applications.
    *   **Salesforce:** Leading CRM provider.
    *   **Various specialized software vendors:** Depending on the specific software category (e.g., security, data analytics).
*   **Consulting:**
    *   **Accenture:** A direct and major competitor in IT consulting and digital transformation.
    *   **Deloitte, PwC, EY, KPMG (Big Four):** Strong consulting arms that compete across various IT and business advisory services.
    *   **Capgemini, Cognizant, Wipro, TCS:** Other large IT services and consulting firms.
*   **Infrastructure:**
    *   **Dell Technologies, HP Enterprise:** Competitors in servers and storage.
    *   **Mainframe Market:** IBM is a dominant player, but the overall market is niche and faces competition from alternative architectures.

IBM's strategy often involves leveraging its deep existing enterprise relationships and its comprehensive portfolio (software, hardware, services) to offer integrated solutions, differentiating it from more specialized competitors.

### 5. Economic Factors

*   **Global Economic Growth/Recession:** Directly impacts enterprise IT spending. A strong economy fuels investment in new technologies and digital transformation, benefiting IBM. A recession leads to budget cuts and delayed projects.
*   **Interest Rates:** Higher interest rates increase the cost of borrowing, affecting companies with significant debt like IBM, and can also dampen overall business investment.
*   **Inflation:** Can increase operating costs for IBM and its clients, potentially impacting margins. However, IBM's pricing power in some software segments might allow it to pass on some costs.
*   **Geopolitical Stability:** Global conflicts or trade tensions can disrupt supply chains, impact international sales, and create uncertainty, leading enterprises to be more cautious with their IT investments.
*   **Currency Fluctuations:** As a global company, IBM's earnings are affected by the strength and weakness of various currencies relative to the US dollar.
*   **Technological Advancements (Pace of Innovation):** Rapid advancements in AI, quantum computing, and cloud technologies create both opportunities and threats. Companies that fail to innovate quickly risk becoming obsolete. IBM's significant R&D investment is a response to this factor.
*   **Regulatory Environment:** Data privacy regulations (e.g., GDPR, CCPA), antitrust scrutiny of tech giants, and export controls can all impact IBM's operations and strategic decisions.

### Conclusion: IBM's Financial Ecosystem

IBM operates within a mature yet dynamically evolving technological landscape. Its **strategic pivot towards hybrid cloud and AI** is crucial for navigating the intense competition and dependency on enterprise spending cycles. The **acquisition of Red Hat** was a landmark move to strengthen its hybrid cloud position.

IBM's **financial health is anchored by its strong free cash flow generation and its established relationships with a vast enterprise client base**. However, it must continuously manage its **significant debt burden** and demonstrate consistent growth in its strategic segments to justify its valuation and appeal to investors.

The company's **competitors are formidable**, spanning cloud giants, specialized software vendors, and large consulting firms. IBM's success hinges on its ability to leverage its integrated portfolio and deep industry expertise to provide differentiated value.

Finally, **macroeconomic conditions and the relentless pace of technological innovation** are constant external forces that IBM must adeptly respond to. Its ability to adapt, innovate, and execute its hybrid cloud strategy will be paramount to its continued relevance and financial success in the coming years.

---

Below is a comprehensive, practical view of IBM’s financial ecosystem: the company’s core revenue relationships, market dependencies, sector and competitor linkages, strategic partnerships, macro and regulatory drivers, and the key financial metrics and risks investors should watch.

Company overview and strategic pillars
- Business model: enterprise software, IT infrastructure (hardware, systems), and professional services/consulting. IBM’s strategic focus for the last several years has been on higher‑margin software and hybrid‑cloud + AI services (Red Hat integration, watsonx, managed services), after spinning off Kyndryl (managed infrastructure services).
- Revenue mix (structural): recurring software/subscription and support; professional services (consulting, integration); infrastructure (mainframes, servers, storage); financing and other. The company aims to grow software/recurring revenue share and monetize AI/hybrid-cloud enterprise workloads.

Key market dependencies and demand drivers
- Corporate IT spending and digital transformation cycles: IBM’s top-line moves with enterprise IT budgets (banks, telcos, retail, manufacturing, government). Economic slowdown or IT budget freezes materially reduce consulting and transformation engagements.
- Cloud adoption and hybrid cloud: growth depends on enterprises’ willingness to adopt hybrid/multi‑cloud architectures (on‑prem + private + public cloud). IBM’s Red Hat is a strategic asset here (OpenShift).
- Enterprise AI spending: demand for AI model development, data platforms, model ops, and trusted/secure on‑prem or hybrid deployments drives software/service revenue if IBM can win enterprise AI deals.
- Interest rates and cost of capital: impact IBM’s interest expense on outstanding debt and discount rates used by investors; higher rates also pressure corporate capex and M&A activity.
- FX exposure: significant global revenue leads to sensitivity to USD strength (strong USD depresses reported revenue when converted).

Sector connections and ecosystem
- Open-source and middleware ecosystem: Red Hat (RHEL/OpenShift/Ansible) is central—ties to Kubernetes, Linux ecosystem, enterprise middleware (JBoss), and developer communities.
- Hardware supply chain: mainframes (z Systems), Power systems, storage depend on semiconductor supply, vendor contracts (chip fabs, component suppliers).
- Services ecosystem: consulting, system integrators, outsourcers (partners/resellers) — IBM both competes with and relies on partner channels to sell integrated solutions.
- Data/security stack: integrations with databases, analytics, security vendors; regulatory compliance and data-residency needs favor hybrid approaches in some industries.

Primary competitors and positioning
- Cloud providers: Amazon Web Services, Microsoft Azure, Google Cloud — dominate public cloud and attract greenfield workloads. IBM is smaller but competes in hybrid/multi‑cloud and regulated workloads.
- Enterprise software vendors: Oracle, SAP, Microsoft (Dynamics/SQL/Power Platform), VMware — competing in enterprise apps, databases, virtualization, and cloud stacks.
- IT services & consulting firms: Accenture, Capgemini, Cognizant, TCS, DXC — compete for large transformation/outsourcing contracts.
- Hardware/Solutions vendors: Hewlett Packard Enterprise, Dell EMC, Cisco, Fujitsu — competing in servers, storage, networking and infrastructure.
- Cloud-native entrants & SaaS specialists: numerous vertical SaaS and cloud‑native platforms taking share of new workloads.
- IBM’s advantage: legacy enterprise relationships, Red Hat’s open-source credibility and hybrid-cloud tech, industry-specific knowledge (financial services, telco), and deep security/regulated-market experience. Weaknesses: smaller public-cloud scale, legacy business tail (mainframes), and previous execution challenges with AI products.

Strategic partnerships and alliances
- Red Hat integration: core to IBM’s hybrid-cloud play—ties to Kubernetes/OpenShift, enterprise open-source ecosystems, and channel partners.
- Technology partnerships: joint work with NVIDIA (AI infrastructure), major ISVs (SAP, Oracle) for co‑selling and certification, and industry-specific alliances (banks, telecoms).
- Channel/partner network: global systems integrators, resellers, and MSPs that extend sales reach and deliver implementations.

Financial relationships and capital allocation
- Revenue quality: mix trending toward higher‑margin, recurring software and subscription revenue, but services and systems still significant. Track recurring revenue % and multi‑year contract bookings.
- Margins: software > services > hardware — continued shift to software should improve gross/operating margins if growth and pricing hold.
- Cash flow: historically strong operating cash flow and free cash flow that supports dividends and buybacks. Capital allocation priorities include R&D, M&A (targeted, e.g., Red Hat), dividends, and buybacks.
- Balance sheet: meaningful debt load at times from acquisitions; watch net debt / adjusted EBITDA and pension obligations (legacy defined‑benefit plans) for leverage and cash outflow risk.
- Shareholder returns: historically consistent dividend payer (attractive yield vs. many tech companies) and opportunistic buybacks. Investors view IBM as income + value play transitioning to growth in software/AI.

Regulatory/legal and geopolitical factors
- Data protection/privacy and localization laws: GDPR, sectoral regulations in finance/healthcare can favor IBM’s hybrid/on‑prem solutions.
- Export controls and sanctions: AI compute, advanced chips, and software exports can be restricted; affects partnerships with certain customers or vendors.
- Antitrust / M&A scrutiny: large deals (e.g., Red Hat) attract regulatory attention and require careful integration planning.

Economic and macro sensitivities
- Recession sensitivity: consulting and new projects often cut first in downturns; large renewal contracts and mission‑critical systems are stickier.
- Interest rate cycles: higher rates increase financing costs and can depress enterprise capex; also pressure valuations.
- Currency fluctuations: strong USD reduces reported international revenues; hedging strategies and geographic mix matter.

Key performance indicators (KPIs) to monitor
- Revenue growth: overall and by segment (Cloud & Cognitive Software, Consulting/Services, Systems).
- Red Hat revenue growth and OpenShift adoption metrics.
- Recurring/contracted revenue % and subscription backlog.
- Gross margin and operating margin trends (showing shift to software).
- Free cash flow and operating cash conversion (FCF/Net income).
- Net debt / EBITDA and pension funding status.
- Large deal wins (multi‑year cloud/AI contracts) and retention of key legacy customers.
- R&D and SG&A as % of revenue (investment vs. cost discipline).
- Dividend coverage and buyback pace.

Risks
- Competitive pressure from hyperscalers and larger SaaS vendors eroding IBM’s addressable market share.
- Execution risk integrating and monetizing Red Hat and new AI offerings (watsonx), and converting consulting engagements into recurring revenue.
- Legacy mainframe business decline faster than growth in high-margin segments.
- High leverage or pension drain limiting capital flexibility.
- Technology shifts (cloud‑native, serverless) that reduce demand for integrated systems/large consult projects.
- Regulatory hurdles or geopolitical restrictions that disrupt global operations.

Opportunities
- Enterprise AI and hybrid-cloud adoption: IBM can sell AI platforms (watsonx), model ops, data governance, and trusted AI to regulated industries.
- Migration and modernization projects for large enterprises moving to hybrid architectures—Red Hat+IBM consulting can capture significant deal value.
- High-margin software subscriptions and SaaS conversions improving margins and predictability.
- Strategic partnerships with GPU/AI suppliers (e.g., NVIDIA) and ISVs to capture AI infrastructure + software revenue.
- Cost savings and portfolio pruning following Kyndryl spin and focus on core software/services.

Scenario framing (simple)
- Bull case: successful monetization of Red Hat + watsonx, strong enterprise AI adoption, margin expansion from software mix, continuing strong cash flow funds dividends and buybacks — equity re‑rating.
- Base case: modest software growth offsetting declines in legacy segments, slow but steady margin improvement, steady cash returns to shareholders.
- Bear case: hyperscalers win hybrid/cloud AI deals, IBM’s offerings underperform, legacy declines accelerate, meaningfully lower revenue and pressure on margins and cash flow.

Practical investor checklist (what to watch next)
- Quarterly revenue and margin breakdown by segment; Red Hat growth rate.
- Announcements of multi‑year cloud/AI contracts or industry-specific wins.
- Trends in recurring revenue / subscription bookings and retention rates.
- Changes in net debt, pension cash requirements, and free cash flow.
- Guidance on capital allocation: dividend policy and share repurchase programs.
- Management commentary on competitive wins vs. AWS/Azure/GCP and partner strategy.
- Macro indicators: enterprise IT spend surveys, interest rates, and currency moves.

Summary
IBM sits at the intersection of legacy enterprise IT (mainframes, services) and the future of hybrid-cloud + enterprise AI. Its financial ecosystem is shaped by large enterprise customer relationships, Red Hat’s open-source stack, competition from hyperscalers and global consultancies, and macro forces that drive IT budgets. The investment thesis rests on IBM’s ability to convert its installed base and Red Hat platform into recurring, high‑margin software and AI revenue while managing legacy decline and leverage. Key metrics to watch: software/recurring revenue growth, margins, free cash flow, net debt/pension trends, and large AI/cloud contract wins.

---

Of course. As a financial analysis expert, here is a comprehensive ecosystem analysis of International Business Machines (IBM).

### **Core Business & Strategic Identity**
IBM has transformed from a hardware-centric "Big Iron" company into a hybrid technology and consulting powerhouse. Its current identity is built on two pillars:
1.  **Hybrid Cloud & AI:** Primarily through its strategic acquisition of Red Hat, positioning it as a key player in open-source, multi-cloud environments.
2.  **Enterprise Consulting & Software:** Providing mission-critical software and services to large, established corporations and governments.

This shift is encapsulated in its spinoff of its legacy IT infrastructure services unit into **Kyndryl (KD)** in 2021, allowing IBM to focus on higher-growth, higher-margin areas.

---

### **Key Financial Relationships & Metrics**

*   **Revenue Streams:** IBM reports in four key segments:
    *   **Software (42% of 2023 revenue):** The growth and margin engine. Includes Red Hat, Automation, Data & AI, and Security.
    *   **Consulting (31%):** Steady, recurring revenue tied to digital transformation projects. Margin pressure is a constant watch item.
    *   **Infrastructure (25%):** Includes legacy mainframes (which have cyclical refresh cycles) and distributed infrastructure. Lower growth but generates strong cash flow.
    *   **Financing (2%):** A smaller segment supporting client purchases.
*   **Profitability & Cash Flow:** Investors focus on **Free Cash Flow** as a key metric. IBM has a long history of generating robust FCF, which it uses to fund its dividend, make acquisitions, and reduce debt. The transition to a software-centric model aims to improve operating margins over time.
*   **Balance Sheet:** The Red Hat acquisition significantly increased IBM's debt load. A key financial relationship is its commitment to **debt reduction** while maintaining its **dividend aristocrat status** (28+ years of consecutive annual dividend increases).

---

### **Market Dependencies & Economic Factors**

IBM's stock is highly sensitive to:
1.  **Enterprise IT Spending:** As a B2B company, its fortunes are directly tied to the capital expenditure budgets of large global enterprises. In economic downturns, these budgets are often cut or delayed, impacting Consulting and Software sales.
2.  **Interest Rates:** High interest rates increase the cost of servicing its substantial debt and can dampen the valuation of its long-duration cash flows (typical for mature tech stocks). Conversely, they make its dividend yield relatively more attractive.
3.  **Foreign Exchange (FX):** Over 50% of IBM's revenue comes from outside the Americas. A strong U.S. dollar negatively translates overseas earnings back to USD, a headwind often cited in earnings reports.
4.  **Technology Adoption Cycles:** Demand for mainframes is "lumpy," with peaks during product refresh cycles. The adoption rate of hybrid cloud and AI platforms among its traditional client base is a critical growth driver.

---

### **Sector Connections & Competitor Relationships**

IBM operates at the intersection of multiple competitive landscapes:

*   **Hybrid Cloud & Platform Software:**
    *   **Primary Competitors:** **Microsoft (MSFT)** with Azure/Windows Server, **Amazon (AMZN)** with AWS, and **Google (GOOGL)** with Google Cloud. These are its most significant and aggressive competitors, with vast scale and capital.
    *   **IBM's Niche:** Unlike the "hyperscalers," IBM does not aim to be the largest public cloud. Its strategy is to manage workloads *across* AWS, Azure, Google Cloud, and private data centers using Red Hat's OpenShift platform. Its main competitor here is **VMware (now part of Broadcom)**.

*   **Enterprise Consulting & IT Services:**
    *   **Primary Competitors:** **Accenture (ACN)**, **Deloitte**, **Infosys (INFY)**, and **TCS**. Accenture is often seen as the gold standard in this space, against which IBM Consulting's growth and margins are compared.

*   **Enterprise AI & Automation Software:**
    *   **Primary Competitors:** A fragmented field including **ServiceNow (NOW)**, **Palantir (PLTR)** for certain AI platforms, and niche players. IBM's **watsonx** platform competes here, leveraging its brand and research heritage.

*   **Legacy Infrastructure:**
    *   **Primary Competitors:** **Dell Technologies (DELL)**, **Hewlett Packard Enterprise (HPE)**, and **Oracle (ORCL)** for integrated systems.

---

### **Strategic Partnerships & Ecosystem**
*   **Hyperscaler Alliances:** Ironically, IBM has deep partnerships with its cloud competitors (AWS, Microsoft Azure, Google Cloud) to offer Red Hat and IBM software on their marketplaces. This is a classic "co-opetition" relationship.
*   **Strategic Consultants:** Firms like **Accenture** and **Deloitte** are both competitors and partners, often implementing IBM software for joint clients.
*   **Kyndryl (KD):** The spun-off company remains IBM's largest client and a critical channel to market for IBM's software. Their success is interdependent in the near-to-medium term.

### **Investment Thesis Summary: Bull vs. Bear**

*   **Bull Case:** IBM is a **value play with a turnaround narrative**. It offers a high dividend yield (~4%), trades at a discount to the broader software market, and is successfully pivoting to higher-growth hybrid cloud and AI via Red Hat and watsonx. Its focus on mission-critical systems for "boring" but essential industries (finance, government, telecom) provides defensive stability.
*   **Bear Case:** IBM is a **value trap**. It is a slow-growth legacy operator in markets dominated by faster, nimbler, and better-capitalized giants like Microsoft and Amazon. Its consulting business faces margin pressure, mainframe revenue is declining long-term, and debt remains elevated. The transition may be too little, too late.

**Conclusion:** IBM's stock is a bet on the execution of its hybrid cloud and AI strategy within its massive, sticky, but slow-moving enterprise client base. Its performance is less about flashy consumer tech and more about the steady, complex digital modernization of the world's established corporations. Its financial health is closely watched through Free Cash Flow generation, debt management, and software revenue growth, all while navigating intense competition and macroeconomic headwinds.
"""

# Helper function to extract key metrics
def extract_key_metrics(text):
    metrics = {}

    # Revenue Mix (from the last detailed section, which explicitly states "42% of 2023 revenue")
    # This section starts with "### **Key Financial Relationships & Metrics**"
    revenue_mix_section_match = re.search(
        r"### \*\*Key Financial Relationships & Metrics\*\*.*?(\*   \*\*Revenue Streams:.*?)(\n\n|\Z)", 
        text, 
        re.DOTALL
    )
    if revenue_mix_section_match:
        revenue_mix_text = revenue_mix_section_match.group(1)
        software_match = re.search(r"Software \((\d+)% of \d{4} revenue\)", revenue_mix_text)
        consulting_match = re.search(r"Consulting \((\d+)%\)", revenue_mix_text)
        infrastructure_match = re.search(r"Infrastructure \((\d+)%\)", revenue_mix_text)
        financing_match = re.search(r"Financing \((\d+)%\)", revenue_mix_text)

        if software_match:
            metrics['Software Revenue Share'] = float(software_match.group(1))
        if consulting_match:
            metrics['Consulting Revenue Share'] = float(consulting_match.group(1))
        if infrastructure_match:
            metrics['Infrastructure Revenue Share'] = float(infrastructure_match.group(1))
        if financing_match:
            metrics['Financing Revenue Share'] = float(financing_match.group(1))

    # Dividend Yield
    dividend_yield_match = re.search(r"high dividend yield \~?\(?(\d+\.?\d*)%\)?", text)
    if dividend_yield_match:
        metrics['Dividend Yield'] = float(dividend_yield_match.group(1))
    
    # Dividend Aristocrat Status
    dividend_aristocrat_match = re.search(r"dividend aristocrat status \((\d+\+ years of consecutive annual dividend increases)\)", text)
    if dividend_aristocrat_match:
        metrics['Dividend Aristocrat Status'] = dividend_aristocrat_match.group(1)
    
    # Financial Focus
    financial_focus_match = re.search(r"commitment to \*\*debt reduction\*\* while maintaining its \*\*dividend aristocrat status\*\*", text)
    if financial_focus_match:
        metrics['Financial Focus'] = "Debt Reduction & Dividend Maintenance"

    # Kyndryl Spinoff Year
    kyndryl_spinoff_match = re.search(r"its spinoff of its legacy IT infrastructure services unit into \*\*Kyndryl \(KD\)\*\* in (\d{4})", text)
    if kyndryl_spinoff_match:
        metrics['Kyndryl Spinoff Year'] = int(kyndryl_spinoff_match.group(1))
        
    return metrics

# Function to parse the analysis text into logical blocks based on '---' separators
def parse_analysis_into_logical_blocks(text):
    blocks = []
    
    # Split by the horizontal rules '---'
    parts = re.split(r'\n---\n', text)
    
    # Block 1: Initial Comprehensive Financial Ecosystem Analysis
    blocks.append({
        "title": "Comprehensive Financial Ecosystem Analysis (Initial)",
        "content": parts[0].strip()
    })
    
    # Block 2: Comprehensive, Practical View of IBM’s Financial Ecosystem
    if len(parts) > 1:
        blocks.append({
            "title": "Comprehensive, Practical View of IBM’s Financial Ecosystem",
            "content": parts[1].strip()
        })

    # Block 3: Expert's Ecosystem Analysis (Summary/Thesis)
    if len(parts) > 2:
        blocks.append({
            "title": "Expert's Ecosystem Analysis & Investment Thesis",
            "content": parts[2].strip()
        })
        
    return blocks

# Function to further split content within a logical block by ### headers
def split_block_by_h3(block_content):
    subsections = {}
    
    # Split by ### headers, keeping the delimiters
    parts = re.split(r'(###\s.+)', block_content)
    
    intro_content = parts[0].strip() # Content before the first ###, if any
    
    current_h3_header = None
    current_h3_content = []

    for i in range(1, len(parts)):
        part = parts[i].strip()
        if part.startswith('###'):
            if current_h3_header: # Save previous subsection before starting a new one
                subsections[current_h3_header] = "\n".join(current_h3_content).strip()
            current_h3_header = part
            current_h3_content = [] # Reset content for new subsection
        else:
            current_h3_content.append(part)
    
    # Save the last subsection after the loop
    if current_h3_header:
        subsections[current_h3_header] = "\n".join(current_h3_content).strip()
            
    return intro_content, subsections


# --- Streamlit App ---
st.set_page_config(layout="wide", page_title="IBM Financial Ecosystem Analysis")

st.title("💰 IBM Financial Ecosystem Analysis")
st.markdown("A deep dive into International Business Machines Corporation's financial landscape.")

# Extract Key Metrics
metrics = extract_key_metrics(ANALYSIS_TEXT)

st.subheader("📊 Key Financial Snapshot")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Important Metrics")
    if metrics:
        st.write(f"**Software Revenue Share (2023):** {metrics.get('Software Revenue Share', 'N/A')}%")
        st.write(f"**Consulting Revenue Share (2023):** {metrics.get('Consulting Revenue Share', 'N/A')}%")
        st.write(f"**Infrastructure Revenue Share (2023):** {metrics.get('Infrastructure Revenue Share', 'N/A')}%")
        st.write(f"**Financing Revenue Share (2023):** {metrics.get('Financing Revenue Share', 'N/A')}%")
        st.write(f"**Dividend Yield (approx):** {metrics.get('Dividend Yield', 'N/A')}%")
        st.write(f"**Dividend Aristocrat Status:** {metrics.get('Dividend Aristocrat Status', 'N/A')}")
        st.write(f"**Kyndryl Spinoff Year:** {metrics.get('Kyndryl Spinoff Year', 'N/A')}")
        st.write(f"**Current Financial Focus:** {metrics.get('Financial Focus', 'N/A')}")
    else:
        st.warning("No specific key metrics extracted.")

with col2:
    st.markdown("### Revenue Mix (2023 Est.)")
    revenue_data = {
        'Segment': [],
        'Share': []
    }
    
    # Check if any revenue share metrics were extracted before trying to plot
    if metrics.get('Software Revenue Share') is not None:
        revenue_data['Segment'].append('Software')
        revenue_data['Share'].append(metrics['Software Revenue Share'])
    if metrics.get('Consulting Revenue Share') is not None:
        revenue_data['Segment'].append('Consulting')
        revenue_data['Share'].append(metrics['Consulting Revenue Share'])
    if metrics.get('Infrastructure Revenue Share') is not None:
        revenue_data['Segment'].append('Infrastructure')
        revenue_data['Share'].append(metrics['Infrastructure Revenue Share'])
    if metrics.get('Financing Revenue Share') is not None:
        revenue_data['Segment'].append('Financing')
        revenue_data['Share'].append(metrics['Financing Revenue Share'])

    df_revenue = pd.DataFrame(revenue_data)

    if not df_revenue.empty and sum(df_revenue['Share']) > 0: # Ensure there's data to plot
        fig = px.pie(df_revenue, values='Share', names='Segment', title='IBM Revenue Mix (2023 Est.)',
                     hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sufficient data to visualize revenue mix.")

st.markdown("---")

# Parse and display the full analysis in logical blocks
logical_blocks = parse_analysis_into_logical_blocks(ANALYSIS_TEXT)

for i, block in enumerate(logical_blocks):
    if i == 0: # First block often starts with the primary H2 title
        h2_title_match = re.match(r"## (.+)", block['content'])
        if h2_title_match:
            main_h2_title = h2_title_match.group(1)
            st.header(main_h2_title)
            # Remove the H2 title from the content to avoid duplication
            content_after_h2 = block['content'][len(h2_title_match.group(0)):].strip()
            intro, subsections = split_block_by_h3(content_after_h2)
        else:
            # Fallback if no H2 title is found at the beginning (e.g., just an intro paragraph)
            st.header(block['title']) # Use the generic block title
            intro, subsections = split_block_by_h3(block['content'])
        
        st.markdown(intro)
        for h3_header, content in subsections.items():
            with st.expander(h3_header.replace("### ", "")):
                st.markdown(content)
    else:
        # Subsequent blocks are given a subheader as their logical block title
        st.subheader(block['title'])
        intro, subsections = split_block_by_h3(block['content'])
        st.markdown(intro) # Display introductory text for this block, if any
        if subsections: # If there are H3 sections within this block
            for h3_header, content in subsections.items():
                with st.expander(h3_header.replace("### ", "")):
                    st.markdown(content)

st.markdown("---")
st.info("This analysis is based on the provided text and aims to highlight key financial aspects and relationships of IBM's ecosystem.")