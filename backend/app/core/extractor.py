from app.core.models import (
    CandidateProfile,
    SkillItem,
    ExperienceItem,
    ProjectItem,
    EducationItem,
    Evidence,
)
from app.services.llm import llm
from app.services.vector_store import vector_store
from app.utils.files import new_id


SYSTEM_PROMPT = """You are HireLens, an expert resume parsing engine.
Extract structured candidate information from resume text.
For EVERY skill, experience, project, and education entry, you MUST include
an evidence object with:
- text: exact quoted text from the resume (verbatim, max 25 words)
- source: resume filename
- page: page number if available else null
- line: approximate line number if available else null
Never invent skills or experience. If a field is not present, omit it or leave empty.
Return a single JSON object matching the requested schema exactly."""


class Extractor:
    def build_schema_hint(self) -> str:
        return """{
  "name": "string",
  "email": "string",
  "phone": "string",
  "location": "string",
  "total_experience_years": number,
  "summary": "string (2-3 sentences)",
  "skills": [
    {"skill": "string", "evidence": {"text": "string", "source": "string", "page": int|null, "line": int|null}, "confidence": "high|medium|low"}
  ],
  "experiences": [
    {"title": "string", "company": "string", "duration": "string", "description": "string", "evidence": {"text": "string", "source": "string", "page": int|null, "line": int|null}}
  ],
  "projects": [
    {"name": "string", "description": "string", "technologies": ["string"], "evidence": {"text": "string", "source": "string", "page": int|null, "line": int|null}}
  ],
  "education": [
    {"degree": "string", "institution": "string", "year": "string", "evidence": {"text": "string", "source": "string", "page": int|null, "line": int|null}}
  ]
}"""

    def _evidence(self, data: dict, filename: str) -> Evidence:
        return Evidence(
            text=str(data.get("text", ""))[:400],
            source=str(data.get("source") or filename),
            page=data.get("page"),
            line=data.get("line"),
        )

    def extract(self, resume_text: str, filename: str) -> CandidateProfile:
        user_prompt = (
            f"Resume filename: {filename}\n\n"
            f"Resume text:\n\"\"\"\n{resume_text[:15000]}\n\"\"\"\n\n"
            f"Return JSON matching this schema:\n{self.build_schema_hint()}"
        )
        data = llm.chat_json(system=SYSTEM_PROMPT, user=user_prompt, temperature=0.1)

        skills = [
            SkillItem(
                skill=str(s.get("skill", "")).strip(),
                evidence=self._evidence(s.get("evidence", {}), filename),
                confidence=s.get("confidence", "medium"),
            )
            for s in (data.get("skills") or [])
            if s.get("skill")
        ]
        experiences = [
            ExperienceItem(
                title=str(e.get("title", "")),
                company=str(e.get("company", "")),
                duration=str(e.get("duration", "")),
                description=str(e.get("description", "")),
                evidence=self._evidence(e.get("evidence", {}), filename),
            )
            for e in (data.get("experiences") or [])
        ]
        projects = [
            ProjectItem(
                name=str(p.get("name", "")),
                description=str(p.get("description", "")),
                technologies=[str(t) for t in (p.get("technologies") or [])],
                evidence=self._evidence(p.get("evidence", {}), filename),
            )
            for p in (data.get("projects") or [])
        ]
        education = [
            EducationItem(
                degree=str(ed.get("degree", "")),
                institution=str(ed.get("institution", "")),
                year=str(ed.get("year", "")),
                evidence=self._evidence(ed.get("evidence", {}), filename),
            )
            for ed in (data.get("education") or [])
        ]

        candidate_id = new_id("cand_")
        profile = CandidateProfile(
            candidate_id=candidate_id,
            name=str(data.get("name") or "Unknown Candidate").strip(),
            email=str(data.get("email", "")).strip(),
            phone=str(data.get("phone", "")).strip(),
            location=str(data.get("location", "")).strip(),
            total_experience_years=float(data.get("total_experience_years") or 0.0),
            summary=str(data.get("summary", "")).strip(),
            skills=skills,
            experiences=experiences,
            projects=projects,
            education=education,
            raw_text=resume_text,
            resume_filename=filename,
        )
        return profile

    def index_in_vector_store(self, profile: CandidateProfile) -> None:
        chunks: list[dict] = []
        for s in profile.skills:
            chunks.append(
                {
                    "text": f"Skill: {s.skill}. Evidence: {s.evidence.text}",
                    "source": s.evidence.source,
                    "page": s.evidence.page or 0,
                    "line": s.evidence.line or 0,
                }
            )
        for e in profile.experiences:
            chunks.append(
                {
                    "text": f"{e.title} at {e.company} ({e.duration}). {e.description}",
                    "source": e.evidence.source,
                    "page": e.evidence.page or 0,
                    "line": e.evidence.line or 0,
                }
            )
        for p in profile.projects:
            chunks.append(
                {
                    "text": f"Project {p.name}: {p.description}. Tech: {', '.join(p.technologies)}",
                    "source": p.evidence.source,
                    "page": p.evidence.page or 0,
                    "line": p.evidence.line or 0,
                }
            )
        vector_store.add_candidate_chunks(
            candidate_id=profile.candidate_id,
            candidate_name=profile.name,
            chunks=chunks,
        )


extractor = Extractor()