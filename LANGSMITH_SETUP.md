"""
LangSmith Configuration and Setup Guide

LangSmith provides observability for LangChain/LangGraph applications.
It's critical for production debugging and performance optimization.
"""

# Setup Instructions:

# 1. Sign up for LangSmith (free tier available):
#    https://smith.langchain.com

# 2. Get your API key from:
#    https://smith.langchain.com/settings

# 3. Add to .env file:
#    LANGSMITH_API_KEY=ls_...
#    LANGCHAIN_TRACING_V2=true
#    LANGCHAIN_PROJECT=market-intelligence-prod
#    LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# 4. LangSmith will auto-trace all LangChain/LangGraph operations


# What LangSmith Provides:

# 1. Traces: Full execution tree
#    - See which agent ran when
#    - View all LLM calls and responses
#    - Track token usage per call

# 2. Debugging:
#    - Why did the workflow fail?
#    - Which prompt generated bad output?
#    - What was the exact input that caused an error?

# 3. Monitoring:
#    - Latency per agent
#    - Cost per run
#    - Success/failure rates

# 4. Optimization:
#    - Compare different prompts
#    - A/B test model choices
#    - Identify bottlenecks


# For Portfolio/Resume:
# - Shows you understand production AI systems
# - Demonstrates observability best practices
# - Critical for enterprise deployments
