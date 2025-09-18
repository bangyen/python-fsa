.PHONY: help install test lint format type-check clean build

help: ## Show this help message
	@echo "Available commands (activate virtual environment first):"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package with development dependencies
	pip install -e ".[dev]"
	pre-commit install

test: ## Run tests with coverage
	pytest tests/ -v --cov=src --cov-report=term-missing

lint: ## Run linting and formatting checks
	ruff check src tests
	black --check src tests

format: ## Format code with black and ruff
	black src tests
	ruff check --fix src tests

type-check: ## Run type checking
	mypy src

check: lint type-check test ## Run all quality checks

clean: ## Clean up build artifacts and caches
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

build: ## Build the package
	python -m build
