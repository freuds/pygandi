SHELL := /bin/bash -eu
.PHONY: default help clean venv build test image image-test image-push

# Variables
REGISTRY ?= docker.io
REGISTRY_USER ?= freuds2k

VERSION_FILE := version.py
VERSION ?= $(shell grep '__version__' $(VERSION_FILE) | awk -F '"' '{print $$2}')
SHA_SHORT ?= $(shell git rev-parse --short HEAD)
APP_NAME = pygandi

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

##  - make venv : Create virtual environment
venv:
	@python3 -m venv .venv
	@source .venv/bin/activate

##  - make build : Build the python package
build: clean venv
	@source .venv/bin/activate && uv pip install build && python3 -m build

##  - make check : Run linting tools & tests
tests: venv
	@source .venv/bin/activate && uv pip install -e ".[test]" && \
		black src/pygandi tests && \
		isort src/pygandi tests && \
		pylint src/pygandi tests && \
		mypy src/pygandi && \
		pytest -v

##  - make image : Create local docker image
image:
	@docker build \
		--build-arg VERSION=$(VERSION) \
		-t $(APP_NAME):$(VERSION) \
		-f Dockerfile .
	@docker images

##  - make image-test : Run docker image test
image-test:
	@docker run --rm \
		--name pygandi-test \
		$(APP_NAME):$(VERSION) \
		apikey=012345678901234567890123 \
		curl -H "Authorization: Bearer d24da6ddb55a78486ffd7980d3a74d77118f4b90" https://id.gandi.net/tokeninfo \
		zone=domain.com \
		record=test1,test2,test3 \
		--log=DEBUG

##  - make image-push : Push local image to docker hub
image-push:
	@docker login
	@docker tag $(APP_NAME):$(VERSION) $(REGISTRY)/$(REGISTRY_USER)/$(APP_NAME):$(VERSION)
	@docker push $(REGISTRY)/$(REGISTRY_USER)/$(APP_NAME):$(VERSION)
