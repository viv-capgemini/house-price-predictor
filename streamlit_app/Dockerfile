FROM python:3.10.20-slim-trixie
WORKDIR /app
COPY app.py requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8501 
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]