SHELL := /bin/bash

CREG=ghcr.io
REGID=avickars
AWS_REGION=us-west-2
ARCH=--platform x86_64
DK=docker
APP_VER_TAG=v1

list-images:
	$(DK) iamge ls

build-auth:
	$(DK) build $(ARCH) --file auth/Dockerfile --tag ghcr.io/$(REGID)/auth:$(APP_VER_TAG) auth

tag-auth:
	$(DK) image tag auth:$(APP_VER_TAG) ghcr.io/$(REGID)/auth:$(APP_VER_TAG)

push-auth:
	$(DK) image push ghcr.io/$(REGID)/auth:$(APP_VER_TAG)
run-auth:
	$(DK) container run -p 30000:30000 --name auth ghcr.io/$(REGID)/auth:$(APP_VER_TAG)
remove-auth:
	$(DK) rm auth



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
