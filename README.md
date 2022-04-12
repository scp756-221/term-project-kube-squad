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

1. Copy/paste ".env-tpl" as ".env".  Add aws access key id, and aws secret access key to ".env".  (If not already created, follow these instructions: 
https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/)

2. Copy/paste "ghcr.io-token-tpl.txt" as "ghcr.io-token.txt".  Add GitHub personal access token to ghcr.io-token.txt. (If 
not already created, create token with read/write/delete access using these instructions: 
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

3. Open "Makefile" and set "REGID" to your own GitHub username.

4. Open k8s/auth.yaml, k8s/subscription.yaml, and k8s/playlist.yaml.  In each of the files, set the image to pull from your own github package repository (image: ghcr.io/avickars/auth:v1 -> image: ghcr.io/your-github-userID/auth:v1)

### DynamoDB Setup

1. "make initialize-aws-1" // This command creates the cloud formation stack "csv-to-dynamo-db", and the S3 bucket "music-service-$(REGID)"
2. "aws cloudformation list-stacks" // Check to ensure the "csv-to-dynamo-db" stack has finished being created
3. "make initialize-aws-2" // This command creates the rest of the Dynamo DB tables required
4. "make initialize-creds" // This command copies the ".env" file to every docker container directory in the repo
5. "make initialize-docker" // This command builds all four containers, and pushes them to your GitHub package repository
6. Navigate to your package repository on GitHub.com, and change the auth, playlist, subscription and mcli containers to public.

## Run/Stopping/Cleaning Up

### EKS

#### Run
1. "start-eks" // Starts the cluster
2. "configure-istio" // Installs Istio into the cluster, and deploys the gateway and virtual service
3. "rollout-eks" // Deploys each service into the cluster
4. Open New Terminal
6. "make get-pods" // Check to ensure all services are ready
7. "make get-istio-svcs" // Note the external IP address of the "istio-ingressgateway" service, it is used send HTTP requests to the cluster

#### Configuring Grafana, Prometheus and Kiali
1. "make analyze-mk8s" // Deploys Grafana, Prometheus and Kiali into the cluster
2. Open New Terminal
3. "make port-forward service=kiali port=20001" // This command forwards Kiali to a local port.  To access Kiali, navigate to localhost:20001 in your web browser
4. Open New Terminal
5. "make port-forward service=grafana port=3000" // This command forwards Grafana to a local port.  To access Grafana, navigate to localhost:3000 in your web browser
6. Open New Terminal
7. "make port-forward service=prometheus port=9090" // This command forwards Prometheus to a local port.  To access Prometheus, navigate to localhost:9090 in your web browser

#### Configuring Auto-Scaling
1. "make deploy-auto-scaler" // Configures the auto scaling according to number of requests per second.
2. To edit the autoscaler metric for each service, navigate to "k8s/auth.yaml", "k8s/playlist.yaml" or "k8s/subscription.yaml", and adjust the metric used starting at line 45.

#### Configuring Circuit-Breaker
1. Adjust the circuit breakers as desired, see k8s/auth_cb.yaml, k8s/subscription_cb.yaml, and k8s/playlist_cb.yaml 
2. Run "make apply-cb-auth", "make apply-cb-subscription" and "make apply-cb-playlist" accordingly
3. To remove circuit breakers, run "make delete-cb-auth", "make delete-cb-subscription" and "make delete-cb-playlist" accordingly

#### Configuring Faults
1. Adjust the faults as desired, see k8s/auth_vs_fault.yaml, k8s/subscription_vs_fault.yaml, and k8s/playlist_vs_fault.yaml 
2. Run "make apply-vs-auth-fault", "make apply-vs-subscription-fault", "make apply-vs-playlist-fault" accordingly // these commands define the virtual services of each service with faults
3. To remove faults, run "make apply-vs-auth", "make apply-vs-subscription", "make apply-vs-playlist" accordingly // these commands define the virtual services of each service without faults

#### Making Requests
Run "make get-istio-svcs", use the EXTERNAL-IP for the "istio-ingressgateway" service to use as the EXTERNAL_IP variable in the sample http requests and mcli application below.

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
1. "make cleanup-aws" // Deletes all AWS resources created during setup
2. "make cleanup-creds" // Removes ".env" file every container directory

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
5. "make get-pods" // Check to ensure all services are ready
6. Make HTTP requests to the cluster using localhost (See below for sample commands)

#### Configuring Grafana, Prometheus and Kiali
1. "make analyze-mk8s" // Deploys Grafana, Prometheus and Kiali into the cluster
2. Open New Terminal
3. "make port-forward service=kiali port=20001" // This command forwards Kiali to a local port.  To access Kiali, navigate to localhost:20001 in your web browser
4. Open New Terminal
5. "make port-forward service=grafana port=3000" // This command forwards Grafana to a local port.  To access Grafana, navigate to localhost:3000 in your web browser
6. Open New Terminal
7. "make port-forward service=prometheus port=9090" // This command forwards Prometheus to a local port.  To access Prometheus, navigate to localhost:9090 in your web browser

#### Configuring Circuit-Breaker
1. Adjust the circuit breakers as desired, see k8s/auth_cb.yaml, k8s/subscription_cb.yaml, and k8s/playlist_cb.yaml 
2. Run "make apply-cb-auth", "make apply-cb-subscription" and "make apply-cb-playlist" accordingly
3. To remove circuit breakers, run "make delete-cb-auth", "make delete-cb-subscription" and "make delete-cb-playlist" accordingly

#### Configuring Faults
1. Adjust the faults as desired, see k8s/auth_vs_fault.yaml, k8s/subscription_vs_fault.yaml, and k8s/playlist_vs_fault.yaml 
2. Run "make apply-vs-auth-fault", "make apply-vs-subscription-fault", "make apply-vs-playlist-fault" accordingly // these commands define the virtual services of each service with faults
3. To remove faults, run "make apply-vs-auth", "make apply-vs-subscription", "make apply-vs-playlist" accordingly // these commands define the virtual services of each service without faults

#### Configuring Auto-Scaling
Note: Auto-Scaling does not work in Minikube

#### Making Requests
Sample Requests:
- curl -v http://localhost/api/v1/auth/logout
- curl -X POST http://localhost/api/v1/auth/register -H 'Content-Type: application/json' -d '{"name":"user","email":"user@sfu.ca", "password":"test"}'
- curl -X POST http://localhost/api/v1/auth/login -H 'Content-Type: application/json' -d '{"user":"user@sfu.ca","password":"test"}'
- curl -X POST http://localhost/api/v1/subscribe/addcard  -H 'Content-Type: application/json' -d '{"card_no":"123456789","cvv":"123","exp_month":"03","exp_year":"2023"}'
- curl -v http://localhost/api/v1/music/getMusicList

Using MCLI:

Note: the MCLI does not work with services deployed to Minikube

#### Stop
1. "make stop-mk8s" // Terminates and deletes cluster

#### Cleanup
1. "start-mk8s" // Removes the created network from Docker (the other containers are removed when stopped)
2. "make cleanup-aws" // Deletes all AWS resources created during setup
3. "make cleanup-creds" // Removes ".env" file every container directory
