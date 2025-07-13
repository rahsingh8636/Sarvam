# Architecture Overview

## Components

- **FastAPI App**: Demo application with versioned endpoints, health checks, and Prometheus metrics.
- **Docker**: Containerizes the FastAPI app for Kubernetes deployment.
- **Kubernetes**: Orchestrates all components in isolated namespaces.
- **Nginx Ingress Controller**: Handles external traffic and supports weighted routing for canary rollouts.
- **Argo Rollouts**: Manages canary deployments, traffic splitting, manual approvals, and integrates with Prometheus for auto-rollback.
- **Prometheus**: Scrapes metrics from the app and provides error rate data to Argo Rollouts.

## Canary Rollout Flow

1. **Initial State**: v1 of the app is running and serving 100% of traffic.
2. **Rollout Triggered**: New image (v2) is deployed via Argo Rollouts.
3. **Traffic Splitting**: Nginx Ingress and Argo Rollouts split traffic in stages (5% → 25% → 50% → 100%).
4. **Manual Approval**: Each stage requires explicit approval before proceeding.
5. **Monitoring**: Prometheus scrapes `/metrics` from the app. If error rate >10%, Argo auto-rolls back.
6. **Rollback**: On failure or manual rejection, traffic returns to stable version.
7. **Audit Logging**: All rollout actions, approvals, and rollbacks are logged and can be extracted for audit.
8. **Emergency Deployment**: For critical fixes, a direct deployment bypasses canary and shifts 100% traffic instantly.

## Diagram

```
User → Nginx Ingress → Argo Rollouts → FastAPI App (v1/v2)
                        ↑           ↓
                Prometheus ← Metrics
```

- **Argo Rollouts** orchestrates the canary process and interacts with Nginx for traffic weights.
- **Prometheus** provides real-time error metrics for automated rollback decisions.
- **Audit logs** are available via Argo Rollouts events and FastAPI logs. 