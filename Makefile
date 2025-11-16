.PHONY: help install install-dev test lint format clean build

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run all linters"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Remove build artifacts and cache files"
	@echo "  make build        - Build distribution packages"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest --cov=gapandas4 --cov-report=html --cov-report=term-missing

lint:
	flake8 gapandas4 tests
	mypy gapandas4
	black --check gapandas4 tests
	isort --check-only gapandas4 tests

format:
	black gapandas4 tests
	isort gapandas4 tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

build: clean
	python -m build
