#
# Front-end to bring some sanity to the litany of tools and switches
# for working with a k8s cluster. Note that this file exercise core k8s
# commands that's independent of the cluster vendor.
#
# All vendor-specific commands are in the make file for that vendor:
# az.mak, eks.mak, gcp.mak, mk.mak
#
# This file addresses APPPLing the Deployment, Service, Gateway, and VirtualService
#
# Be sure to set your context appropriately for the log monitor.
#
# The intended approach to working with this makefile is to update select
# elements (body, id, IP, port, etc) as you progress through your workflow.
# Where possible, stodout outputs are tee into .out files for later review.

# These will be filled in by template processor
CREG=ZZ-CR-ID
REGID=ZZ-REG-ID
AWS_REGION=ZZ-AWS-REGION

# Keep all the logs out of main directory
LOG_DIR=logs

# These should be in your search path
KC=kubectl
DK=docker
AWS=aws
IC=istioctl
EKS=eksctl

# Application versions
# Override these by environment variables and `make -e`
APP_VER_TAG=v1
S2_VER=v1
LOADER_VER=v1

# these might need to change
NS=c756ns
CLUSTER_NAME=aws756
EKS_CTX=aws756

# Kubernetes parameters that most of the time will be unchanged
# but which you might override as projects become sophisticated
APP_NS=c756ns
ISTIO_NS=istio-system

# this is used to switch M1 Mac to x86 for compatibility with x86 instances/students
ARCH=--platform x86_64

NGROUP=worker-nodes
NTYPE=t3.medium
REGION=us-west-2
KVER=1.21


# ----------------------------------------------------------------------------------------
# -------  Targets to be invoked directly from command line                        -------
# ----------------------------------------------------------------------------------------

# ---  templates:  Instantiate all template files
#
# This is the only entry that *must* be run from k8s-tpl.mak
# (because it creates k8s.mak)
templates:
	tools/process-templates.sh

start: showcontext
	# Creating cluster
	$(EKS) create cluster --name $(CLUSTER_NAME) --version $(KVER) --region $(REGION) --nodegroup-name $(NGROUP) --node-type $(NTYPE) --nodes 2 --nodes-min 2 --nodes-max 2 --managed | tee $(LOG_DIR)/eks-start.log

	# Renaming the context
	$(KC) config rename-context `$(KC) config current-context` $(EKS_CTX) | tee -a $(LOG_DIR)/eks-start.log

	# Using the current Context
	$(KC) config use-context aws756

	# Creating a namespace inside this context
	$(KC) create ns c756ns

	# Setting this context to use this namespace
	$(KC) config set-context aws756 --namespace=c756ns

stop:
	$(EKS) delete cluster --name $(CLUSTER_NAME) --region $(REGION) | tee $(LOG_DIR)/eks-stop.log
	$(KC) config delete-context $(EKS_CTX) | tee -a $(LOG_DIR)/eks-stop.log

istio:
	$(KC) config use-context aws756
	$(IC) install -y --set profile=demo --set hub=gcr.io/istio-release
	$(KC) label namespace c756ns istio-injection=enabled
namespaces-all:
	$(KC) get services --all-namespaces
context-list:
	$(KC) config get-contexts
context-current:
	$(KC) config current-context
build:
	
$(LOG_DIR)/s1.repo.log: s1/Dockerfile s1/app.py s1/requirements.txt
	$(DK) build $(ARCH) -t $(CREG)/$(REGID)/cmpt756s1:$(APP_VER_TAG) s1 | tee $(LOG_DIR)/s1.img.log

	# Build the s2 service
$(LOG_DIR)/s2-$(S2_VER).repo.log: s2/$(S2_VER)/Dockerfile s2/$(S2_VER)/app.py s2/$(S2_VER)/requirements.txt
	$(DK) build $(ARCH) -t $(CREG)/$(REGID)/cmpt756s2:$(S2_VER) s2 | tee $(LOG_DIR)/s2-$(S2_VER).img.log

	# Build the db service
$(LOG_DIR)/db.repo.log: db/Dockerfile db/app.py db/requirements.txt
	$(DK) build $(ARCH) -t $(CREG)/$(REGID)/cmpt756db:$(APP_VER_TAG) db | tee $(LOG_DIR)/db.img.log

	# Build the loader
$(LOG_DIR)/loader.repo.log: loader/app.py loader/requirements.txt loader/Dockerfile registry-login
	$(DK) build $(ARCH) -t $(CREG)/$(REGID)/cmpt756loader:$(LOADER_VER) loader  | tee $(LOG_DIR)/loader.img.log
	
push:
	# Push the s1 service
	$(DK) push $(CREG)/$(REGID)/cmpt756s1:$(APP_VER_TAG) | tee $(LOG_DIR)/s1.repo.log

	# Push the s2 service
	$(DK) push $(CREG)/$(REGID)/cmpt756s2:$(S2_VER) | tee $(LOG_DIR)/s2-$(S2_VER).repo.log

	# Push the db service
	$(DK) push $(CREG)/$(REGID)/cmpt756db:$(APP_VER_TAG) | tee $(LOG_DIR)/db.repo.log

	# Push the loader
	$(DK) push $(CREG)/$(REGID)/cmpt756loader:$(LOADER_VER) | tee $(LOG_DIR)/loader.repo.log

deploy: gw db s2

gw: cluster/service-gateway.yaml
	$(KC) -n $(APP_NS) apply -f $< > $(LOG_DIR)/gw.log

# Update DB and associated monitoring, rebuilding if necessary
db: 
	$(LOG_DIR)/db.repo.log cluster/awscred.yaml cluster/dynamodb-service-entry.yaml cluster/db.yaml cluster/db-sm.yaml cluster/db-vs.yaml
	$(KC) -n $(APP_NS) apply -f cluster/awscred.yaml | tee $(LOG_DIR)/db.log
	$(KC) -n $(APP_NS) apply -f cluster/dynamodb-service-entry.yaml | tee -a $(LOG_DIR)/db.log
	$(KC) -n $(APP_NS) apply -f cluster/db.yaml | tee -a $(LOG_DIR)/db.log
	$(KC) -n $(APP_NS) apply -f cluster/db-sm.yaml | tee -a $(LOG_DIR)/db.log
	$(KC) -n $(APP_NS) apply -f cluster/db-vs.yaml | tee -a $(LOG_DIR)/db.log

# Update S2 and associated monitoring, rebuilding if necessary
s2: rollout-s2 cluster/s2-svc.yaml cluster/s2-sm.yaml cluster/s2-vs.yaml
	$(KC) -n $(APP_NS) apply -f cluster/s2-svc.yaml | tee $(LOG_DIR)/s2.log
	$(KC) -n $(APP_NS) apply -f cluster/s2-sm.yaml | tee -a $(LOG_DIR)/s2.log
	$(KC) -n $(APP_NS) apply -f cluster/s2-vs.yaml | tee -a $(LOG_DIR)/s2.log

# --- rollout-s2: Rollout a new deployment of S2
rollout-s2: $(LOG_DIR)/s2-$(S2_VER).repo.log  cluster/s2-dpl-$(S2_VER).yaml
	$(KC) -n $(APP_NS) apply -f cluster/s2-dpl-$(S2_VER).yaml | tee $(LOG_DIR)/rollout-s2.log
	$(KC) rollout -n $(APP_NS) restart deployment/cmpt756s2-$(S2_VER) | tee -a $(LOG_DIR)/rollout-s2.log

# Run the loader, rebuilding if necessary, starting DynamDB if necessary, building ConfigMaps
loader: dynamodb-init $(LOG_DIR)/loader.repo.log cluster/loader.yaml
	$(KC) -n $(APP_NS) delete --ignore-not-found=true jobs/cmpt756loader
	tools/build-configmap.sh gatling/resources/users.csv cluster/users-header.yaml | kubectl -n $(APP_NS) apply -f -
	tools/build-configmap.sh gatling/resources/music.csv cluster/music-header.yaml | kubectl -n $(APP_NS) apply -f -
	$(KC) -n $(APP_NS) apply -f cluster/loader.yaml | tee $(LOG_DIR)/loader.log

# --- dynamodb-init: set up our DynamoDB tables
#
dynamodb-init: $(LOG_DIR)/dynamodb-init.log

# Start DynamoDB at the default read and write rates
$(LOG_DIR)/dynamodb-init.log: cluster/cloudformationdynamodb.json
	@# "|| true" suffix because command fails when stack already exists
	@# (even with --on-failure DO_NOTHING, a nonzero error code is returned)
	$(AWS) cloudformation create-stack --stack-name db-avickars --template-body file://$< || true | tee $(LOG_DIR)/dynamodb-init.log
	# Must give DynamoDB time to create the tables before running the loader
	sleep 20


# --- registry-login: Login to the container registry
#
registry-login:
	@/bin/sh -c 'cat cluster/${CREG}-token.txt | $(DK) login $(CREG) -u $(REGID) --password-stdin'

# --- Variables defined for URL targets
# Utility to get the hostname (AWS) or ip (everyone else) of a load-balanced service
# Must be followed by a service
IP_GET_CMD=tools/getip.sh $(KC) $(ISTIO_NS)

# This expression is reused several times
# Use back-tick for subshell so as not to confuse with make $() variable notation
INGRESS_IP=`$(IP_GET_CMD) svc/istio-ingressgateway`





