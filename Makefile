SHELL := /bin/bash

CREG=ghcr.io
REGID=avickars
AWS_REGION=us-west-2
ARCH=--platform x86_64
DK=docker
APP_VER_TAG=v1

list-images:
	$(DK) image ls

# ************ IMAGE BUILDING ************

build: build-auth build-playlist

build-auth:
	$(DK) build $(ARCH) --file auth/Dockerfile --tag ghcr.io/$(REGID)/auth:$(APP_VER_TAG) auth

build-playlist:
	$(DK) build $(ARCH) --file playlist/Dockerfile --tag ghcr.io/$(REGID)/playlist:$(APP_VER_TAG) playlist

# ************ CONTAINER RUNNING ************

run: run-auth run-playlist

run-auth:
	$(DK) container run -d -p 3000:3000 --name auth ghcr.io/$(REGID)/auth:$(APP_VER_TAG)

run-playlist:
	$(DK) container run -d -p 4000:4000 --name playlist ghcr.io/$(REGID)/playlist:$(APP_VER_TAG)

# ************ CONTAINER STOPPING & removing ************

stop: stop-auth stop-playlist

stop-auth:
	$(DK) stop auth
	$(DK) rm auth

stop-playlist:
	$(DK) stop playlist
	$(DK) rm playlist

# ************ CONTAINER PUSHING ************





instantionate-local: instantionate-.env instantionate-python

instantionate-.env:
	cp .env auth
	cp .env mcli
	cp .env playlist
	cp .env subcription

instantionate-python:
	pip install virtualenv

	virtualenv auth/venv
	auth/venv/bin/pip install -r auth/requirements.txt

	virtualenv mcli/venv
	auth/venv/bin/pip install -r auth/requirements.txt

	virtualenv playlist/venv
	playlist/venv/bin/pip install -r auth/requirements.txt

	virtualenv subcription/venv
	subcription/venv/bin/pip install -r auth/requirements.txt

cleanup: cleanup-venv

cleanup-venv:
	rm -r auth/venv
	rm -r mcli/venv
	rm -r playlist/venv
	rm -r subcription/venv

cleanup-.env:
	rm auth/.env
	rm mcli/.env
	rm playlist/.env
	rm subcription/.env

cleanup-__pycache__:
	rm -r auth/__pycache__
	rm -r mcli/__pycache__
	rm -r playlist/__pycache__
	rm -r subcription/__pycache__
