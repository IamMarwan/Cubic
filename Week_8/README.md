# Week_8 - Standalone AI Workflow Agents

This project contains two standalone AI agents:

1. Document Summary Agent
2. Meeting Minutes Agent

## How to run

Activate the virtual environment, then run each agent from its folder.

### Document Summary Agent
python main.py sample_input.txt

API:
python -m uvicorn api:app --port 8000

### Meeting Minutes Agent
python main.py sample_input.txt

API:
python -m uvicorn api:app --port 8001
