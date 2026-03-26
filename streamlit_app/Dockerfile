FROM python:3.11-slim
WORKDIR /app
COPY app.py requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev curl \
    && pip install --upgrade pip && pip install -r requirements.txt \
    && apt-get purge -y gcc python3-dev && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
EXPOSE 8501 8502
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD ["python", "-c", "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8502/healthz', timeout=3).status == 200 else 1)"]
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]