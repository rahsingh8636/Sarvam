#!/bin/bash
set -e

echo "[1/7] Creating namespaces..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/nginx-ingress/namespace.yaml
kubectl apply -f k8s/argo-rollouts/install.yaml
kubectl apply -f k8s/prometheus/namespace.yaml

echo "[2/7] Deploying Nginx Ingress Controller..."
kubectl apply -f k8s/nginx-ingress/controller.yaml

echo "[3/7] Installing Argo Rollouts CRDs..."
kubectl apply -f k8s/argo-rollouts/crds.yaml

echo "[4/7] Deploying Prometheus..."
kubectl apply -f k8s/prometheus/configmap.yaml
kubectl apply -f k8s/prometheus/deployment.yaml

echo "[5/7] Deploying App ConfigMap and Service..."
kubectl apply -f k8s/app/configmap.yaml
kubectl apply -f k8s/app/service.yaml

echo "[6/7] Deploying App Ingress..."
kubectl apply -f k8s/app/ingress.yaml

echo "[7/7] Deploying Argo Rollout and AnalysisTemplate..."
kubectl apply -f k8s/app/analysis-template.yaml
kubectl apply -f k8s/app/rollout.yaml

echo "Setup complete!"
echo "You can now deploy the FastAPI app image and start the canary rollout." 