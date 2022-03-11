VENV_DIR = .venv
PYTHON = $(shell pwd)/$(VENV_DIR)/bin/python

APP_PORT = 8000


.PHONY: backend
backend:
	APP_PORT=$(APP_PORT) ./entrypoint.sh dev


.PHONY: tests
tests:
	$(PYTHON) -m pytest


.PHONY: docker_up
docker_up:
	docker-compose up


.PHONY: docker_tests
docker_tests:
	docker-compose -f ./docker-compose.tests.yml up --force-recreate --build
