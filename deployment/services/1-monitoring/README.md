# Monitoring Deployment Code
Monitoring with Prometheus uses a Helm chart so that needs to be installed before hand.

### Installing Helm
To install helm version 3 on Linux or MacOS, you can follow following instructions.
- ``` curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash ```

You could further refer to [Official HELM Install Instructions]() for alternative options.
Verify the installtion is successful,
```
helm --help
helm version
```
### Deploying Prometheus stack with HELM
Deploy Prometheus Stack with HELM
Read about [kube-prometheus-stack 33.1.0 · prometheus/prometheus-community]() chart at
artifacthub.io
Add helm repository using ,
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

## Install the helm chart to setup Prometheus and Grafana
```
helm upgrade --install prometheus   -n monitoring   --create-namespace   prometheus-community/kube-prometheus-stack   -f deployment/services/1-monitoring/values.yml
```
- Prometheus NodePort is `30300`, but in k3d this is not automatically exposed on macOS host.
- Use port-forward to access targets locally:
```
kubectl -n monitoring port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
```
- status of endpoint can be found here - http://localhost:9090/targets
- Grafana NodePort is `30200`, but in k3d this is not automatically exposed on macOS host.
- Use port-forward to access Grafana locally:
```
kubectl -n monitoring port-forward svc/prometheus-grafana 3000:80
```
- Grafana dashboard can be accessed at - http://localhost:3000
- Get password with `kubectl get secret --namespace monitoring -l app.kubernetes.io/component=admin-secret -o jsonpath="{.items[0].data.admin-password}" | base64 --decode ; echo`
## Metrics you can scrape from promethus
- http_requests_total
- histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m]))
by (le, handler))
- rate(http_request_size_bytes_sum[1m])