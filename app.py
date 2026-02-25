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

st.set_page_config(page_title="Microsoft (MSFT) Financial Ecosystem Analysis", layout="wide")

# --- Helper Functions ---
def get_key_metric(text, section_title):
    """Extracts a key metric if present, otherwise returns None."""
    # This is a simplified approach. For production, consider NLP or regex.
    keywords = [
        "Market cap", "revenue", "operating margins", "FCF", "debt", "cash",
        "stock performance", "AAA credit rating", "price"
    ]
    for keyword in keywords:
        if keyword in text.lower():
            try:
                # Attempt to find a numerical value associated with the keyword
                start_index = text.lower().find(keyword)
                if start_index != -1:
                    # Look for numbers around the keyword
                    value_str = ""
                    for char in text[start_index:]:
                        if char.isdigit() or char in ['.', ',', '$', '~', '%']:
                            value_str += char
                        elif value_str and not (char.isdigit() or char in ['.', ',', '$', '~', '%']):
                            break
                    if value_str:
                        # Basic cleanup and conversion
                        value_str = value_str.replace('~', '').replace('$', '').replace(',', '')
                        if '%' in value_str:
                            return f"{keyword.capitalize()}: {value_str.strip()}"
                        elif value_str.lower().startswith('approx') or value_str.lower().startswith('around'):
                             return f"{keyword.capitalize()}: {value_str.strip()}"
                        else:
                            return f"{keyword.capitalize()}: {value_str.strip()}"
            except Exception:
                pass
    return None

def parse_financial_text(text):
    """Parses the financial analysis text into structured data."""
    sections = {
        "Overview": [],
        "Key Financial Relationships": [],
        "Market Dependencies": [],
        "Sector Connections": [],
        "Competitor Relationships": [],
        "Economic & Regulatory Factors": [],
        "Growth Catalysts & Risks": [],
        "Financial Ecosystem Summary": []
    }
    current_section = None
    key_metrics = {}

    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect section headers
        if line.startswith("---"):
            continue
        if line.startswith("##"):
            current_section = line[2:].strip()
            if current_section not in sections:
                sections[current_section] = []
            continue
        if line.startswith("###"):
            sub_section_title = line[3:].strip()
            if current_section:
                sections[current_section].append({"type": "subsection", "title": sub_section_title, "content": []})
            else:
                sections[sub_section_title] = [] # If no section before, treat as a new section
            continue

        # Process content within sections
        if current_section:
            metric = get_key_metric(line, current_section)
            if metric:
                key_metrics[metric.split(':')[0]] = metric.split(':')[1].strip()

            if sections[current_section] and isinstance(sections[current_section][-1], dict) and sections[current_section][-1]["type"] == "subsection":
                 sections[current_section][-1]["content"].append(line)
            else:
                sections[current_section].append(line)
        else:
            # Handle content before the first section if any
            sections["Overview"].append(line)

    # Clean up empty lists and reconstruct
    cleaned_sections = {}
    for sec_name, sec_content in sections.items():
        if sec_content:
            if sec_name == "Overview" and isinstance(sec_content[0], str) and sec_content[0].startswith("Microsoft is a global technology leader"):
                 cleaned_sections[sec_name] = sec_content
            elif sec_name == "Financial Ecosystem Summary":
                 cleaned_sections[sec_name] = sec_content
            else:
                cleaned_sections[sec_name] = sec_content
    return cleaned_sections, key_metrics

# --- Data ---
analysis_text = """
# Microsoft (MSFT): A Deep Dive into its Financial Ecosystem

Microsoft is a technology giant with a sprawling portfolio, making its financial ecosystem incredibly complex and interconnected. Here's a breakdown of its key financial relationships, market dependencies, sector connections, competitor relationships, and economic factors.

## 1. Key Financial Relationships and Metrics

Microsoft's financial health and performance are driven by several core business segments and their associated revenue streams and cost structures.

*   **Revenue Streams:**
    *   **Intelligent Cloud (Azure, Server Products):** This is Microsoft's fastest-growing and increasingly dominant segment. Azure's growth is critical, driven by cloud infrastructure, platform services, and hybrid cloud solutions. Server products like Windows Server and SQL Server also contribute.
    *   **Productivity and Business Processes (Office 365/Microsoft 365, Dynamics 365, LinkedIn):** This segment benefits from recurring subscription revenue, which provides stability and predictability. Office 365 (now Microsoft 365) continues to be a cash cow, while Dynamics 365 is expanding its market share in enterprise resource planning (ERP) and customer relationship management (CRM). LinkedIn's advertising and premium subscriptions add another layer.
    *   **More Personal Computing (Windows, Devices, Gaming):** This segment is more cyclical and hardware-dependent. Windows licensing and PC shipments are key drivers, while the Xbox gaming division (including hardware, software, and subscriptions like Game Pass) is a significant contributor, especially with recent acquisitions.

*   **Profitability Drivers:**
    *   **Gross Margins:** Cloud services generally have higher gross margins than hardware, contributing to the overall margin expansion trend.
    *   **Operating Expenses:** Significant investments in R&D, sales & marketing, and general & administrative expenses are crucial for innovation and market expansion. Cloud infrastructure costs are also a major operational expense.
    *   **Net Income & EPS:** These are the ultimate measures of profitability and are closely watched by investors.

*   **Balance Sheet Strength:**
    *   **Cash & Equivalents:** Microsoft maintains a substantial cash pile, enabling strategic acquisitions, share buybacks, and dividend payouts.
    *   **Debt:** While Microsoft has taken on debt, its strong cash flow generation generally allows for efficient debt management.
    *   **Shareholder Equity:** Reflects the accumulated profits and investments in the company.

*   **Cash Flow Generation:**
    *   **Operating Cash Flow:** Consistently strong, driven by recurring revenue and efficient operations. This is a key indicator of the company's ability to generate cash from its core business.
    *   **Free Cash Flow:** The cash available after capital expenditures. This is a vital metric for assessing the company's financial flexibility for investments, dividends, and buybacks.

*   **Shareholder Returns:**
    *   **Dividends:** Microsoft pays a consistent and growing dividend, appealing to income-focused investors.
    *   **Share Buybacks:** The company actively repurchases its shares, which can boost earnings per share (EPS) and signal confidence in its valuation.

### 2. Market Dependencies

Microsoft's performance is deeply intertwined with several market trends and dependencies.

*   **Digital Transformation:** The ongoing shift by businesses to digital technologies, cloud computing, AI, and data analytics is a primary growth driver for Microsoft's Intelligent Cloud and Productivity segments.
*   **PC Market Health:** The "More Personal Computing" segment, particularly Windows, is still somewhat reliant on PC sales, which can be cyclical and influenced by consumer spending and enterprise refresh cycles.
*   **Gaming Industry Growth:** The expansion of online gaming, cloud gaming (Xbox Cloud Gaming), and the increasing value of game franchises are critical for the Gaming division.
*   **Enterprise Spending:** A significant portion of Microsoft's revenue comes from large enterprises. Their willingness and ability to spend on software, cloud services, and hardware directly impacts MSFT.
*   **Small and Medium Business (SMB) Adoption:** The adoption of Microsoft 365 and other cloud services by SMBs is a crucial growth area.
*   **AI Adoption and Integration:** The rapid integration of AI across all its products and services (e.g., Copilot) is a major dependency for future growth and competitive positioning.

### 3. Sector Connections

Microsoft operates across multiple tech sub-sectors, creating complex interdependencies.

*   **Software & Services:** This is Microsoft's core. It spans operating systems (Windows), productivity suites (Microsoft 365), enterprise applications (Dynamics 365), and cloud platforms (Azure).
*   **Cloud Computing (IaaS, PaaS, SaaS):** Azure is a direct competitor in the Infrastructure as a Service (IaaS) and Platform as a Service (PaaS) markets, while Microsoft 365 and Dynamics 365 operate in the Software as a Service (SaaS) space.
*   **Hardware:** While not its primary focus, Microsoft designs and sells Surface devices and Xbox consoles, connecting it to the consumer electronics and gaming hardware sectors.
*   **Gaming:** The acquisition of Activision Blizzard firmly entrenches Microsoft as a major player in the video game industry, encompassing content creation, distribution, and hardware.
*   **Artificial Intelligence (AI):** Microsoft is heavily investing in and integrating AI across its product portfolio, making it a key player in the AI sector.
*   **Cybersecurity:** As a major cloud provider and software vendor, cybersecurity is integral to its offerings and a critical area of investment.
*   **Enterprise Software:** Dynamics 365 competes in the ERP and CRM markets.

### 4. Competitor Relationships

Microsoft faces intense competition across all its major segments.

*   **Cloud Computing (Azure):**
    *   **Amazon Web Services (AWS):** The market leader, a formidable competitor.
    *   **Google Cloud Platform (GCP):** A strong challenger, particularly in AI and data analytics.
*   **Productivity & Business Processes:**
    *   **Google Workspace:** The primary competitor to Microsoft 365.
    *   **Salesforce:** The dominant player in CRM, a direct competitor to Dynamics 365.
    *   **Oracle, SAP:** Major competitors in ERP solutions.
    *   **Slack (owned by Salesforce), Zoom:** Competitors in collaboration and communication tools.
*   **More Personal Computing (Windows):**
    *   **Apple (macOS, iOS):** A key competitor in operating systems and devices.
    *   **Google (ChromeOS, Android):** Competes with Windows on PCs and mobile devices.
    *   **Various PC Manufacturers (Dell, HP, Lenovo):** While partners, they also offer competing devices and ecosystems.
*   **Gaming:**
    *   **Sony (PlayStation):** The primary console competitor.
    *   **Nintendo (Switch):** A significant player in the console market, often with a different focus.
    *   **Mobile Game Developers/Publishers:** For mobile gaming revenue.
    *   **Other Cloud Gaming Services:** NVIDIA GeForce NOW, Amazon Luna.

### 5. Economic Factors

Microsoft's financial performance is sensitive to broader economic conditions.

*   **Global Economic Growth:** Strong economic growth generally translates to higher enterprise spending on technology, benefiting Microsoft's cloud and productivity segments.
*   **Interest Rates:** Higher interest rates can increase borrowing costs for Microsoft (though it has a strong balance sheet) and can also impact the valuation of growth stocks like MSFT by making future earnings less valuable in present terms.
*   **Inflation:** Rising inflation can increase operating costs (e.g., cloud infrastructure, wages) and potentially impact consumer discretionary spending on PCs and gaming.
*   **Geopolitical Stability:** Conflicts and trade tensions can disrupt supply chains, impact international sales, and create uncertainty, which can affect business investment.
*   **Currency Fluctuations:** As a global company, fluctuations in exchange rates can impact reported revenues and profits from international markets.
*   **Technological Adoption Cycles:** The pace at which businesses and consumers adopt new technologies (e.g., AI, cloud migration, 5G) directly influences demand for Microsoft's products and services.
*   **Government Regulations:** Regulatory scrutiny concerning antitrust, data privacy (e.g., GDPR, CCPA), and AI ethics can create compliance costs and potential business model adjustments.

### Overall Financial Ecosystem Synthesis:

Microsoft's financial ecosystem is a testament to its strategic diversification and ability to adapt.

*   **Cloud Dominance:** The "Intelligent Cloud" segment, particularly Azure, is the primary engine of growth and innovation, driving higher revenue and improving overall gross margins. This segment's success is crucial for future valuations.
*   **Recurring Revenue Stability:** The "Productivity and Business Processes" segment, powered by Microsoft 365 subscriptions, provides a bedrock of stable, predictable revenue and cash flow.
*   **Synergistic Investments:** Microsoft's strength lies in the synergy between its segments. For example, AI investments enhance Azure and Microsoft 365, while Xbox's growth can be boosted by cloud integration.
*   **Acquisition Strategy:** Strategic acquisitions (like Activision Blizzard) are critical for expanding market reach and acquiring new technologies and talent, although they also bring integration challenges and financial commitments.
*   **Resilience and Flexibility:** Its strong balance sheet and robust cash flow generation provide significant financial flexibility to weather economic downturns, invest in new technologies, and return capital to shareholders.
*   **AI as the Next Frontier:** The successful integration and monetization of AI across its entire product suite represent the most significant opportunity and a key dependency for continued high growth.

In essence, Microsoft's financial ecosystem is a powerful, interconnected web where cloud infrastructure, enterprise software, productivity tools, and emerging technologies like AI converge, supported by a strong financial foundation and driven by global digital transformation trends. Investors closely monitor Azure's growth, the recurring revenue of Microsoft 365, and the company's ability to successfully navigate the competitive landscape and evolving economic and regulatory environments.

---

Below is a structured, comprehensive map of Microsoft Corporation’s (MSFT) financial ecosystem: its revenue and cost relationships, market dependencies, sector and competitor connections, supplier and partner dynamics, macro drivers, regulatory exposures, and the key metrics and events that most directly move the stock.

1) Business model & revenue streams (how money is made)
- Productivity and Business Processes: Microsoft 365 (Office commercial and consumer subscriptions), LinkedIn, Dynamics CRM/ERP. High-margin, subscription-based recurring revenue; strong enterprise lock-in and multi-year contracts.
- Intelligent Cloud: Azure (IaaS/PaaS), server products (Windows Server, SQL Server), GitHub, cloud management services. Rapid-growth, high-capex but high-margin after scale; Azure is core growth engine.
- More Personal Computing: Windows OEM and licensing, Surface hardware, Search/advertising (Bing), Xbox gaming & Game Pass. Mix of licensing, transactional hardware, and subscription (Game Pass).
- New/strategic: AI products and services (Copilot, Azure OpenAI Service), enterprise AI solutions, professional services. These are becoming major drivers of incremental revenue and enterprise spend.

2) Segment-level competitor map (by product)
- Cloud infrastructure/platform: AWS (Amazon) is #1; Azure is #2 (Google Cloud is #3). Competition on pricing, features, regional presence, enterprise sales.
- Productivity/collaboration: Microsoft 365/Office + Teams vs Google Workspace (Google) and point solutions (Slack/Zoom historically; Slack now Salesforce).
- CRM/ERP: Dynamics vs Salesforce (CRM leader), SAP, Oracle.
- Operating systems: Windows dominates PC OS; macOS (Apple) for premium devices; Chromebooks for low-cost segment.
- Search/ad: Bing vs Google Search/Ads; advertising is a minor revenue share but strategically important.
- Gaming: Xbox ecosystem and studios vs Sony (PlayStation) and Nintendo; PC gaming and Epic/Steam ecosystem also relevant.
- Developer tools/repositories: GitHub vs GitLab, Bitbucket, and independent tools.
- AI infrastructure/tools: Partnerships and competition with Google Cloud, AWS, and smaller AI infrastructure firms; close relationship and partial overlap with OpenAI.

3) Key suppliers, partners, and channel relationships
- OEMs: PC manufacturers (HP, Dell, Lenovo, Acer, Asus) are critical for Windows distribution and licensing revenue.
- Semiconductor suppliers: Intel, AMD, and Nvidia are central for client/server CPU/GPU supply. Nvidia GPUs are particularly critical for Azure’s AI workloads; supply constraints or export controls on advanced GPUs materially affect Azure AI capacity and costs.
- Data center builders and suppliers: Equinix, local contractors, power providers — capex and energy inputs drive capital intensity and operating cost profile.
- Systems integrators, ISVs, channel partners: Large partner ecosystem (Microsoft Partner Network, Value-Added Resellers, consultancies like Accenture/Deloitte/IBM/Capgemini) extend sales reach and integration capability.
- Strategic partners: OpenAI (exclusive cloud provider relationship; Azure OpenAI integration), large enterprise customers (multi-year contracts and co-development), telcos for edge services.

4) Customer base & demand drivers
- Enterprise IT budgets (large enterprises, SMBs): recurring subscription renewals, digital transformation projects, ERP/CRM modernizations, migration to cloud.
- Government and regulated industries: large, multi-year contracts but subject to security and compliance requirements.
- Consumers: Surface, Xbox hardware, individual Microsoft 365/subscribers.
- Developer & startup ecosystems: GitHub, Azure credits, marketplace drives long-term lock-in.

5) Financial relationships & metrics to monitor
- Revenue mix and growth: commercial cloud (Azure + server products + enterprise services) growth rate vs productivity revenue growth.
- Recurring revenue % (subscriptions vs perpetual licenses) and retention/renewal rates.
- Gross margin and operating margin by segment (cloud expansion tends to depress margins short-term due to capex; SaaS margins are high).
- Free cash flow (FCF) generation and conversion from EBIT; Microsoft historically strong FCF, used for buybacks/dividends and M&A.
- Capital expenditures (data center buildouts) vs depreciation; capex intensity tied to cloud growth and AI infrastructure needs.
- Deferred revenue and remaining performance obligations (indicators of near-term revenue).
- Commercial cloud margin and RPO/ARR: indicators of sustainability of cloud growth.
- R&D as % of revenue: investment intensity for AI, cloud, security, developer tools.
- Balance sheet metrics: net cash / debt levels, liquidity, and ability to fund M&A or large capex.

6) Macro and market dependencies
- Corporate IT spend cycle: enterprise capex and SaaS/cloud spend correlates with economic growth and corporate budgets; recession risk can slow upgrades and cloud migrations (though cloud can be a cost-saver vs on-prem).
- Interest rates: higher rates compress valuation multiples for growth stocks and can reduce present value of long-duration earnings.
- FX / USD strength: impacts reported revenue and margins from international sales.
- Energy prices: data center OPEX is sensitive to electricity prices; energy efficiency and renewable procurement are factors.
- Semiconductor supply and geopolitical export controls: constraints on high-end GPUs (Nvidia) or CPUs can limit Azure capacity for AI workloads.
- Consumer spending: affects Surface and Xbox hardware and gaming consumables.

7) Strategic & regulatory risks
- Antitrust and competition scrutiny (U.S., EU, other jurisdictions): large size invites regulatory attention on acquisitions, bundling, and market conduct.
- Data protection and privacy (GDPR, CCPA-like laws) and localization requirements; impacts cloud data storage strategy and compliance costs.
- National security and export controls on AI chips and models; restrictions (e.g., on Nvidia H100 exports) can materially affect cloud AI capacity.
- Content moderation and gaming regulation (loot boxes, monetization) in various jurisdictions.
- M&A approvals: large acquisitions (e.g., past Activision attempt) face stringent review that can alter strategy.

8) AI-specific dynamics (critical post-2023/24)
- Partnership and investment in OpenAI: Microsoft’s exclusive cloud relationship and integration of OpenAI models into Microsoft 365 and Azure is a major growth and differentiation driver.
- Copilot and AI features: success of AI integrations into Office, Windows, Dynamics, and developer tools will govern new revenue streams, pricing power, and upsell potential.
- Cost structure of AI: large models drive incremental cloud infrastructure, GPU costs, model training/serving expenses; economics depend on Microsoft’s ability to optimize model serving, pass costs to customers, and secure GPU supply.
- Competitive pressure from Google (Bard/GCP AI), AWS offerings, and in-house models from hyperscalers.

9) Competitive/partner paradox
- Microsoft is both partner and competitor with many firms: e.g., OEMs (partners for Windows) can compete via ChromeOS/Android ecosystems; cloud providers also partner with ISVs that may sell on multiple clouds; Microsoft’s partnership with OpenAI positions it as a customer and investor but also subjects it to model/strategic risks.

10) Key catalysts and downside triggers
Catalysts:
- Sustained acceleration of commercial cloud (Azure) growth and margin improvement.
- Broad enterprise adoption of Copilot/AI features with demonstrable productivity gains and paid-upgrades or premium pricing.
- Large multi-year enterprise/government cloud contracts announced or renewed.
- Successful M&A that strengthens strategic positioning.
- Continued strong FCF enabling buybacks/dividends and M&A.

Downside triggers:
- Prolonged slowdown in enterprise IT spend or macro recession reducing renewals.
- Supply constraints (GPUs, CPUs) or material jump in compute costs for AI workloads.
- Regulatory actions limiting product bundling, cloud market practices, or blocking major acquisitions.
- Security breaches/major outages impacting trust and leading to customer churn.
- Failure to monetize AI investments sufficiently relative to costs.

11) How MSFT’s stock behavior is influenced in markets
- Index flows: MSFT is a large S&P 500/Nasdaq constituent; passive fund flows into indices and ETFs affect short-term liquidity and volatility.
- Growth vs value rotation: as a large-cap growth name with strong earnings, its multiple expands/contracts with investor appetite for growth and interest rate expectations.
- News sensitivity: product launches (Windows/Office updates), AI announcements, large contracts, or legal/regulatory developments provoke outsized market moves.

12) Practical monitoring checklist (for investors/analysts)
- Commercial cloud revenue and growth rate (Azure + server products).
- Office and LinkedIn subscription growth and churn.
- Gross and operating margin trends by segment (are cloud margins improving?).
- Capex guidance and actual spend (data centers, AI infrastructure).
- RPO / deferred revenue trends and renewal rates.
- R&D spending and major partnerships (OpenAI updates, developer tools enhancements).
- Large customer wins/losses and government contract outcomes.
- Regulatory filings and antitrust developments.
- Semiconductor supply indicators and Nvidia/AMD/Intel announcements.
- Share buyback activity and dividend policy shifts.

13) Conclusion — strengths vs vulnerabilities
Strengths:
- Highly diversified revenue base across enterprise and consumer products.
- Leading positions in cloud, productivity, OS, and strong enterprise relationships.
- Strong balance sheet and cash flow enabling investments, buybacks, and acquisitions.
- Strategic early-mover positioning in enterprise AI through OpenAI partnership and product integrations.

Vulnerabilities:
- Heavy dependence on continued enterprise cloud adoption and availability of advanced compute (GPUs).
- Regulatory and antitrust risk due to scale and M&A activity.
- Rising operational costs associated with large-scale AI deployments and capex dependency.
- Competitive pressure across multiple fronts (AWS, Google, Salesforce, Apple, Nvidia/AMD for hardware dynamics).

If you want, I can:
- Translate this into the specific financial metrics to watch on MSFT’s next earnings release (revenue by segment, Azure growth, margins, capex, deferred revenue).
- Build a scenario model (bull/base/bear) showing how different Azure growth and AI monetization assumptions impact valuation.
- Produce a competitor heatmap or SWOT focused on Microsoft’s AI strategy and cloud economics.

Disclaimer: This is analysis for informational purposes, not investment advice.

---

**Analysis of Microsoft Corporation (MSFT)**

---

### **1. Company Overview**
Microsoft is a global technology leader with a diversified business model spanning:
- **Productivity & Business Processes:** Office 365, Dynamics, LinkedIn.
- **Intelligent Cloud:** Azure, server products, enterprise services.
- **More Personal Computing:** Windows, Xbox, Surface, Bing, advertising.

Market cap: ~$3.2 trillion (as of 2024).
Stock performance: Consistently outperforms S&P 500, driven by cloud growth and AI integration.

---

### **2. Key Financial Relationships**
- **Revenue Streams:** ~40% from cloud services (Azure), ~33% from productivity/software, remainder from hardware and gaming.
- **Profit Margins:** High operating margins (~45%) due to software dominance and scalable cloud infrastructure.
- **Cash Flow:** Strong FCF (~$70B annually) supports dividends, buybacks, and strategic acquisitions (e.g., Activision Blizzard, Nuance).
- **Balance Sheet:** Minimal debt relative to cash reserves, AAA credit rating.

---

### **3. Market Dependencies**
- **Enterprise IT Spending:** Azure growth tied to corporate digital transformation.
- **Consumer PC Market:** Windows and Surface depend on device refresh cycles.
- **Advertising Market:** Search (Bing) and LinkedIn ads correlate with digital ad trends.
- **Global Economic Health:** Enterprise budgets shrink in recessions, affecting cloud and software sales.

---

### **4. Sector Connections**
- **Cloud Computing:** Competes with AWS (Amazon) and Google Cloud. Azure is #2 globally.
- **Software/SaaS:** Office 365 competes with Google Workspace; Dynamics competes with Salesforce, SAP.
- **Gaming:** Xbox competes with Sony (PlayStation) and Nintendo; Activision acquisition expands mobile gaming.
- **AI & Emerging Tech:** Partnerships with OpenAI (ChatGPT integration), AI-driven tools across Azure, Office, and security.
- **Hardware:** Surface competes with Apple iPad/MacBook, Dell, HP.

---

### **5. Competitor Relationships**
- **Direct Competitors:**
  - **Cloud:** Amazon (AWS), Alphabet (Google Cloud).
  - **Software:** Adobe, Salesforce, Oracle.
  - **Gaming:** Sony, Nintendo, Tencent.
  - **Search/Advertising:** Google, Meta.
- **Coopetition:** Competes with Apple in OS/hardware but partners in software (Office for Mac); competes with Google in search but uses Android for mobile services.

---

### **6. Economic & Regulatory Factors**
- **Interest Rates:** Higher rates pressure valuation multiples but strengthen Microsoft’s cash-rich position for M&A.
- **Inflation:** Could increase cloud/data center costs, though pricing power mitigates impact.
- **Currency Fluctuations:** ~50% revenue from overseas; strong USD hurts international earnings.
- **Regulation:**
  - Antitrust scrutiny in cloud, gaming, and AI.
  - Data privacy laws (GDPR, CCPA) affect product compliance.
  - Global tensions (e.g., US-China) may limit market access.

---

### **7. Growth Catalysts & Risks**
- **Catalysts:**
  - AI monetization via Azure OpenAI, Copilot subscriptions.
  - Cloud market share gains.
  - Gaming expansion post-Activision.
- **Risks:**
  - Cloud growth slowdown.
  - AI competition from Google, Amazon.
  - Regulatory hurdles in major markets.

---

### **8. Financial Ecosystem Summary**
Microsoft’s ecosystem is **defensive yet growth-oriented**, leveraging:
- **Recurring revenue models** (subscriptions, cloud contracts).
- **Cross-selling synergies** (e.g., Azure + Office + Security).
- **Strategic moats** (enterprise lock-in, developer tools like GitHub).
- **Balance sheet strength** to invest in innovation during downturns.

The stock is sensitive to **tech sector sentiment**, **interest rate expectations**, and **AI adoption trends**, but its diversification reduces volatility relative to pure-play cloud or consumer tech firms.

---

**Bottom Line:** MSFT is a **core holding** in tech portfolios, acting as both a **growth engine** (cloud/AI) and **dividend-paying stalwart**. Its financial ecosystem is resilient but requires monitoring of cloud margins, AI execution, and regulatory developments.
"""

# --- App Structure ---
st.title("Microsoft (MSFT) Financial Ecosystem Analysis")
st.markdown("An interactive exploration of Microsoft's financial landscape based on the provided analysis.")

# Parse the text
parsed_data, key_metrics = parse_financial_text(analysis_text)

# --- Key Metrics Section ---
st.header("Key Financial Metrics")
if key_metrics:
    metric_df = pd.DataFrame(list(key_metrics.items()), columns=["Metric", "Value"])
    st.dataframe(metric_df, use_container_width=True)
else:
    st.info("No specific key financial metrics were extracted. Please check the analysis text.")

st.markdown("---")

# --- Visualizing Sections ---
st.header("Analysis Breakdown")

section_names = list(parsed_data.keys())

# Create a DataFrame for plotting section lengths and content types
section_data = []
for section, content in parsed_data.items():
    num_lines = len(content)
    has_subsections = any(isinstance(item, dict) and item.get("type") == "subsection" for item in content)
    section_data.append({
        "Section": section,
        "Number of Lines": num_lines,
        "Has Subsections": has_subsections
    })
section_df = pd.DataFrame(section_data)

# Chart 1: Number of Lines per Section
fig_lines = px.bar(section_df, x="Section", y="Number of Lines",
                   title="Content Volume per Section",
                   labels={"Section": "Analysis Section", "Number of Lines": "Content Volume (Lines)"},
                   text="Number of Lines")
fig_lines.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig_lines, use_container_width=True)

# Chart 2: Presence of Subsections
fig_subsections = px.scatter(section_df, x="Section", y="Number of Lines",
                             size="Number of Lines", color="Has Subsections",
                             title="Content Volume vs. Presence of Subsections",
                             hover_name="Section",
                             labels={"Section": "Analysis Section", "Number of Lines": "Content Volume (Lines)"},
                             color_discrete_map={True: 'green', False: 'red'})
fig_subsections.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig_subsections, use_container_width=True)


st.markdown("---")

# --- Detailed Section View ---
st.header("Detailed Analysis Sections")

# Use columns to display sections side-by-side if many
num_sections = len(section_names)
cols = st.columns(min(3, num_sections)) # Max 3 columns

for i, section_name in enumerate(section_names):
    col_index = i % 3
    with cols[col_index]:
        st.subheader(section_name)
        content = parsed_data[section_name]
        if content:
            for item in content:
                if isinstance(item, dict) and item.get("type") == "subsection":
                    st.markdown(f"**{item['title']}**")
                    for sub_item in item["content"]:
                        st.markdown(f"- {sub_item}")
                else:
                    st.markdown(item)
        else:
            st.info("No content available for this section.")

st.markdown("---")

# --- Text Summary ---
st.header("Full Analysis Text")
with st.expander("Show Full Text"):
    st.text(analysis_text)

st.markdown("---")
st.markdown(" *Disclaimer: This app processes and visualizes the provided text. It does not perform live financial data fetching or analysis.*")