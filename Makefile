# Makefile

.PHONY: install test lint format clean docs

install:
	pip install -r requirements/dev.txt
	pre-commit install

test:
	# Updated "--cov=src" to "--cov=cmate"
	pytest tests/ -v --cov=cmate --cov-report=term-missing

lint:
	# Updated "src" → "cmate"
	flake8 cmate tests
	mypy cmate tests
	black --check cmate tests
	isort --check-only cmate tests

format:
	# Updated "src" → "cmate"
	black cmate tests
	isort cmate tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

docs:
	sphinx-build -b html docs/source docs/build/html
