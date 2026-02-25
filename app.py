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

# Set page config for a wider layout
st.set_page_config(layout="wide", page_title="MSFT Financial Analysis")

# --- Raw Analysis Text ---
# The complete financial analysis text is embedded here.
analysis_text = """
## MSFT: Deep Dive into a Dominant Tech Giant

As a Senior Equity Research Analyst, I'm presenting a high-conviction, forward-looking analysis of Microsoft Corporation (MSFT). MSFT's entrenched position across cloud, productivity, and increasingly, AI, makes it a compelling investment.

### Fundamental Evaluation

**Recent Performance & Outlook:** Microsoft has delivered robust financial results, consistently exceeding expectations.

*   **Cloud Strength (Azure):** Azure continues its impressive growth trajectory, driven by digital transformation initiatives and strong enterprise adoption. We anticipate this trend to continue, fueled by ongoing demand for cloud infrastructure and services.
*   **Productivity & Business Processes (Office 365, Dynamics):** The secular shift towards subscription-based software and hybrid work models continues to benefit Office 365. Dynamics 365 is also gaining traction as businesses seek integrated CRM and ERP solutions.
*   **AI Integration:** Microsoft's strategic investments in AI, particularly through its partnership with OpenAI, are beginning to manifest across its product suite. This integration is a key driver for future growth and differentiation.

**Projected Performance (Next 3-6 Months):** We expect MSFT to maintain its strong performance in the upcoming quarters.

*   **Revenue Growth:** Continued double-digit revenue growth, primarily driven by Azure and Office 365, will be the hallmark. We anticipate AI-related services and new product features to contribute an accelerating share of this growth.
*   **Margin Expansion:** Operating margins are likely to remain healthy, benefiting from economies of scale in the cloud and continued efficiency gains. AI investments, while significant, are expected to be accretive to margins in the medium-to-long term as they unlock new revenue streams.
*   **Earnings per Share (EPS):** EPS growth is projected to outpace revenue growth due to strong operating leverage and disciplined capital allocation.

**Key Catalysts for the Next 3-6 Months:**

1.  **Accelerated AI Adoption & Monetization:** We expect Microsoft to announce further tangible results of its AI integration, including new features for Copilot across its product lines (Windows, Office, Dynamics) and broader enterprise adoption of AI-powered solutions. Clearer monetization strategies for these AI services will be a significant positive.
2.  **Continued Cloud Market Share Gains:** As businesses continue to migrate workloads to the cloud and as AI adoption necessitates robust infrastructure, Azure is well-positioned to capture market share from competitors. Any commentary on increasing Azure's competitive moat through specialized AI hardware or services would be a catalyst.
3.  **Strong Holiday Season/Enterprise Spending:** The upcoming holiday season, coupled with typical end-of-year enterprise budget allocations, could lead to robust demand for Microsoft's productivity and cloud services, especially as businesses invest in tools to enhance efficiency and remote collaboration.

### Peer Benchmarking

| Metric               | Microsoft (MSFT) | Alphabet (GOOGL) | Amazon (AMZN) | Oracle (ORCL) |
| :------------------- | :--------------- | :--------------- | :------------ | :------------ |
| **P/E Ratio (TTM)**  | ~32.5x           | ~27.0x           | ~53.0x        | ~30.0x        |
| **YoY Revenue Growth** | ~18%             | ~10%             | ~12%          | ~5%           |
| **Market Share (Cloud)** | ~23% (Azure)     | ~31% (GCP)       | ~40% (AWS)    | ~3% (OCI)     |
| **Market Cap**       | ~$3.1 Trillion   | ~$2.1 Trillion   | ~$1.7 Trillion | ~$390 Billion |

**Analysis:** MSFT trades at a premium to Alphabet and Oracle, reflecting its superior growth profile, particularly in cloud and AI, and its diversified revenue streams. While Amazon's AWS holds the largest cloud market share, Azure's growth rate is often more robust, and MSFT's broader ecosystem offers significant advantages. Oracle, while a cloud contender, lags in growth and breadth.

### Adjacent Industry Analysis

**1. Semiconductor Industry (Upstream):**

*   **Current State:** The semiconductor industry is experiencing a cyclical recovery, with strong demand for AI-specific chips (GPUs, TPUs) and continued demand for general-purpose processors. Supply chain constraints have largely eased, but lead times for specialized components can still be a factor.
*   **Tailwinds/Headwinds:**
    *   **Tailwind:** Increased demand for advanced semiconductors to power AI workloads directly benefits Microsoft, which is a significant consumer of these chips for Azure and its own AI development. Strategic partnerships with chip manufacturers and potential for custom silicon development offer further advantages.
    *   **Headwind:** While less of a concern for MSFT than for pure hardware manufacturers, any resurgence in global chip shortages or significant price increases for essential components could marginally impact margins on hardware-dependent services or R&D costs.

**2. Digital Advertising & E-commerce (Downstream):**

*   **Current State:** The digital advertising market is dynamic, with shifts towards AI-driven targeting and measurement. E-commerce continues its steady growth, albeit at a more normalized pace post-pandemic. Consumer spending sentiment is a key variable.
*   **Tailwinds/Headwinds:**
    *   **Tailwind:** Microsoft's LinkedIn platform benefits from a healthy digital advertising market, as does its growing search advertising business (Bing). Enterprise clients' investment in digital transformation and cloud services indirectly supports this sector by enabling more sophisticated online operations.
    *   **Headwind:** A significant slowdown in consumer or enterprise discretionary spending could dampen advertising budgets and reduce e-commerce activity, indirectly impacting LinkedIn's advertising revenue and potentially slowing the pace of digital transformation for some smaller businesses. However, MSFT's core enterprise cloud and productivity segments are more resilient to these fluctuations.

### Risk Assessment

**Bear Case (Next Quarter):**

*   **Intensified Cloud Competition:** While Azure is growing strongly, a more aggressive pricing strategy or significant innovation from AWS or GCP could put pressure on Azure's market share gains and margins.
*   **Slower AI Monetization:** The market's expectations for AI revenue generation might be overly optimistic, leading to disappointment if initial monetization efforts don't meet ambitious targets or if adoption of paid AI features is slower than anticipated.
*   **Macroeconomic Slowdown Impacting Enterprise Spending:** A sharper-than-expected economic downturn could lead enterprises to cut back on IT spending, impacting new cloud migrations and renewals for productivity software, even for a company as critical as Microsoft.

**Bull Case (Next Quarter):**

*   **Accelerated AI Revenue & Enterprise Adoption:** Microsoft announces exceeding targets for Copilot adoption and monetization across Office 365 and other enterprise solutions, proving its AI strategy is not just hype but a tangible revenue driver.
*   **Azure Outperformance:** Azure's growth rate accelerates further, driven by significant wins from large enterprises migrating critical workloads and a surge in AI-related cloud compute demand.
*   **Strong Renewals & Upsells:** High customer retention and successful upselling of premium features and services in Office 365 and Dynamics 365, demonstrating continued value proposition and sticky customer relationships.

**Conclusion:**

Microsoft remains a foundational technology company with exceptional execution. Its strategic positioning in cloud computing, the enduring strength of its productivity suite, and its aggressive push into AI present a compelling growth narrative. While competitive pressures and macroeconomic factors warrant attention, the catalysts for continued outperformance are substantial. We maintain a **Strong Buy** rating on MSFT, with a forward-looking price target that reflects its ongoing innovation and market leadership.

---

Company overview
- Ticker/company: MSFT — Microsoft Corporation.
- Primary industry: Technology — enterprise software, cloud infrastructure and services, productivity applications, gaming and devices.
- Business mix: Large, diversified technology platform spanning Azure cloud infrastructure and platform services; Microsoft 365 (Office) productivity and collaboration; Dynamics/enterprise applications; LinkedIn; Windows and Surface; Xbox/Activision content and services; enterprise security. Deep cash-generation, large enterprise customer base, and strategic partnerships (notably with OpenAI) that position Microsoft as a bridge between legacy enterprise IT and the emerging AI-enabled stack.

3–6 month outlook
- Financial fundamentals and recent trends: Through mid‑2024 Microsoft has shown resilient top‑line growth driven by Azure and commercial cloud services, steady subscription renewals in Microsoft 365/Office, and improving monetization of AI features (Copilot integrations) and LinkedIn advertising. Operating margin profile benefits from recurring software revenue and scale in cloud, though Microsoft continues to invest heavily in AI infrastructure and go‑to‑market. The company generates strong free cash flow and uses buybacks and dividends to return cash.
- Macroeconomic context: Global GDP growth is uneven and enterprise IT budgets are sensitive to macro softness. However, the current investment theme of AI appears to be re-prioritizing corporate IT spend toward cloud and AI platforms even when overall capex is constrained. Currency fluctuations (a stronger U.S. dollar) could modestly reduce reported revenue growth in constant currency.
- Industry dynamics: The cloud market remains concentrated but intensely competitive. AI adoption is accelerating demand for GPU‑accelerated infrastructure, higher‑value cloud services, and software subscriptions with AI features. Supply constraints and pricing dynamics for AI GPUs (and power/real estate for data centers) are important near‑term factors.
- Company catalysts and near‑term risks:
  - Catalysts: Continued enterprise adoption of Azure AI services and Microsoft 365 Copilot; expanded commercial relationships tied to OpenAI and other AI partnerships; sticky subscription revenue; cross‑sell opportunities from Activision content into Game Pass and services; ongoing cost efficiencies and product‑led upsell.
  - Risks: Weakening enterprise IT budgets could slow license growth; competitive price/mix pressure in cloud; GPU supply constraints or higher data‑center costs; regulatory scrutiny around large AI partnerships or bundling; FX headwinds.
- Probabilistic outlook (3–6 months): Expect continued positive revenue momentum driven by cloud/AI and subscription renewal stability. Earnings may show modest operating margin pressure if incremental AI infrastructure investments accelerate, but cash flow should remain strong. Market performance will be sensitive to macro risk sentiment, AI news flow (product wins, partnerships), and any supply constraints for GPU capacity.

Competitive comparison (selected peers)
- Amazon (AMZN — Amazon Web Services)
  - Strengths: Largest cloud market share and breadth of infrastructure services; deep experience running large-scale data centers; entrenched enterprise and web-scale customers.
  - Weaknesses vs. Microsoft: Less integrated productivity/app ecosystem; AWS competes mainly on services breadth and scale rather than desktop productivity or Office integrations.
  - Relative position: AWS is the cost‑efficient IaaS leader; Microsoft is stronger at turning cloud infrastructure into enterprise workflows via Office/Teams/Dynamics integration and packaged AI offerings.
- Alphabet (GOOGL — Google Cloud)
  - Strengths: Fastest recent growth in cloud, strong data/ML/AI tooling, and differentiated ML stack (TensorFlow, Vertex AI); broad advertising revenue base supports R&D.
  - Weaknesses vs. Microsoft: Smaller enterprise application footprint and less entrenched productivity software; monetization of enterprise offerings still scaling.
  - Relative position: Google Cloud competes on AI and data analytics; Microsoft competes on end‑to‑end enterprise productivity + cloud + apps.
- Oracle (ORCL)
  - Strengths: Deep enterprise database footprint, strong high‑margin licensing business, and a growing cloud IaaS/PaaS push focused on enterprise migrations.
  - Weaknesses vs. Microsoft: Slower overall growth, historically less developer/AI ecosystem traction; Oracle’s cloud footprint is smaller.
  - Relative position: Oracle is a legacy enterprise software specialist; Microsoft offers broader horizontal cloud + productivity integration, making it more attractive for many customers moving to SaaS/AI.
- Salesforce (CRM)
  - Strengths: Market leader in CRM and customer-focused SaaS; strong enterprise relationships and growing AI features (Einstein).
  - Weaknesses vs. Microsoft: Narrower horizontal footprint (less infrastructure), more dependent on CRM demand; faces competition in sales/productivity integrations.
  - Relative position: Salesforce and Microsoft compete in CRM/ERP/workflows (Dynamics), but Microsoft’s broader platform (Azure + Microsoft 365) gives cross‑sell advantages.

Adjacent industries and transmission channels
- Semiconductor/AI hardware (NVIDIA and other GPU suppliers): Availability and pricing of GPUs directly affect Microsoft’s ability to expand Azure AI capacity and launch large models. Tight supply or higher prices increase capex and operating costs or limit service capacity.
- Data center real estate and energy markets: Rising energy prices or constraints on data‑center permits/locations increase operating costs and slow expansion. Efficient site selection and power procurement reduce these risks.
- Cybersecurity services: Growing demand for security increases take‑up of Microsoft’s security offerings (Secure Score, Defender suite), boosting Average Revenue Per User (ARPU) in enterprise segments.
- Enterprise services and consulting: Firms modernizing apps and adopting AI rely on systems integrators and Microsoft partners; partner ecosystem health influences deployment speed.
- Advertising and macro consumer spend: LinkedIn and search advertising revenue are sensitive to overall ad budgets; consumer hardware/gaming cycles affect Xbox and Surface revenue.
- Regulation and policy: Antitrust/competition rules, AI governance, and data‑localization laws can alter go‑to‑market strategies, partnerships, and product features.

Key risks and opportunities
- Opportunities
  - AI monetization: Embedding Copilot across Microsoft 365 and Azure AI managed services could materially increase ARPU and create sticky revenue streams.
  - Cross‑product synergies: Ability to bundle cloud, productivity, security and developer tools gives Microsoft a durable enterprise moat.
  - Gaming/IP leverage: Activision content and Game Pass expansion can monetize a different customer base and increase recurring subscription revenue.
- Risks
  - Macro slowdown: A sharper decline in enterprise IT spending would slow license renewals and new cloud commitments.
  - Competitive pricing and margin pressure: Aggressive price moves by competitors (AWS, Google) or higher infrastructure costs could compress margins.
  - Hardware/GPU supply constraints: Limits access to capacity needed for training/hosting large models, slowing AI product delivery.
  - Regulatory/legal: Increased scrutiny of large tech platforms and AI partnerships could constrain certain business practices or deal structures.
  - Execution risk: Rapid product integrations and major acquisitions (e.g., gaming) raise integration and management complexity.

Summary judgment
Over the next 3–6 months Microsoft is well positioned to sustain revenue growth and strong cash generation driven by Azure and AI‑enhanced software offerings, even as macro sentiment remains the principal near‑term market risk. Its differentiated advantage is the integration of cloud infrastructure with a pervasive productivity and business‑application ecosystem, which supports higher customer retention and cross‑sell potential. Key variables to monitor are the pace of AI adoption (and related GPU capacity), enterprise IT budgets, and regulatory developments. Relative to peers, Microsoft occupies a balanced position: not the cheapest nor the fastest‑growing in raw cloud metrics, but among the most defensible and monetizable platforms given its software franchises and enterprise reach.

This assessment is forward‑looking commentary, not investment advice; outcomes will depend on material developments in macroeconomics, competitive moves, and Microsoft’s execution.

---

# Microsoft (MSFT) - Comprehensive Analysis

## **Market Sentiment & Expectations (Last 3-6 Months)**

*   **Overwhelmingly Bullish:** The dominant sentiment from analysts, investors, and financial media is highly positive. Microsoft is consistently rated a "Strong Buy" or "Buy" by the vast majority of Wall Street firms.
*   **AI as the Primary Catalyst:** The primary driver of optimism is Microsoft's aggressive and successful integration of artificial intelligence, particularly through its partnership with OpenAI (ChatGPT, GPT-4). The rollout of **Copilot** across its product suite (Microsoft 365, GitHub, Security, Dynamics) is seen as a major growth engine.
    *   **Quote (CNBC, April 2024):** "Microsoft's AI bet is paying off in a big way... Azure's growth re-accelerated, directly attributed to AI services." – Analyst commentary post-Q3 FY24 earnings.
    *   **Bullish Perspective:** The market views Microsoft as the best-positioned "picks and shovels" play in the AI gold rush, providing the essential cloud infrastructure (Azure AI) and productivity tools to enterprises.
    *   **Bearish/Cautious Perspective:** Some concerns exist about the **high capital expenditures** required to build AI data centers and whether the monetization of Copilot will meet lofty expectations in the near term. There are also questions about cloud growth deceleration in a broader economic slowdown.
*   **Strong Financial Performance:** Recent earnings (Q3 FY24) beat estimates, with notable strength in Intelligent Cloud revenue ($26.7 billion, up 21%). Commercial bookings growth was strong, indicating healthy future revenue.

## **Competitive Positioning (vs. Key Peers: Amazon AWS, Google Cloud, Apple, Oracle)**

*   **Strengths:**
    *   **Diverse Revenue Streams:** Unlike pure-play cloud competitors, Microsoft has a "fortress" balance sheet with strong, recurring revenue from **Office 365, Windows, LinkedIn, and Gaming (Activision Blizzard)**. This provides stability and funds massive AI investments.
    *   **Enterprise Entrenchment:** Deep relationships with global corporations through its legacy software. Migrating these clients to Azure and layering on AI products (Copilot) is a powerful cross-selling opportunity.
    *   **Leading AI Narrative:** Currently perceived as the AI leader among mega-cap tech, thanks to its first-mover advantage with OpenAI integration.
*   **Weaknesses:**
    *   **Regulatory Scrutiny:** The Activision Blizzard acquisition and its dominant position in software/cloud attract ongoing regulatory attention in the US, EU, and UK.
    *   **Slower Growth in Some Segments:** The More Personal Computing segment (Windows, devices) can be cyclical and tied to the sluggish PC market.
*   **Opportunities:**
    *   **Full Monetization of AI:** Upselling existing Azure and M365 customers to premium AI-powered tiers.
    *   **Cybersecurity:** Microsoft Security is now a $20+ billion annual business and growing rapidly, leveraging AI (Security Copilot) to compete directly with specialists like CrowdStrike and Palo Alto Networks.
*   **Threats:**
    *   **Intense Cloud Competition:** **Amazon AWS** remains the market share leader in cloud infrastructure and is investing heavily in its own AI chips (Trainium, Inferentia) and models. **Google Cloud** is aggressively competing with its Gemini AI models and is gaining market share.
    *   **Open Source AI Models:** The rise of powerful, open-source LLMs (like Meta's Llama) could potentially erode the advantage of proprietary models like GPT-4 in the long run.

## **Adjacent Industry Impact**

*   **Semiconductor Industry:** Microsoft's AI ambitions are directly tied to the **supply of advanced GPUs from Nvidia and, increasingly, its own custom AI chips (Azure Maia)**. Constraints in the high-end chip supply chain could limit Azure's capacity growth. Microsoft's move into chip design signals a strategic shift to reduce dependency and control costs.
*   **Cybersecurity Industry:** As mentioned, Microsoft's integrated, AI-driven security suite is disrupting the standalone cybersecurity market. Its bundling with enterprise licenses poses a significant threat to adjacent security software firms.
*   **Regulatory & Legal Environment:** Global regulatory trends concerning **data privacy, AI ethics, and antitrust** directly impact Microsoft's operations and acquisition strategy. Compliance costs and operational limitations are a persistent influence.
*   **Gaming & Entertainment:** The acquisition of Activision Blizzard places Microsoft as a major player in this adjacent industry. It now faces different competitive dynamics (vs. Sony, Nintendo) and regulatory landscapes, but also gains opportunities in mobile gaming and the metaverse.
*   **Professional Networking & HR Tech:** Through **LinkedIn**, Microsoft is deeply connected to the job market and B2B marketing trends. A softening labor market could impact LinkedIn's hiring solutions revenue, but it also provides unique data on economic trends.

## **Critical Findings Summary**

*   **✅ Major Opportunity:** Microsoft's **AI integration across its entire stack** is its single biggest strength and the core reason for its premium valuation. Success in commercializing Copilot is the key to near-term performance.
*   **⚠️ Major Risk:** **Capital Intensity and Execution.** The billions spent on AI infrastructure must translate into sustained, high-margin revenue growth. Any stumble in AI monetization or a significant loss of cloud market share to AWS/Google would negatively impact the stock.
*   **🔍 Watch:** The competitive dynamics in the **cloud war** and the adoption rates/price points for **Microsoft 365 Copilot** licenses in the coming quarters will be the most critical indicators of success.
"""

# --- Data Extraction Functions ---

def parse_peer_benchmarking(text):
    """
    Parses the Peer Benchmarking table from the analysis text into a pandas DataFrame.
    Converts values to appropriate numeric types (e.g., percentages, trillions, billions).
    """
    # This regex looks for the '### Peer Benchmarking' header, then captures all table lines
    # until an empty line, a new markdown header, or the end of the string.
    match = re.search(r'### Peer Benchmarking\s*\n\| Metric.*?\n\| :---.*?\n(.*?)(?=\n\n|\n[#]{1,3}\s|\Z)', text, re.DOTALL)
    if not match:
        return pd.DataFrame()

    table_data_str = match.group(1) # This group contains all data rows
    lines = table_data_str.strip().split('\n')
    
    # Extract headers (assuming it's the line right before the separator '---')
    header_line_match = re.search(r'### Peer Benchmarking\s*\n(\| Metric.*\|)', text)
    if not header_line_match: return pd.DataFrame()
    
    header_line = header_line_match.group(1)
    headers = [h.strip().replace('**', '') for h in header_line.split('|') if h.strip()]
    
    parsed_rows = []
    for line in lines:
        if not line.strip() or line.startswith('| :---'): # Skip empty lines or the separator line
            continue
        row_values = [v.strip() for v in line.split('|') if v.strip()]
        if len(row_values) == len(headers): # Ensure consistent number of columns
            parsed_rows.append(row_values)
            
    df = pd.DataFrame(parsed_rows, columns=headers)
    
    processed_data = []
    for _, row in df.iterrows():
        metric = row['Metric']
        for col_name in headers[1:]: # Iterate through company columns (skip 'Metric')
            company = col_name
            value_str = row[col_name]
            
            numeric_value = None
            if isinstance(value_str, str):
                cleaned_str = value_str.replace('~', '').replace('$', '').strip()
                
                if 'Trillion' in cleaned_str:
                    numeric_value = float(cleaned_str.replace('Trillion', '')) * 1_000_000_000_000
                elif 'Billion' in cleaned_str:
                    numeric_value = float(cleaned_str.replace('Billion', '')) * 1_000_000_000
                elif '%' in cleaned_str:
                    num_match = re.search(r'(\d+\.?\d*)%', cleaned_str)
                    if num_match:
                        numeric_value = float(num_match.group(1)) / 100.0
                elif 'x' in cleaned_str:
                    try: # Handle P/E ratios like '32.5x'
                        numeric_value = float(cleaned_str.replace('x', ''))
                    except ValueError:
                        pass
                else: # Generic float conversion
                    try:
                        numeric_value = float(cleaned_str)
                    except ValueError:
                        pass # Keep as None if not parsable

            processed_data.append({
                'Metric': metric,
                'Company': company,
                'Value': numeric_value
            })

    df_melted = pd.DataFrame(processed_data)
    
    return df_melted


def extract_key_metrics(text):
    """
    Extracts specific key financial metrics from the analysis text.
    """
    metrics = {}
    
    # Intelligent Cloud Revenue and Growth
    # Regex for "Intelligent Cloud revenue ($26.7 billion, up 21%)" or similar
    ic_revenue_match = re.search(r'Intelligent Cloud revenue \(\$([\d.]+)\s*billion, up (\d+)%\)', text)
    if ic_revenue_match:
        revenue_value = float(ic_revenue_match.group(1)) * 1_000_000_000 # Convert to actual number
        growth_rate = int(ic_revenue_match.group(2))
        metrics['Intelligent Cloud Revenue'] = revenue_value
        metrics['Intelligent Cloud Growth'] = growth_rate
        
    # Security Business Revenue
    # Regex for "Microsoft Security is now a $20+ billion annual business"
    security_revenue_match = re.search(r'Microsoft Security is now a \$([\d.]+)\+ billion annual business', text)
    if security_revenue_match:
        metrics['Security Business Revenue'] = float(security_revenue_match.group(1)) * 1_000_000_000
        
    return metrics

# --- Main Streamlit App ---
def main():
    st.title("📊 MSFT: Deep Dive into a Dominant Tech Giant")
    st.markdown("As a Senior Equity Research Analyst, I'm presenting a high-conviction, forward-looking analysis of Microsoft Corporation (MSFT). MSFT's entrenched position across cloud, productivity, and increasingly, AI, makes it a compelling investment.")
    st.markdown("---")

    # --- Key Metrics Section ---
    st.header("Key Financial Metrics & Highlights")
    st.markdown("Snapshot of key performance indicators directly extracted from the analysis.")

    col1, col2, col3 = st.columns(3)

    # Extract metrics using the helper function
    metrics = extract_key_metrics(analysis_text)
    
    if 'Intelligent Cloud Revenue' in metrics:
        col1.metric(
            label="Intelligent Cloud Revenue (Q3 FY24)",
            value=f"${metrics['Intelligent Cloud Revenue'] / 1_000_000_000:.1f}B",
            delta=f"{metrics['Intelligent Cloud Growth']}% YoY Growth"
        )
    if 'Security Business Revenue' in metrics:
        col2.metric(
            label="Security Business Annual Revenue",
            value=f"${metrics['Security Business Revenue'] / 1_000_000_000:.1f}B+",
            help="Growing rapidly, leveraging AI (Security Copilot)"
        )
    
    # Extract Market Cap for MSFT from the peer table for display in metrics
    peer_df_melted = parse_peer_benchmarking(analysis_text)
    msft_market_cap = None
    if not peer_df_melted.empty:
        # Filter for MSFT's Market Cap, ensuring a valid value exists
        msft_market_cap_row = peer_df_melted[(peer_df_melted['Metric'] == 'Market Cap') & (peer_df_melted['Company'] == 'Microsoft (MSFT)')]
        if not msft_market_cap_row.empty and pd.notna(msft_market_cap_row['Value'].iloc[0]):
            msft_market_cap = msft_market_cap_row['Value'].iloc[0]
            col3.metric(
                label="Microsoft Market Cap",
                value=f"${msft_market_cap / 1_000_000_000_000:.1f} Trillion"
            )

    st.markdown("---")

    # --- Peer Benchmarking Visualizations ---
    st.header("Competitive Peer Benchmarking")
    st.markdown("A visual comparison of Microsoft against key competitors across important financial and operational metrics.")

    if not peer_df_melted.empty:
        # Filter for each metric and drop rows with NaN values in 'Value' column to prevent chart errors
        pe_ratio_df = peer_df_melted[peer_df_melted['Metric'] == 'P/E Ratio (TTM)'].dropna(subset=['Value'])
        yoy_growth_df = peer_df_melted[peer_df_melted['Metric'] == 'YoY Revenue Growth'].dropna(subset=['Value'])
        market_share_df = peer_df_melted[peer_df_melted['Metric'] == 'Market Share (Cloud)'].dropna(subset=['Value'])
        market_cap_df = peer_df_melted[peer_df_melted['Metric'] == 'Market Cap'].dropna(subset=['Value'])

        col_charts1, col_charts2 = st.columns(2)
        col_charts3, col_charts4 = st.columns(2)

        # P/E Ratio (TTM) Chart
        if not pe_ratio_df.empty:
            fig_pe = px.bar(
                pe_ratio_df, x='Company', y='Value', title='P/E Ratio (TTM)',
                labels={'Value': 'P/E Ratio'}, color='Company',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig_pe.update_layout(showlegend=False)
            col_charts1.plotly_chart(fig_pe, use_container_width=True)
        else: col_charts1.write("P/E Ratio data not available for charting.")

        # YoY Revenue Growth Chart
        if not yoy_growth_df.empty:
            fig_yoy = px.bar(
                yoy_growth_df, x='Company', y='Value', title='YoY Revenue Growth',
                labels={'Value': 'Growth Rate'}, color='Company',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig_yoy.update_layout(yaxis_tickformat=".0%", showlegend=False) # Format as percentage
            col_charts2.plotly_chart(fig_yoy, use_container_width=True)
        else: col_charts2.write("YoY Revenue Growth data not available for charting.")
            
        # Cloud Market Share Chart
        if not market_share_df.empty:
            fig_share = px.bar(
                market_share_df, x='Company', y='Value', title='Cloud Market Share',
                labels={'Value': 'Market Share'}, color='Company',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig_share.update_layout(yaxis_tickformat=".0%", showlegend=False) # Format as percentage
            col_charts3.plotly_chart(fig_share, use_container_width=True)
        else: col_charts3.write("Cloud Market Share data not available for charting.")

        # Market Cap Chart
        if not market_cap_df.empty:
            fig_mcap = px.bar(
                market_cap_df, x='Company', y='Value', title='Market Cap',
                labels={'Value': 'Market Cap'}, color='Company',
                color_discrete_sequence=px.colors.qualitative.Plotly,
                hover_data={'Value': ':.2s'} # Format large numbers nicely on hover
            )
            fig_mcap.update_layout(yaxis_tickformat=".2s", showlegend=False) # Format as significant figures
            col_charts4.plotly_chart(fig_mcap, use_container_width=True)
        else: col_charts4.write("Market Cap data not available for charting.")

    else:
        st.warning("Could not parse peer benchmarking data from the analysis text. Please ensure the table format is correct.")

    st.markdown("---")

    # --- Sections and Summaries ---
    st.header("Detailed Analysis Sections")
    st.markdown("Explore the complete in-depth breakdown of Microsoft's performance, outlook, and risks in collapsible sections.")
    
    # Split the analysis text into logical blocks based on the '---' separators for easier display.
    # We find the indices of the separators to extract content between them.
    
    # The initial block starts after the main title and ends before the first '---'
    start_first_block_content = analysis_text.find("### Fundamental Evaluation") # Start after intro and main title
    end_first_block_content = analysis_text.find("---", start_first_block_content)
    first_major_block_content = analysis_text[start_first_block_content:end_first_block_content].strip()

    # The second block is between the first and second '---'
    start_second_block_content = end_first_block_content + 3 # Skip '---' and newline
    end_second_block_content = analysis_text.find("---", start_second_block_content)
    second_major_block_content = analysis_text[start_second_block_content:end_second_block_content].strip()
    
    # The third block is after the second '---'
    start_third_block_content = end_second_block_content + 3
    third_major_block_content = analysis_text[start_third_block_content:].strip()

    # Display each major block in a Streamlit expander for a clean layout
    with st.expander("**1. Fundamental Evaluation, Adjacent Industries & Risk Assessment**"):
        st.markdown(first_major_block_content)

    with st.expander("**2. Company Overview, Outlook & Detailed Competitive Comparison**"):
        st.markdown(second_major_block_content)
        
    with st.expander("**3. Comprehensive Analysis: Market Sentiment, Positioning & Critical Findings**"):
        st.markdown(third_major_block_content)

    st.markdown("---")
    st.info("Disclaimer: This analysis is forward-looking commentary and not investment advice; outcomes will depend on material developments in macroeconomics, competitive moves, and Microsoft’s execution.")

if __name__ == "__main__":
    main()