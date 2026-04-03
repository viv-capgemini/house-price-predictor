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


### Expose Argocd on Nodeport to access outside cluster but on same network

kubectl create -f deployment/services/3-argocd/argocd-server-nodeport.yaml
### Endpoints
Argo CD UI (HTTP): http://localhost:30200
Argo CD UI (HTTPS): https://localhost:32443
Username: admin
Password: NEWPASSWORD

### Application Auto scaling
kubectl apply --server-side -f https://github.com/kedacore/keda/releases/download/v2.19.0/keda-2.19.0-core.yaml

### Install Argocd CLI
sudo curl -sSL -o /usr/local/bin/argocd \
  https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64

sudo chmod +x /usr/local/bin/argocd


### Login to argocd via cli
argocd login localhost:8080 --username admin --password NEWPASSWORD --insecure

### Add repo
argocd repo add https://github.com/viv-capgemini/house-price-predictor.git

### Create argocd applications
kubectl apply -f gitops/argocd/model-app.yaml -n argocd
kubectl apply -f gitops/argocd/streamlit-app.yaml -n argocd
argocd app get model

kubectl -n argocd get svc argocd-server
