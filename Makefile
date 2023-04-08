.PHONY: build up start down destroy stop restart

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

stop:
	docker compose stop

restart: stop up