.PHONY: help build test lint security run run-local run-cloud clean

IMAGE_NAME := api-reports
VERSION := $(shell cat VERSION)

.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make build       - Build Docker image"
	@echo "  make test        - Run tests with coverage"
	@echo "  make lint        - Run code linting (ruff)"
	@echo "  make lint-fix    - Run code linting with auto-fix"
	@echo "  make security    - Run security checks (semgrep, gitleaks)"
	@echo "  make run         - Run Docker container"
	@echo "  make run-local   - Run locally with reload (dev)"
	@echo "  make run-cloud   - Run locally with production settings"
	@echo "  make clean       - Clean cleanup artifacts"

build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

test:
	PYTHONPATH=. pytest tests/ --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/
lint-fix:
	ruff check --fix src/ tests/


security:
	# Placeholder for security tools execution
	@echo "Running Semgrep..."
	# semgrep --config=p/python src/
	@echo "Running Gitleaks..."
	# gitleaks detect --source . -v

run:
	docker run -d -p 8000:8000 --name $(IMAGE_NAME) $(IMAGE_NAME):$(VERSION)

run-local:
	ENVIRONMENT=development PYTHONPATH=. python -m uvicorn src.main:app --reload --port 8000

run-cloud:
	# Simulates cloud run with production settings
	ENVIRONMENT=production PYTHONPATH=. python -m uvicorn src.main:app --port 8000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
