# Week 10 - AI Document Classification & Metadata Extraction

## Goal
Build an AI-powered Document Control Assistant for construction project documentation. The system accepts PDF and DOCX files, classifies the document type, extracts key metadata, and returns a confidence score.

## Supported document categories
- Drawing
- Specification
- Method Statement
- Material Submittal
- Shop Drawing
- Inspection Report
- Contract
- Meeting Minutes
- RFI

## Extracted metadata
- Document Title
- Revision Number
- Project Name
- Contractor
- Consultant
- Submission Date
- Discipline

## Deliverables included
- Working document upload API using FastAPI.
- Classification engine using construction document keyword scoring.
- Metadata extraction engine using field labels and fallback pattern matching.
- Test dataset generator that creates at least 50 sample DOCX files.
- Demo script showing successful classification and metadata extraction.
- Unit tests for the core engine.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Generate the 50-document test dataset
```bash
python scripts/generate_sample_dataset.py
```

Output:
```text
generated_dataset/
├── docx/
└── dataset_index.csv
```

## Run the API
```bash
uvicorn app.main:app --reload
```

Then open:
```text
http://127.0.0.1:8000/docs
```

Upload a PDF or DOCX file through the `/upload` endpoint.

## Run the demo
```bash
python scripts/run_demo.py
```

The demo generates the dataset if needed, processes the sample files, and prints classification + metadata results.

## API response example
```json
{
  "filename": "DOC-001_Drawing.docx",
  "document_type": "Drawing",
  "confidence_score": 0.93,
  "metadata": {
    "document_title": "Ground Floor Structural Drawing",
    "revision_number": "Rev. A",
    "project_name": "Cubic Tower Development",
    "contractor": "BuildRight Contracting LLC",
    "consultant": "Cubic Engineering Consultancy",
    "submission_date": "2026-06-07",
    "discipline": "Structural"
  }
}
```

## Notes
This is a practical baseline implementation. It can later be upgraded with OCR, database storage, LLM extraction, vector search, and a web dashboard.
