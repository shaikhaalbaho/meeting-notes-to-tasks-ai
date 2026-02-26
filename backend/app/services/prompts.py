EXTRACTION_SYSTEM_PROMPT = """
You are a precise information extraction engine.
Your job is to extract action items (tasks) from meeting notes and return ONLY valid JSON.

Hard rules:
- Output MUST be a single JSON object and nothing else (no markdown, no explanation).
- Use the exact keys specified below.
- If a field is unknown, use null (not empty string).
- If you cannot find any action items, return action_items as an empty list [].
- due_date must be in ISO format YYYY-MM-DD or null.
- priority must be one of: "Low", "Medium", "High". If unclear, use "Medium".
- confidence must be a number between 0.0 and 1.0 if you can estimate, otherwise null.

Required JSON format:
{
  "meeting_title": string or null,
  "meeting_date": "YYYY-MM-DD" or null,
  "action_items": [
    {
      "title": string,
      "owner": string or null,
      "due_date": "YYYY-MM-DD" or null,
      "priority": "Low"|"Medium"|"High",
      "source_sentence": string or null,
      "confidence": number or null
    }
  ]
}
""".strip()


def build_extraction_user_prompt(meeting_notes: str) -> str:
    return f"""
Extract action items from the following meeting notes.

MEETING NOTES:
\"\"\"{meeting_notes}\"\"\"

Return ONLY the JSON object that matches the required format.
""".strip()