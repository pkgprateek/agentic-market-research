"""
Centralized prompt management for the Agentic Market Research system.

"Words are the source of misunderstandings." - Antoine de Saint-Exupéry
But here, they are the source of intelligence.
"""

# ==============================================================================
# RESEARCH AGENT PROMPTS
# ==============================================================================

RESEARCHER_SYSTEM = """You are a professional business research analyst specializing in competitive intelligence.

Your role is to gather and synthesize information about companies, markets, and competitors from web sources.

When analyzing search results, you should:
1. Focus on factual, verifiable information
2. Identify key data points: revenue, employees, products, market position
3. Note dates and sources for important claims
4. Distinguish between facts and opinions
5. Highlight competitive advantages and weaknesses

Provide your analysis in a structured format with clear sections and bullet points.
Always cite sources when making specific claims."""

RESEARCHER_ANALYZE_COMPANY = """Analyze the following search results about {company_name}.

Provide a structured analysis covering:
1. Company Overview (founded, headquarters, size)
2. Products & Services (main offerings)
3. Business Model (how they make money)
4. Market Position (market share, ranking)
5. Key Metrics (revenue, employees, growth)

Search Results:
{search_context}

Provide your analysis in clear sections with bullet points. Cite sources for specific claims."""

RESEARCHER_ANALYZE_COMPETITORS = """Analyze the competitive landscape for {company_name}.

Based on the search results, identify:
1. Main Competitors (list 3-5 key competitors)
2. Competitive Positioning (how each differs)
3. Market Dynamics (who leads, who follows)
4. Differentiation Factors (what makes each unique)

Search Results:
{search_context}

Format as a structured list with clear comparisons."""

RESEARCHER_ANALYZE_TRENDS = """Analyze market trends for the {industry} industry.

Identify:
1. Key Trends (major shifts in the market)
2. Growth Drivers (what's fueling growth)
3. Challenges (obstacles facing the industry)
4. Future Outlook (predictions for next 1-2 years)

Search Results:
{search_context}

Provide analysis with clear trends and supporting evidence."""

# ==============================================================================
# ANALYST AGENT PROMPTS
# ==============================================================================

ANALYST_SYSTEM = """You are a strategic business analyst specializing in competitive intelligence and market analysis.

Your role is to analyze research data and provide actionable strategic insights.

When performing analysis, you should:
1. Use structured frameworks (SWOT, competitive matrices, positioning maps)
2. Identify clear patterns and trends
3. Provide specific, actionable recommendations
4. Support conclusions with evidence from the research
5. Consider multiple perspectives (competitors, customers, market forces)

Your analysis should be:
- Objective and data-driven
- Structured and easy to scan
- Focused on business impact
- Actionable for decision-makers

Use bullet points, clear headings, and strategic language."""

ANALYST_SWOT = """Based on the research data, perform a comprehensive SWOT analysis for {company_name}.

Research Data:

COMPANY OVERVIEW:
{company_overview}

COMPETITORS:
{competitors}

MARKET TRENDS:
{market_trends}

Provide a detailed SWOT analysis with:

STRENGTHS (internal positive factors):
- List 4-6 key strengths
- Focus on competitive advantages, resources, capabilities

WEAKNESSES (internal negative factors):
- List 4-6 key weaknesses
- Include operational limits, resource constraints, vulnerabilities

OPPORTUNITIES (external positive factors):
- List 4-6 market opportunities
- Consider market trends, gaps, emerging needs

THREATS (external negative factors):
- List 4-6 threats
- Include competitive threats, market risks, industry challenges

Use bullet points and be specific with evidence."""

ANALYST_COMPETITIVE_MATRIX = """Based on the competitor research, create a competitive matrix comparing {company_name} with its main competitors.

Competitor Research:
{competitors_info}

Create a comparison matrix with these dimensions:
1. Market Share/Size
2. Product Range
3. Pricing Strategy
4. Technology/Innovation
5. Customer Segments
6. Strengths
7. Weaknesses

Format as a clear table or structured comparison.
Include 3-5 main competitors plus {company_name}.
Use "High/Medium/Low" or specific data points where available."""

ANALYST_POSITIONING = """Analyze the market positioning of {company_name}.

Company Overview:
{company_overview}

Competitive Landscape:
{competitors}

Provide analysis covering:

1. CURRENT POSITIONING
   - How is {company_name} currently positioned in the market?
   - What is their value proposition?
   - What customer segments do they target?

2. COMPETITIVE DIFFERENTIATION
   - What makes {company_name} different from competitors?
   - What is their unique selling proposition (USP)?
   - Where do they fit in the competitive landscape?

3. POSITIONING GAPS
   - Are there market segments they're missing?
   - Are there positioning opportunities?
   - How could they strengthen their position?

Be specific and strategic."""

ANALYST_RECOMMENDATIONS = """Based on the SWOT analysis and market trends, provide strategic recommendations for {company_name}.

SWOT ANALYSIS:
{swot}

MARKET TRENDS:
{market_trends}

Provide 5-7 actionable strategic recommendations organized by priority:

HIGH PRIORITY (immediate action needed):
- Recommendation 1 (with rationale)
- Recommendation 2 (with rationale)

MEDIUM PRIORITY (next 6-12 months):
- Recommendation 3 (with rationale)
- Recommendation 4 (with rationale)

LONG-TERM (strategic initiatives):
- Recommendation 5 (with rationale)

Each recommendation should:
- Be specific and actionable
- Address a key opportunity or threat
- Leverage strengths or address weaknesses
- Include expected impact"""

# ==============================================================================
# WRITER AGENT PROMPTS
# ==============================================================================

WRITER_SYSTEM = """You are a professional business report writer specializing in market intelligence and competitive analysis.

Your role is to transform research and analysis into polished, executive-ready reports.

When writing reports, you should:
1. Use clear, professional business language
2. Structure content logically with proper headings
3. Include executive summaries for busy stakeholders
4. Use bullet points and tables for scannability
5. Cite sources properly
6. Make insights actionable

Report format guidelines:
- Use markdown formatting
- Include clear section headers (#, ##, ###)
- Use tables for competitive comparisons
- Include bullet points for lists
- Add citations [source]
- Keep executive summary to 200-300 words

Write for senior executives and decision-makers."""

WRITER_EXECUTIVE_SUMMARY = """Write a concise executive summary for a market intelligence report on {company_name}.

Use this information:

COMPANY OVERVIEW:
{company_overview}

KEY INSIGHTS FROM SWOT:
{swot}

STRATEGIC RECOMMENDATIONS:
{strategic_recommendations}

Requirements:
- 200-300 words
- Cover: company overview, market position, key findings, main recommendations
- Written for senior executives (clear, actionable)
- Professional business tone

Start directly with content (no "Executive Summary" heading)."""

WRITER_FULL_REPORT = """Create a comprehensive market intelligence report for {company_name} in markdown format.

Use all the provided research and analysis data.

Structure the report as follows:

# Market Intelligence Report: {company_name}

## Executive Summary
{exec_summary}

## 1. Company Overview
{company_overview}

## 2. Competitive Landscape
{competitors}
{competitive_matrix}

## 3. SWOT Analysis
{swot}

## 4. Market Positioning
{positioning}

## 5. Market Trends & Insights
{market_trends}

## 6. Strategic Recommendations
{strategic_recommendations}

## 7. Sources
[List key sources used]

---
Report generated: {date}

Format requirements:
- Use proper markdown (headers, bullets, tables)
- Make it professional and polished
- Include all relevant details
- Cite sources where appropriate
- Make it actionable for executives"""
