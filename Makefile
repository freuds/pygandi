SHELL:=/bin/bash -eu

.PHONY: default install build test
default: help

# python modules
PYTHON_MODULES = pipenv wheel pytest rstcheck

# The binary to build (just the base).
BIN := $(shell basename $$PWD)

# Where to push the docker image.
REGISTRY ?= docker.io
REGISTRY_USER ?= freuds2k

# This version-strategy uses git tags to set the version string
VERSION ?= $(shell cat VERSION)
# Get the short SHA
SHA_SHORT ?= $(shell git rev-parse --short HEAD)
APP_NAME = pygandi
##########################################################################
## Usage: make <command>
##
## Available Commands:
##  - make help : Display help for this command (default)
help:
		@cat $(MAKEFILE_LIST) | grep ^\#\# | grep -v ^\#\#\# |cut -c 4-

pymods:
		@pip install --user ${PYTHON_MODULES}

clean:
		@rm -rf .pytest_cache
		@rm -rf build
		@rm -rf dist

##  - make pyenv : Create python environment and install needed python modules
pyenv: pymods
		@pipenv install --dev --skip-lock
		@pipenv shell

##  - make pywheel : Create the python wheel package
pywheel: clean
		@python3 setup.py bdist_wheel

##  - make pytest : launch pytest on src directory
pytest:
		# pipenv install --dev --user pytest pytest-mock
		PYTHONPATH=./src pytest

##  - make image : create local docker image
image:
		@docker build \
			--build-arg VERSION=$(VERSION) \
			-t $(APP_NAME):$(VERSION) \
			-f Dockerfile .
		@docker images

##  - make image-test : run docker image
image-test:
		@docker run --rm \
		 	--APP_NAME pygandi-test \
			$(APP_NAME):$(VERSION) \
			apikey=012345678901234567890123 \
			zone=domain.com \
			record=test1,test2,test3 \
			--log=DEBUG

##  - make image-push : push local image on docker hub
image-push:
		@docker login
		@docker tag $(APP_NAME):$(VERSION) $(REGISTRY)/$(REGISTRY_USER)/$(APP_NAME):$(VERSION)
		@docker push $(REGISTRY_USER)/$(APP_NAME):$(VERSION)
