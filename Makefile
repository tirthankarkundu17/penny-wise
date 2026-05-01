.PHONY: help install run dev clean format lint

# Default shell
SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo "  make install    Install dependencies using uv"
	@echo "  make run        Run the FastAPI application"
	@echo "  make dev        Run the application in development mode with hot reload"
	@echo "  make clean      Remove python cache files and build artifacts"
	@echo "  make format     Format code using ruff"
	@echo "  make lint       Check code for linting issues using ruff"

install:
	uv sync

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

format:
	uv run ruff format .

lint:
	uv run ruff check .
