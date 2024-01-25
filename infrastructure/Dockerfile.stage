# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

# Copy the current directory contents into the container at /usr/src/app
COPY domore.py .
COPY config.py .
COPY app app


ENV FLASK_APP domore.py

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "domore:app"]
