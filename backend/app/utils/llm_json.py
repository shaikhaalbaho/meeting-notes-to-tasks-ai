import json
import re
from typing import Tuple, Optional
from app.models.extraction_schema import ExtractionResult


class LLMJSONError(Exception):
    """Raised when LLM output cannot be parsed/validated as expected JSON."""
    pass


def _extract_json_object(text: str) -> str:
    """
    Tries to find the first JSON object in a text blob.
    Handles cases where the model accidentally wraps JSON with extra text.
    """
    text = text.strip()

    # Fast path: already looks like JSON object
    if text.startswith("{") and text.endswith("}"):
        return text

    # Try to find a JSON object with a conservative regex
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise LLMJSONError("No JSON object found in model output.")
    return match.group(0)


def parse_and_validate_extraction(raw_model_output: str) -> ExtractionResult:
    """
    Returns a validated ExtractionResult (Pydantic model).
    Raises LLMJSONError with a clear message on failure.
    """
    try:
        json_str = _extract_json_object(raw_model_output)
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise LLMJSONError(f"Invalid JSON: {e}") from e
    except Exception as e:
        raise LLMJSONError(str(e)) from e

    try:
        return ExtractionResult.model_validate(data)
    except Exception as e:
        raise LLMJSONError(f"Schema validation failed: {e}") from e


def try_parse_extraction(raw_model_output: str) -> Tuple[bool, Optional[ExtractionResult], Optional[str]]:
    """
    Non-throwing helper for APIs:
    - ok=True returns (True, result, None)
    - ok=False returns (False, None, error_message)
    """
    try:
        result = parse_and_validate_extraction(raw_model_output)
        return True, result, None
    except Exception as e:
        return False, None, str(e)