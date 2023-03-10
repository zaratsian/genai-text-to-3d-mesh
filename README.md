# Deploy Text to 3d models on Google GKE Autopilot

This repo contains a ML serving framework for deploying a text to 3d image model (from openAI, called Point-e) on Google GKE Autopilot. 

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

1. Navigate into the services directory

```
cd ./services
```

2. Copy the .env.sample into a file called .env, then edit the environment variables to match your preferred setup.

```
cd ./services

# Copy the .env.sample
cp .env.sample .env

# Edit the env variables within the file
vi .env

# Apply the env variables
. .env
```

3. Build the ML Serving Container and Deploy to Artifact Registry

```
cd ./services/app
./cloudbuild_trigger.sh
```

4. Deploy the service to GKE

```
cd ./services
./deploy_to_gke.sh
```

5. Wait a few minutes for the service to start up.

```
kubectl get services -n genai-ns
kubectl get pods -n genai-ns
```

6. Test the Endpoint

I have provided 2 options for testing the deployed model. 

You can run the raw python code (as shown below, and it will save a mesh.ply file on your local machine based on the text you enter. Or you can use the [Notebook call test_endpoint.ipynb](./services/app/test_endpoint.ipynb) that I provided, which will render a 3d image mesh that you can view and manipulate via Plotly. 

```
export SERVICE_IP=$(kubectl get svc genai-service -n genai-ns -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

python3 ./services/app/test_endpoint.py --host $SERVICE_IP --port 80 --text "surfing goat with sunset in the background"
```



