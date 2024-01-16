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
EXPOSE 9091 8081 4001

# Define entrypoint
ENTRYPOINT ["firebase", "emulators:start", "--only", "firestore,auth"]
