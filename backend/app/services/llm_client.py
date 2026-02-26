import os
from dotenv import load_dotenv

load_dotenv()


class LLMClientError(Exception):
    pass


class LLMClient:
    """
    Provider-agnostic LLM client.
    Today: OpenAI
    Tomorrow: Gemini / Azure / local model (same interface).
    """

    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()

        if self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            if not self.api_key:
                raise LLMClientError("Missing OPENAI_API_KEY in environment.")
        else:
            raise LLMClientError(f"Unsupported LLM_PROVIDER: {self.provider}")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Returns raw text output from the model (expected to be JSON).
        """
        if self.provider == "openai":
            return self._generate_openai(system_prompt, user_prompt)

        raise LLMClientError(f"Unsupported provider: {self.provider}")

    def _generate_openai(self, system_prompt: str, user_prompt: str) -> str:
        try:
            # Lazy import so the project can run without OpenAI installed until needed
            from openai import OpenAI  # type: ignore
        except Exception as e:
            raise LLMClientError(
                "OpenAI SDK not installed. Add 'openai' to requirements.txt"
            ) from e

        client = OpenAI(api_key=self.api_key)

        try:
            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            raise LLMClientError(f"OpenAI request failed: {e}") from e