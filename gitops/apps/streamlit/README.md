# Streamlit Helm Chart Operations

## Prerequisites

- Kubernetes context is reachable
- Helm 3 installed
- Current directory is repo root

## Install

```bash
helm install streamlit gitops/apps/streamlit \
  --namespace default \
  --kube-context kind-kind
```

## Update (Upgrade)

```bash
helm upgrade streamlit gitops/apps/streamlit \
  --namespace default \
  --kube-context kind-kind
```

## Update With Overrides

```bash
helm upgrade streamlit gitops/apps/streamlit \
  --namespace default \
  --kube-context kind-kind \
  --set image.tag=v1.0.2
```

## Uninstall

```bash
helm uninstall streamlit \
  --namespace default \
  --kube-context kind-kind
```

## Testing

### 1) Render Templates Locally

```bash
helm template streamlit gitops/apps/streamlit
```

### 2) Lint Chart

```bash
helm lint gitops/apps/streamlit
```

### 3) Run Helm Test Hooks

```bash
helm test streamlit \
  --namespace default \
  --kube-context kind-kind
```

### 4) Verify Runtime Resources

```bash
kubectl --context kind-kind get deploy,svc,servicemonitor -n default
kubectl --context kind-kind rollout status deploy/streamlit -n default
```
