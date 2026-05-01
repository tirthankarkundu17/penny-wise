.PHONY: help install run dev clean format lint docker-build docker-run docker-stop docker-login docker-push docker-push-multi docker-buildx-setup

# Variables
APP_NAME := penny-wise
PORT := 8000
DOCKER_USER := tirthankarkundu17
VERSION := latest
IMAGE_NAME := $(DOCKER_USER)/$(APP_NAME):$(VERSION)
PLATFORMS := linux/amd64,linux/arm64

# Default shell
SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo "  make install            Install dependencies using uv"
	@echo "  make run                Run the FastAPI application"
	@echo "  make dev                Run the application in development mode with hot reload"
	@echo "  make clean              Remove python cache files and build artifacts"
	@echo "  make format             Format code using ruff"
	@echo "  make lint               Check code for linting issues using ruff"
	@echo "  make docker-build       Build the Docker image (local architecture)"
	@echo "  make docker-run         Run the application in a Docker container"
	@echo "  make docker-stop        Stop the Docker container"
	@echo "  make docker-login       Login to Docker Hub"
	@echo "  make docker-push        Tag and push the local image to Docker Hub"
	@echo "  make docker-push-multi  Build and push multi-platform images (amd64, arm64) using buildx"

install:
	uv sync

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

dev:
	uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT) --reload

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

docker-build:
	docker build -t $(APP_NAME) .
	docker tag $(APP_NAME) $(IMAGE_NAME)

docker-run:
	docker run -p $(PORT):$(PORT) --env-file .env --name $(APP_NAME) $(APP_NAME)

docker-stop:
	docker stop $(APP_NAME) || true
	docker rm $(APP_NAME) || true

docker-login:
	docker login

docker-push: docker-build
	docker push $(IMAGE_NAME)

docker-buildx-setup:
	docker buildx create --use --name multi-platform-builder || docker buildx use multi-platform-builder

docker-push-multi: docker-login docker-buildx-setup
	docker buildx build --platform $(PLATFORMS) -t $(IMAGE_NAME) --push .
