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
	docker image ls

list-IPaddresses:
	docker inspect $(SERVICE) | grep "IPAddress"

create-stack:
	aws cloudformation create-stack --capabilities CAPABILITY_NAMED_IAM --stack-name csv-to-dynamo-db --template-body file://dynamo-db/CSVToDynamo.template --parameters ParameterKey=BucketName,ParameterValue=music-service-$(REGID) ParameterKey=DynamoDBTableName,ParameterValue=music ParameterKey=FileName,ParameterValue=music_100.csv
upload-music:
	aws s3 cp dynamo-db/music_100.csv s3://music-service-$(REGID)/music_100.csv


# ************ IMAGE BUILDING ************

build: build-network build-auth build-playlist build-subcription build-mcli

build-network:
	docker network create music-service-net

build-auth:
	docker build $(ARCH) --file auth/Dockerfile --tag ghcr.io/$(REGID)/auth:$(APP_VER_TAG) auth

build-playlist:
	docker build $(ARCH) --file playlist/Dockerfile --tag ghcr.io/$(REGID)/playlist:$(APP_VER_TAG) playlist

build-subcription:
	docker build $(ARCH) --file subcription/Dockerfile --tag ghcr.io/$(REGID)/subcription:$(APP_VER_TAG) subcription

build-mcli:
	docker build $(ARCH) --file mcli/Dockerfile --tag ghcr.io/$(REGID)/mcli:$(APP_VER_TAG) mcli

# ************ CONTAINER RUNNING ************

run: run-auth run-playlist run-subcription run-mcli

run-auth:
	docker container run -d --net  music-service-net --rm -p $(AUTH_PORT):$(AUTH_PORT) --name auth ghcr.io/$(REGID)/auth:$(APP_VER_TAG)

run-playlist:
	docker container run -d --net  music-service-net --rm -p $(PLAYLIST_PORT):$(PLAYLIST_PORT) --name playlist ghcr.io/$(REGID)/playlist:$(APP_VER_TAG)

run-subcription:
	docker container run -d --net  music-service-net --rm -p $(SUBSCRIPTION_PORT):$(SUBSCRIPTION_PORT) --name subcription ghcr.io/$(REGID)/subcription:$(APP_VER_TAG)

run-mcli:
	docker container run -it --rm --net  music-service-net --name mcli ghcr.io/$(REGID)/mcli:$(APP_VER_TAG) python3 mcli.py $(SERVER) $(AUTH_PORT) $(PLAYLIST_PORT) 

# ************ CONTAINER STOPPING & removing ************

stop: stop-auth stop-playlist stop-subcription stop-mcli

stop-auth:
	docker stop auth
	# $(DK) rm auth

stop-playlist:
	docker stop playlist
	# $(DK) rm playlist

stop-subcription:
	docker stop subcription
	# $(DK) rm subcription

stop-mcli:
	docker stop mcli
	# $(DK) rm mcli

stop-network:
	docker stop network music-service-net



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
