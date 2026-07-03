# AI Document Control Assistant - Week 13

A unified AI-powered document control platform for managing engineering and project documents through their full lifecycle: ingestion, metadata extraction, classification, workflow routing, approval control, version tracking, search, analytics, and reporting.

## Key features

- Document register with upload and metadata extraction
- AI-assisted document classification and risk scoring
- Workflow states: Draft, In Review, Approved, Issued, Rejected, Archived
- Version control and audit trail
- Dashboard with document KPIs, status distribution, discipline distribution, and overdue review alerts
- REST API for integrations
- End-to-end demo data and automated tests
- Architecture documentation, technical documentation, accuracy/performance report, and demo presentation

## Project structure

```text
app/
  main.py                  FastAPI web app and dashboard routes
  models.py                Domain models and workflow rules
  database.py              SQLite persistence layer
  services/
    ai_engine.py           AI-assisted metadata/classification/risk logic
    document_control.py    Document lifecycle orchestration
    analytics.py           KPI and reporting logic
  templates/               Dashboard HTML templates
  static/                  UI styling
sample_documents/          Demo document files
scripts/
  seed_demo.py             Creates an end-to-end demo dataset
  evaluate_ai.py           Generates accuracy/performance report data
tests/                     Unit and workflow tests
docs/                      Architecture and technical documentation
reports/                   Accuracy/performance report
presentation/              Demo presentation
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed_demo.py
uvicorn app.main:app --reload
```

Open the dashboard at: `http://127.0.0.1:8000`

## Run tests

```bash
pytest -q
```

## Run evaluation report

```bash
python scripts/evaluate_ai.py
```

## API examples

```bash
curl http://127.0.0.1:8000/api/documents
curl http://127.0.0.1:8000/api/analytics/summary
curl -X POST http://127.0.0.1:8000/api/documents/1/transition \
  -H "Content-Type: application/json" \
  -d '{"target_state":"In Review","actor":"Document Controller","comment":"Submitted for review"}'
```

## Demo flow

1. Seed demo data.
2. Open the dashboard.
3. Review status and discipline analytics.
4. Open the document register.
5. Move a draft document to review.
6. Approve and issue a document.
7. Confirm the audit trail and updated dashboard analytics.
