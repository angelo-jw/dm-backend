# DoMore
FROM python:slim as domore

ARG COMMIT_HASH

RUN useradd domore

WORKDIR /home/domore

COPY requirements.txt requirements.txt
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY domore.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP domore.py

RUN chown -R domore:domore ./
USER domore

EXPOSE 8000

# Set a label for the commit hash
LABEL commit_hash=$COMMIT_HASH

ENTRYPOINT ["./boot.sh"]

# Firebase
FROM openjdk:11-jre-slim as firebase

# Install Node.js
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Firebase CLI
RUN npm install -g firebase-tools

WORKDIR /home/domore

# Copy Firebase configuration files
COPY .firebaserc .firebaserc
COPY firebase.json firebase.json
COPY firestore.rules firestore.rules
COPY firestore.indexes.json firestore.indexes.json

# Expose the necessary ports
EXPOSE 8080 9099

# Define entrypoint
ENTRYPOINT ["firebase", "emulators:start", "--only", "firestore,auth"]
