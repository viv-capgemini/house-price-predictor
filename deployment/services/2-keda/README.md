# Load Testing

### Auto Scaling Models with KEDA
```
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda \
--namespace keda \
--create-namespace
```
Check installation of KEDA
`kubectl get all -n keda`
### Instal VPA
```
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler/
./hack/vpa-up.sh
```
### Add Resource Spec to the Model Pod Deployment Manifest file
# Apply the ScaledObject Manifest
`kubectl create -f deployment/services/1-keda/fastapi-scaledobject.yaml`
```
kubectl get scaledobject
kubectl get hpa # KEDA will create a linked HPA here
kubectl get scaledobject,hpa,pods -n keda
```
### Validate and Monitor
Watch KEDA logs: `kubectl logs -n keda deploy/keda-operator`
See autoscaling in action via `kubectl get pods`
### Run a Load Test
**
Install ~[hey]()~ – Minimal HTTP load generator
Installation**
```sudo snap install hey```

Create a json file to send data for predictions
File : `predict.json`
```
{
    "sqft": 4500,
    "bedrooms": 4,
    "bathrooms": 2,
    "year_built": 2014,
    "condition": "Good",
    "location": "Urban"
}

### Load Test with Hey
- installation of hey on mack ```brew install hey```
- Make a prediction
```
curl -X POST http://localhost:30100/predict \
-H "Content-Type: application/json" \
-d @deployment/charts/monitoring/predict.json
```
- Results
```
{"predicted_price":837567.34,"confidence_interval":[753810.61,921324.07],"features_importance":{},"prediction_time":"2026-03-24T14:39:03.064992"}%
```
- Run a longer load test making 5000 request
```
hey -n 5000 -c 200 -m POST \
-H "Content-Type: application/json" \
-D deployment/monitoring/predict.json \
http://localhost:30100/predict
```
- Sample output
```
Summary:
  Total:        71.9109 secs
  Slowest:      3.8930 secs
  Fastest:      0.0041 secs
  Average:      2.3584 secs
  Requests/sec: 69.5305
  
  Total data:   725000 bytes
  Size/request: 145 bytes

Response time histogram:
  0.004 [1]     |
  0.393 [23]    |■
  0.782 [15]    |
  1.171 [31]    |■
  1.560 [40]    |■
  1.949 [759]   |■■■■■■■■■■■■■■■■■
  2.337 [1830]  |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  2.726 [1385]  |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  3.115 [573]   |■■■■■■■■■■■■■
  3.504 [188]   |■■■■
  3.893 [155]   |■■■


Latency distribution:
  10%% in 1.8926 secs
  25%% in 2.0023 secs
  50%% in 2.2063 secs
  75%% in 2.6976 secs
  90%% in 2.9971 secs
  95%% in 3.4014 secs
  99%% in 3.7027 secs

Details (average, fastest, slowest):
  DNS+dialup:   0.0005 secs, 0.0000 secs, 0.0178 secs
  DNS-lookup:   0.0002 secs, 0.0000 secs, 0.0059 secs
  req write:    0.0000 secs, 0.0000 secs, 0.0155 secs
  resp wait:    2.3569 secs, 0.0040 secs, 3.8929 secs
  resp read:    0.0008 secs, 0.0000 secs, 0.0946 secs

Status code distribution:
  [200] 5000 responses
```
- Run a load test with an interval of 3 minitues
```
hey -z 3m -c 200 -m POST \
-H "Content-Type: application/json" \
-D deployment/charts/monitoring/predict.json \
http://localhost:30100/predict
```
- Sample Output
```
Summary:
  Total:        184.5604 secs
  Slowest:      4.7011 secs
  Fastest:      0.0994 secs
  Average:      2.4146 secs
  Requests/sec: 81.5235
  
  Total data:   2181670 bytes
  Size/request: 145 bytes

Response time histogram:
  0.099 [1]     |
  0.560 [16]    |
  1.020 [39]    |
  1.480 [39]    |
  1.940 [91]    |
  2.400 [7366]  |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  2.860 [6680]  |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  3.321 [705]   |■■■■
  3.781 [86]    |
  4.241 [7]     |
  4.701 [16]    |


Latency distribution:
  10%% in 2.1033 secs
  25%% in 2.2967 secs
  50%% in 2.4001 secs
  75%% in 2.5052 secs
  90%% in 2.7023 secs
  95%% in 2.8960 secs
  99%% in 3.2926 secs

Details (average, fastest, slowest):
  DNS+dialup:   0.0003 secs, 0.0000 secs, 0.0478 secs
  DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0047 secs
  req write:    0.0000 secs, 0.0000 secs, 0.0041 secs
  resp wait:    2.4135 secs, 0.0714 secs, 4.7010 secs
  resp read:    0.0007 secs, 0.0000 secs, 0.1367 secs

Status code distribution:
  [200] 15046 responses
```