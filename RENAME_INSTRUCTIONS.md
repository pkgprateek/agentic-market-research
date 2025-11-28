# Rename Instructions

## GitHub Repo Rename

1. Go to: https://github.com/pkgprateek/agentic-research-orchestrator/settings
2. Scroll to "Repository name"
3. Change to: `agentic-market-research`
4. Click "Rename"

GitHub automatically redirects old URLs, so nothing breaks.

## Update Local Git Remote

```bash
cd /Users/prateekkumargoel/Projects/agentic-research-orchestrator

# Update remote URL
git remote set-url origin https://github.com/pkgprateek/agentic-market-research.git

# Verify
git remote -v
```

## Optionally Rename Local Directory

```bash
cd /Users/prateekkumargoel/Projects/
mv agentic-research-orchestrator agentic-market-research
cd agentic-market-research
```

All references in code have been updated to use `agentic-market-research`.
