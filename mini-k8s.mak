# These will be filled in by template processor
CREG=ghcr.io
REGID=avickars
AWS_REGION=us-west-2

# These should be in your search path
MKS=minikube 
KC=kubectl
ISC=istioctl
DK=docker

# Application versions
# Override these by environment variables and `make -e`
APP_VER_TAG=v1
S2_VER=v1
LOADER_VER=v1

# Keep all the logs out of main directory
LOG_DIR=logs

# these might need to change
CLUSTER_NAME=aws756
MKS_CTX=aws756

# this is used to switch M1 Mac to x86 for compatibility with x86 instances/students
ARCH=--platform x86_64

start:
	$(MKS) start --nodes=2 --profile ${CLUSTER_NAME} tee $(LOG_DIR)/eks-start.log
	$(KC) config use-context aws756
	$(KC) create ns c756ns
	$(KC) config set-context aws756 --namespace=c756ns
	$(ISC) install -y --set profile=demo --set hub=gcr.io/istio-release
	$(KC) label namespace c756ns istio-injection=enabled
stop:
	$(MKS) stop
delete:
	$(MKS) delete
delete-all:
	$(MKS) delete --all
view-all:
	$(MKS) profile list
context-current:
	$(KC) config current-context
context-list:
	$(KC) config get-contexts
context-change:
	$(KC) config use-context ${context} --user=cluster-admin
config:
	$(KC) config view
build:
	# Build the s1 service
	$(DK) build $(ARCH) -t $(CREG)/$(REGID)/cmpt756s1:$(APP_VER_TAG) s1 | tee $(LOG_DIR)/s1.img.log

	# Build the s2 service
	$(DK) build $(ARCH) -t $(CREG)/$(REGID)/cmpt756s2:$(S2_VER) s2 | tee $(LOG_DIR)/s2-$(S2_VER).img.log

	# Build the db service
	$(DK) build $(ARCH) -t $(CREG)/$(REGID)/cmpt756db:$(APP_VER_TAG) db | tee $(LOG_DIR)/db.img.log

	# Build the loader
	$(DK) build $(ARCH) -t $(CREG)/$(REGID)/cmpt756loader:$(LOADER_VER) loader  | tee $(LOG_DIR)/loader.img.log
deply: appns


# Create and configure the application namespace
appns:
	# Appended "|| true" so that make continues even when command fails
	# because namespace already exists
	$(KC) create ns $(APP_NS) || true
	$(KC) label namespace $(APP_NS) --overwrite=true istio-injection=enabled


