# Project Do-More: Flask and Firebase Application

## Introduction
This is the server side of the DoMore App, a Flask web application integrated with Firebase for Firestore and authentication. It's deployed in a Docker image to GCloud Run.

## Prerequisites
To work on this project, ensure you have the following installed:
- **Python 3.11**: The core language used for the project.
- **Docker**: For running Firebase emulators.
- **Make**: To use the provided Makefile commands for Docker operations.

## Setup

### Virtual Environment and Dependencies
1. **Create a Virtual Environment**: Set up a virtual environment in your project directory:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
2. **Install Requirements**: Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment File
- **Obtaining the `.env` File**: Request the environment file from your team, which contains necessary configuration variables.

### Firestore Emulator and Authentication
To set up the Firestore emulator and authentication:
1. **Install the gcloud CLI**: Install and initialize the gcloud CLI, selecting a Google Cloud project with the required access.
2. **Create Credential File**:
   - Execute `gcloud auth application-default login`. After signing in, place the generated `application_default_credentials.json` in the project root.

### Docker and Firebase Emulators Using Makefile
- **Building the Docker Image**: Run `make build` to build the Docker image.
- **Running the Container**: Use `make run` to start the container.
- **Stopping the Container**: Execute `make stop` to stop the running container.
- **Restarting the Container**: Use `make restart` to restart the container.

### Running Tests
- Ensure the Firebase emulator is running (use `make run`).
- Run tests using the Pytest framework:
  ```bash
  pytest
  ```

### Access to the Do-More App
- You must have access to the Do-More application on the GCloud project. Contact your team for permissions.

## Running the Application
After completing the setup, run the Flask application using the Flask command:
```bash
flask run
```
Access the application through the provided localhost URL.
