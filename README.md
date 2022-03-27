[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=6952704&assignment_repo_type=AssignmentRepo)

# Term Project README

## Prerequisites

- Docker
- Istio
- AWS CLI (Configured)
- Kubectl
- Eksctl
- GitHub 

## Setup

Execute every command and action to configure the service.

### Initial Setup

1. Copy/paste ".env-tpl" as ".env".  Add aws access key id, aws secret access key and preferred 
aws region to ".env".  (If not already created, follow these instructions: 
https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/)

2. Copy/paste "ghcr.io-token-tpl.txt" as "ghcr.io-token.txt".  Add GitHub personal access token to ghcr.io-token.txt. (If 
not already created, create token with read/write/delete access using these instructions: 
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

3. Open "Makefile" and set "REGID" to your own GitHub username.

### DynamoDB Setup

1. "make initialize-aws-1" // This command creates the cloud formation stack "csv-to-dynamo-db", and the S3 bucket "music-service-$(REGID)"
2. "aws cloudformation list-stacks" // Check to ensure the "csv-to-dynamo-db" stack has finished being created
3. "make initialize-aws-2" // This command creates the rest of the Dynamo DB tables required
4. "make initialize-creds" // This command copies the ".env" file to every docker container directory in the repo
5. "make initialize-docker" // This command builds all four containers
6. "make push-docker" // This command pushes each container to your GitHub Packages registry

## Run/Stopping/Cleaning Up

### As Containers Locally

#### Run
1. "make run-docker" // Runs all containers
2. Interact with MCLI Service  as needed

#### Stop
1. "make stop-docker" // Stops and removes all containers

#### Cleanup
1. "make cleanup-docker" // Removes the created network from Docker (the other containers are removed when stopped)
2. "make cleanup-aws" // Deletes all AWS resources created during setup
3. "make cleanup-creds" // Removes ".env" file every container directory

### Minikube

#### Run
1. "start-mk8s" // Starts the cluster
2. "configure-istio" // Installs Istio into the cluster, and deploys the gateway and virtual service
3. "rollout-mk8s" // Deploys each service into the cluster, and creates tunnel into the cluster.  NOTE: AutoScaling does not work on MK8S, ignore errors
4. Enter super-user password into terminal as requested to allow tunnel access.
5. Open New Terminal
6. "make analyze-mk8s" // Deploys Grafana, Prometheus and Kiali into the cluster
7. Grafana, Kiali and Prometheus ACCESS HERE
8. Make HTTP requests to the cluster using localhost (See below for sample commands)
9. "make get-pods" // Check to ensure all services are ready

#### Making Requests
Sample Requests:
- curl -v http://localhost/api/v1/auth/logout
- curl -X POST http://localhost/api/v1/auth/register -H 'Content-Type: application/json' -d '{"name":"user","email":"user@sfu.ca", "password":"test"}'
- curl -X POST http://localhost/api/v1/auth/login -H 'Content-Type: application/json' -d '{"user":"user@sfu.ca","password":"test"}'
- curl -X POST http://localhost/api/v1/subscribe/addcard  -H 'Content-Type: application/json' -d '{"card_no":"123456789","cvv":"123","exp_month":"03","exp_year":"2023"}'
- curl -v http://localhost/api/v1/music/getMusicList

#### Stop
1. "make stop-mk8s" // Terminates and deletes cluster

#### Cleanup
1. "start-mk8s" // Removes the created network from Docker (the other containers are removed when stopped)
2. "make cleanup-aws" // Deletes all AWS resources created during setup
3. "make cleanup-creds" // Removes ".env" file every container directory

### EKS

#### Run
1. "start-eks" // Starts the cluster
2. "configure-istio" // Installs Istio into the cluster, and deploys the gateway and virtual service
3. "rollout-eks" // Deploys each service into the cluster, and creates tunnel into the cluster
4. Open New Terminal
5. "make analyze-mk8s" // Deploys Grafana, Prometheus and Kiali into the cluster
6. Grafana, Kiali and Prometheus ACCESS HERE
7. "make get-pods" // Check to ensure all services are ready
8. "make get-istio-svcs" // Note the external IP address here, it is used send HTTP requests to the cluster

#### Making Requests
Sample HTTP Requests:
- curl -v http://<EXTERNAL_IP>/api/v1/auth/logout
- curl -X POST http://<EXTERNAL_IP>/api/v1/auth/register -H 'Content-Type: application/json' -d '{"name":"user","email":"user@sfu.ca", "password":"test"}'
- curl -X POST http://<EXTERNAL_IP>/api/v1/auth/login -H 'Content-Type: application/json' -d '{"user":"user@sfu.ca","password":"test"}'
- curl -X POST http://<EXTERNAL_IP>/api/v1/subscribe/addcard  -H 'Content-Type: application/json' -d '{"card_no":"123456789","cvv":"123","exp_month":"03","exp_year":"2023"}'
- curl -v http://<EXTERNAL_IP>/api/v1/music/getMusicList

Using MCLI:

"make run-mcli SERVER=<EXTERNAL_IP> PORT=80 DPL_TYPE=k8s"

#### Stop
1. "make stop-eks" // Terminates and deletes cluster

#### Cleanup
1. "stop-eks" // Removes the created network from Docker (the other containers are removed when stopped)
2. "make cleanup-aws" // Deletes all AWS resources created during setup
3. "make cleanup-creds" // Removes ".env" file every container directory