SHELL := /bin/bash

CREG=ghcr.io
REGID=avickars
AWS_REGION=us-west-2
ARCH=--platform x86_64
DK=docker
APP_VER_TAG=v1

PLAYLIST_PORT = 5000
AUTH_PORT = 3000
SUBSCRIPTION_PORT = 4000
SERVER=0.0.0.0
SERVICE = auth

list-images:
	$(DK) image ls

list-IPaddresses:
	$(DK) sudo docker inspect $(SERVICE) | grep "IPAddress"

# ************ IMAGE BUILDING ************

build: build-network build-auth build-playlist build-subcription build-mcli

build-network:
	docker network create music-service-net

build-auth:
	$(DK) build $(ARCH) --file auth/Dockerfile --tag ghcr.io/$(REGID)/auth:$(APP_VER_TAG) auth

build-playlist:
	$(DK) build $(ARCH) --file playlist/Dockerfile --tag ghcr.io/$(REGID)/playlist:$(APP_VER_TAG) playlist

build-subcription:
	$(DK) build $(ARCH) --file subcription/Dockerfile --tag ghcr.io/$(REGID)/subcription:$(APP_VER_TAG) subcription

build-mcli:
	$(DK) build $(ARCH) --file mcli/Dockerfile --tag ghcr.io/$(REGID)/mcli:$(APP_VER_TAG) mcli

# ************ CONTAINER RUNNING ************

run: run-auth run-playlist run-subcription run-mcli

run-auth:
	$(DK) container run -d --net  music-service-net --rm -p $(AUTH_PORT):$(AUTH_PORT) --name auth ghcr.io/$(REGID)/auth:$(APP_VER_TAG)

run-playlist:
	$(DK) container run -d --net  music-service-net --rm -p $(PLAYLIST_PORT):$(PLAYLIST_PORT) --name playlist ghcr.io/$(REGID)/playlist:$(APP_VER_TAG)

run-subcription:
	$(DK) container run -d --net  music-service-net --rm -p $(SUBSCRIPTION_PORT):$(SUBSCRIPTION_PORT) --name subcription ghcr.io/$(REGID)/subcription:$(APP_VER_TAG)

run-mcli:
	docker container run -it --rm --net  music-service-net --name mcli ghcr.io/$(REGID)/mcli:$(APP_VER_TAG) python3 mcli.py $(SERVER) $(AUTH_PORT) $(PLAYLIST_PORT) 

# ************ CONTAINER STOPPING & removing ************

stop: stop-auth stop-playlist stop-subcription stop-mcli

stop-auth:
	$(DK) stop auth
	# $(DK) rm auth

stop-playlist:
	$(DK) stop playlist
	# $(DK) rm playlist

stop-subcription:
	$(DK) stop subcription
	# $(DK) rm subcription

stop-mcli:
	$(DK) stop mcli
	# $(DK) rm mcli

stop-network:
	docker network music-service-net



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
	mcli/venv/bin/pip install -r auth/requirements.txt

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
