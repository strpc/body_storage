VENV_DIR = .venv
PYTHON = $(shell pwd)/$(VENV_DIR)/bin/python

APP_PORT = 8000

.PHONY: backend
backend:
	APP_PORT=$(APP_PORT) ./entrypoint.sh dev

.PHONY: tests
tests:
	$(PYTHON) -m pytest
