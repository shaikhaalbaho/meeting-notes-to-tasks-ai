from fastapi import APIRouter, HTTPException

from app.models.api_models import ExtractRequest, ExtractResponse
from app.services.extractor import ExtractionService, ExtractionServiceError

router = APIRouter(prefix="/extract", tags=["Extraction"])


@router.post("", response_model=ExtractResponse)
def extract_action_items(payload: ExtractRequest):
    service = ExtractionService()

    try:
        result = service.extract_action_items(payload.meeting_notes)
        return ExtractResponse(result=result)
    except ExtractionServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")