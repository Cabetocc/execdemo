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

# The full analysis text provided by the user
ANALYSIS_TEXT = """
## MSFT: A Deep Dive into the Cloud Giant's Future

**Company:** Microsoft Corporation (MSFT)
**Date:** October 26, 2023
**Analyst:** [Your Name/Firm Name], Senior Equity Research Analyst

**Executive Summary:**

Microsoft (MSFT) continues to demonstrate robust performance, driven primarily by the sustained strength of its Intelligent Cloud segment, particularly Azure. While facing ongoing macroeconomic uncertainties and increased competition, the company is well-positioned to capitalize on key secular trends in cloud computing, artificial intelligence (AI), and digital transformation. We anticipate continued positive momentum for MSFT over the next 3-6 months, supported by product innovation, strategic partnerships, and a solid enterprise demand environment.

---

### Fundamental Evaluation: Near-Term Outlook and Catalysts

**Recent Performance & Projection (Next 3-6 Months):**

MSFT has delivered consistently strong financial results, with its Intelligent Cloud segment (Azure, Windows Server, SQL Server, GitHub) being the primary engine of growth. Recent earnings reports have showcased impressive revenue and profit growth, driven by Azure's expansion and the integration of AI capabilities into its cloud offerings. The Productivity and Business Processes segment (Office 365, LinkedIn, Dynamics) also shows resilience, benefiting from a shift towards subscription-based models and increased remote work adoption. The More Personal Computing segment (Windows, Xbox, Surface) has experienced some cyclicality but remains a significant contributor.

**For the next 3-6 months, we project continued healthy revenue growth, albeit with potential moderation in the pace as macroeconomic headwinds persist.** We anticipate:

*   **Intelligent Cloud:** Continued double-digit revenue growth for Azure, fueled by ongoing digital transformation initiatives and an increasing adoption of AI services. Microsoft's commitment to integrating cutting-edge AI models into its Azure platform positions it favorably to capture a significant share of the rapidly expanding AI market.
*   **Productivity and Business Processes:** Steady growth, driven by commercial cloud adoption and the continued expansion of Microsoft 365's feature set, including AI-powered Copilot features.
*   **More Personal Computing:** Mixed performance, with Windows likely to see moderate demand as PC refresh cycles continue, while Xbox gaming revenue may see some normalization after a strong period.

**Key Catalysts (Next 3-6 Months):**

1.  **Expansion of AI Capabilities & Copilot Adoption:** The widespread rollout and adoption of **Microsoft Copilot** across its product suite (Microsoft 365, Dynamics 365, GitHub) will be a major driver. Successful integration and demonstration of productivity gains for businesses will lead to increased adoption and potentially higher ARPU (Average Revenue Per User). Positive customer testimonials and early success stories will be critical.
2.  **Continued Azure Momentum & Enterprise Cloud Spending:** Despite economic uncertainties, enterprises remain committed to cloud migration and digital transformation. We expect **continued robust demand for Azure services** as companies seek to optimize costs, enhance scalability, and leverage advanced analytics and AI capabilities. Any signs of enterprise IT spending resilience or acceleration would be a significant tailwind.
3.  **Strategic Partnerships & Ecosystem Growth:** Microsoft's ongoing investments in strategic partnerships, particularly with AI leaders like OpenAI, and its ability to integrate these capabilities seamlessly into its cloud and software offerings, will continue to strengthen its competitive moat. New product integrations or expanded cloud partnerships could emerge as positive catalysts.

---

### Peer Benchmarking:

| Metric              | MSFT      | GOOGL     | AMZN      | CRM       |
| :------------------ | :-------- | :-------- | :-------- | :-------- |
| **P/E Ratio (TTM)** | ~31x      | ~25x      | ~70x      | ~60x      |
| **YoY Revenue Growth** | ~7%       | ~7%       | ~11%      | ~19%      |
| **Market Share (Cloud)** | ~23-25%   | ~9-11%    | ~32-35%   | N/A       |
| **Gross Margin**    | ~69%      | ~56%      | ~42%      | ~76%      |
| **Operating Margin**| ~42%      | ~27%      | ~3%       | ~24%      |

*Note: Market share figures are estimates and can vary depending on the source and segment. P/E and growth figures are dynamic and subject to change based on latest earnings and market conditions. CRM (Salesforce) is a key competitor in the productivity and CRM space, with a significant cloud presence, though not directly comparable in the cloud infrastructure market to AWS and Azure.*

**Analysis:** MSFT trades at a premium valuation compared to Alphabet (GOOGL) but is significantly cheaper than Amazon (AMZN) on a P/E basis, despite similar cloud market share. Its revenue growth is solid, but lags behind Salesforce (CRM). However, MSFT's superior operating and gross margins highlight its efficiency and strong profitability, particularly in its cloud operations. This suggests a more mature and highly profitable cloud business compared to some peers.

---

### Adjacent Industry Analysis:

**1. Semiconductor Industry (Upstream):**

*   **Current State:** The semiconductor industry, particularly for AI-focused chips (e.g., GPUs), is experiencing immense demand. Companies like NVIDIA are facing supply constraints as demand for their advanced chips, crucial for AI training and inference, surges.
*   **Tailwinds/Headwinds for MSFT:**
    *   **Tailwind:** The demand for advanced semiconductors directly fuels Microsoft's AI ambitions. MSFT's strategic partnerships with chip manufacturers and its ability to secure supply of these critical components will be key to its AI-driven cloud growth. However, *any easing of supply chain constraints for GPUs and other AI accelerators would be a significant tailwind for Azure's AI service expansion.*
    *   **Headwind:** High chip prices and limited availability can impact the cost and speed of deployment for new AI infrastructure within Azure, potentially affecting margins or the pace of new service rollouts if supply is severely constrained. Conversely, the current tightness creates a strong environment for chipmakers, which could lead to higher costs for MSFT if they are a significant purchaser.

**2. Business Software & Services (Downstream):**

*   **Current State:** The market for business software, including CRM, ERP, and productivity tools, is undergoing a significant transformation with the integration of AI. Companies are increasingly looking for integrated solutions that can enhance productivity, automate tasks, and provide deeper insights.
*   **Tailwinds/Headwinds for MSFT:**
    *   **Tailwind:** MSFT's broad portfolio (Office 365, Dynamics 365, LinkedIn) and the integration of AI through Copilot create a powerful ecosystem advantage. As businesses seek to leverage AI across their operations, MSFT is well-positioned to offer a comprehensive suite of solutions, driving deeper customer engagement and higher recurring revenue.
    *   **Headwind:** Intense competition from specialized software providers (like Salesforce in CRM, Oracle in ERP, and various AI-native startups) remains a challenge. Customers may opt for best-of-breed solutions rather than a fully integrated suite, especially if they have existing investments or specific needs not fully met by Microsoft's offerings. The adoption of Copilot will depend on demonstrating clear ROI and overcoming integration complexities within existing workflows.

---

### Risk Assessment:

**Bear Case (Next Quarter):**

*   **Slower-than-expected AI monetization:** Despite strong underlying AI investment, the pace at which Microsoft can translate these investments into significant revenue growth and profit from its AI services (especially Copilot) could be slower than anticipated. This could be due to slower customer adoption, integration challenges, or competitive pressures forcing price concessions.
*   **Deterioration in Enterprise IT Spending:** A more pronounced economic slowdown leading to significant cuts in enterprise IT budgets could impact Azure growth and the adoption of new software solutions across the board. This would directly affect both the Intelligent Cloud and Productivity segments.
*   **Increased Regulatory Scrutiny:** Ongoing antitrust concerns and potential regulatory actions, particularly in cloud computing and AI, could lead to fines, operational restrictions, or forced divestitures, creating uncertainty and impacting investor sentiment.

**Bull Case (Next Quarter):**

*   **Accelerated Copilot Adoption & Revenue Generation:** Demonstrating strong early success and rapid adoption of Microsoft Copilot across enterprise customers, leading to clear productivity gains and an upward revision of ARPU expectations for Microsoft 365. This could significantly boost investor confidence in Microsoft's AI monetization strategy.
*   **Surge in Azure Demand Driven by AI Workloads:** A significant increase in demand for Azure's AI infrastructure and services as businesses accelerate their AI adoption, especially for training large language models and deploying AI applications. This would lead to stronger-than-expected Intelligent Cloud growth.
*   **Positive Macroeconomic Indicators & Resilient Enterprise Spending:** Easing inflation, declining interest rates, or signs of an economic rebound could lead to increased enterprise confidence and sustained or even accelerated IT spending, benefiting all of Microsoft's segments.

---

**Conclusion:**

Microsoft remains a core holding for investors seeking exposure to secular growth trends in cloud computing and artificial intelligence. While macroeconomic uncertainties and competitive pressures exist, the company's strong execution, expansive product portfolio, and strategic positioning in AI provide a compelling growth runway. We maintain a **positive outlook** on MSFT for the next 3-6 months, anticipating continued performance driven by the accelerating adoption of its cloud and AI offerings.

---

Company overview
- Ticker: MSFT — Microsoft Corporation.
- Primary industry: Enterprise software and cloud computing; major activities also include productivity applications (Office 365), operating systems (Windows), professional social networking (LinkedIn), gaming (Xbox and content), developer tools (GitHub), and a growing AI platform/business layer (Copilot, Azure OpenAI Services).
- Strategic position: Market leader across several high-margin enterprise segments (productivity suites, enterprise software, identity/security) and one of the two largest public cloud providers (Azure). Large installed base, strong recurring revenue from subscriptions, broad partner/developer ecosystem, and significant balance-sheet capacity for R&D and M&A.

3–6 month outlook

Expected performance summary
- Directionally positive but sensitive to macro sentiment: Over the next 3–6 months, Microsoft is likely to continue delivering top-line growth driven by Azure and AI-related services, steady recurring revenue from Microsoft 365 and enterprise agreements, and ongoing monetization of AI features. Near-term performance will be influenced heavily by (1) enterprise IT spending trends, (2) the pace of enterprise adoption and monetization of AI features (Copilot, Azure OpenAI), and (3) investor risk appetite toward growth/AI narratives versus macro concerns.

Drivers supporting modest outperformance
- Cloud + AI demand: Continued migration to cloud and accelerating pilot-to-production adoption of generative AI services should translate into higher consumption of Azure compute, platform, and managed AI services.
- Recurring revenue resilience: Large share of subscription-based revenue (Office 365, Azure support contracts, enterprise agreements) provides revenue visibility and margin leverage.
- Scale and cross-sell: Microsoft’s breadth (security, identity, productivity, infrastructure) enables cross-selling and stickiness, which tends to sustain margins even in slower macro periods.

Constraining factors that could temper near-term gains
- Enterprise budget caution: If corporations pull back on non-essential IT spend because of macro or sector-specific weakness, consumption growth could slow, particularly for big-ticket cloud migrations and premium AI deployments requiring high compute.
- Compute cost and capex dynamics: Rapid AI adoption increases demand for high-end GPUs/accelerators; supply constraints or rising prices for cloud compute can compress gross margins unless Microsoft passes costs to customers.
- Market sentiment and rates: Short-term equity performance will remain tied to risk-on/risk-off swings driven by macro surprises (inflation, central bank moves). Elevated rates raise discounting of growth expectations.

Company-specific catalysts (next 3–6 months)
- Product rollouts and enterprise deals: Broader enterprise launches, pricing/packaging changes for Copilot and enterprise AI offerings, and large multi-year deals will be positive catalysts.
- Developer and partner ecosystem announcements (GitHub, Visual Studio integrations) can boost long-term monetization prospects.
- Any visible improvement in Azure gross margins (through pricing or cost efficiencies) would be a near-term positive.

Company-specific risks
- Execution on AI monetization (pricing, uptake) and margin control on compute costs.
- Regulatory or contractual uncertainty (privacy, data residency, competition/antitrust scrutiny) that could affect product features or deal timelines.
- Large-scale cyber incidents or major gaming/content integration issues could create one-off hits or reputational costs.

Competitive comparison
Selected peers: Amazon (AMZN – AWS), Alphabet (GOOGL – Google Cloud), Nvidia (NVDA), Oracle (ORCL).

1) Amazon (AWS)
- Strengths: Market share leader in cloud infrastructure; extremely broad service portfolio and global footprint; strong operational scalability and pricing flexibility.
- Weaknesses relative to Microsoft: Less vertical enterprise software integration (Office, Windows, Dynamics, LinkedIn); weaker enterprise SaaS ecosystem for productivity and security.
- Comparative view: Microsoft’s advantage is enterprise relationships and software incumbency that drive hybrid-cloud and SaaS cross-sell; AWS remains a stronger pure-play infrastructure provider and often the low-cost leader. Over 3–6 months, competition will center on large enterprise deals and differentiated AI services.

2) Alphabet (Google Cloud)
- Strengths: Leadership in data analytics, AI/ML tooling, and open-source technologies; strength in developer mindshare for AI workloads.
- Weaknesses relative to Microsoft: Less entrenched in enterprise productivity and desktop/server OS markets; advertising revenue exposure creates a different macro sensitivity profile.
- Comparative view: Google Cloud is a key competitor in AI infrastructure and developer services; Microsoft competes on packaged enterprise AI and end-to-end solutions. Near-term, partnerships and exclusive AI models/features could shift workload choices.

3) Nvidia (NVDA)
- Strengths: Dominant supplier of high-performance GPUs that underpin modern generative AI workloads; powerful moat in AI training/inference hardware and ecosystem.
- Weaknesses relative to Microsoft: Not a cloud/platform vendor — more cyclical and capital-goods exposure, with revenue tied to semiconductor cycles.
- Comparative view: Nvidia is more of an upstream enabler/partner than a direct competitor. Microsoft’s access to GPUs (supply and cost) and any proprietary hardware initiatives (e.g., custom accelerators) will materially affect Azure’s unit economics. Over 3–6 months, GPU supply dynamics and pricing can influence Microsoft’s margins and capacity to scale AI offerings.

4) Oracle (ORCL)
- Strengths: Strong enterprise relationships in databases and ERP, attractive high-margin SaaS offerings for legacy workloads; increasingly competitive cloud compute for enterprise applications.
- Weaknesses relative to Microsoft: Smaller footprint in productivity and developer tools; less diversified consumer-facing offerings.
- Comparative view: Oracle competes for large enterprise deals—especially where database and ERP are central. Microsoft’s advantage is a wider horizontal stack; Oracle competes on price/performance in core enterprise workloads.

Adjacent industries impact (transmission channels)

1) Semiconductors / AI accelerators
- Channel: Supply and pricing of GPUs/accelerators affect Azure capacity/costs and the economics of offering AI services. Shortages or price increases raise Microsoft’s cloud gross costs; oversupply helps margins.

2) Enterprise IT spending / Services industry
- Channel: Macro-driven corporate capex and IT budgets determine pace of cloud migrations and purchases of premium AI solutions. Consulting and systems integrators (Accenture, Deloitte) mediate large enterprise transformations—Microsoft’s partner relationships are critical.

3) Cybersecurity
- Channel: Rising cyber threats increase demand for identity and security services (Azure AD, Defender), bolstering Microsoft’s security revenue and stickiness.

4) Advertising & Consumer Tech
- Channel: Slower consumer ad spend can indirectly affect LinkedIn ad revenue, and consumer device cycles (PC sales, Windows OEM) feed Windows licensing and surface device demand.

5) Telecom / Edge computing
- Channel: 5G and edge deployments create opportunities for Azure edge services and low-latency AI offerings; partnerships with telecoms can open new enterprise workloads.

Key risks and opportunities

Risks
- Macroeconomic contraction leading to IT budget cuts, slowing Azure and new AI deployments.
- Rising compute costs (GPU pricing) compressing cloud gross margins.
- Execution risk on AI pricing/monetization and integration complexities across large enterprise clients.
- Increased regulatory scrutiny (competition, data privacy) in the U.S., EU, and other jurisdictions.
- Concentration risk if reliance on a small set of AI models/providers creates supplier bargaining power.

Opportunities
- Strong monetization runway for generative-AI features embedded across productivity, developer, and business applications (Copilot for enterprise, GitHub Copilot).
- Cross-sell synergies: bundling AI with Microsoft 365, Dynamics, and security suites can lift ARPU and reduce churn.
- Expansion of managed AI services (Azure OpenAI) and industry cloud solutions (healthcare, finance, manufacturing).
- Leveraging balance sheet for strategic M&A to accelerate vertical offerings or secure tech/supply.

Summary judgment
Microsoft enters the next 3–6 months from a position of structural strength: diversified, recurring revenue streams; leading enterprise relationships; and a central role in cloud and enterprise AI transitions. Short-term performance will be a function of how quickly enterprises convert AI pilots into higher-consumption, monetized deployments and how well Microsoft manages compute costs and pricing. Compared with peers, Microsoft’s unique combination of productivity software, enterprise software, and cloud infrastructure gives it an advantage in cross-selling AI across the enterprise stack; AWS will remain the benchmark for raw infrastructure scale, Google for AI/ML tooling, Nvidia for hardware supply, and Oracle for core enterprise apps.

Bottom line (non-investment view): Over 3–6 months expect continued revenue resilience and upside potential tied to AI adoption, but also meaningful sensitivity to macro-driven IT budget shifts and compute-cost dynamics. For investors or stakeholders, focus should be on sequential metrics: Azure consumption growth, AI product monetization cadence, gross-margin trends (compute cost pass-through), and large enterprise contract announcements as the clearest near-term indicators of trajectory.

---

# **Analysis of Microsoft Corporation (MSFT)**
*Analysis conducted based on information from Q4 2023 and Q1 2024. Sources include recent earnings reports, analyst notes from Morgan Stanley, Goldman Sachs, and Wedbush, financial news (CNBC, Bloomberg, Reuters), industry publications, and commentary from tech forums.*

---

### **1. Market Sentiment & Expectations**
Overall sentiment is **decidedly bullish**, with Microsoft being viewed as a top-tier "must-own" mega-cap stock, largely due to its leadership in Artificial Intelligence (AI).

*   **Bullish Perspectives (Dominant View):**
    *   **AI Monetization Leader:** Microsoft is seen as the clearest and most immediate beneficiary of generative AI through its partnership with OpenAI and its integration of Copilot across its product suite (Azure, Office 365, Windows, Security). Analysts at **Wedbush** have called it a "1995 Moment" for the company.
    *   **Azure Growth Engine:** The Azure cloud segment is expected to re-accelerate, fueled by new AI workloads. The company reported **30% constant currency growth** in Azure in Q1 FY24, with 3 points of growth attributed directly to AI services.
    *   **Strong Financials:** Consistent double-digit revenue and earnings growth, robust profit margins (~44% operating margin), and a fortress balance sheet ($144 billion in cash and short-term investments as of Dec 2023) provide a solid foundation.
    *   **Analyst Ratings:** Overwhelmingly positive. The consensus price target is ~$465 (as of late April 2024), implying significant upside. **Morgan Stanley** named MSFT its "Top Pick," citing durable growth and AI leadership.

*   **Bearish/Cautious Perspectives:**
    *   **Valuation Concerns:** The stock trades at a premium (P/E ~36), reflecting high expectations. Any stumble in AI monetization or cloud growth could lead to a sharp correction.
    *   **Regulatory Scrutiny:** The company faces increasing antitrust attention, particularly regarding its OpenAI partnership and cloud computing practices in Europe and the UK.
    *   **Execution Risk:** Successfully integrating AI across all products and convincing enterprises to pay premium prices for Copilot features is not guaranteed. Competition is intensifying.

---

### **2. Competitive Positioning**
Microsoft operates from a position of significant strength in its core markets.

*   **Strengths:**
    *   **Unmatched Enterprise Ecosystem:** The seamless integration of Azure, Microsoft 365, Dynamics 365, and LinkedIn creates a powerful "stickiness" with corporate clients.
    *   **Diversified Revenue Streams:** Balanced across Productivity & Business Processes (Office), Intelligent Cloud (Azure), and More Personal Computing (Windows, Xbox). This reduces reliance on any single market.
    *   **First-Mover Advantage in AI:** The multi-year, multi-billion-dollar partnership with OpenAI gives it a technological and branding edge over competitors in commercializing AI.

*   **Weaknesses (Relative):**
    *   **Consumer Hardware:** The Surface device line and Xbox gaming console business are not market leaders and face intense competition (Apple, Sony).
    *   **Mobile:** Remains a minor player in mobile operating systems and app stores compared to Google and Apple.

*   **Competitive Landscape (Key Peers):**
    *   **vs. Amazon (AWS):** In cloud, AWS is the market share leader, but Azure is growing faster and is considered more advanced in AI/ML offerings for enterprises. Microsoft's hybrid cloud strategy (Azure Arc) is also a key differentiator.
    *   **vs. Google (Google Cloud, Workspace):** Google Cloud is a strong #3 with its own AI prowess (Gemini). Competition is fiercest in AI-powered productivity tools (Copilot vs. Duet AI) and cloud services for startups/AI-native companies.
    *   **vs. Salesforce/Oracle:** In enterprise software, Microsoft's Dynamics 365 is a growing challenger to Salesforce's CRM dominance, leveraging its integrated ecosystem.
    *   **vs. Apple:** Primarily in consumer ecosystems (PC vs. Mac) and services. Microsoft is stronger in enterprise, Apple in premium consumer hardware.

---

### **3. Adjacent Industry Impact**
Several external sectors are significantly influencing Microsoft's trajectory.

*   **Positive Impacts:**
    *   **Semiconductor Industry (e.g., NVIDIA, AMD):** Advances in GPU technology are the fuel for AI. Microsoft's massive investment in NVIDIA H100/A100 clusters is a direct enabler of its Azure AI infrastructure. Stronger, more efficient chips directly benefit Azure's capabilities and cost structure.
    *   **Cybersecurity Industry:** The escalating threat landscape drives demand for Microsoft's integrated security solutions (Sentinel, Defender, Entra), which are becoming a major growth pillar ($20+ billion annual revenue).
    *   **Professional Networking & Talent Market (LinkedIn):** LinkedIn provides unique data and a distribution channel for Microsoft's enterprise and learning tools, benefiting from trends in remote work and skills-based hiring.

*   **Negative/Risk Impacts:**
    *   **Global Regulatory Environment:** Increased data sovereignty laws (e.g., in the EU) and digital market regulations can increase compliance costs and force changes to business practices, particularly for Azure and Windows.
    *   **Energy & Utilities Sector:** The enormous power demands of AI data centers pose a challenge. Microsoft's ability to secure sustainable, reliable, and cost-effective energy is a critical long-term operational factor. The company is investing heavily in nuclear and renewable energy deals.
    *   **Gaming Industry Consolidation:** The recent completion of the Activision Blizzard acquisition makes Microsoft the world's third-largest gaming company by revenue. This exposes it to the cyclical and hit-driven nature of the gaming industry, as well as regulatory pushback on future M&A.

### **Critical Findings & Summary**
*   **Major Opportunity:** Microsoft is the market's preferred vehicle for investing in the enterprise AI transformation. Successful rollout and adoption of **Microsoft Copilot** across its portfolio is the single most important driver for stock performance over the next 12-24 months.
*   **Major Risk:** **High valuation and execution pressure.** The stock price assumes flawless execution and rapid adoption of AI products. Any sign of a slowdown in Azure growth or disappointing Copilot uptake would likely trigger a significant negative reaction.
*   **Conclusion:** Microsoft is exceptionally well-positioned due to its diversified model, enterprise dominance, and AI leadership. While not without risks (regulation, valuation), the consensus view is that its strengths and market positioning will allow it to navigate challenges and capitalize on the AI megatrend better than nearly any other large-cap company.
"""

def extract_section(text, start_keyword, end_keyword=None, is_regex=False):
    """
    Extracts a section of text between a start_keyword and an optional end_keyword.
    If no end_keyword, it goes to the next major heading (defined by --- or ###).
    """
    start_match = re.search(re.escape(start_keyword) if not is_regex else start_keyword, text, re.IGNORECASE)
    if not start_match:
        return ""

    start_index = start_match.end()

    if end_keyword:
        end_match = re.search(re.escape(end_keyword) if not is_regex else end_keyword, text[start_index:], re.IGNORECASE)
        if end_match:
            return text[start_index : start_index + end_match.start()].strip()
        else:
            return text[start_index:].strip() # If end keyword not found, take till end of text

    # If no explicit end_keyword, find the next '---' or a new main section header
    # and take content until then.
    next_separator_match = re.search(r'\n---\n|\n# |\n## |\n### ', text[start_index:])
    if next_separator_match:
        return text[start_index : start_index + next_separator_match.start()].strip()
    return text[start_index:].strip()

def extract_key_metrics(text):
    """Extracts key numerical metrics from the analysis text."""
    metrics = {}
    # Azure Growth
    azure_growth_match = re.search(r'reported \*\*(?P<total_growth>\d+)% constant currency growth\*\* in Azure in Q1 FY24, with (?P<ai_contribution>\d+) points of growth attributed directly to AI services', text)
    if azure_growth_match:
        metrics['Azure Q1 FY24 Growth'] = float(azure_growth_match.group('total_growth'))
        metrics['Azure AI Contribution to Growth'] = float(azure_growth_match.group('ai_contribution'))

    # Operating Margin
    op_margin_match = re.search(r'robust profit margins \(\~(?P<margin>\d+)% operating margin\)', text)
    if op_margin_match:
        metrics['Operating Margin'] = float(op_margin_match.group('margin'))

    # Cash and Investments
    cash_match = re.search(r'\$(?P<cash>[\d,]+) billion in cash and short-term investments as of Dec 2023', text)
    if cash_match:
        metrics['Cash & Short-term Investments (Dec 2023)'] = float(cash_match.group('cash').replace(',', ''))

    # Security Revenue
    security_rev_match = re.search(r'becoming a major growth pillar \(\$(?P<revenue>[\d,]+)\+ billion annual revenue\)', text)
    if security_rev_match:
        metrics['Annual Security Revenue'] = float(security_rev_match.group('revenue').replace(',', ''))

    # P/E Ratio (from sentiment section)
    pe_sentiment_match = re.search(r'stock trades at a premium \(P/E \~(?P<pe>\d+)\)', text)
    if pe_sentiment_match:
        metrics['Current P/E Ratio (Sentiment)'] = float(pe_sentiment_match.group('pe'))

    # Consensus Price Target
    pt_match = re.search(r'consensus price target is \~\$(?P<target>\d+) \(as of late April 2024\)', text)
    if pt_match:
        metrics['Consensus Price Target'] = float(pt_match.group('target'))

    return metrics

def get_peer_benchmarking_data():
    """Manually parses the peer benchmarking table for robustness."""
    data = {
        'Metric': ['P/E Ratio (TTM)', 'YoY Revenue Growth', 'Cloud Market Share', 'Gross Margin', 'Operating Margin'],
        'MSFT': [31, 7, '23-25%', 69, 42],
        'GOOGL': [25, 7, '9-11%', 56, 27],
        'AMZN': [70, 11, '32-35%', 42, 3],
        'CRM': [60, 19, 'N/A', 76, 24]
    }
    df = pd.DataFrame(data)

    # Clean up numerical columns and handle 'N/A' or ranges
    for col in ['MSFT', 'GOOGL', 'AMZN', 'CRM']:
        df[col] = df[col].astype(str).str.replace('~', '').str.replace('x', '').str.replace('%', '')
        # For ranges like '23-25%', take the lower bound for consistency in visualization
        df[col] = df[col].apply(lambda x: float(x.split('-')[0]) if '-' in str(x) else (float(x) if x not in ['N/A'] else pd.NA))
    return df

# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="MSFT Financial Analysis", icon="📊")

st.title("📊 MSFT: A Deep Dive into the Cloud Giant's Future")
st.markdown("---")

# Extracting general info for sidebar
company_info_match = re.search(r"\*\*Company:\*\* (.*)\n\*\*Date:\*\* (.*)\n\*\*Analyst:\*\* (.*)", ANALYSIS_TEXT)
if company_info_match:
    st.sidebar.markdown(f"**Company:** {company_info_match.group(1)}")
    st.sidebar.markdown(f"**Ticker:** MSFT")
    st.sidebar.markdown(f"**Analysis Date:** {company_info_match.group(2)}")
    st.sidebar.markdown(f"**Analyst:** {company_info_match.group(3)}")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Navigation")
    st.sidebar.markdown("- [Key Metrics](#key-financial-performance-metrics)")
    st.sidebar.markdown("- [Peer Benchmarking](#peer-benchmarking-analysis)")
    st.sidebar.markdown("- [Detailed Analysis Sections](#detailed-analysis-sections)")

# --- Key Metrics Extraction and Display ---
st.header("📈 Key Financial & Performance Metrics")
metrics = extract_key_metrics(ANALYSIS_TEXT)

metrics_display_data = []
for metric, value in metrics.items():
    unit = ''
    if 'Growth' in metric or 'Margin' in metric:
        unit = '%'
        value_str = f"{value:.1f}{unit}"
    elif 'Cash' in metric or 'Revenue' in metric:
        value_str = f"${value:,.0f} Billion"
    elif 'Target' in metric:
        value_str = f"${value:,.0f}"
    elif 'P/E' in metric:
        value_str = f"{value:.0f}x"
    metrics_display_data.append({'Metric': metric, 'Value': value_str})

# Display metrics using st.columns
cols = st.columns(3)
for i, metric_item in enumerate(metrics_display_data):
    with cols[i % 3]:
        st.metric(label=metric_item['Metric'], value=metric_item['Value'])
st.markdown("---")

# Chart for Azure growth breakdown
if 'Azure Q1 FY24 Growth' in metrics and 'Azure AI Contribution to Growth' in metrics:
    azure_growth_data = {
        'Category': ['Total Azure Growth', 'AI Contribution to Growth'],
        'Growth (%)': [metrics['Azure Q1 FY24 Growth'], metrics['Azure AI Contribution to Growth']]
    }
    azure_df = pd.DataFrame(azure_growth_data)

    fig_azure = px.bar(
        azure_df,
        x='Category',
        y='Growth (%)',
        text='Growth (%)',
        title='Azure Q1 FY24 Constant Currency Growth',
        labels={'Growth (%)': 'Growth (%)', 'Category': ''},
        color='Category',
        color_discrete_map={'Total Azure Growth': '#1f77b4', 'AI Contribution to Growth': '#ff7f0e'},
        height=400
    )
    fig_azure.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    fig_azure.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Total Azure Growth', 'AI Contribution to Growth']},
                            yaxis_title='Growth (%)')
    st.plotly_chart(fig_azure, use_container_width=True)
    st.markdown("---")


# --- Peer Benchmarking ---
st.header("👥 Peer Benchmarking Analysis")
peer_df = get_peer_benchmarking_data()

# Display the raw data table
st.subheader("Comparative Peer Metrics Table")
# Custom formatting for the dataframe
styled_peer_df = peer_df.copy()
for col in ['MSFT', 'GOOGL', 'AMZN', 'CRM']:
    styled_peer_df[col] = styled_peer_df.apply(lambda row: f"{row[col]:.0f}x" if "P/E" in row['Metric'] and pd.notna(row[col]) else \
                                                      (f"{row[col]:.0f}%" if pd.notna(row[col]) else 'N/A'), axis=1)

st.dataframe(styled_peer_df, use_container_width=True)

st.subheader("Visualizing Peer Comparisons")
# Create charts for each metric
metrics_to_chart = ['P/E Ratio (TTM)', 'YoY Revenue Growth', 'Cloud Market Share', 'Gross Margin', 'Operating Margin']
chart_cols = st.columns(2) # Two columns for charts

for i, metric in enumerate(metrics_to_chart):
    chart_data = peer_df[peer_df['Metric'] == metric].drop(columns='Metric').transpose().reset_index()
    chart_data.columns = ['Company', 'Value']
    chart_data['Value'] = pd.to_numeric(chart_data['Value'], errors='coerce') # Ensure numeric
    chart_data = chart_data.dropna(subset=['Value']) # Drop N/A for charting

    if not chart_data.empty:
        with chart_cols[i % 2]:
            fig = px.bar(
                chart_data,
                x='Company',
                y='Value',
                title=f'{metric} Comparison',
                labels={'Value': metric, 'Company': 'Company'},
                text='Value',
                height=350,
                color='Company',
                color_discrete_sequence=px.colors.qualitative.Plotly # Consistent colors
            )
            # Conditional text template for percentage vs. multiplier
            if '%' in metric or 'Share' in metric:
                fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
                fig.update_layout(yaxis_title=metric)
            elif 'P/E' in metric:
                fig.update_traces(texttemplate='%{y:.0f}x', textposition='outside')
                fig.update_layout(yaxis_title=metric)
            else:
                fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')
                fig.update_layout(yaxis_title=metric)

            fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# --- Sections and Summaries (using tabs for clean layout) ---
st.header("Detailed Analysis Sections")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Executive Summary", "Fundamental Evaluation", "Adjacent Industry",
    "Risk Assessment", "Comprehensive Outlook (3-6 mo)", "Market Sentiment & Comp. Positioning",
    "Critical Findings & Summary"
])

with tab1:
    st.subheader("Executive Summary")
    st.markdown(extract_section(ANALYSIS_TEXT, "**Executive Summary:**", "---"))

with tab2:
    st.subheader("Fundamental Evaluation: Near-Term Outlook and Catalysts")
    st.markdown(extract_section(ANALYSIS_TEXT, "### Fundamental Evaluation: Near-Term Outlook and Catalysts", "---"))

with tab3:
    st.subheader("Adjacent Industry Analysis")
    st.markdown(extract_section(ANALYSIS_TEXT, "### Adjacent Industry Analysis:", "---"))

with tab4:
    st.subheader("Risk Assessment")
    st.markdown(extract_section(ANALYSIS_TEXT, "### Risk Assessment:", "**Conclusion:**")) # Specific end to avoid overlap

with tab5:
    st.subheader("Comprehensive 3-6 Month Outlook")
    st.markdown(extract_section(ANALYSIS_TEXT, "Company overview", "# **Analysis of Microsoft Corporation (MSFT)**", is_regex=True))

with tab6:
    st.subheader("Market Sentiment & Competitive Positioning (Q4 2023 / Q1 2024)")
    sentiment_section = extract_section(ANALYSIS_TEXT, "### **1. Market Sentiment & Expectations**", "### **3. Adjacent Industry Impact**")
    st.markdown(sentiment_section)

with tab7:
    st.subheader("Critical Findings & Summary")
    st.markdown(extract_section(ANALYSIS_TEXT, "### Critical Findings & Summary", is_regex=True))

st.markdown("---")
st.info("Disclaimer: This analysis is based on the provided text and should not be considered financial advice. "
        "Financial data and market conditions are dynamic and subject to change.")