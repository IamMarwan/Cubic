# Technical Documentation - AI Document Control Assistant

## Purpose
The system supports engineering document control by managing documents from intake through review, approval, issue, and archive.

## Features delivered
- Unified dashboard with document KPIs.
- Document register and detail page.
- AI-assisted metadata extraction and classification.
- Controlled workflow state transitions.
- Audit trail for lifecycle events.
- Analytics API for reporting.
- Seed data, tests, Dockerfile, Makefile, demo script, architecture diagram, and presentation.

## API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Dashboard. |
| GET | `/documents` | Document register. |
| GET | `/documents/{id}` | Document detail page. |
| GET | `/api/documents` | JSON document register. |
| GET | `/api/documents/{id}` | JSON document detail. |
| POST | `/api/documents/{id}/transition` | Apply workflow transition. |
| GET | `/api/documents/{id}/audit` | Document audit trail. |
| GET | `/api/analytics/summary` | Analytics summary. |

## Run commands
```bash
pip install -r requirements.txt
python scripts/seed_demo.py
uvicorn app.main:app --reload
pytest -q
python scripts/evaluate_ai.py
```

## Production roadmap
- Add authentication and role-based approvals.
- Add OCR and PDF/DOCX parsing.
- Add PostgreSQL and object storage.
- Add email notifications and overdue escalations.
- Add reviewer feedback loops for continuous model evaluation.
