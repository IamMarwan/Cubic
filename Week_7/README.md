\# Week 07 — AI Document Intelligence Service



\## Overview

Standalone AI-powered service that extracts structured information from uploaded business documents.



\## Features

\- Upload PDF, DOCX, or TXT documents

\- Extract structured fields:

&nbsp; - Project Name

&nbsp; - Organization Names

&nbsp; - Important Dates

&nbsp; - Responsibilities

&nbsp; - Financial / Contractual Clauses

\- Enforced JSON schema using structured outputs

\- API + CLI workflow

\- Repeatable extraction results



\## Architecture

\- FastAPI backend

\- OpenAI structured JSON extraction

\- Pydantic schema validation

\- Multi-format document ingestion



\## Run API	
uvicorn app.main:app --reload
Access: http://127.0.0.1:8000/docs

## CLI Usage
python scripts\\extract\_cli.py <input\_file> --out <output\_file>



\## Example Outputs

See `outputs/` folder.



\## Objective

Simulates intelligent document understanding service for future integration.

