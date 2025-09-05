# Banking RM Agent Makefile

.PHONY: help install install-dev test lint format clean run-streamlit run-api docs

help:  ## Show this help message
	@echo "Banking RM Agent - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest tests/ -v

lint:  ## Run linting checks
	flake8 src/ tests/
	mypy src/

format:  ## Format code with black
	black src/ tests/

clean:  ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

run-streamlit:  ## Run Streamlit web interface
	python scripts/run_streamlit.py

run-api:  ## Run FastAPI server
	python scripts/run_api.py

run-test:  ## Run test script
	python tests/test_agent.py

docs:  ## Generate documentation
	cd docs && sphinx-build -b html . _build/html

setup-env:  ## Setup environment file
	cp config/env_example.txt .env
	@echo "Please edit .env file with your configuration"

check-env:  ## Check if .env file exists
	@if [ ! -f .env ]; then echo "Error: .env file not found. Run 'make setup-env' first."; exit 1; fi

install-hooks:  ## Install pre-commit hooks
	pre-commit install

# Development workflow
dev-setup: setup-env install-dev install-hooks  ## Complete development setup
	@echo "Development environment setup complete!"

# Production deployment
build: clean  ## Build package for distribution
	python -m build

upload-test: build  ## Upload to test PyPI
	python -m twine upload --repository testpypi dist/*

upload: build  ## Upload to PyPI
	python -m twine upload dist/*

# Docker commands
docker-build:  ## Build Docker image
	docker build -t banking-rm-agent .

docker-run:  ## Run Docker container
	docker run -p 8501:8501 -p 8000:8000 banking-rm-agent

# Monitoring and maintenance
logs:  ## Show application logs
	tail -f banking_rm_agent.log

stats:  ## Show agent statistics
	curl -s http://localhost:8000/statistics | python -m json.tool

health:  ## Check system health
	curl -s http://localhost:8000/health | python -m json.tool
