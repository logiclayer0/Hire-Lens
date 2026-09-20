import json
from app.core.models import (
    CandidateProfile,
    CandidateMatch,
    InterviewKit,
    InterviewQuestion,
    JobDescription,
    EvaluationReport,
    EvaluationArea,
    Evidence,
)
from app.services.llm import llm


QUESTION_SYSTEM = """You are HireLens, an expert technical interviewer.
Generate role-specific interview questions for a candidate based on:
1. Their evidence-backed strengths (verify depth).
2. Their partial/missing requirements (probe gaps).
3. Role must-have requirements.
Each question must reference a specific requirement.
Categories: "verify" (confirm a claim), "probe_gap" (explore missing area), "depth" (technical depth), "behavioral".
Include an `evidence` object when the question references a specific claim in the resume.
Return JSON only."""


EVAL_SYSTEM = """You are HireLens, an interview evaluation engine.
Given interview notes and the job requirements, produce a structured evaluation.
For each requirement, mark status: "covered", "partial", or "unanswered".
Identify unanswered evaluation areas.
Provide an overall recommendation: "strong_yes", "yes", "maybe", "no".
Base everything ONLY on the provided notes. Do not invent facts.
Return JSON only."""


class Interviewer:
    def _questions_schema(self) -> str:
        return """{
  "questions": [
    {
      "question": "string",
      "category": "verify|probe_gap|depth|behavioral",
      "target_requirement": "string",
      "evidence": {"text": "string", "source": "string", "page": int|null, "line": int|null} | null
    }
  ]
}"""

    def generate_questions(
        self,
        profile: CandidateProfile,
        match: CandidateMatch,
        jd: JobDescription,
    ) -> InterviewKit:
        strengths = [
            {
                "requirement": m.requirement_text,
                "reasoning": m.reasoning,
                "evidence": [e.model_dump() for e in m.evidence],
            }
            for m in match.matched_requirements
            if m.status == "met"
        ]
        gaps = [
            {
                "requirement": m.requirement_text,
                "reasoning": m.reasoning,
                "status": m.status,
            }
            for m in match.matched_requirements
            if m.status in {"partial", "missing"}
        ]
        payload = {
            "candidate_name": profile.name,
            "role_title": jd.title,
            "summary": profile.summary,
            "strengths": strengths,
            "gaps": gaps,
        }
        user_prompt = (
            f"Input:\n{json.dumps(payload, indent=2)}\n\n"
            f"Generate 6-8 interview questions. Return JSON matching:\n{self._questions_schema()}"
        )
        data = llm.chat_json(system=QUESTION_SYSTEM, user=user_prompt, temperature=0.3)

        questions: list[InterviewQuestion] = []
        for q in data.get("questions") or []:
            ev = q.get("evidence")
            evidence = None
            if isinstance(ev, dict) and ev.get("text"):
                evidence = Evidence(
                    text=str(ev.get("text", ""))[:400],
                    source=str(ev.get("source", "")),
                    page=ev.get("page"),
                    line=ev.get("line"),
                )
            questions.append(
                InterviewQuestion(
                    question=str(q.get("question", "")).strip(),
                    category=q.get("category", "verify"),
                    target_requirement=str(q.get("target_requirement", "")),
                    evidence=evidence,
                )
            )

        return InterviewKit(
            candidate_id=profile.candidate_id,
            candidate_name=profile.name,
            questions=questions,
        )

    def _eval_schema(self) -> str:
        return """{
  "overall_recommendation": "strong_yes|yes|maybe|no",
  "summary": "string (3-4 sentences)",
  "areas": [
    {
      "requirement_id": "string",
      "status": "covered|partial|unanswered",
      "notes": "string"
    }
  ]
}"""

    def evaluate(
        self,
        profile: CandidateProfile,
        jd: JobDescription,
        notes: str,
    ) -> EvaluationReport:
        reqs = [
            {"requirement_id": r.requirement_id, "text": r.text, "category": r.category}
            for r in jd.requirements
        ]
        user_prompt = (
            f"Job requirements:\n{json.dumps(reqs, indent=2)}\n\n"
            f"Candidate: {profile.name}\n"
            f"Interview notes:\n\"\"\"\n{notes[:8000]}\n\"\"\"\n\n"
            f"Return JSON matching:\n{self._eval_schema()}"
        )
        data = llm.chat_json(system=EVAL_SYSTEM, user=user_prompt, temperature=0.2)

        req_map = {r.requirement_id: r for r in jd.requirements}
        areas: list[EvaluationArea] = []
        for a in data.get("areas") or []:
            rid = str(a.get("requirement_id", ""))
            req = req_map.get(rid)
            if not req:
                continue
            areas.append(
                EvaluationArea(
                    requirement_id=rid,
                    requirement_text=req.text,
                    status=a.get("status", "unanswered"),
                    notes=str(a.get("notes", "")),
                )
            )

        unanswered = [a.requirement_text for a in areas if a.status == "unanswered"]

        return EvaluationReport(
            candidate_id=profile.candidate_id,
            candidate_name=profile.name,
            overall_recommendation=data.get("overall_recommendation", "maybe"),
            areas=areas,
            unanswered_areas=unanswered,
            summary=str(data.get("summary", "")),
        )


interviewer = Interviewer()