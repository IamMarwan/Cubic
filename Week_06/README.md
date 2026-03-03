# Week 06 – AI Knowledge Platform

Standalone production-ready AI Knowledge Assistant.

## Features

- Project-based knowledge separation
- Document upload (PDF, DOCX, TXT)
- Website ingestion
- Automatic chunking & indexing
- Persistent vector storage
- Structured citations with similarity score
- Logging
- Health monitoring endpoint
- Docker-ready

## Run Locally

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Set environment variable:
$env:OPENAI_API_KEY="your_key_here"

Run:
uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/docs

## Docker

docker build -t knowledge-platform .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key knowledge-platform