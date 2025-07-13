#!/bin/bash
set -e
NAMESPACE=canary-demo

# Success scenario: canary rollout from v1 to v2

echo "[1/3] Starting canary rollout: v1 -> v2"
kubectl -n $NAMESPACE argo rollouts set image canary-app-rollout canary-app=canary-demo:latest
kubectl -n $NAMESPACE argo rollouts promote canary-app-rollout --full

echo "[2/3] Simulating failure at 25% stage (injecting errors)"
echo "Triggering errors on v2 pods..."
POD=$(kubectl -n $NAMESPACE get pods -l app=canary-app -o jsonpath='{.items[0].metadata.name}')
kubectl -n $NAMESPACE exec $POD -- curl -X POST http://localhost:8000/simulate-error?error_rate=1.0 || true

echo "[3/3] Emergency deployment (bypass canary)"
kubectl apply -f k8s/emergency/deployment.yaml

echo "Demo complete! Check rollout status and logs for details." 