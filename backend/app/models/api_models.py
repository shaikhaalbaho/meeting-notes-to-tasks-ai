from pydantic import BaseModel
from app.models.extraction_schema import ExtractionResult


class ExtractRequest(BaseModel):
    meeting_notes: str


class ExtractResponse(BaseModel):
    result: ExtractionResult