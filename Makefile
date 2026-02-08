.PHONY: help install install-dev test lint format clean build publish

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e ".[dev]"
	pre-commit install

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=cognitive_guard --cov-report=term-missing --cov-report=html

lint:  ## Run linters
	black --check cognitive_guard tests
	ruff cognitive_guard tests
	mypy cognitive_guard

format:  ## Format code
	black cognitive_guard tests
	ruff --fix cognitive_guard tests

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build distribution packages
	python -m build

publish-test:  ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI
	python -m twine upload dist/*

demo:  ## Run demo
	cd examples && ./demo.sh

docs:  ## Serve documentation locally
	@echo "📚 Documentation available in docs/"
	@echo "README: docs/README.md"
	@echo "Architecture: docs/ARCHITECTURE.md"

.DEFAULT_GOAL := help
