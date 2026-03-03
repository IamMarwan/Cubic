from pydantic import BaseModel


class QuestionRequest(BaseModel):
    project_name: str
    question: str


class WebsiteRequest(BaseModel):
    project_name: str
    url: str