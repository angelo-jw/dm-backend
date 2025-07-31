FROM python:3.9-slim

WORKDIR /app

# Install system dependencies, including netcat-openbsd for the healthcheck
RUN apt-get update && \
    apt-get install -y gcc python3-dev netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN pip install gunicorn pymysql cryptography

COPY domore.py .
COPY config.py .
COPY app app

EXPOSE 5000

# The CMD is now handled in the docker-compose.yml to include the healthcheck