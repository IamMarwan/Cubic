from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.extractor import extract_structured_from_upload

router = APIRouter()

@router.post("/extract")
async def extract(file: UploadFile = File(...)):
    try:
        result = await extract_structured_from_upload(file)
        return result.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {e}")