# Troubleshooting Guide

## Common Issues

### 1. Nginx Ingress Not Routing Traffic
- Ensure the ingress controller is running in the `ingress-nginx` namespace.
- Check that the ingress resource has the correct annotations and host.
- Make sure your `/etc/hosts` file points `canary-demo.local` to your cluster IP.

### 2. Argo Rollouts Not Progressing
- Use `kubectl argo rollouts get rollout canary-app-rollout -n canary-demo` to check status.
- If stuck on a pause, approve the step with:
  ```bash
  kubectl argo rollouts promote canary-app-rollout -n canary-demo
  ```
- Check for errors in the rollout events:
  ```bash
  kubectl -n canary-demo get events --field-selector involvedObject.name=canary-app-rollout
  ```

### 3. Prometheus Not Scraping Metrics
- Ensure Prometheus is running in the `monitoring` namespace.
- Check the `prometheus.yml` configmap for correct scrape configs.
- Verify the FastAPI app exposes `/metrics` and is reachable from Prometheus.

### 4. Rollout Not Auto-Rolling Back
- Confirm the AnalysisTemplate is correctly configured and referenced in the Rollout.
- Check Prometheus query results for error rates.
- Ensure the app exposes the correct Prometheus metrics (`http_requests_total`, `http_errors_total`).

### 5. Emergency Deployment Not Working
- Make sure the emergency deployment manifest is applied in the `canary-demo` namespace.
- Check for pod status and logs for errors.

## Debugging Tips
- Use `kubectl describe` on pods, services, and rollouts for detailed info.
- Check logs of the FastAPI app and Argo Rollouts controller.
- Use `kubectl port-forward` to access Prometheus or the app directly.

## Getting Help
- See Argo Rollouts and Prometheus documentation for advanced troubleshooting.
- Check the `scripts/audit-log.sh` output for audit and event history. 