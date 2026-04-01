# 🏠 House Price Predictor – An MLOps Learning Project

Welcome to the **House Price Predictor** project! This is a real-world, end-to-end MLOps use case designed to help you master the art of building and operationalizing machine learning pipelines.

You'll start from raw data and move through data preprocessing, feature engineering, experimentation, model tracking with MLflow, and optionally using Jupyter for exploration – all while applying industry-grade tooling.

> 🚀 **Want to master MLOps from scratch?**  
Check out the [MLOps Bootcamp at School of DevOps](https://schoolofdevops.com) to level up your skills.

---

## 📦 Project Structure

```
house-price-predictor/
├── configs/                     # YAML-based configuration for models
├── data/                        # Raw and processed datasets
├── deployment/
|   ├── kubernetes/              # Kubernetes manifest files
|   ├── mlflow/                  # Docker Compose setup for MLflow 
│   └── charts/
|        ├── prometheus
|        ├── house-price-model
|        ├──
|         
├── models/                      # Trained models and preprocessors
├── notebooks/                   # Optional Jupyter notebooks for experimentation
├── src/
│   ├── data/                    # Data cleaning and preprocessing scripts
│   ├── features/                # Feature engineering pipeline
│   ├── models/                  # Model training and evaluation
├── requirements.txt             # Python dependencies
└── README.md                    # You’re here!
```
---

## 🛠️ Setting up Learning/Development Environment

To begin, ensure the following tools are installed on your system:

- [Python 3.11](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Visual Studio Code](https://code.visualstudio.com/) or your preferred editor
- [UV – Python package and environment manager](https://github.com/astral-sh/uv)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 

---

## 🚀 Preparing Your Environment

**Build a KIND cluster:**
  ```
  git clone https://github.com/initcron/k8s-code.git
  cd k8s-code/helper/kind/
  kind create cluster --config kind-three-node-cluster.yaml
  kubectl cluster-info --context kind-kind
  kubectl get nodes
  ```

1. **Fork this repo** on GitHub.

2. **Clone your forked copy:**

   ```bash
   git clone git@gitlab.com:machine-learning2861113/house-price-model.git
   cd house-price-model
   ```

3. **Setup Python Virtual Environment using UV:**
  - Install on Ubuntu curl -LsSf https://astral.sh/uv/install.sh | sh
  - uv --version

   ```bash
   uv venv --python python3.11
   source .venv/bin/activate
   ```

4. **Install dependencies:**

   ```bash
   uv pip install -r requirements.txt
   ```
---

## 📊 Setup MLflow for Experiment Tracking

To track experiments and model runs:

```bash
cd deployment/mlflow
docker-compose up -d
docker-compose ps
```

Access the MLflow UI at [http://localhost:5555](http://localhost:5555)

---

## 📒 Using JupyterLab (Optional)

If you prefer an interactive experience, launch JupyterLab with:

```bash
uv python -m jupyterlab
# or
python -m jupyterlab
```

---

## 🔁 Model Workflow

### 🧹 Step 1: Data Processing

Clean and preprocess the raw housing dataset:

```bash
python src/data/run_processing.py   --input data/raw/house_data.csv   --output data/processed/cleaned_house_data.csv
```

---

### 🧠 Step 2: Feature Engineering

Apply transformations and generate features:

```bash
python src/features/engineer.py   --input data/processed/cleaned_house_data.csv   --output data/processed/featured_house_data.csv   --preprocessor models/trained/preprocessor.pkl
```

---

### 📈 Step 3: Modeling & Experimentation

Train your model and log everything to MLflow:

```bash
python src/models/train_model.py   --config configs/model_config.yaml   --data data/processed/featured_house_data.csv   --models-dir models/trained   --mlflow-tracking-uri http://localhost:5555

python src/models/train_model.py \
  --config configs/model_config.yaml \
  --data data/processed/featured_house_data.csv \
  --models-dir models \
  --mlflow-tracking-uri http://localhost:5555
```

---

## Building FastAPI and Streamlit 

The code for both the apps are available in `src/api` and `streamlit_app` already. To build and launch these apps 

Set API_URL=http://localhost:8000` in the streamlit app's environment. 


Once you have launched both the apps, you should be able to access streamlit web ui and make predictions. 

You could also test predictions with FastAPI directly using 

```
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "sqft": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "location": "suburban",
  "year_built": 2000,
  "condition": fair
}'

```

Be sure to replace `http://localhost:8000/predict` with actual endpoint based on where its running. 


## 🧠 Learn More About MLOps

In this project you'll learn how to:

- Build and track ML pipelines
- Containerize and deploy models
- Automate training workflows using GitHub Actions or Argo Workflows
- Apply DevOps principles to Machine Learning systems
## 🧠 Application Endpoints
Helm deployment location
API endpoint in kubernates http://localhost:30100/docs#/
Streamlit endpoint http://localhost:30000/

## Kubernates Auto scalers with KEDA
- Installing KEDA via HELM 
```
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda \
 --namespace keda \
 --create-namespace
```
- Validate - `kubectl get all -n keda`
- keda

## Load Test with Hey
- installation of hey on mac ```brew install hey```
- Install on Linux 
``` sudo apt install snap && sudo snap install hey```
- Make a prediction
```
curl -X POST http://localhost:30100/predict \
-H "Content-Type: application/json" \
-d @deployment/monitoring/predict.json
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
-D deployment/monitoring/predict.json \
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

```

Summary:
  Total:	43.0401 secs
  Slowest:	8.4493 secs
  Fastest:	0.0469 secs
  Average:	1.3998 secs
  Requests/sec:	116.1706

  Total data:	720000 bytes
  Size/request:	144 bytes

Response time histogram:
  0.047 [1]	|
  0.887 [2488]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  1.727 [1569]	|■■■■■■■■■■■■■■■■■■■■■■■■■
  2.568 [143]	|■■
  3.408 [250]	|■■■■
  4.248 [209]	|■■■
  5.088 [95]	|■■
  5.929 [50]	|■
  6.769 [39]	|■
  7.609 [39]	|■
  8.449 [117]	|■■


Latency distribution:
  10% in 0.2329 secs
  25% in 0.6290 secs
  50% in 0.8890 secs
  75% in 1.1069 secs
  90% in 3.6800 secs
  95% in 5.0618 secs
  99% in 8.2212 secs

Details (average, fastest, slowest):
  DNS+dialup:	0.0022 secs, 0.0469 secs, 8.4493 secs
  DNS-lookup:	0.0018 secs, 0.0000 secs, 0.1107 secs
  req write:	0.0001 secs, 0.0000 secs, 0.0214 secs
  resp wait:	1.3572 secs, 0.0060 secs, 8.4076 secs
  resp read:	0.0392 secs, 0.0000 secs, 0.0814 secs
  ```