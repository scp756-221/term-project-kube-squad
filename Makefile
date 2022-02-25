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

# **************************************************************************** AWS COMMANDS ****************************************************************************

# ************ STACK COMMANDS ************
create-stack:

	aws cloudformation create-stack --capabilities CAPABILITY_NAMED_IAM --stack-name csv-to-dynamo-db --template-body file://dynamo-db/CSVToDynamo.template --parameters ParameterKey=BucketName,ParameterValue=music-service-$(REGID) ParameterKey=DynamoDBTableName,ParameterValue=music ParameterKey=FileName,ParameterValue=music_100.csv

delete-stack:
	aws cloudformation delete-stack --stack-name csv-to-dynamo-db

upload-music:
	aws s3 cp dynamo-db/music_100.csv s3://music-service-$(REGID)/music_100.csc

empty-bucket:
	aws s3 rm s3://music-service-$(REGID) --recursive

delete-bucket:
	aws s3 rb s3://music-service-$(REGID) --force

# **************************************************************************** DOCKER COMMANDS ****************************************************************************

# ************ HELPFUL COMMANDS ************

list-containers-all:
	docker image ls

list-ipaddress:
	docker inspect $(SERVICE) | grep "IPAddress"

list-containers-running:
	docker ps

# ************ IMAGE BUILDING ************
build-docker: build-network build-auth build-playlist build-subcription build-mcli

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

run-docker: run-auth run-playlist run-subcription run-mcli

run-auth:
	docker container run -d --net  music-service-net --rm -p $(AUTH_PORT):$(AUTH_PORT) --name auth ghcr.io/$(REGID)/auth:$(APP_VER_TAG)

run-playlist:
	docker container run -d --net  music-service-net --rm -p $(PLAYLIST_PORT):$(PLAYLIST_PORT) --name playlist ghcr.io/$(REGID)/playlist:$(APP_VER_TAG)

run-subcription:
	docker container run -d --net  music-service-net --rm -p $(SUBSCRIPTION_PORT):$(SUBSCRIPTION_PORT) --name subcription ghcr.io/$(REGID)/subcription:$(APP_VER_TAG)

run-mcli:
	docker container run -it --rm --net  music-service-net --name mcli ghcr.io/$(REGID)/mcli:$(APP_VER_TAG) python3 mcli.py $(SERVER) $(AUTH_PORT) $(PLAYLIST_PORT) 

# ************ CONTAINER STOPPING ************

stop-docker: stop-auth stop-playlist stop-subcription stop-mcli

stop-auth:
	docker stop auth

stop-playlist:
	docker stop playlist

stop-subcription:
	docker stop subcription

stop-mcli:
	docker stop mcli

# ************ CONTAINER REMOVING ************

rm-docker: rm-auth rm-playlist rm-subcription rm-mcli

rm-auth:
	docker rm auth

rm-playlist:
	docker rm playlist

rm-subcription:
	docker rm subcription

rm-mcli:
	docker rm mcli

rm-network:
	docker network rm music-service-net

# **************************************************************************** CREDENTIAL COMMANDS ****************************************************************************

# ************ CREDENTIAL CREATION ************

instantionate-.env:
	cp .env auth
	cp .env mcli
	cp .env playlist
	cp .env subcription

# ************ CREDENTIAL REMOVAL ************

cleanup-.env:
	rm auth/.env
	rm mcli/.env
	rm playlist/.env
	rm subcription/.env

