### Install Argo CD
```
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace argocd
helm install argocd argo/argo-cd -n argocd
```
### Change password

kubectl patch secret argocd-secret -n argocd \
  --type merge \
  -p '{
    "stringData": {
      "admin.password": "$2a$10$Tfx0hRScLkmTIrV/Du0qwO/Iac.8hCAmS1ZNq2DGFCCEZLgbsIrTS%",
      "admin.passwordMtime": "'$(date +%FT%T%Z)'"
    }
  }'
### reset deployment

kubectl rollout restart deployment argocd-server -n argocd


### Endpoint

kubectl apply -f deployment/argocd/argocd-server-nodeport.yaml

Argo CD UI (HTTP): http://localhost:32080
Argo CD UI (HTTPS): https://localhost:32443

### Auto scaling

kubectl apply --server-side -f https://github.com/kedacore/keda/releases/download/v2.19.0/keda-2.19.0-core.yaml
### Remove ARGOCD

kubectl delete -n argocd -f kubectl apply -k https://github.com/argoproj/argo-cd/manifests/crds\?ref\=stableyaml --ignore-not-found=true && kubectl delete namespace argocd --ignore-not-found=true

###

argocd repo add https://github.com/viv-capgemini/house-price-predictor.git
kubectl apply -f deployment/argocd/house-price-predictor-app.yaml -n argocd\n
argocd app get house-price-predictor\n