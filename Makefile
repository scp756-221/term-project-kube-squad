SHELL := /bin/bash
REGID=avickars

CREG=ghcr.io
AWS_REGION=us-west-2
ARCH=--platform x86_64
APP_VER_TAG=v1

PLAYLIST_PORT = 5000
AUTH_PORT = 3000
SUBSCRIPTION_PORT = 4000
SERVER=0.0.0.0
SERVICE = auth

# **************************************************************************** COMMANDS ****************************************************************************

# ************ LOCAL COMMANDS ************

initialize-local-1: initialize-aws-1

initialize-local-2: initialize-aws-2 initialize-creds initialize-docker

run-local: run-docker

stop-local: stop-docker

cleanup-local: cleanup-aws cleanup-creds cleanup-docker

# **************************************************************************** AWS COMMANDS ****************************************************************************

# ************ COMMANDS ************

initialize-aws-1: create-stack

initialize-aws-2:upload-music create-table-user create-table-cards create-table-playlists

cleanup-aws: empty-bucket delete-bucket delete-stack

# ************ INITIALIZATION COMMANDS ************

create-stack:
	aws cloudformation create-stack \
	--capabilities CAPABILITY_NAMED_IAM \
	--stack-name csv-to-dynamo-db \
	--template-body file://dynamo-db/CSVToDynamo.template \
	--parameters ParameterKey=BucketName,ParameterValue=music-service-$(REGID) \
		ParameterKey=DynamoDBTableName,ParameterValue=music \
		ParameterKey=FileName,ParameterValue=music_100.csv
upload-music:
	aws s3 cp dynamo-db/music_100.csv s3://music-service-$(REGID)/music_100.csv

create-table-user:
	aws dynamodb create-table \
    --table-name User \
    --attribute-definitions \
        AttributeName=email,AttributeType=S \
    --key-schema \
        AttributeName=email,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

create-table-cards:
	aws dynamodb create-table \
    --table-name Cards \
    --attribute-definitions \
        AttributeName=card_no,AttributeType=S \
    --key-schema \
        AttributeName=card_no,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

create-table-playlists:
	aws dynamodb create-table \
    --table-name playlist \
    --attribute-definitions \
        AttributeName=playlist_uuid,AttributeType=S \
        AttributeName=playlist_name,AttributeType=S \
    --key-schema \
        AttributeName=playlist_uuid,KeyType=HASH \
        AttributeName=playlist_name,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST

# ************ CLEANUP COMMANDS ************

empty-bucket:
	aws s3 rm s3://music-service-$(REGID) --recursive

delete-bucket:
	aws s3 rb s3://music-service-$(REGID) --force

delete-stack:
	aws cloudformation delete-stack --stack-name csv-to-dynamo-db

delete-table-user:
	aws dynamodb delete-table --table-name User

delete-table-playlist:
	aws dynamodb delete-table --table-name playlist

delete-table-cards:
	aws dynamodb delete-table --table-name Cards
# **************************************************************************** DOCKER COMMANDS ****************************************************************************

# ************ COMMANDS ************

initialize-docker: build-docker

run-docker: run-auth run-playlist run-subscription run-mcli

stop-docker: stop-auth stop-playlist stop-subscription stop-mcli

cleanup-docker: rm-network

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

run-auth:
	docker container run -d --net  music-service-net --rm -p $(AUTH_PORT):$(AUTH_PORT) --name auth ghcr.io/$(REGID)/auth:$(APP_VER_TAG)

run-playlist:
	docker container run --net  music-service-net --rm -p $(PLAYLIST_PORT):$(PLAYLIST_PORT) --name playlist ghcr.io/$(REGID)/playlist:$(APP_VER_TAG)

run-subscription:
	docker container run -d --net  music-service-net --rm -p $(SUBSCRIPTION_PORT):$(SUBSCRIPTION_PORT) --name subscription ghcr.io/$(REGID)/subcription:$(APP_VER_TAG)

run-mcli:
	docker container run -it --rm --net  music-service-net --name mcli ghcr.io/$(REGID)/mcli:$(APP_VER_TAG) python3 mcli.py $(SERVER) $(AUTH_PORT) $(PLAYLIST_PORT) 

# ************ CONTAINER STOPPING ************

stop-auth:
	docker stop auth

stop-playlist:
	docker stop playlist

stop-subscription:
	docker stop subscription

stop-mcli:
	docker stop mcli

# ************ CONTAINER REMOVING ************

# Don't need to rm the containers as it is automatically done when stopping the containers
rm-auth:
	docker rm auth

rm-playlist:
	docker rm playlist

rm-subscription:
	docker rm subscription

rm-mcli:
	docker rm mcli

rm-network:
	docker network rm music-service-net

# **************************************************************************** CREDENTIAL COMMANDS ****************************************************************************

initialize-creds: initialize-.env

cleanup-creds: cleanup-.env

# ************ INITIALIZATION COMMANDS ************

initialize-.env:
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
