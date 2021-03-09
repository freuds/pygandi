SHELL:=/bin/bash -eu

.PHONY: default install install-db test
default: help

##########################################################################
## This command manage helm release with the cluster Kubernetes
## Usage: make <command>
##
## Available Commands:
##  - make help : Display help for this command (default)
help:
		@cat $(MAKEFILE_LIST) | grep ^\#\# | grep -v ^\#\#\# |cut -c 4-

##  - make install : Create env with pip
install:
		pipenv install --dev --skip-lock

##  - make build : Create the wheel package
build:
		python setup.py bdist_wheel

##  - make test : launch pytest on src directory
test:
		# pipenv install --dev --user pytest pytest-mock
		PYTHONPATH=./src pytest