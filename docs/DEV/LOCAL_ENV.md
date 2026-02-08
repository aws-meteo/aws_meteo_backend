# Developer Guide: Local Environment Setup

This guide provides instructions for running the SbnAI Meteo Backend locally using Docker, ensuring parity with the AWS Lambda production environment.

## Prerequisites
- Docker installed and running.
- (Optional) `curl` for health checks.

## 1. Build the Docker Image
The image uses the AWS Lambda Web Adapter to run standard FastAPI inside the container.

```bash
docker build -t aws-meteo-backend .
```

## 2. Run the Container
Map the internal port 8000 to your local port 8000.

```bash
docker run -p 8000:8000 aws-meteo-backend
```

## 3. Verify Health
Ensure the API is responding correctly.

```bash
curl http://localhost:8000/health
```
Expected response: `{"status":"ok"}` (or similar JSON).

## 4. Connecting the Frontend
In your Frontend configuration (`.env` or similar), set the following:

```env
VITE_API_URL=http://localhost:8000
```

## 5. Development with Devcontainers
Alternatively, use the provided `.devcontainer` configuration in VS Code to open the workspace directly inside the container for a seamless development experience.
