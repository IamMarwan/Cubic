from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.database import reset_db
from app.models import WorkflowState
from app.services.document_control import create_document_from_text, transition_document

reset_db()
sample_dir = ROOT / "sample_documents"
docs = []
for path in sample_dir.glob("*.txt"):
    docs.append(create_document_from_text(path.read_text(), path.name, "Document Controller", "Cubic Demo Project"))
transition_document(docs[0].id, WorkflowState.IN_REVIEW, "Lead Engineer", "Submitted for interdisciplinary review.")
transition_document(docs[0].id, WorkflowState.APPROVED, "Project Manager", "Approved for issue.")
transition_document(docs[0].id, WorkflowState.ISSUED, "Document Controller", "Issued to project team.")
transition_document(docs[1].id, WorkflowState.IN_REVIEW, "Electrical Engineer", "Submitted for review.")
print(f"Seeded {len(docs)} demo documents into {ROOT / 'document_control.db'}")
