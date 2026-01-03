.PHONY: help install test lint typecheck check run clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	uv pip install -r requirements.txt

test:  ## Run all tests
	pytest

lint:  ## Run linter (ruff)
	ruff check src/ tests/ --exclude src/ui/app_mock.py

lint-fix:  ## Run linter with auto-fix
	ruff check --fix src/ tests/ --exclude src/ui/app_mock.py

typecheck:  ## Run type checker (mypy)
	mypy src/

check:  ## Run all checks (lint + typecheck + test)
	@echo "Running Ruff (Linting)..."
	ruff check src/ tests/ --exclude src/ui/app_mock.py
	@echo ""
	@echo "Running Mypy (Type Checking)..."
	mypy src/
	@echo ""
	@echo "Running Pytest..."
	pytest
	@echo ""
	@echo "✅ All checks passed!"

run:  ## Run the Gradio UI
	python src/ui/app.py

clean:  ## Remove build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
