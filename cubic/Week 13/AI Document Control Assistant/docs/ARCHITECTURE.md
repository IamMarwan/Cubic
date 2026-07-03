# Architecture Documentation - AI Document Control Assistant Platform

## Platform overview
The Week 13 platform consolidates the previously developed document intake, metadata extraction, AI classification, workflow tracking, audit logging, analytics, and reporting modules into one FastAPI application.

## Main modules
| Layer | Component | Responsibility |
|---|---|---|
| Presentation | Web dashboard | Shows KPIs, document register, detail view, and workflow actions. |
| API | FastAPI routes | Provides document, workflow, audit, and analytics endpoints. |
| AI services | Metadata and classification engine | Extracts title, document number, revision, discipline, type, confidence, and risk. |
| Control services | Workflow engine | Enforces controlled state transitions and records lifecycle history. |
| Reporting services | Analytics engine | Produces status, discipline, type, risk, confidence, and overdue metrics. |
| Data | SQLite database | Stores documents and audit events for the demonstration. |

## Workflow lifecycle
Draft -> In Review -> Approved -> Issued -> Archived. Rejection routes allow In Review -> Rejected -> Draft for correction and resubmission.

## Integration approach
The platform uses service modules that can be replaced later with enterprise components. SQLite can be replaced with PostgreSQL, rule-based AI services can be replaced with OCR/LLM pipelines, and the dashboard can be integrated with SSO and role-based approval workflows.

## Architecture diagram
See `architecture_diagram.png` in this folder.
