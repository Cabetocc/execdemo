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
import numpy as np
import plotly.express as px
import re

def parse_analysis_text(text):
    """
    Parses the financial analysis text to extract sections,
    prioritizing the second, highly structured analysis block for its detailed outline.
    Integrates key insights from other blocks where appropriate.
    """
    sections = {}
    
    # Split the entire text into distinct analysis blocks based on "---"
    parts = text.split("---")
    
    # Part 0: The initial introduction before the first "##" header
    initial_intro_block = parts[0].strip()
    first_formal_header_idx = initial_intro_block.find("## Ericsson (ERIC) - Financial Ecosystem Analysis")
    if first_formal_header_idx != -1:
        sections["Overall Introduction"] = initial_intro_block[:first_formal_header_idx].strip()
    else:
        sections["Overall Introduction"] = initial_intro_block # Fallback if header not found
    
    # Extract SWOT Analysis from the first block (explicitly present there)
    swot_match = re.search(r'\*\*7\. SWOT Analysis \((.*?)\):\n(.*?)(?=\n\nIn summary, Ericsson operates|$)', initial_intro_block, re.DOTALL)
    if swot_match:
        sections["SWOT Analysis"] = swot_match.group(2).strip()
    
    # Part 1: The second structured analysis block (index 1 after splitting by "---")
    # This block starts with "Below is a comprehensive, structured analysis of ERIC..."
    if len(parts) > 1:
        structured_analysis_text = parts[1].strip()
        # Remove the leading introductory sentence from this block itself
        structured_analysis_text = re.sub(r'Below is a comprehensive, structured analysis of ERIC.*?Nasdaq\), focused on the financial ecosystem:.*?\.\s*', '', structured_analysis_text, flags=re.DOTALL).strip()
        
        # Define the exact headers present in this block for parsing
        known_headers_ordered = [
            "Company snapshot (context)",
            "Key financial relationships and drivers",
            "Market dependencies",
            "Sector and technology connections",
            "Competitors and industry relationships",
            "Customer concentration and counterparty risk",
            "Regulatory, geopolitical and macroeconomic factors",
            "Intellectual property & litigation",
            "Financial health, valuation drivers and metrics to monitor",
            "Opportunities (bull case)",
            "Risks (bear case)",
            "Practical monitoring checklist",
            "Valuation and investor considerations (high-level)",
            "Bottom line"
        ]
        
        for i, header in enumerate(known_headers_ordered):
            start_idx = structured_analysis_text.find(header)
            if start_idx == -1:
                sections[header] = ""
                continue
            
            content_start_idx = start_idx + len(header)
            
            end_idx = -1
            if i < len(known_headers_ordered) - 1:
                next_header = known_headers_ordered[i+1]
                end_idx = structured_analysis_text.find(next_header, content_start_idx)
            
            if end_idx == -1: # Last section or next section not found
                section_content = structured_analysis_text[content_start_idx:].strip()
            else:
                section_content = structured_analysis_text[content_start_idx:end_idx].strip()
            
            # Clean up the specific prompt's follow-up if it's there
            if "If you want, I can:" in section_content:
                section_content = section_content.split("If you want, I can:")[0].strip()
            
            # Remove any leading non-bullet intro lines, but preserve proper markdown bullet points
            # This regex attempts to remove a non-bullet first line if it's followed by a bullet list
            section_content = re.sub(r'^(.*?)\n- ', r'- ', section_content.strip(), count=1, flags=re.DOTALL)
            section_content = section_content.strip()

            sections[header] = section_content
            
    # Final cleanups: Ensure bullet points in sections that are expected to have them
    for key in ["Company snapshot (context)", "Key financial relationships and drivers", "Market dependencies",
                "Sector and technology connections", "Competitors and industry relationships",
                "Customer concentration and counterparty risk", "Regulatory, geopolitical and macroeconomic factors",
                "Intellectual property & litigation", "Financial health, valuation drivers and metrics to monitor",
                "Opportunities (bull case)", "Risks (bear case)", "Practical monitoring checklist",
                "Valuation and investor considerations (high-level)", "Bottom line", "SWOT Analysis"]:
        if key in sections and sections[key].strip() and not sections[key].strip().startswith('-'):
            # This is a bit aggressive, assuming most content in these is bulleted.
            # A more nuanced approach would check if the content *looks* like it should be bulleted.
            # For simplicity, if not starting with '-', prepend to ensure markdown bullet list.
            sections[key] = '- ' + sections[key].replace('\n\n', '\n- ').replace('\n', '\n- ').strip()
        sections[key] = sections[key].replace('\n- \n- ', '\n- ') # Remove empty bullet points
        sections[key] = sections[key].replace('\n- - ', '\n- ') # Fix for double bullets in SWOT
        
    return sections


def generate_hypothetical_data():
    """Generates hypothetical financial data for Ericsson, based on qualitative analysis."""
    years = pd.to_datetime([f'{y}-12-31' for y in range(2020, 2024)])
    
    # Revenue data: 5G boom, then stabilization
    revenue_mseks = np.array([232.4, 243.3, 271.5, 263.9]) * 1000 # in MSEK
    revenue_growth_rate = [0] + [((revenue_mseks[i] - revenue_mseks[i-1]) / revenue_mseks[i-1]) * 100 for i in range(1, len(revenue_mseks))]
    
    df_revenue = pd.DataFrame({
        'Year': years,
        'Revenue (MSEK)': revenue_mseks,
        'Revenue Growth (%)': revenue_growth_rate
    })

    # Margins: volatile, then improving or impacted by specific events
    gross_margin = np.array([38.5, 39.0, 41.0, 39.5]) # %
    operating_margin = np.array([10.2, 11.5, 9.8, 8.5]) # % - impacted by R&D, Vonage, competition
    net_profit_margin = np.array([6.5, 7.2, 5.0, 4.2]) # %
    
    df_margins = pd.DataFrame({
        'Year': years,
        'Gross Margin (%)': gross_margin,
        'Operating Margin (%)': operating_margin,
        'Net Profit Margin (%)': net_profit_margin
    })

    # Revenue by segment (hypothetical distribution, as percentages based on analysis text "Networks largest")
    df_segment_revenue = pd.DataFrame({
        'Segment': ['Networks', 'Digital Services', 'Managed Services', 'Emerging Business & Others'],
        'Revenue Share (%)': [70, 15, 10, 5], 
        'Revenue (MSEK)': revenue_mseks[-1] * np.array([0.70, 0.15, 0.10, 0.05])
    })

    # Competitor Market Share (hypothetical for RAN market, illustrating oligopoly)
    df_market_share = pd.DataFrame({
        'Vendor': ['Huawei', 'Ericsson', 'Nokia', 'Samsung', 'ZTE', 'Others'],
        'Market Share (%)': [28, 25, 20, 12, 10, 5] 
    })
    
    # Debt-to-Equity (illustrative, showing Vonage impact in 2022)
    d_to_e = np.array([0.8, 0.75, 1.2, 1.1]) 
    df_debt_equity = pd.DataFrame({
        'Year': years,
        'Debt-to-Equity Ratio': d_to_e
    })

    # Key Financial Metrics Table (snapshot)
    key_metrics_data = {
        'Metric': [
            'Latest Annual Revenue (MSEK)',
            'Revenue Growth (YoY %)',
            'Gross Margin (%)',
            'Operating Margin (%)',
            'Net Debt/Equity Ratio',
            'R&D Spend (as % of Revenue)'
        ],
        'Value': [
            f"{df_revenue['Revenue (MSEK)'].iloc[-1]:,.0f}",
            f"{df_revenue['Revenue Growth (%)'].iloc[-1]:.1f}%",
            f"{df_margins['Gross Margin (%)'].iloc[-1]:.1f}%",
            f"{df_margins['Operating Margin (%)'].iloc[-1]:.1f}%",
            f"{df_debt_equity['Debt-to-Equity Ratio'].iloc[-1]:.2f}",
            "~15-18%" # Qualitative from text "High R&D spending"
        ]
    }
    df_key_metrics = pd.DataFrame(key_metrics_data)

    return {
        'df_revenue': df_revenue,
        'df_margins': df_margins,
        'df_segment_revenue': df_segment_revenue,
        'df_market_share': df_market_share,
        'df_debt_equity': df_debt_equity,
        'df_key_metrics': df_key_metrics
    }


def create_charts(data):
    """Creates Plotly charts based on hypothetical data."""

    # 1. Revenue and Revenue Growth
    fig_revenue = px.line(data['df_revenue'], x='Year', y='Revenue (MSEK)',
                          title='Hypothetical Annual Revenue (MSEK)',
                          labels={'Revenue (MSEK)': 'Revenue (MSEK)'},
                          markers=True)
    fig_revenue.update_traces(hovertemplate='Year: %{x|%Y}<br>Revenue: %{y:,.0f} MSEK')
    fig_revenue.update_layout(xaxis_title="Year", yaxis_title="Revenue (MSEK)")

    fig_revenue_growth = px.bar(data['df_revenue'], x='Year', y='Revenue Growth (%)',
                                title='Hypothetical Revenue Growth (%)',
                                labels={'Revenue Growth (%)': 'Growth (%)'},
                                color='Revenue Growth (%)',
                                color_continuous_scale=px.colors.sequential.Viridis)
    fig_revenue_growth.update_traces(hovertemplate='Year: %{x|%Y}<br>Growth: %{y:.1f}%')
    fig_revenue_growth.update_layout(xaxis_title="Year", yaxis_title="Growth (%)")


    # 2. Profit Margins
    fig_margins = px.line(data['df_margins'], x='Year', y=['Gross Margin (%)', 'Operating Margin (%)', 'Net Profit Margin (%)'],
                          title='Hypothetical Profit Margin Trends (%)',
                          labels={'value': 'Margin (%)', 'variable': 'Margin Type'},
                          markers=True)
    fig_margins.update_layout(xaxis_title="Year", yaxis_title="Margin (%)")
    fig_margins.update_traces(hovertemplate='Year: %{x|%Y}<br>Margin: %{y:.1f}%')


    # 3. Revenue by Segment
    fig_segment_revenue = px.pie(data['df_segment_revenue'], values='Revenue Share (%)', names='Segment',
                                 title='Hypothetical Revenue Distribution by Segment (Latest Year)',
                                 hole=0.3)
    fig_segment_revenue.update_traces(textinfo='percent+label', pull=[0.05 if s == 'Networks' else 0 for s in data['df_segment_revenue']['Segment']],
                                      hovertemplate='<b>%{label}</b><br>Share: %{percent}<br>Revenue: %{customdata:,.0f} MSEK',
                                      customdata=data['df_segment_revenue']['Revenue (MSEK)'])
    fig_segment_revenue.update_layout(showlegend=True)


    # 4. Competitor Market Share
    fig_market_share = px.bar(data['df_market_share'], x='Market Share (%)', y='Vendor', orientation='h',
                              title='Hypothetical Global RAN Market Share Distribution',
                              color='Market Share (%)',
                              color_continuous_scale=px.colors.sequential.Plasma)
    fig_market_share.update_layout(yaxis={'categoryorder':'total ascending'})
    fig_market_share.update_traces(hovertemplate='Vendor: %{y}<br>Share: %{x:.1f}%')


    # 5. Debt-to-Equity Ratio
    fig_debt_equity = px.line(data['df_debt_equity'], x='Year', y='Debt-to-Equity Ratio',
                              title='Hypothetical Debt-to-Equity Ratio',
                              labels={'Debt-to-Equity Ratio': 'D/E Ratio'},
                              markers=True)
    fig_debt_equity.update_traces(hovertemplate='Year: %{x|%Y}<br>D/E Ratio: %{y:.2f}')
    fig_debt_equity.update_layout(xaxis_title="Year", yaxis_title="Ratio")


    return {
        'fig_revenue': fig_revenue,
        'fig_revenue_growth': fig_revenue_growth,
        'fig_margins': fig_margins,
        'fig_segment_revenue': fig_segment_revenue,
        'fig_market_share': fig_market_share,
        'fig_debt_equity': fig_debt_equity
    }


# The full analysis text provided in the prompt
FINANCIAL_ANALYSIS_TEXT = """
Let's dive into an analysis of **Ericsson (ERIC)**, a prominent player in the telecommunications infrastructure and services sector. To provide a comprehensive financial ecosystem analysis, we'll break it down into several key areas:

## Ericsson (ERIC) - Financial Ecosystem Analysis

**1. Core Business and Revenue Drivers:**

*   **Primary Business:** Ericsson is a leading provider of telecommunications equipment, software, and services. Their core offerings include:
    *   **Networks:** This segment is the largest and includes mobile radio access (5G, 4G, 3G), core network solutions, and transmission equipment. This is heavily driven by network deployments and upgrades, particularly the ongoing 5G rollout globally.
    *   **Digital Services:** This encompasses cloud-native software solutions for operators, including cloud-native core networks, orchestrations, AI/ML-driven operations, and business support systems (BSS) and operations support systems (OSS). This segment is crucial for operators looking to modernize their networks and leverage cloud technologies.
    *   **Managed Services:** Ericsson provides end-to-end managed services for telecommunications networks, including network operations, maintenance, and optimization. This offers a recurring revenue stream for the company.
    *   **Emerging Business:** This includes areas like IoT connectivity solutions, enterprise networks, and private networks, which are becoming increasingly important growth areas.
*   **Key Revenue Drivers:**
    *   **5G Network Deployments:** The global transition to 5G is the most significant driver of Ericsson's revenue. Demand for radio access network (RAN) equipment, core network components, and associated services is directly tied to this rollout.
    *   **Operator Spending Cycles:** Telecommunications operators have cyclical capital expenditure (CapEx) cycles. Investments in new technologies (like 5G) and network upgrades are major catalysts.
    *   **North America and Asia-Pacific Markets:** These regions are typically major drivers of network spending due to high mobile penetration and rapid technological adoption.
    *   **Service Contracts:** Long-term managed service contracts and professional services contribute to stable, recurring revenue.
    *   **Enterprise and Private Networks:** Growth in private 5G networks for industries and the expansion of IoT are emerging revenue streams.

**2. Financial Health and Key Ratios (General Observations - specific numbers require current data):**

*   **Revenue Growth:** Analyze trends in reported revenue, paying attention to segment performance. Look for consistent growth, especially in Network and Digital Services.
*   **Profitability:**
    *   **Gross Profit Margin:** Indicates efficiency in production and service delivery.
    *   **Operating Profit Margin (EBIT Margin):** Crucial for understanding profitability from core operations. Watch for trends and any impact from R&D investments or competitive pressures.
    *   **Net Profit Margin:** The bottom line.
    *   **EBITDA:** A measure of operational cash flow generation.
*   **Balance Sheet:**
    *   **Debt-to-Equity Ratio:** Indicates leverage. A high ratio can signal higher financial risk.
    *   **Current Ratio/Quick Ratio:** Measures short-term liquidity.
*   **Cash Flow:**
    *   **Operating Cash Flow:** The most important indicator of a company's ability to generate cash from its core business.
    *   **Free Cash Flow (FCF):** Cash available after capital expenditures, crucial for dividends, buybacks, and debt reduction.
*   **Key Performance Indicators (KPIs) for the Telecom Infrastructure Sector:**
    *   **Gross Margin Evolution:** Particularly in the RAN segment, margins can be sensitive to competitive pricing and product mix.
    *   **R&D Intensity:** High R&D spending is crucial for staying ahead in the technology race, but it can impact short-term profitability.
    *   **Order Intake/Backlog:** A forward-looking indicator of future revenue.

**3. Market Dependencies and Industry Structure:**

*   **Oligopolistic Market:** The telecommunications infrastructure market is highly consolidated, with a few major global players.
*   **Key Competitors:**
    *   **Nokia (NOK):** Ericsson's most direct and significant competitor in RAN and core network solutions.
    *   **Huawei (HW):** A major global competitor, though its market share has been impacted by geopolitical restrictions in some regions.
    *   **Samsung (005930.KS):** A growing player, particularly in specific markets and technologies.
    *   **ZTE (000063.SZ):** Another Chinese competitor with a significant presence.
    *   **Cloud Providers (AWS, Azure, GCP):** While not direct hardware competitors, they are increasingly involved in providing cloud infrastructure that underpins network functions (e.g., cloud-native core networks).
*   **Customer Concentration:** Ericsson's customer base consists of a relatively small number of large telecommunications operators worldwide. This can lead to significant revenue concentration with individual clients.
*   **Technology Lifecycle:** The industry is driven by rapid technological evolution (3G -> 4G -> 5G -> future 6G). Companies need to invest heavily in R&D to remain competitive.
*   **Supply Chain:** Ericsson relies on a complex global supply chain for its components. Disruptions (like semiconductor shortages) can significantly impact production and delivery.

**4. Sector Connections and Interdependencies:**

*   **Telecommunications Operators:** Ericsson's fate is intrinsically linked to the financial health and CapEx spending of mobile network operators (MNOs) like Verizon, AT&T, T-Mobile, Vodafone, Orange, etc.
*   **Semiconductor Manufacturers:** As a hardware provider, Ericsson is a major customer of semiconductor companies that produce chips for its equipment.
*   **Software and Cloud Providers:** Increasing reliance on cloud-native software means stronger ties with cloud infrastructure providers and software developers.
*   **Enterprise and Vertical Industries:** Growing involvement in private networks and IoT connects Ericsson to sectors like manufacturing, logistics, healthcare, and smart cities.
*   **Governments and Regulators:** Government policies, spectrum auctions, and national security concerns (especially regarding Chinese vendors) can significantly influence the competitive landscape and market access.

**5. Geopolitical and Regulatory Factors:**

*   **US-China Tech Rivalry:** Restrictions on Huawei in many Western markets have benefited competitors like Ericsson and Nokia. However, this also creates uncertainty and can lead to retaliatory measures or shifts in global supply chains.
*   **National Security Concerns:** Governments are increasingly scrutinizing the security of telecommunications infrastructure, leading to "cleansing" initiatives in some countries where foreign vendors are being phased out.
*   **Spectrum Allocation:** The availability and cost of radio spectrum are critical for operators, influencing their investment decisions in new network technologies.
*   **Trade Policies and Tariffs:** Global trade policies can impact the cost of components and the competitiveness of Ericsson's products in different markets.
*   **Data Privacy Regulations:** Increasingly stringent data privacy laws can influence the development and deployment of network services.

**6. Economic Factors:**

*   **Global Economic Growth:** A strong global economy generally translates to higher consumer spending on mobile services, encouraging operator investment.
*   **Interest Rates:** Higher interest rates can increase the cost of capital for both Ericsson and its operator customers, potentially impacting CapEx.
*   **Inflation:** Rising inflation can affect component costs, labor costs, and overall pricing power.
*   **Currency Fluctuations:** Ericsson operates globally, so fluctuations in currency exchange rates can impact reported revenues and profitability.
*   **Consumer Demand for Data:** The ever-increasing demand for mobile data, video streaming, and online services is a fundamental driver for network upgrades and expansion.

**7. SWOT Analysis (Internal Strengths/Weaknesses, External Opportunities/Threats):**

*   **Strengths:** Strong R&D capabilities, global presence, established relationships with major operators, comprehensive product portfolio.
*   **Weaknesses:** Intense competition, sensitivity to operator CapEx cycles, potential margin pressure, reliance on a few large customers.
*   **Opportunities:** Global 5G rollout, growth in private networks, expansion into emerging markets and enterprise solutions, cloudification of networks.
*   **Threats:** Geopolitical risks, intense competition (especially from Huawei and Samsung), supply chain disruptions, regulatory changes, economic downturns impacting operator spending.

**In summary, Ericsson operates in a dynamic and capital-intensive industry.** Its financial performance is heavily influenced by the pace of global 5G deployments, the CapEx decisions of major telecommunications operators, and the complex geopolitical landscape. Success hinges on continuous innovation, efficient execution, and navigating the intricate relationships with its customers, competitors, and regulators.

**To perform a truly in-depth analysis, you would need to:**

*   **Access current financial statements:** Review Ericsson's latest quarterly and annual reports for specific revenue figures, profitability ratios, debt levels, and cash flow.
*   **Analyze historical performance:** Track trends over several years to understand cyclicality and long-term growth.
*   **Examine analyst reports and guidance:** See what financial analysts are projecting for Ericsson's future performance.
*   **Monitor industry news:** Stay updated on 5G deployment trends, competitor announcements, and regulatory developments.

By considering these interconnected factors, one can build a robust understanding of Ericsson's financial ecosystem and its prospects.

---

Below is a comprehensive, structured analysis of ERIC (Telefonaktiebolaget LM Ericsson — traded as ERIC on Nasdaq), focused on the financial ecosystem: key revenue relationships, market and sector dependencies, competitor and partner dynamics, supplier and customer concentration, regulatory and macroeconomic drivers, principal risks and upside opportunities, and practical indicators for monitoring the stock.

Company snapshot (context)
- Core business lines: Radio Access Network (RAN) equipment (macro and small cells), Transport/optical networks, Core networks and cloud-native software (including 5G core), Managed services and network rollout services, and patent/IP licensing.
- Revenue profile: mix of equipment sales (project/capex-driven) and recurring/services revenue (managed services, software, maintenance). R&D-intensive with substantial patent/IP activity and licensing income.

Key financial relationships and drivers
- Operator capex cycles -> Revenues and margins: Telecom carriers’ capital expenditure (capex) plans directly drive Ericsson’s equipment sales. When carriers accelerate 5G rollouts or upgrade backhaul/transport, Ericsson sees large equipment orders and revenue recognition events.
- Services/Software mix -> Margin stability and recurring cash flows: Growth in managed services and software increases recurring revenue and typically produces higher, steadier gross margins than one-off hardware sales. Shift from hardware to software/cloud (network-as-software) improves EBITDA margin potential over time.
- Order intake & backlog -> Forward revenue visibility: New contract wins and order backlog are leading indicators of revenue over next quarters. Large multi-year deals create revenue visibility and recurring service streams.
- R&D spend -> IP portfolio, product competitiveness: High R&D is needed to keep parity/lead in 5G/6G, cloud-native cores, Open RAN, and optical solutions. R&D increases hamper short-term free cash flow but protect long-term market position and licensing income.
- Working capital & project execution -> Cash flow volatility: Large projects, milestone billing, and contract performance (penalties/bonuses) can produce lumpy free cash flow. Effective project management is critical to protect margins and cash conversion.
- Currency: Reported in SEK but large portion of revenue in USD/EUR. FX swings (SEK vs USD/EUR) affect reported results and costs (R&D payroll in SEK, sales in global currencies).

Market dependencies
- 5G rollout phases: Ericsson’s near- to medium-term growth is tightly coupled to global 5G phases — initial coverage builds, capacity densification, and enterprise/private 5G adoption. Enterprise 5G, FWA (fixed wireless access), and industrial IoT are growth channels after initial mobile-network buildouts.
- Operator capex health: Carrier profitability, ARPU, subscriber trends, and debt levels influence their willingness to spend. Macroeconomic weakness or higher interest rates can compress carrier capex.
- Spectrum auctions and availability: Timelines and outcomes for spectrum allocation determine operator build plans and procurement timing.
- Government procurement policy and telecom security initiatives: Western government restrictions on certain vendors (e.g., Huawei) or support packages (procurement preferences, security-driven vendor selection) materially affect competitive positioning and addressable market in multiple countries.

Sector and technology connections
- Semiconductor and optical component supply chain: Ericsson depends on timely supply of high-end semiconductors (RF front-end, baseband processors, custom ASICs/FPGAs), photonics, and passive components. Global chip shortages or export controls can delay deliveries and increase costs.
- Cloud providers & virtualization ecosystem: Partnerships/integration with AWS, Microsoft Azure, Google Cloud and major cloud-native/open-source stacks are central as networks virtualize. Ericsson’s cloud-native core and network functions depend on these ecosystems for deployment and market reach.
- Open RAN & disaggregation movement: Momentum toward Open RAN standards affects hardware/software margins and supplier relationships. Open RAN can create opportunities (new vendors, software sales) but introduces new competitors and price pressure.
- Optical/transport partners & competitors: For transport and optical segments, competitors like Ciena and Nokia come into play; interop with vendors in optical supply chain matters.

Competitors and industry relationships
- Primary competitors: Nokia (public peer), Huawei (private—dominant in many markets), Samsung Networks, ZTE (China-focused), and to some extent Cisco/Juniper/Ciena in transport and core segments.
- Differentiation pressures: Huawei’s price/performance in many markets creates pricing pressure; Nokia is a close technological and commercial peer. Samsung is competitive in certain markets (e.g., SK Telecom, some Asian carriers).
- Enterprise/IT competitors: For cloud-native cores, orchestration, network slicing, and edge computing, competition overlaps with large IT players and cloud vendors (Cisco, VMware historically, cloud hyperscalers that partner or compete).
- Partner ecosystem: Ericsson partners with major global operators (Verizon, AT&T, T-Mobile, Vodafone, Telefonica, China Mobile/Unicom/Telecom where contracts exist), cloud providers (AWS/Azure/Google), and numerous systems integrators. Strategic alliances can accelerate deployments and reduce time-to-market for new services.

Customer concentration and counterparty risk
- Large carriers as anchor customers: A small number of large carriers typically drive a meaningful share of sales. Losses or delayed spend by a key customer (e.g., a major US carrier or a large European/Asian operator) can materially affect revenue.
- Contract structure risk: Large multi-year contracts often include milestones, penalty clauses, and long payment cycles—contract terms can affect cash conversion and margin if implementation problems occur.

Regulatory, geopolitical and macroeconomic factors
- Geopolitics & export controls: U.S.-China tensions and export controls on advanced chips or telecommunications equipment can limit addressable markets (e.g., ability to sell certain high-end products into China) or conversely open opportunities in Western markets due to restrictions on certain suppliers.
- National security policies: Governments’ decisions to restrict vendors for “security” reasons can reconfigure market share across regions (positive for Ericsson in Western markets if competitors are excluded).
- Subsidies and stimulus (e.g., digital infrastructure funding): Government grants or stimulus for broadband/5G infrastructure (e.g., US funding programs) support accelerated deployments.
- Macro cycle: GDP growth, consumer spending, and enterprise IT budgets influence carrier revenues and capex; higher rates increase carriers’ cost of capital and may delay capex.
- Currency and inflation: Inflationary cost pressures (labor, component prices) can compress margins unless price increases or productivity offset. SEK/USD/EUR moves affect reported performance.

Intellectual property & litigation
- Licensing income and patent portfolio: Ericsson’s IP licensing provides higher-margin revenue, but licensing is sensitive to litigation outcomes, disputes, and global legal frameworks.
- Compliance and legal risk: Historical compliance fines and potential legal disputes (e.g., sales practices in some countries) can create episodic charges and reputational issues.

Financial health, valuation drivers and metrics to monitor
- Revenue mix shifts: Watch the proportion of equipment vs services/software revenue. Increasing services/software share is often positive for margins and predictability.
- Order intake & backlog growth: Rising order intake and healthy backlog point to sustained revenue growth; cancellations or downward revisions are red flags.
- Gross and operating margins: Margins reflect product mix, pricing, and execution. Improvement in software/services mix and better supply chain execution should raise margins.
- Free cash flow and cash conversion: Because large projects can be lumpy, FCFF and operating cash flow conversion relative to EBITDA are key for valuation and dividend sustainability.
- Leverage / net debt: Capital structure and ability to fund R&D and working capital without excessive leverage matters for risk profile.
- R&D intensity and capex: Sustained investment is required to maintain competitiveness; monitor absolute R&D and capex as percent of sales.
- Dividend / capital returns policy: If applicable, track payout ratios and cash available for shareholders vs reinvestment needs.

Opportunities (bull case)
- Acceleration of 5G network deployments (especially in Western markets and enterprise/private 5G).
- Market share gains where competitors are restricted (security-driven exclusions of other vendors).
- Growth of managed services, software, and cloud-native network functions that produce recurring, higher-margin revenue.
- Open RAN uptake where Ericsson can leverage software/virtualization strengths or partner with new hardware suppliers.
- Expansion in adjacent markets: private 5G, industrial IoT, fixed wireless access, edge compute, and enterprise networking.

Risks (bear case)
- Intense pricing competition, particularly from Huawei and low-cost suppliers, compresses margins.
- Execution risk on large contracts: rollout delays, penalties, higher-than-expected costs.
- Geopolitical limits on market access (e.g., losing or being unable to serve large markets due to export controls).
- Semiconductor/parts shortages or rising component costs reducing shipments and margin.
- Carrier capex slowdown due to weaker macro/interest rates raising financing costs for carriers.
- Regulatory or legal costs related to compliance or litigation.

Practical monitoring checklist (what to watch quarterly/monthly)
- Order intake and order backlog trends and commentary on timing of deliveries.
- Revenue growth by segment: RAN, Cloud/Core, Managed Services, Transport, Licensing.
- Gross margin and operating margin evolution and drivers (mix, pricing, restructuring).
- Free cash flow, capex, and working capital swings — note any one-off timing effects.
- R&D spending levels and any statements on roadmap for 5G evolution and 6G initiatives.
- Major contract announcements or losses (especially with top carriers).
- Geopolitical/regulatory announcements affecting market access (e.g., nation-level bans or subsidy programs).
- Supplier constraints or component cost movements (semiconductor availability).
- Changes in major customer capex guidance (large carriers’ quarterly reports and capex guidance).
- Patent disputes / licensing settlements or rulings.

Valuation and investor considerations (high-level)
- Relative valuation vs peers (Nokia, assuming public peers) should reflect growth prospects, margin trajectory, and capital intensity.
- Investors valuing ERIC should consider the cyclicality of equipment revenue, the trend toward higher-margin services/software, the company’s order/backlog cadence, and geopolitical tailwinds/he
adwinds.
- Key catalysts: large multi-year contracts, favorable regulatory shifts, acceleration in enterprise 5G, or significant improvements in cash conversion and margins.

Bottom line
ERIC’s financial ecosystem is tightly coupled to global telecom operator capex cycles, the pace of 5G and next-generation network rollouts, supply-chain stability (especially semiconductors), and geopolitically driven market access. Long-term upside comes from software and services recurring revenue, Open RAN/cloud-native opportunities, and IP licensing. Principal near-term risks are execution on large contracts, competitive pricing pressure (notably from Huawei), and macro-driven capex slowdowns. For investors, tracking order intake, backlog, services revenue share, margins, cash conversion, and major customer/country developments provides the clearest window into future performance.

If you want, I can:
- Pull the latest quarterly metrics (revenue by segment, margins, backlog, order intake) and show how they’ve trended in the last 4 quarters;
- Produce a peer-comparison table (key multiples, margins) versus Nokia, Samsung (if market-data available), and Ciena; or
- Model a scenario-based sensitivity (e.g., operator capex down 10% vs up 10%) to estimate potential revenue and earnings impact. Which would you prefer?

---

Of course. Here is a comprehensive financial ecosystem analysis for **Ericsson (ERIC)**, the Swedish multinational networking and telecommunications company.

### **1. Core Business & Financial Identity**
Ericsson is a **leader in the Information Technology and Communication Equipment sector**, primarily focused on:
*   **Networks:** Building mobile and fixed network infrastructure (5G, IoT).
*   **Digital Services:** Cloud-native software and services for telecom operators.
*   **Managed Services:** Outsourcing network operations and optimization.
*   **Emerging Business:** Enterprise wireless solutions (private networks) and the Vonage acquisition (cloud communications APIs).

**Key Financial Metrics & Health:**
*   **Revenue Model:** Heavily project-based and cyclical, tied to global telecom operator capital expenditure (CapEx).
*   **Profitability:** Historically volatile, but has undergone significant restructuring. Focus is on improving margins, particularly in the high-margin software segments.
*   **Balance Sheet:** Generally strong, but carries debt. The acquisition of Vonage in 2022 significantly increased leverage, which management is committed to reducing.
*   **Geographic Exposure:** Diversified globally, with key markets in North America (Verizon, AT&T), Europe, and parts of Asia. Notably **exposed to geopolitical tensions** (e.g., exit from China, sanctions impacting Russia).

### **2. Primary Market Dependencies & Economic Factors**
Ericsson's performance is a direct function of macro and industry-specific cycles.

*   **Telecom Operator CapEx Cycles:** The single biggest driver. Global rollouts of 5G networks have been a multi-year tailwind, but spending is now entering a more normalized, potentially uneven phase as operators focus on monetization.
*   **Global GDP & Interest Rates:** Economic slowdowns can cause operators to delay or reduce infrastructure spending. Higher interest rates increase financing costs for both Ericsson and its customers, potentially dampening large projects.
*   **Technology Adoption Curve:** The pace of 5G deployment, followed by the future roadmap to 6G, dictates the upgrade cycle. Adoption of IoT and enterprise private networks represents a growth vector.
*   **Currency Fluctuations:** As a global company reporting in SEK, a strong Swedish Krona can negatively impact translated revenues and profits from key markets like the US.

### **3. Sector Connections & The Value Chain**
Ericsson sits at the **core of the telecom ecosystem**:

*   **Upstream (Suppliers):** Relies on semiconductor manufacturers (e.g., Intel, Qualcomm, analog/RF chipmakers), hardware component suppliers, and software partners. Supply chain disruptions and chip shortages directly impact delivery and costs.
*   **Downstream (Customers):** Almost entirely **Telecom Service Providers (TSPs)** like Verizon, AT&T, Deutsche Telekom, Vodafone, and emerging market operators. Their financial health and strategic priorities are paramount.
*   **Parallel Industries:** Cloud providers (AWS, Microsoft Azure) are both partners (for cloud-native solutions) and potential long-term competitors in enterprise networks. The **enterprise/private network** segment connects it to verticals like manufacturing, logistics, healthcare, and ports.

### **4. Competitor Relationships & The Competitive Landscape**
Ericsson operates in a highly concentrated, oligopolistic global market.

*   **Direct Head-to-Head Competitors:**
    *   **Nokia (NOK):** Its most direct European rival across all product lines. Market share battles are intense in every region.
    *   **Huawei (China):** The global market share leader, but its position has been eroded in many Western markets (US, UK, Sweden, Australia) due to geopolitical security concerns. This has been a **major secular tailwind** for Ericsson and Nokia.
    *   **Samsung:** A strong competitor in specific markets (notably South Korea and the US) and a growing force in network equipment, particularly in 5G.
*   **Competitive Dynamics:** The market is characterized by intense pricing pressure, high R&D costs (to stay at the technology frontier), and strategic long-term contracts. Differentiation is increasingly through software, automation, and energy efficiency.

### **5. Key Risks & Catalysts**
**Risks:**
*   **Geopolitical Risk:** Trade wars, sanctions (Russia), and national security policies can instantly alter market access (e.g., loss of business in China, uncertainty in other regions).
*   **Customer Concentration:** A small number of large operators account for a significant portion of revenue.
*   **Execution & Integration Risk:** Successfully integrating Vonage and realizing its promised platform synergies is critical.
*   **Technological Disruption:** Failure to lead in 6G R&D or a shift towards open RAN (Open Radio Access Networks), which could lower barriers to entry.

**Catalysts:**
*   **New 5G Spectrum Auctions:** Release of new mid-band spectrum (e.g., in India, Europe) triggers new investment cycles.
*   **Enterprise Growth:** Successful scaling of the private networks and wireless enterprise business, leveraging Vonage's API platform.
*   **Market Share Gains:** Continued substitution of Huawei in geopolitically aligned markets.
*   **Margin Expansion:** Successful execution on cost savings and a higher mix of software sales improving overall profitability.
*   **Reduction in Net Debt:** Faster-than-expected deleveraging post-Vonage would be viewed positively by the market.

### **6. Investment Thesis Summary**
Ericsson is a **cyclical growth and turnaround story** intertwined with **geopolitical realignment**.

*   **Bull Case:** Ericsson is a primary beneficiary of the global 5G rollout and the exclusion of Huawei from key markets. Its technology leadership, combined with the potential of its enterprise and cloud-native software strategy (via Vonage), positions it for sustained margin improvement and less cyclical earnings.
*   **Bear Case:** The company is at the mercy of volatile telecom CapEx cycles. Intense competition with Nokia and Samsung limits pricing power. The Vonage acquisition was expensive and adds execution risk and debt. Geopolitical tensions remain a persistent threat.

**Final Note:** Analyzing ERIC requires monitoring **quarterly reports for order intake, gross margin trends, and free cash flow**, as well as **industry data on global telecom CapEx forecasts**. It is not just a stock, but a proxy for the health and direction of global telecommunications infrastructure investment.
"""

# --- Streamlit App ---
st.set_page_config(layout="wide", page_title="Ericsson (ERIC) Financial Analysis")

st.title("Ericsson (ERIC) - Comprehensive Financial Ecosystem Analysis")

# Parse the text
parsed_sections = parse_analysis_text(FINANCIAL_ANALYSIS_TEXT)

# Generate hypothetical data and charts
hypothetical_data = generate_hypothetical_data()
charts = create_charts(hypothetical_data)

# --- Display Content ---

# Overall Introduction
st.markdown(parsed_sections.get("Overall Introduction", "No overall introduction found."))
st.markdown("---") 

# Key Metrics Snapshot (Hypothetical)
st.header("Key Metrics Snapshot (Hypothetical)")
st.dataframe(hypothetical_data['df_key_metrics'].set_index('Metric'), use_container_width=True)
st.info("Note: All numerical values and charts presented are hypothetical and illustrative, based on the qualitative analysis provided in the text. They do not reflect real-time financial data.")

# Financial Charts
st.subheader("Key Financial Trends (Hypothetical)")
col1_metrics, col2_metrics = st.columns(2)
with col1_metrics:
    st.plotly_chart(charts['fig_revenue'], use_container_width=True)
with col2_metrics:
    st.plotly_chart(charts['fig_revenue_growth'], use_container_width=True)

st.plotly_chart(charts['fig_margins'], use_container_width=True)
st.plotly_chart(charts['fig_debt_equity'], use_container_width=True)
st.plotly_chart(charts['fig_segment_revenue'], use_container_width=True)

st.markdown("---")

# Company Snapshot (Context)
st.header("Company Snapshot (Context)")
st.markdown(parsed_sections.get("Company snapshot (context)", "No company snapshot details found."))
st.markdown("---")

# Key Financial Relationships & Drivers
st.header("Key Financial Relationships & Drivers")
st.markdown(parsed_sections.get("Key financial relationships and drivers", "No key financial relationships and drivers found."))
st.markdown("---")

# Market Dependencies
st.header("Market Dependencies")
st.markdown(parsed_sections.get("Market dependencies", "No market dependencies found."))
st.markdown("---")

# Sector and Technology Connections
st.header("Sector & Technology Connections")
st.markdown(parsed_sections.get("Sector and technology connections", "No sector and technology connections found."))
st.markdown("---")

# Competitors and Industry Relationships
st.header("Competitors & Industry Relationships")
st.markdown(parsed_sections.get("Competitors and industry relationships", "No competitor information found."))
st.plotly_chart(charts['fig_market_share'], use_container_width=True) # Competitor Market Share Chart
st.markdown("---")

# Customer Concentration and Counterparty Risk
st.header("Customer Concentration & Counterparty Risk")
st.markdown(parsed_sections.get("Customer concentration and counterparty risk", "No customer concentration information found."))
st.markdown("---")

# Regulatory, Geopolitical and Macroeconomic Factors
st.header("Regulatory, Geopolitical & Macroeconomic Factors")
st.markdown(parsed_sections.get("Regulatory, geopolitical and macroeconomic factors", "No regulatory, geopolitical or macroeconomic factors found."))
st.markdown("---")

# Intellectual Property & Litigation
st.header("Intellectual Property & Litigation")
st.markdown(parsed_sections.get("Intellectual property & litigation", "No IP & litigation information found."))
st.markdown("---")

# Financial Health, Valuation Drivers & Metrics to Monitor
st.header("Financial Health, Valuation Drivers & Metrics to Monitor")
st.markdown(parsed_sections.get("Financial health, valuation drivers and metrics to monitor", "No financial health or metrics to monitor found."))
st.markdown("---")

# SWOT Analysis (from the first block, distinct from O/R from the second block)
st.header("SWOT Analysis")
st.markdown(parsed_sections.get("SWOT Analysis", "No SWOT analysis found."))
st.markdown("---")

# Opportunities (Bull Case) & Risks (Bear Case)
st.header("Opportunities (Bull Case) & Risks (Bear Case)")
col_opp, col_risk = st.columns(2)
with col_opp:
    st.subheader("Opportunities (Bull Case)")
    st.markdown(parsed_sections.get("Opportunities (bull case)", "No opportunities found."))
with col_risk:
    st.subheader("Risks (Bear Case)")
    st.markdown(parsed_sections.get("Risks (bear case)", "No risks found."))
st.markdown("---")

# Practical Monitoring Checklist
st.header("Practical Monitoring Checklist")
st.markdown(parsed_sections.get("Practical monitoring checklist", "No monitoring checklist found."))
st.markdown("---")

# Valuation and Investor Considerations
st.header("Valuation & Investor Considerations (High-Level)")
st.markdown(parsed_sections.get("Valuation and investor considerations (high-level)", "No investor considerations found."))
st.markdown("---")

# Bottom Line
st.header("Bottom Line")
st.markdown(parsed_sections.get("Bottom line", "No bottom line summary found."))
st.markdown("---")

st.markdown("""
<br><br>
**Disclaimer:** This analysis is based on the provided text and contains hypothetical data for illustrative purposes only. It should not be considered financial advice. For actual investment decisions, consult current financial statements, professional analysts, and market data.
""", unsafe_allow_html=True)