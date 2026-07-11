SHELL := /bin/bash -eu
.PHONY: default help install-uv clean venv build tests test-all image image-test image-push

# Variables
REGISTRY ?= docker.io
REGISTRY_USER ?= freuds2k

VERSION_FILE := version.py
VERSION ?= $(shell grep '__version__' $(VERSION_FILE) | awk -F '"' '{print $$2}')
SHA_SHORT ?= $(shell git rev-parse --short HEAD)
APP_NAME = pygandi

# Python interpreter used for venv/build/tests. Override to target a
# specific version, e.g. `make tests PYTHON=python3.13`.
PYTHON ?= python3
# Supported versions for `make test-all`.
PYTHON_VERSIONS := 3.12 3.13 3.14

##########################################################################
## Usage: make <command>
##
## Available Commands:

default: help

##  - make help : Display help for this command (default)
help:
	@cat $(MAKEFILE_LIST) | grep ^\#\# | grep -v ^\#\#\# |cut -c 4-

##  - make install-uv : Install uv package manager if not already installed
install-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv package manager..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
		echo "uv is already installed: $$(uv --version)"; \
	fi

##  - make clean : Clean build artifacts and virtual environment
clean:
	@rm -rf .pytest_cache .mypy_cache build dist *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@rm -rf .venv

##  - make venv : Create virtual environment (set PYTHON=pythonX.Y to pick the interpreter)
venv:
	@$(PYTHON) -m venv --clear .venv
	@source .venv/bin/activate

##  - make build : Build the python package
build: clean venv
	@source .venv/bin/activate && uv pip install build && python3 -m build

##  - make tests : Run linting tools & tests (set PYTHON=pythonX.Y to pick the interpreter)
tests: venv
	@source .venv/bin/activate && uv pip install -e ".[test]" && \
		black src/pygandi tests && \
		isort src/pygandi tests && \
		pylint src/pygandi tests && \
		mypy src/pygandi && \
		pytest -v

##  - make test-all : Run tests on every supported Python version found on PATH
test-all:
	@for v in $(PYTHON_VERSIONS); do \
		if command -v python$$v >/dev/null 2>&1; then \
			echo "=== Running tests on Python $$v ==="; \
			$(MAKE) clean tests PYTHON=python$$v; \
		else \
			echo "=== Skipping Python $$v (not installed) ==="; \
		fi; \
	done

##  - make image : Create local docker image
image:
	@docker build \
		--build-arg VERSION=$(VERSION) \
		-t $(APP_NAME):$(VERSION) \
		-f Dockerfile .
	@docker images

##  - make image-test : Run docker image test
image-test:
	docker run --rm -it \
		--volume .:/app \
		--volume /app/.venv \
		--name pygandi-test \
		-e API_TOKEN="0123456789012345678901234567890123456789" \
		$(APP_NAME):$(VERSION) \
		pygandi \
		zone=domain.com \
		record=test1,test2,test3 \
		--log=DEBUG
		--dry-run

##  - make image-push : Push local image to docker hub
image-push:
	@docker login
	@docker tag $(APP_NAME):$(VERSION) $(REGISTRY)/$(REGISTRY_USER)/$(APP_NAME):$(VERSION)
	@docker push $(REGISTRY)/$(REGISTRY_USER)/$(APP_NAME):$(VERSION)
