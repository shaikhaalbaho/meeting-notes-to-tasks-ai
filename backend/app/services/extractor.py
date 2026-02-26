from app.models.extraction_schema import ExtractionResult
from app.services.llm_client import LLMClient
from app.services.prompts import EXTRACTION_SYSTEM_PROMPT, build_extraction_user_prompt
from app.utils.llm_json import parse_and_validate_extraction, LLMJSONError


class ExtractionServiceError(Exception):
    pass


class ExtractionService:
    def __init__(self) -> None:
        self.llm = LLMClient()

    def extract_action_items(self, meeting_notes: str) -> ExtractionResult:
        if not meeting_notes or not meeting_notes.strip():
            # Return empty valid object
            return ExtractionResult(meeting_title=None, meeting_date=None, action_items=[])

        system_prompt = EXTRACTION_SYSTEM_PROMPT
        user_prompt = build_extraction_user_prompt(meeting_notes)

        raw = self.llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)

        try:
            return parse_and_validate_extraction(raw)
        except LLMJSONError as e:
            raise ExtractionServiceError(f"LLM output invalid: {e}") from e