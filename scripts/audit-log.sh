#!/bin/bash
set -e
NAMESPACE=canary-demo
ROLLOUT=canary-app-rollout

# Extract rollout events

echo "[Audit Log] Rollout Events for $ROLLOUT in $NAMESPACE"
kubectl -n $NAMESPACE get events --field-selector involvedObject.name=$ROLLOUT --sort-by=.lastTimestamp

echo "[Audit Log] Rollout History"
kubectl -n $NAMESPACE argo rollouts history $ROLLOUT

echo "[Audit Log] Manual Approvals (Pauses)"
kubectl -n $NAMESPACE argo rollouts get rollout $ROLLOUT -o yaml | grep -A 5 pause

echo "[Audit Log] User Info (if RBAC auditing enabled)"
kubectl -n $NAMESPACE get events --field-selector involvedObject.name=$ROLLOUT -o json | jq '.items[] | {user: .reportingInstance, time: .lastTimestamp, reason: .reason, message: .message}' 