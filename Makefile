.PHONY: help

.DEFAULT_GOAL := help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA.Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

build: ## Build up container
	docker compose build

up: ## Build and Up the container
	docker compose up -d

down: ## Down the container
	docker compose down

stop: ## Stop the container
	docker compose stop

restart: stop up ## Restart the container

l: lint
lint: ## Python lint
	PYTHONPATH=. ruff --config ruff.toml app
