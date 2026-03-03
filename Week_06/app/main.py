import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.document_loader import load_document
from app.website_loader import load_website
from app.chunking import chunk_text
from app.vector_store import add_chunks
from app.rag_pipeline import ask_question
from app.schemas import QuestionRequest, WebsiteRequest
from app.config import UPLOAD_FOLDER
from app.logger import logger

app = FastAPI(title="AI Knowledge Platform")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_document(
    project_name: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        text = load_document(file_path)
        chunks = chunk_text(text)
        add_chunks(project_name, chunks, file.filename)

        logger.info(f"Document uploaded: {file.filename} | Project: {project_name}")

        return {"message": f"Document indexed under project '{project_name}'"}

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-website")
def upload_website(request: WebsiteRequest):
    try:
        text = load_website(request.url)
        chunks = chunk_text(text)
        add_chunks(request.project_name, chunks, request.url)

        logger.info(f"Website indexed: {request.url} | Project: {request.project_name}")

        return {"message": f"Website indexed under project '{request.project_name}'"}

    except Exception as e:
        logger.error(f"Website upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query_knowledge(request: QuestionRequest):
    try:
        response = ask_question(request.project_name, request.question)
        logger.info(f"Query executed | Project: {request.project_name}")
        return JSONResponse(content=response)

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {
        "status": "running",
        "service": "AI Knowledge Platform"
    }