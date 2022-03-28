#!/bin/bash -e
CLUSTER_NAME=eks_cluster_name
REGION=us-west-2
AWS_ACCOUNT_ID=123456789012
OIDC_PROVIDER=oidc.eks.us-west-2.amazonaws.com/id/B12345678ABCD123EB1234567891ABCD
AMP_WORKSPACE_ID=ws-123445-abcd-1234-1234-123455asdbde
AMP_ENDPOINT=https://aps-workspaces.us-west-2.amazonaws.com/workspaces/${AMP_WORKSPACE_ID}/


#
# Set up a trust policy designed for a specific combination of K8s service account and namespace to sign in from a Kubernetes cluster which hosts the OIDC Idp.
#
cat <<EOF > TrustPolicy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "${OIDC_PROVIDER}:sub": "system:serviceaccount:prometheus:iamproxy-service-account"
        }
      }
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "${OIDC_PROVIDER}:sub": "system:serviceaccount:grafana:iamproxy-service-account"
        }
      }
    }
  ]
}
EOF

#
# Write amp_query_override_values.yaml
#
cat <<EOF > amp_query_override_values.yaml

serviceAccount:
    name: "iamproxy-service-account"
    annotations:

        eks.amazonaws.com/role-arn: "arn:aws:iam::${AWS_ACCOUNT_ID}:role/EKS-AMP-ServiceAccount-Role"
grafana.ini:
  auth:
    sigv4_auth_enabled: true
EOF

#
# Write my_prometheus_values_yaml
#
cat <<EOF > my_prometheus_values_yaml
## The following is a set of default values for prometheus server helm chart which enable remoteWrite to AMP
## For the rest of prometheus helm chart values see: https://github.com/prometheus-community/helm-charts/blob/main/charts/prometheus/values.yaml
##
serviceAccounts:
        server:
            name: "amp-iamproxy-ingest-service-account"
            annotations:
                eks.amazonaws.com/role-arn: "arn:aws:iam::${AWS_ACCOUNT_ID}:role/amp-iamproxy-ingest-role"
server:
    remoteWrite:
        - url: ${AMP_ENDPOINT}api/v1/remote_write
          sigv4:
            region: ${REGION}
          queue_config:
            max_samples_per_send: 1000
            max_shards: 200
            capacity: 2500
EOF
