# Week 5 – Deployment and Observability

This week completes the Cubic RAG training by deploying the system in a
containerized environment with basic monitoring and metrics.

## Features

- FastAPI-based RAG service
- Dockerized deployment
- Request latency and error tracking
- Token usage reporting
- Metrics endpoint for observability

## Run Locally (Docker)

From the Week_5 directory:

```bash
docker build -t cubic-rag -f docker/Dockerfile .
docker run -p 8000:8000 cubic-rag