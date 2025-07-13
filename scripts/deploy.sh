#!/bin/bash
set -e

IMAGE_NAME=${1:-canary-demo:latest}
NAMESPACE=canary-demo

# Build and push Docker image

echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME ./app

echo "Pushing Docker image: $IMAGE_NAME"
docker push $IMAGE_NAME

echo "Updating rollout to use new image..."
kubectl -n $NAMESPACE set image rollout/canary-app-rollout canary-app=$IMAGE_NAME

echo "Deployment triggered! Use 'kubectl argo rollouts get rollout canary-app-rollout -n $NAMESPACE' to monitor." 