.PHONY: help

.DEFAULT_GOAL := help

APP_DIR = ./app

LOAD_ENV_CMD = export `cat .env`

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA.Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort


# Local developpment

local-static: ## Setup local static files
	$(LOAD_ENV_CMD) && mkdir -p STATIC_DIR_ROOT && $(APP_DIR)/manage.py collectstatic

local-run:  ## Run localy server
	$(LOAD_ENV_CMD) && gunicorn --pythonpath "$(APP_DIR)" app.config.wsgi

# Docker compose commands

build: ## Build and Up container
	docker compose up -d --build


up: ## Up the container
	docker compose up -d


down: ## Down the container
	docker compose down


stop: ## Stop the container
	docker compose stop


restart: stop up ## Restart the container


af: autoformat ## Alias `autoformat`
autoformat: ## Run the autoformater
	isort --atomic --profile black  $(APP_DIR)
	black --line-length 88 --preview $(APP_DIR)


l: lint ## Alias for `lint`
lint: ## Run Ruff, a Python linter
	PYTHONPATH=$(APP_DIR) ruff --config ruff.toml $(APP_DIR)


test: ## Test via Django tester
	$(APP_DIR)/manage.py test $(APP_DIR)


precommit: af l test ## Precommit rules applied : af l test

sass: ## Watch sass files
	sass $(APP_DIR)/static/sass/:$(APP_DIR)/static/css/ \
	$(APP_DIR)/comets/static/comets/sass/:$(APP_DIR)/comets/static/comets/css/ --watch
