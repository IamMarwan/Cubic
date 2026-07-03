from __future__ import annotations
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.database import init_db, get_document
from app.models import WorkflowState
from app.services.analytics import build_summary, reporting_rows
from app.services.document_control import create_document_from_text, get_audit_trail, get_register, transition_document

app = FastAPI(title="AI Document Control Assistant", version="1.0.0")
init_db()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

class TransitionRequest(BaseModel):
    target_state: WorkflowState
    actor: str = "Document Controller"
    comment: str = "Workflow updated from dashboard/API."

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    docs = get_register()
    summary = build_summary(docs)
    return templates.TemplateResponse("dashboard.html", {"request": request, "documents": docs, "summary": summary})

@app.get("/documents", response_class=HTMLResponse)
def documents_page(request: Request):
    docs = get_register()
    return templates.TemplateResponse("documents.html", {"request": request, "documents": docs, "states": [s.value for s in WorkflowState]})

@app.get("/documents/{document_id}", response_class=HTMLResponse)
def document_detail(request: Request, document_id: int):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    audit = get_audit_trail(document_id)
    return templates.TemplateResponse("document_detail.html", {"request": request, "document": doc, "audit": audit, "states": [s.value for s in WorkflowState]})

@app.post("/upload")
async def upload_document(file: UploadFile = File(...), owner: str = Form("Document Controller"), project: str = Form("Cubic Project"), due_date: str = Form(None)):
    raw = await file.read()
    content = raw.decode("utf-8", errors="ignore")
    create_document_from_text(content, file.filename or "uploaded_document.txt", owner, project, due_date or None)
    return RedirectResponse(url="/documents", status_code=303)

@app.post("/documents/{document_id}/transition-form")
def transition_form(document_id: int, target_state: str = Form(...), actor: str = Form("Document Controller"), comment: str = Form("Updated from dashboard.")):
    try:
        transition_document(document_id, WorkflowState(target_state), actor, comment)
    except (ValueError, LookupError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return RedirectResponse(url=f"/documents/{document_id}", status_code=303)

@app.get("/api/documents")
def api_documents():
    return reporting_rows(get_register())

@app.get("/api/documents/{document_id}")
def api_document(document_id: int):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc.to_dict()

@app.post("/api/documents/{document_id}/transition")
def api_transition(document_id: int, payload: TransitionRequest):
    try:
        return transition_document(document_id, payload.target_state, payload.actor, payload.comment).to_dict()
    except (ValueError, LookupError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/api/documents/{document_id}/audit")
def api_audit(document_id: int):
    return [event.to_dict() for event in get_audit_trail(document_id)]

@app.get("/api/analytics/summary")
def api_summary():
    return build_summary(get_register())
