from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class ActionItem(BaseModel):
    title: str
    owner: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = "Medium"
    source_sentence: Optional[str] = None
    confidence: Optional[float] = None


class ExtractionResult(BaseModel):
    meeting_title: Optional[str] = None
    meeting_date: Optional[date] = None
    action_items: List[ActionItem]