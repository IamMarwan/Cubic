from __future__ import annotations

import re
from pathlib import Path

try:
    from docx import Document
except ImportError:  # pragma: no cover
    Document = None

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None


FIELD_PATTERNS = {
    "document_number": r"(?:Document\s*(?:No\.?|Number)|Doc\s*No\.?)\s*[:\-]\s*([A-Z0-9\-_/]+)",
    "revision": r"(?:Revision|Rev\.?)\s*[:\-]\s*([A-Z0-9]+)",
    "approval_status": r"(?:Approval\s*Status|Status)\s*[:\-]\s*([A-Za-z ]+)",
    "date": r"(?:Date|Submission\s*Date|Issue\s*Date)\s*[:\-]\s*([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{2}/[0-9]{2}/[0-9]{4})",
    "prepared_by": r"Prepared\s*By\s*[:\-]\s*([A-Za-z .,&]+)",
    "checked_by": r"Checked\s*By\s*[:\-]\s*([A-Za-z .,&]+)",
    "approved_by": r"Approved\s*By\s*[:\-]\s*([A-Za-z .,&]+)",
    "discipline": r"Discipline\s*[:\-]\s*([A-Za-z ]+)",
    "project_name": r"Project\s*Name\s*[:\-]\s*(.+)",
}


def extract_text(file_path: str | Path) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".txt":
        return path.read_text(encoding="utf-8")

    if suffix == ".docx":
        if Document is None:
            raise RuntimeError("python-docx is required to read DOCX files.")
        doc = Document(path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)

    if suffix == ".pdf":
        if PdfReader is None:
            raise RuntimeError("pypdf is required to read PDF files.")
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    raise ValueError(f"Unsupported file type: {suffix}")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for key, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            metadata[key] = match.group(1).strip()
    return metadata


def detect_document_type(text: str, rules: dict) -> str:
    lowered = text.lower()
    best_type = "unknown"
    best_score = 0

    for document_type, rule_config in rules.get("document_types", {}).items():
        keywords = rule_config.get("keywords", [])
        score = sum(1 for keyword in keywords if keyword.lower() in lowered)
        if score > best_score:
            best_score = score
            best_type = document_type

    return best_type
