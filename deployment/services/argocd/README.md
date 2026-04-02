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
### Install Argocd CLI

sudo curl -sSL -o /usr/local/bin/argocd \
  https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64

sudo chmod +x /usr/local/bin/argocd


### Login and apply deployment

argocd login 192.168.0.217:32400 --username admin --password NEWPASSWORD --insecure

argocd repo add https://github.com/viv-capgemini/house-price-predictor.git
kubectl apply -f deployment/argocd/house-price-predictor-app.yaml -n argocd\n
argocd app get house-price-predictor\n

kubectl -n argocd get svc argocd-server
