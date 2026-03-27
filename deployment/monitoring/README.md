# Monitoring Deployment Code
Monitoring with Prometheus uses a Helm chart so that needs to be installed before hand


## Deploying Prometheus
```
helm upgrade --install prometheus \
  -n monitoring \
  --create-namespace \
  prometheus-community/kube-prometheus-stack \
  -f deployment/monitoring/values.yml
```
- status of endpoint can be found here - http://localhost:30300/targets
- Get password with `kubectl get secret --namespace monitoring -l app.kubernetes.io/component=admin-secret -o jsonpath="{.items[0].data.admin-password}" | base64 --decode ; echo`
## Metrics you can scrape from promethus
- http_requests_total
- histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m]))
by (le, handler))
- rate(http_request_size_bytes_sum[1m])