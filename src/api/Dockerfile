FROM python:3.11-slim
WORKDIR /app
COPY src/api/requirements.txt ./requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev curl \
    && pip install --upgrade pip && pip install -r requirements.txt \
    && apt-get purge -y gcc python3-dev && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
COPY src/api/ ./
COPY models/trained/ ./models/trained/
EXPOSE 8000 9100
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]