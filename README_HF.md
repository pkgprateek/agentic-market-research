---
title: Agentic Market Research
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "5.0.0"
app_file: src/ui/app.py
pinned: false
---

# Agentic Market Research

Enterprise-grade multi-agent AI system for automated competitive intelligence. **80x faster, 2000x cheaper** than manual research.

## What It Does

Enter a company name → Get a comprehensive market intelligence report in ~15 minutes.

**Report includes:**
- Company deep dive & business model
- SWOT analysis
- Competitive landscape
- Market positioning
- Strategic recommendations
- Cited sources

## How It Works

Three specialized AI agents work in sequence:

1. **Research Agent** - Web search + data gathering
2. **Analysis Agent** - SWOT + competitive analysis  
3. **Writer Agent** - Professional report generation

Powered by LangGraph orchestration with real-time cost tracking.

## Cost

- Free tier (Groq): $0.00
- Production (Claude/GPT-4): $1-2 per analysis

vs $3,000 for manual research.

## Technology

- LangGraph for multi-agent coordination
- Groq (primary) or OpenRouter (fallback) for LLM access
- Tavily API for web search
- Gradio deployment

**Source code:** [github.com/pkgprateek/agentic-market-research](https://github.com/pkgprateek/agentic-market-research)

---

Built by **Prateek Kumar Goel**
