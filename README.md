# Kubernetes Canary Deployment with Argo Rollouts

This project demonstrates a complete weight-based canary deployment setup using Kubernetes, Argo Rollouts, and FastAPI. It includes manual approval workflows, traffic splitting, monitoring, and emergency deployment capabilities.


---

## Architecture Overview

See [docs/architecture.md](docs/architecture.md)

## Features

- **4-Stage Canary Deployment**: 5% → 25% → 50% → 100% traffic splitting
- **Manual Approval Workflow**: Each stage requires explicit approval
- **Rollback Capability**: Ability to reject/abort at any stage
- **Health Checks**: Proper health endpoints for monitoring
- **Prometheus Integration**: Error rate monitoring with auto-rollback
- **Emergency Deployment**: Bypass canary for critical hotfixes
- **Audit Logging**: Complete deployment activity tracking
- **Version Identification**: Clear version display in responses

## Project Structure

```
.
├── README.md                           # This file
├── k8s/                               # Kubernetes manifests
│   ├── namespace.yaml                 # Project namespace
│   ├── nginx-ingress/                 # Nginx ingress controller
│   ├── argo-rollouts/                 # Argo Rollouts setup
│   ├── prometheus/                    # Prometheus monitoring
│   ├── app/                          # Application manifests
│   └── emergency/                    # Emergency deployment
├── app/                              # FastAPI application
│   ├── Dockerfile                    # Container image
│   ├── requirements.txt              # Python dependencies
│   ├── main.py                       # FastAPI application
│   └── versions/                     # Different app versions
├── scripts/                          # Utility scripts
│   ├── setup.sh                      # Complete setup script
│   ├── deploy.sh                     # Deployment script
│   └── demo.sh                       # Demo scenarios
└── docs/                             # Documentation
    ├── architecture.md               # Detailed architecture
    └── troubleshooting.md            # Troubleshooting guide
```

## Prerequisites

- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl CLI tool
- Docker
- Argo Rollouts CLI (`kubectl argo rollouts`)

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd kubernetes-canary-deployment
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

2. **Deploy the application**:
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```

3. **Run demo scenarios**:
   ```bash
   chmod +x scripts/demo.sh
   ./scripts/demo.sh
   ```

## Manual Setup Steps

### 1. Install Nginx Ingress Controller

```bash
kubectl apply -f k8s/nginx-ingress/
```

### 2. Install Argo Rollouts

```bash
kubectl apply -f k8s/argo-rollouts/
kubectl argo rollouts install
```

### 3. Deploy Prometheus

```bash
kubectl apply -f k8s/prometheus/
```

### 4. Deploy Application

```bash
kubectl apply -f k8s/app/
```

## Demo Scenarios

### Success Scenario
1. Deploy v1 of the application
2. Initiate canary deployment to v2
3. Approve each stage (5% → 25% → 50% → 100%)
4. Verify traffic splitting and version identification

### Failure Scenario
1. Deploy v1 of the application
2. Initiate canary deployment to v2
3. At 25% stage, trigger high error rate
4. Observe auto-rollback due to Prometheus metrics
5. Manually reject deployment

### Emergency Deployment
1. Use emergency deployment manifest
2. Bypass canary stages
3. Deploy directly to 100% traffic

## Monitoring and Metrics

- **Application Metrics**: Available at `/metrics` endpoint
- **Prometheus**: Scrapes metrics every 30 seconds
- **Error Rate Threshold**: 10% 5xx errors triggers auto-rollback
- **Argo Rollouts Dashboard**: Available at port 3100

## API Endpoints

- `GET /` - Main endpoint with version info
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics
- `GET /version` - Version information
- `POST /simulate-error` - Simulate errors for testing




## License

MIT License - see LICENSE file for details. 