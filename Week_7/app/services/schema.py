from pydantic import BaseModel
from typing import List, Optional

class ImportantDate(BaseModel):
    raw: str
    iso: Optional[str] = None
    context: Optional[str] = None

class Clause(BaseModel):
    type: str
    snippet: str
    notes: Optional[str] = None

class ExtractionResult(BaseModel):
    project_name: Optional[str] = None
    organization_names: List[str] = []
    important_dates: List[ImportantDate] = []
    responsibilities: List[str] = []
    financial_or_contractual_clauses: List[Clause] = []

    # Make these optional (system metadata)
    source_filename: Optional[str] = None
    source_type: Optional[str] = None