# Deploy AI Models on Google GKE Autopilot

This repo contains a ML serving framework for deploying AI models specifically from [Hugging Face models](https://huggingface.co/models) on Google GKE Autopilot. 

[GKE Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview) is a mode of operation in GKE in which Google manages your cluster configuration, including your nodes, scaling, security, and other preconfigured settings. Autopilot clusters are optimized to run most production workloads, and provision compute resources based on your Kubernetes manifests.

## Deployment Infra

1. Copy the .env.sample to .env and edit the environment variables based on your preferences. 

```
cp .env.sample .env
```

2. Set env variables

```
. .env
```

3. Deploy infrastructure

```
cd infra
terraform init
terraform apply
```

## Build and Deploy Models






