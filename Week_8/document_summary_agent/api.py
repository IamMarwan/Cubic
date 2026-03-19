from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import summarize_document

app = FastAPI(title="Document Summary Agent API")


class DocumentRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "Document Summary Agent API is running."}


@app.post("/summarize")
def summarize(request: DocumentRequest):
    try:
        result = summarize_document(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))