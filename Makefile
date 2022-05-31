SHELL := /bin/bash

all: build test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

shell:
	docker-compose run shuttleapp /env/bin/python /app/manage.py shell

test: up
	docker-compose exec shuttleapp /env/bin/python /app/manage.py test

migrate: up
	docker-compose exec shuttleapp /env/bin/python /app/manage.py migrate

makemigrations: up
	docker-compose exec shuttleapp /env/bin/python /app/manage.py makemigrations

.PHONY: build up test
