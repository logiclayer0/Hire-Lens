import json
import re
from typing import Any, Optional
from groq import Groq
from app.config import settings


class LLMError(Exception):
    pass


class LLMService:
    def __init__(self) -> None:
        if not settings.GROQ_API_KEY:
            raise LLMError("GROQ_API_KEY missing in .env")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.fast_model = settings.GROQ_FAST_MODEL

    def _strip_code_fences(self, text: str) -> str:
        text = text.strip()
        fence = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)
        return fence.sub("", text).strip()

    def _extract_json(self, text: str) -> Any:
        cleaned = self._strip_code_fences(text)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1 and end > start:
                return json.loads(cleaned[start : end + 1])
            start = cleaned.find("[")
            end = cleaned.rfind("]")
            if start != -1 and end != -1 and end > start:
                return json.loads(cleaned[start : end + 1])
            raise LLMError(f"Could not parse JSON from LLM output: {cleaned[:200]}")

    def chat(
        self,
        system: str,
        user: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        model: Optional[str] = None,
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            raise LLMError(f"Groq chat failed: {exc}") from exc

    def chat_json(
        self,
        system: str,
        user: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        model: Optional[str] = None,
    ) -> Any:
        json_system = (
            system
            + "\n\nYou must respond with valid JSON only. "
            + "No prose, no markdown fences, no explanation outside JSON."
        )
        raw = self.chat(
            system=json_system,
            user=user,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
        )
        return self._extract_json(raw)


llm = LLMService()