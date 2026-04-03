# Model Helm Chart Operations

## Prerequisites

- Kubernetes context is reachable
- Helm 3 installed
- Current directory is repo root

## Install

```bash
helm install model gitops/apps/model \
	--namespace default \
	--kube-context kind-kind
```

## Update (Upgrade)

```bash
helm upgrade model gitops/apps/model \
	--namespace default \
	--kube-context kind-kind
```

## Update With Overrides

```bash
helm upgrade model gitops/apps/model \
	--namespace default \
	--kube-context kind-kind \
	--set image.tag=v1.0.3
```

## Uninstall

```bash
helm uninstall model \
	--namespace default \
	--kube-context kind-kind
```

## Testing

### 1) Render Templates Locally

```bash
helm template model gitops/apps/model
```

### 2) Lint Chart

```bash
helm lint gitops/apps/model
```

### 3) Run Helm Test Hooks

```bash
helm test model \
	--namespace default \
	--kube-context kind-kind
```

### 4) Verify Runtime Resources

```bash
kubectl --context kind-kind get deploy,svc,vpa -n default
kubectl --context kind-kind rollout status deploy/model -n default
```
