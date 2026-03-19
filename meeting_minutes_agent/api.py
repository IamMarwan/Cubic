from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import extract_meeting_minutes

app = FastAPI()

class MeetingRequest(BaseModel):
    text: str

@app.post("/extract-minutes")
def extract_minutes(request: MeetingRequest):
    try:
        return extract_meeting_minutes(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))