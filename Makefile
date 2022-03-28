SHELL := /bin/bash
REGID=rishabhkaushal07


CREG=ghcr.io
AWS_REGION=us-west-2
ARCH=--platform x86_64
APP_VER_TAG=v1

PLAYLIST_PORT = 6000
AUTH_PORT = 3000
SUBSCRIPTION_PORT = 4000
PORT = 80
SERVER = localhost
ISTIO_PATH = /Users/rishabhkaushal/My_Apps/istio-1.13.2/samples/addons

DPL_TYPE = local

CLUSTER_NAME=aws756
EKS_CTX=aws756

MIN_NODES = 1


NGROUP=worker-nodes
NTYPE=t3.medium
REGION=us-west-2
KVER=1.21

LOG_DIR=logs

AMP_WORKSPACE_NAME=aws-prometheus-workspace
AMP_WORKSPACE_ID = $(shell aws amp list-workspaces --alias aws-prometheus-workspace --query "workspaces[].[workspaceId]" --output text)

OIDC_URL = $(shell aws eks describe-cluster --name aws756 --query "cluster.identity.oidc.issuer" --output text)
ACCOUNT_ID = $(shell aws sts get-caller-identity --query "Account" --output text)
SLEEP_10 = $(shell sleep 10)
SLEEP_2 = $(shell sleep 2)

GRAFANA_POD_NAME=$(shell kubectl get pods -n grafana --no-headers -o custom-columns=":metadata.name")

# testing
test-var:
	echo $(SLEEP_2)

# **************************************************************************** COMMANDS ****************************************************************************

# ************ EKS DEPLOYMENT COMMANDS ************
initialize-eks-1: initialize-aws-1

initialize-eks-2: initialize-aws-2 initialize-creds initialize-docker

run-eks: start-eks

configure-eks: configure-istio rollout-eks

analyze-eks: apply-grafana apply-prometheus apply-kiali

deploy-auto-scaler:
	kubectl apply -f ./kube-metrics-adapter/

######## AMP - Grafana Starts ########
initialize-AMP: create-AMP-Workspace create-EKS-AMP-ServiceAccount-Role create-AMP-Policies approve-iam-oidc-provider

analyze-eks-AMP: deploy-prometheus-for-amp deploy-local-grafana upgrade-grafana-env forward-local-grafana-5001

get-grafana-login-pswd:
	kubectl get secrets grafana-for-amp -n grafana -o jsonpath='{.data.admin-password}' | base64 --decode ; echo

get-AMP-prometheusEndpoint:
	aws amp describe-workspace --workspace-id $(AMP_WORKSPACE_ID) --query "workspace.prometheusEndpoint" --output text

cleanup-AMP-Grafana: delete-AMP-Workspace cleanup-AMP-Role cleanup-prom-grafana-namepaces stop-port-forwarding-5001

######## AMP - Grafana Ends ########

stop-eks: delete-eks

cleanup-eks: cleanup-aws cleanup-creds cleanup-docker


# **************************************************************************** AWS Prometheus - Grafana commands STARTS ****************************************************************************

# 0
create-AMP-Workspace:
	aws amp create-workspace --alias $(AMP_WORKSPACE_NAME) --region $(REGION)
	echo $(SLEEP_10)

create-AMP-Policies: create-AWSManagedPrometheusWriteAccessPolicy attach-EKS-AMP-ServiceAccount-Role

# 1
create-AWSManagedPrometheusWriteAccessPolicy:
	aws iam create-policy --policy-name "AWSManagedPrometheusWriteAccessPolicy" --policy-document file://./AMP-policies/AWSManagedPrometheusWriteAccessPolicy.json

# 2
create-EKS-AMP-ServiceAccount-Role:
	aws iam create-role --role-name "EKS-AMP-ServiceAccount-Role" --assume-role-policy-document file://./AMP-policies/TrustPolicy.json --description "SERVICE ACCOUNT IAM ROLE DESCRIPTION" --query "Role.Arn" --output text

# 3
attach-EKS-AMP-ServiceAccount-Role:
	aws iam attach-role-policy --role-name "EKS-AMP-ServiceAccount-Role" --policy-arn "arn:aws:iam::$(ACCOUNT_ID):policy/AWSManagedPrometheusWriteAccessPolicy"

# 4.1
approve-iam-oidc-provider:
	eksctl utils associate-iam-oidc-provider --cluster $(CLUSTER_NAME) --approve

# 4.2
deploy-prometheus-for-amp:
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	kubectl create ns prometheus-namespace
	helm install prometheus-for-amp prometheus-community/prometheus -n prometheus-namespace -f ./AMP-policies/amp_ingest_override_values.yaml --set serviceAccounts.server.annotations."eks\.amazonaws\.com/role-arn"="arn:aws:iam::$(ACCOUNT_ID):role/EKS-AMP-ServiceAccount-Role" --set server.remoteWrite[0].url="https://aps-workspaces.$(REGION).amazonaws.com/workspaces/$(AMP_WORKSPACE_ID)/api/v1/remote_write" --set server.remoteWrite[0].sigv4.region=$(REGION)
	# helm upgrade prometheus-for-amp prometheus-community/prometheus -n prometheus-namespace -f ./AMP-policies/my_prometheus_values_yaml

# 5
deploy-local-grafana:
	helm repo add grafana https://grafana.github.io/helm-charts
	kubectl create ns grafana
	helm install grafana-for-amp grafana/grafana -n grafana

# 6
upgrade-grafana-env:
	helm upgrade --install grafana-for-amp grafana/grafana -n grafana -f ./AMP-policies/amp_query_override_values.yaml
	echo $(SLEEP_10)

# 7
# get-kubernetes-secret-pswd:
# 	kubectl get secrets grafana-for-amp -n grafana -o jsonpath='{.data.admin-password}' | base64 --decode ; echo

# 8
forward-local-grafana-5001:
	kubectl port-forward -n grafana $(GRAFANA_POD_NAME) 5001:3000

# cleanups:
get-all-AMP-Workspaces:
	aws amp list-workspaces --alias $(AMP_WORKSPACE_NAME)

delete-AMP-Workspace:
	aws amp delete-workspace --workspace-id $(AMP_WORKSPACE_ID)
	echo $(SLEEP_10)

cleanup-AMP-Role: detach-AWSManagedPrometheusWriteAccessPolicy delete-AWSManagedPrometheusWriteAccessPolicy delete-EKS-AMP-ServiceAccount-Role

detach-AWSManagedPrometheusWriteAccessPolicy:
	aws iam detach-role-policy --role-name EKS-AMP-ServiceAccount-Role --policy-arn arn:aws:iam::$(ACCOUNT_ID):policy/AWSManagedPrometheusWriteAccessPolicy

delete-AWSManagedPrometheusWriteAccessPolicy:
	aws iam delete-policy --policy-arn arn:aws:iam::$(ACCOUNT_ID):policy/AWSManagedPrometheusWriteAccessPolicy

delete-EKS-AMP-ServiceAccount-Role:
	aws iam delete-role --role-name "EKS-AMP-ServiceAccount-Role"

cleanup-prom-grafana-namepaces: delete-AWS_Prometheus-namespace delete-local-grafana-namespace

delete-AWS_Prometheus-namespace:
	kubectl delete namespaces prometheus-namespace

delete-local-grafana-namespace:
	kubectl delete namespaces grafana

stop-port-forwarding-5001: kill-grafana-for-amp-processes

kill-grafana-for-amp-processes:
	ps -ef | grep 'grafana-for-amp' | grep -v grep | awk '{print $2}' | xargs kill -9

# **************************************************************************** AWS Prometheus - Grafana commands ENDS ****************************************************************************


# ************ LOCAL (DOCKER) DEPLOYMENT COMMANDS ************

initialize-local-1: initialize-aws-1

initialize-local-2: initialize-aws-2 initialize-creds initialize-docker

run-local: run-docker

stop-local: stop-docker

cleanup-local: cleanup-aws cleanup-creds cleanup-docker

# ************ MK8S DEPLOYMENT COMMANDS ************

initialize-mk8s-1: initialize-aws-1

initialize-mk8s-2: initialize-aws-2 initialize-creds initialize-docker

run-mk8s: start-mk8s configure-istio rollout-mk8s

analyze-mk8s: apply-grafana apply-prometheus apply-kiali

stop-mk8s: delete-mk8s

cleanup-mk8s: cleanup-aws cleanup-creds cleanup-docker

# **************************************************************************** K8S COMMANDS ****************************************************************************

# ************ EKS COMMANDS ************

start-eks:
	eksctl create cluster --name $(CLUSTER_NAME) --version $(KVER) --region $(REGION) --nodegroup-name $(NGROUP) --node-type $(NTYPE) --nodes 2 --nodes-min 2 --nodes-max 2 --managed | tee $(LOG_DIR)/eks-start.log

delete-eks:
	eksctl delete cluster --name $(CLUSTER_NAME) --region $(REGION) | tee $(LOG_DIR)/eks-stop.log

# ************ ISTIO COMMANDS ************

configure-istio: install-istio label-namespace-istio apply-gateway apply-vs

apply-vs: apply-vs-auth apply-vs-playlist apply-vs-subscription

apply-vs-fault: apply-vs-auth-fault apply-vs-playlist-fault apply-vs-subscription-fault

delete-vs: delete-vs-auth delete-vs-playlist delete-vs-subscription

# ------------------

label-namespace-istio:
	kubectl label namespace default istio-injection=enabled

# ------------------

install-istio:
	istioctl install -y

# ------------------

apply-gateway:
	kubectl apply -f k8s/gateway.yaml

delete-gateway:
	kubectl delete -f k8s/gateway.yaml

# ------------------

apply-vs-auth:
	kubectl apply -f k8s/auth_vs.yaml

apply-vs-playlist:
	kubectl apply -f k8s/playlist_vs.yaml

apply-vs-subscription:
	kubectl apply -f k8s/subscription_vs.yaml

# ------------------

delete-vs-auth:
	kubectl delete -f k8s/auth_vs.yaml

delete-vs-playlist:
	kubectl delete -f k8s/playlist_vs.yaml

delete-vs-subscription:
	kubectl delete -f k8s/subscription_vs.yaml

# ------------------

apply-vs-auth-fault:
	kubectl apply -f k8s/auth_vs_fault.yaml

apply-vs-playlist-fault:
	kubectl apply -f k8s/playlist_vs_fault.yaml

apply-vs-subscription-fault:
	kubectl apply -f k8s/subscription_vs_fault.yaml

# ************ ADDON COMMANDS ************

port-forward:
	kubectl port-forward svc/$(service) -n istio-system $(port)

# ************ ADDON COMMANDS ************

apply-grafana:
	kubectl apply -f $(ISTIO_PATH)/grafana.yaml

apply-prometheus:
	kubectl apply -f $(ISTIO_PATH)/prometheus.yaml

apply-kiali:
	kubectl apply -f $(ISTIO_PATH)/kiali.yaml

delete-grafana:
	kubectl delete -f $(ISTIO_PATH)/grafana.yaml

delete-prometheus:
	kubectl delete -f $(ISTIO_PATH)/prometheus.yaml

delete-kiali:
	kubectl delete -f $(ISTIO_PATH)/kiali.yaml

# ************ GET COMMANDS ************

get-istio-svcs:
	kubectl get svc -n istio-system

get-contexts:
	kubectl config get-contexts

get-namespaces:
	kubectl get namespace

get-config:
	kubectl config view

get-deployments:
	kubectl get deployments

get-clusters:
	kubectl config get-clusters

get-services:
	kubectl get services

get-pods:
	kubectl get pods -o wide

get-service-accounts:
	kubectl get serviceAccounts

# ************ ROLLOUT COMMANDS ************

rollout-mk8s: rollout-auth rollout-subscription rollout-playlist create-tunnel

rollout-eks: rollout-auth rollout-subscription rollout-playlist

rollout-auth:
	kubectl create -f k8s/auth.yaml

update-auth:
	kubectl apply -f k8s/auth.yaml

rollout-subscription:
	kubectl create -f k8s/subscription.yaml

rollout-playlist:
	kubectl create -f k8s/playlist.yaml

# ************ DELETE COMMANDS ************

delete-pods: delete-auth delete-subscription delete-playlist

delete-auth:
	kubectl delete -f k8s/auth.yaml

delete-subscription:
	kubectl delete -f k8s/subscription.yaml

delete-playlist:
	kubectl delete -f k8s/playlist.yaml

delete-pod:
	kubectl delete pods $(pod_name)

# ************ TUNNEL COMMANDS ************

create-namespace:
	kubectl create -f k8s/namespace.yaml

create-tunnel:
	minikube tunnel

# ************ SET COMMANDS ************

set-context:
	kubectl config use-context $(ctx) --namespace=$(ns)

set-namespace:
	kubectl config set-context --current --namespace=$(ns)

# ************ CLUSTER COMMANDS ************

start-mk8s:
	minikube start --nodes 1

stop-mk8s:
	minikube stop

delete-mk8s:
	minikube delete

get-mk8s-dashboard:
	minikube dashboard


# **************************************************************************** AWS COMMANDS ****************************************************************************

# ************ COMMANDS ************

initialize-aws-1: create-stack

initialize-aws-2:upload-music create-table-user create-table-cards create-table-playlists

cleanup-aws: empty-bucket delete-bucket delete-stack delete-table-playlist delete-table-cards delete-table-user

# ************ INITIALIZATION COMMANDS ************

create-stack:
	aws cloudformation create-stack \
	--capabilities CAPABILITY_NAMED_IAM \
	--stack-name csv-to-dynamo-db \
	--template-body file://dynamo-db/CSVToDynamo.template \
	--parameters ParameterKey=BucketName,ParameterValue=music-service-$(REGID) \
		ParameterKey=DynamoDBTableName,ParameterValue=music \
		ParameterKey=FileName,ParameterValue=music_100.csv | tee $(LOG_DIR)/stack.log
upload-music:
	aws s3 cp dynamo-db/music_100.csv s3://music-service-$(REGID)/music_100.csv | tee $(LOG_DIR)/s3.log

create-table-user:
	aws dynamodb create-table \
    --table-name User \
    --attribute-definitions \
        AttributeName=email,AttributeType=S \
    --key-schema \
        AttributeName=email,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST | tee $(LOG_DIR)/dynamodb.log

create-table-cards:
	aws dynamodb create-table \
    --table-name Cards \
    --attribute-definitions \
        AttributeName=card_no,AttributeType=S \
    --key-schema \
        AttributeName=card_no,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST | tee $(LOG_DIR)/dynamodb.log

create-table-playlists:
	aws dynamodb create-table \
    --table-name playlist \
    --attribute-definitions \
        AttributeName=playlist_uuid,AttributeType=S \
        AttributeName=playlist_name,AttributeType=S \
    --key-schema \
        AttributeName=playlist_uuid,KeyType=HASH \
        AttributeName=playlist_name,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST | tee $(LOG_DIR)/dynamodb.log

# ************ CLEANUP COMMANDS ************

empty-bucket:
	aws s3 rm s3://music-service-$(REGID) --recursive | tee $(LOG_DIR)/s3.log

delete-bucket:
	aws s3 rb s3://music-service-$(REGID) --force | tee $(LOG_DIR)/s3.log

delete-stack:
	aws cloudformation delete-stack --stack-name csv-to-dynamo-db | tee $(LOG_DIR)/stack.log

delete-table-user:
	aws dynamodb delete-table --table-name User | tee $(LOG_DIR)/dynamodb.log

delete-table-playlist:
	aws dynamodb delete-table --table-name playlist | tee $(LOG_DIR)/dynamodb.log

delete-table-cards:
	aws dynamodb delete-table --table-name Cards | tee $(LOG_DIR)/dynamodb.log
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
build-docker: build-network build-auth build-playlist build-subscription build-mcli

build-network:
	docker network create music-service-net

build-auth:
	docker build $(ARCH) --file auth/Dockerfile --tag ghcr.io/$(REGID)/auth:$(APP_VER_TAG) auth

build-playlist:
	docker build $(ARCH) --file playlist/Dockerfile --tag ghcr.io/$(REGID)/playlist:$(APP_VER_TAG) playlist

build-subscription:
	docker build $(ARCH) --file subscription/Dockerfile --tag ghcr.io/$(REGID)/subscription:$(APP_VER_TAG) subscription

build-mcli:
	docker build $(ARCH) --file mcli/Dockerfile --tag ghcr.io/$(REGID)/mcli:$(APP_VER_TAG) mcli

# ************ IMAGE PUSHING ************
push-docker: registry-login push-auth push-playlist push-subscription push-mcli

push-auth: registry-login
	docker push ghcr.io/$(REGID)/auth:$(APP_VER_TAG)

push-playlist: registry-login
	docker push ghcr.io/$(REGID)/playlist:$(APP_VER_TAG)

push-subscription: registry-login
	docker push ghcr.io/$(REGID)/subscription:$(APP_VER_TAG)

push-mcli: registry-login
	docker push ghcr.io/$(REGID)/mcli:$(APP_VER_TAG)

# ************ CONTAINER REGISTRY ************

registry-login:
	@/bin/sh -c 'cat ${CREG}-token.txt | docker login $(CREG) -u $(REGID) --password-stdin'

# ************ CONTAINER RUNNING ************

run-auth:
	docker container run -d --net music-service-net --rm -p $(AUTH_PORT):$(AUTH_PORT) --name auth ghcr.io/$(REGID)/auth:$(APP_VER_TAG)

run-playlist:
	docker container run -d --net music-service-net --rm -p $(PLAYLIST_PORT):$(PLAYLIST_PORT) --name playlist ghcr.io/$(REGID)/playlist:$(APP_VER_TAG)

run-subscription:
	docker container run -d --net music-service-net --rm -p $(SUBSCRIPTION_PORT):$(SUBSCRIPTION_PORT) --name subscription ghcr.io/$(REGID)/subscription:$(APP_VER_TAG)

run-mcli:
	docker container run -it --rm --net music-service-net --name mcli ghcr.io/$(REGID)/mcli:$(APP_VER_TAG) python3 mcli.py $(SERVER) $(PORT) $(DPL_TYPE)

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
	cp .env subscription

# ************ CREDENTIAL REMOVAL ************

cleanup-.env:
	rm auth/.env
	rm mcli/.env
	rm playlist/.env
	rm subscription/.env
