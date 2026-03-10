from fastapi import FastAPI
from app.routes.extract import router as extract_router

app = FastAPI(
    title="Week07 Document Intelligence Service",
    version="0.1.0"
)

app.include_router(extract_router)