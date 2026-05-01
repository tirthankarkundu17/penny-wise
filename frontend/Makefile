.PHONY: help install dev build preview lint clean docker-build docker-run

# Variables
APP_NAME := penny-wise-frontend
PORT := 5173
DOCKER_USER := tirthankark
VERSION := latest
IMAGE_NAME := $(DOCKER_USER)/$(APP_NAME):$(VERSION)

# Default shell
SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo "  make install        Install dependencies"
	@echo "  make dev            Run development server"
	@echo "  make build          Build for production"
	@echo "  make preview        Preview the production build"
	@echo "  make lint           Run linting"
	@echo "  make clean          Remove build artifacts and node_modules"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run Docker container"

install:
	npm install

dev:
	npm run dev

build:
	npm run build

preview:
	npm run preview

lint:
	npm run lint

clean:
	rm -rf dist
	rm -rf node_modules
	rm -rf .vite

docker-build:
	docker build -t $(APP_NAME) .
	docker tag $(APP_NAME) $(IMAGE_NAME)

docker-run:
	docker run -p $(PORT):$(PORT) --name $(APP_NAME) $(APP_NAME)
