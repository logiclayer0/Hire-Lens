from app.core.models import JobDescription, JDRequirement
from app.services.llm import llm
from app.utils.files import new_id


SYSTEM_PROMPT = """You are HireLens, an expert job description analyzer.
Break a job description into atomic, testable requirements.
Each requirement must be a single clear statement (skill, years, domain, tool, etc).
Categorize each as "must_have" or "nice_to_have".
Extract the core skill/tool as `skill` if applicable.
Extract `min_years` if the requirement mentions years of experience.
Return JSON only."""


class JDParser:
    def build_schema_hint(self) -> str:
        return """{
  "title": "string",
  "company": "string",
  "summary": "string (2 sentences)",
  "requirements": [
    {
      "text": "string (one clear requirement)",
      "category": "must_have|nice_to_have",
      "skill": "string",
      "min_years": number|null
    }
  ]
}"""

    def parse(self, jd_text: str) -> JobDescription:
        user_prompt = (
            f"Job description:\n\"\"\"\n{jd_text[:15000]}\n\"\"\"\n\n"
            f"Return JSON matching this schema:\n{self.build_schema_hint()}"
        )
        data = llm.chat_json(system=SYSTEM_PROMPT, user=user_prompt, temperature=0.1)

        requirements: list[JDRequirement] = []
        for i, r in enumerate(data.get("requirements") or [], start=1):
            text = str(r.get("text", "")).strip()
            if not text:
                continue
            requirements.append(
                JDRequirement(
                    requirement_id=f"req_{i}",
                    text=text,
                    category=r.get("category", "must_have"),
                    skill=str(r.get("skill", "")).strip(),
                    min_years=r.get("min_years"),
                )
            )

        return JobDescription(
            title=str(data.get("title", "Untitled Role")),
            company=str(data.get("company", "")),
            summary=str(data.get("summary", "")),
            requirements=requirements,
            raw_text=jd_text,
        )


jd_parser = JDParser()