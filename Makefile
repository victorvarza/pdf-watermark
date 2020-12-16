#!make
VERSION ?= $(shell cat VERSION)
COMMIT ?= $(shell git rev-parse HEAD)

lint:
	flake8 --ignore=E501,W503 src/

dev.setup:
	@if [ ! -d venv ]; then mkdir venv; fi
	@if [ ! -f venv/bin/activate ]; then python3 -m venv venv; fi
	source venv/bin/activate && pip3 install -r requirements.txt
