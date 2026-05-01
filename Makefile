.PHONY: help-backend install-backend run-backend dev-backend clean-backend format-backend lint-backend docker-build-backend docker-run-backend docker-stop-backend docker-login-backend docker-push-backend docker-push-multi-backend docker-buildx-setup-backend \
        help-frontend install-frontend dev-frontend build-frontend preview-frontend lint-frontend clean-frontend docker-build-frontend docker-run-frontend

# Variables
APP_NAME := penny-wise
PORT := 8000
FE_PORT := 5173
DOCKER_USER := tirthankark
VERSION := latest
IMAGE_NAME := $(DOCKER_USER)/$(APP_NAME):$(VERSION)
FE_IMAGE_NAME := $(DOCKER_USER)/$(APP_NAME)-frontend:$(VERSION)
PLATFORMS := linux/amd64,linux/arm64

# Default shell
SHELL := /bin/bash

# --- Backend ---

help-backend:
	@echo "Backend Usage:"
	@echo "  make install-backend            Install dependencies using uv"
	@echo "  make run-backend                Run the FastAPI application"
	@echo "  make dev-backend                Run the application in development mode with hot reload"
	@echo "  make clean-backend              Remove python cache files and build artifacts"
	@echo "  make format-backend             Format code using ruff"
	@echo "  make lint-backend               Check code for linting issues using ruff"
	@echo "  make docker-build-backend       Build the Docker image (local architecture)"
	@echo "  make docker-run-backend         Run the application in a Docker container"
	@echo "  make docker-stop-backend        Stop the Docker container"
	@echo "  make docker-login-backend       Login to Docker Hub"
	@echo "  make docker-push-backend        Tag and push the local image to Docker Hub"
	@echo "  make docker-push-multi-backend  Build and push multi-platform images (amd64, arm64) using buildx"

install-backend:
	cd backend && uv sync

run-backend:
	cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

dev-backend:
	cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT) --reload

clean-backend:
	cd backend && find . -type d -name "__pycache__" -exec rm -rf {} +
	cd backend && find . -type f -name "*.pyc" -delete
	cd backend && find . -type f -name "*.pyo" -delete
	cd backend && find . -type f -name "*.pyd" -delete
	cd backend && find . -type f -name ".DS_Store" -delete
	cd backend && rm -rf .pytest_cache
	cd backend && rm -rf .ruff_cache
	cd backend && rm -rf .mypy_cache
	cd backend && rm -rf build/
	cd backend && rm -rf dist/
	cd backend && rm -rf *.egg-info

format-backend:
	cd backend && uv run ruff format .

lint-backend:
	cd backend && uv run ruff check .

docker-build-backend:
	docker build -t $(APP_NAME) ./backend
	docker tag $(APP_NAME) $(IMAGE_NAME)

docker-run-backend:
	docker run -p $(PORT):$(PORT) --env-file backend/.env --name $(APP_NAME) $(APP_NAME)

docker-stop-backend:
	docker stop $(APP_NAME) || true
	docker rm $(APP_NAME) || true

docker-login-backend:
	docker login

docker-push-backend: docker-build-backend
	docker push $(IMAGE_NAME)

docker-buildx-setup-backend:
	docker buildx create --use --name multi-platform-builder || docker buildx use multi-platform-builder

docker-push-multi-backend: docker-login-backend docker-buildx-setup-backend
	docker buildx build --platform $(PLATFORMS) -t $(IMAGE_NAME) --push ./backend

# --- Frontend ---

help-frontend:
	@echo "Frontend Usage:"
	@echo "  make install-frontend           Install dependencies"
	@echo "  make dev-frontend               Run development server"
	@echo "  make build-frontend             Build for production"
	@echo "  make preview-frontend           Preview the production build"
	@echo "  make lint-frontend              Run linting"
	@echo "  make clean-frontend             Remove build artifacts and node_modules"
	@echo "  make docker-build-frontend      Build Docker image"
	@echo "  make docker-run-frontend        Run Docker container"

install-frontend:
	cd frontend && npm install

dev-frontend:
	cd frontend && npm run dev

build-frontend:
	cd frontend && npm run build

preview-frontend:
	cd frontend && npm run preview

lint-frontend:
	cd frontend && npm run lint

clean-frontend:
	cd frontend && rm -rf dist node_modules .vite

docker-build-frontend:
	docker build -t $(APP_NAME)-frontend ./frontend
	docker tag $(APP_NAME)-frontend $(FE_IMAGE_NAME)

docker-run-frontend:
	docker run -p $(FE_PORT):80 --name $(APP_NAME)-frontend $(APP_NAME)-frontend
