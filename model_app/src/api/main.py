from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from inference import predict_price, batch_predict
from schemas import HousePredictionRequest, PredictionResponse
from prometheus_fastapi_instrumentator import Instrumentator  # type: ignore # For Prometheus monitoring
from prometheus_client import start_http_server
import threading
from fastapi.responses import JSONResponse
import time
import socket
import os
import psutil
import prometheus_client  # type: ignore
from typing import Dict

# Initialize FastAPI app with metadata
app = FastAPI(
    title="House Price Prediction API",
    description=(
        "An API for predicting house prices based on various features. "
        "This application is part of the MLOps project demonstration. "
        "Edited by Vivienne Ansah."
    ),
    version="1.0.2",
    contact={
        "name": "Vivienne Ansah",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
start_time = time.time()


# Start Prometheus metrics server on port 9100 in a background thread
def start_metrics_server():
    start_http_server(9100)


# Start the metrics server in a separate thread
metrics_thread = threading.Thread(target=start_metrics_server)
metrics_thread.daemon = True
metrics_thread.start()

# Example: model metadata (replace with your actual model loader)
MODEL_NAME = "house-price-model"
MODEL_VERSION = "v12"
MODEL_LOADED = True
MODEL_INFERENCE_TIME_MS = 14  # example static value


# Example dependency checks
def check_redis():
    try:
        # ping redis here
        return {"status": "ok", "latency_ms": 1}
    except Exception:
        return {"status": "down"}


def check_postgres():
    try:
        # run a lightweight SELECT 1
        return {"status": "ok", "latency_ms": 12}
    except Exception:
        return {"status": "down"}


def get_prom_metric(metric_name: str):
    try:
        metric = prometheus_client.REGISTRY.get_sample_value(metric_name)
        return metric
    except Exception:
        return None


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize and instrument Prometheus metrics
Instrumentator().instrument(app).expose(app)


# Health check endpoint
@app.get("/health")
async def health() -> JSONResponse:
    uptime = time.time() - start_time

    # Kubernetes metadata
    k8s_info = {
        "pod_name": os.getenv("HOSTNAME"),
        "namespace": os.getenv("POD_NAMESPACE"),
        "node_name": os.getenv("NODE_NAME"),
        "pod_ip": socket.gethostbyname(socket.gethostname()),
        "restart_count": os.getenv("RESTART_COUNT"),
    }

    # System metrics
    process = psutil.Process(os.getpid())
    system_info = {
        "cpu_usage_percent": psutil.cpu_percent(interval=0.1),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "open_file_descriptors": process.num_fds()
        if hasattr(process, "num_fds")
        else None,
        "thread_count": process.num_threads(),
    }

    # Autoscaling-friendly metrics
    autoscaling_metrics = {
        "request_rate_1m": get_prom_metric("http_requests_total"),
        "latency_p95_ms": get_prom_metric("http_request_duration_seconds_bucket"),
        "inflight_requests": get_prom_metric("inflight_requests"),
    }

    # Model diagnostics
    model_info = {
        "name": MODEL_NAME,
        "version": MODEL_VERSION,
        "loaded": MODEL_LOADED,
        "inference_time_ms": MODEL_INFERENCE_TIME_MS,
        "drift_score": get_prom_metric("model_drift_score"),
    }

    # Dependencies
    dependencies = {
        "postgres": check_postgres(),
        "redis": check_redis(),
    }

    response = {
        "status": "healthy",
        "uptime_seconds": uptime,
        "version": os.getenv("APP_VERSION", "unknown"),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "kubernetes": k8s_info,
        "system": system_info,
        "metrics": autoscaling_metrics,
        "model": model_info,
        "dependencies": dependencies,
    }

    return JSONResponse(content=response)


# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: HousePredictionRequest):
    return predict_price(request)


# Batch prediction endpoint
@app.post("/batch-predict", response_model=list)
async def batch_predict_endpoint(requests: list[HousePredictionRequest]):
    return batch_predict(requests)
