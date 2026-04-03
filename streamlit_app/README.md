# streamlit_app
Streamlit is an open-source Python framework for data scientists and AI/ML engineers to deliver dynamic data apps with only a few lines of code.
- https://docs.streamlit.io/

## Getting started
This repo is a wrapper for house price model.
This application is exposed on port 8501 
Health check endpoint is exposed on port 8502 at /healthz (also /health).

## Use the docker compose file to run application locally 

- You can visit house-price-model api on localhost:8008/docs
- Yo have access the streamlit app on localhost:8501
- You can verify streamlit health at http://localhost:8502/healthz

## Purpose of Streamlit

- 🖥️ 1. A user‑friendly interface for predictions
        Your model API (FastAPI + XGBoost) is a backend service.
        It exposes /predict, but that’s not something a normal user wants to call manually.

- 🔗 2. A bridge between humans and the model API
    Streamlit communicates with your model service inside Kubernetes:

    - Streamlit sends user inputs → model API
    - Model API returns predictions → Streamlit displays them

    It’s the glue between the user and the backend model.

- 📊 3. A live dashboard for monitoring and debugging
    You’ve instrumented Streamlit with a /metrics endpoint.

- 🧪 4. A safe environment to test new model versions
    Because Streamlit is deployed via Helm and GitOps.

Streamlit gives you a simple, Python‑native UI layer that fits seamlessly into this ecosystem.

No React.
No HTML.
No frontend engineering.
Just Python.

It keeps your entire stack consistent and easy to maintain.