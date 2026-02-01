from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User query text"
    )


class ErrorResponse(BaseModel):
    status: str
    data: None
    error: dict