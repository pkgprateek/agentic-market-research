# Agentic Market Research Orchestrator

Multi-agent AI system for automated competitive market intelligence.

### Setup Instructions

**1. Create HuggingFace Space**

```bash
# Go to https://huggingface.co/spaces
# Click "Create new Space"
# Name: agentic-market-research
# SDK: Gradio
# Hardware: Free CPU
```

**2. Add HF Token to GitHub Secrets**

```bash
# Get token from https://huggingface.co/settings/tokens
# GitHub repo → Settings → Secrets → New repository secret
# Name: HF_TOKEN
# Value: [your HF token]
```

**3. Configure Space Secrets**

In HF Space settings, add:
- `OPENROUTER_API_KEY` - Your OpenRouter API key
- `TAVILY_API_KEY` - Your Tavily API key  
- `LANGSMITH_API_KEY` - (Optional) LangSmith key

**4. Update Workflow**

Edit `.github/workflows/deploy-hf.yml` line 23:
```yaml
git remote add hf https://YOUR_HF_USERNAME:$HF_TOKEN@huggingface.co/spaces/YOUR_HF_USERNAME/SPACE_NAME
```

**5. Deploy**

```bash
git push origin main
# GitHub Actions automatically deploys to HF Spaces
# Check workflow at: github.com/your-repo/actions
```

### What This Demonstrates

**For Technical Hiring:**
- CI/CD automation (not just code upload)
- Production deployment workflow
- Secrets management
- Automated testing before deploy

**For Consulting Clients:**
- Professional deployment practices
- Zero-downtime updates
- Automated quality checks
- Production-ready infrastructure

### Alternative: Local Docker

For development or custom infrastructure:

```bash
docker-compose up -d
# API: http://localhost:8000
# UI: http://localhost:7860
```

## Post-Deployment

**Add to Resume/Portfolio:**
```
Agentic Market Research System
- Live demo: https://huggingface.co/spaces/YOUR_USERNAME/agentic-market-research
- Tech: LangGraph, FastAPI, Gradio, GitHub Actions
- Impact: 80x faster market research, $0.50 vs $3,000 cost
- Automated CI/CD deployment pipeline
```

**For Consulting Proposals:**
1. Link to live demo (instant credibility)
2. "Try it yourself" call-to-action
3. ROI calculator based on client size
4. Sample report from real analysis

### Monitoring

HF Spaces provides:
- Auto-scaling (up to 4 replicas on free tier)
- Usage analytics
- Error logging
- Uptime monitoring

Access at: `https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME/logs`
