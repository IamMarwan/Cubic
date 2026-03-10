from pypdf import PdfReader
from docx import Document
import io

SUPPORTED = {".pdf", ".docx", ".txt"}

def _ext(filename: str) -> str:
    filename = filename.lower().strip()
    for e in SUPPORTED:
        if filename.endswith(e):
            return e
    return ""

def extract_text_from_bytes(filename: str, content: bytes):
    ext = _ext(filename)
    if not ext:
        raise ValueError("Unsupported file type. Use PDF, DOCX or TXT.")

    if ext == ".txt":
        return content.decode("utf-8", errors="replace"), ext

    if ext == ".pdf":
        reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text, ext

    if ext == ".docx":
        doc = Document(io.BytesIO(content))
        text = "\n".join(p.text for p in doc.paragraphs if p.text)
        return text, ext