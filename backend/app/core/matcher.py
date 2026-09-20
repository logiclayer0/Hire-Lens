import json
from app.core.models import (
    CandidateProfile,
    JobDescription,
    RequirementMatch,
    CandidateMatch,
    Evidence,
)
from app.services.llm import llm


SYSTEM_PROMPT = """You are HireLens, an evidence-based hiring matcher.
For each (requirement, candidate) pair, decide if the candidate MEETS, PARTIALLY MEETS, or is MISSING the requirement.
Rules:
- Base every judgment ONLY on the candidate's provided evidence.
- Quote exact candidate evidence text in the `evidence` list.
- Never hallucinate skills.
- Provide a 0-100 score and a one-sentence reasoning.
- If information is unclear, mark status "partial" and confidence "low".
Return JSON only."""


class Matcher:
    def _profile_snapshot(self, profile: CandidateProfile) -> dict:
        return {
            "candidate_id": profile.candidate_id,
            "name": profile.name,
            "total_experience_years": profile.total_experience_years,
            "summary": profile.summary,
            "skills": [
                {"skill": s.skill, "evidence": s.evidence.model_dump()}
                for s in profile.skills
            ],
            "experiences": [
                {
                    "title": e.title,
                    "company": e.company,
                    "duration": e.duration,
                    "description": e.description,
                    "evidence": e.evidence.model_dump(),
                }
                for e in profile.experiences
            ],
            "projects": [
                {
                    "name": p.name,
                    "description": p.description,
                    "technologies": p.technologies,
                    "evidence": p.evidence.model_dump(),
                }
                for p in profile.projects
            ],
            "education": [
                {
                    "degree": ed.degree,
                    "institution": ed.institution,
                    "year": ed.year,
                    "evidence": ed.evidence.model_dump(),
                }
                for ed in profile.education
            ],
        }

    def _schema_hint(self) -> str:
        return """{
  "matches": [
    {
      "requirement_id": "string",
      "status": "met|partial|missing",
      "score": number (0-100),
      "reasoning": "string (1 sentence)",
      "confidence": "high|medium|low",
      "evidence": [
        {"text": "string", "source": "string", "page": int|null, "line": int|null}
      ]
    }
  ]
}"""

    def match_candidate(
        self,
        profile: CandidateProfile,
        jd: JobDescription,
    ) -> CandidateMatch:
        requirements_payload = [
            {
                "requirement_id": r.requirement_id,
                "text": r.text,
                "category": r.category,
                "skill": r.skill,
                "min_years": r.min_years,
            }
            for r in jd.requirements
        ]
        user_prompt = (
            f"Job requirements:\n{json.dumps(requirements_payload, indent=2)}\n\n"
            f"Candidate profile:\n{json.dumps(self._profile_snapshot(profile), indent=2)}\n\n"
            f"Return JSON matching this schema:\n{self._schema_hint()}"
        )
        data = llm.chat_json(system=SYSTEM_PROMPT, user=user_prompt, temperature=0.1)

        req_map = {r.requirement_id: r for r in jd.requirements}
        matched: list[RequirementMatch] = []
        for m in data.get("matches") or []:
            rid = str(m.get("requirement_id", ""))
            req = req_map.get(rid)
            if not req:
                continue
            evidences = [
                Evidence(
                    text=str(e.get("text", ""))[:400],
                    source=str(e.get("source", "")),
                    page=e.get("page"),
                    line=e.get("line"),
                )
                for e in (m.get("evidence") or [])
            ]
            matched.append(
                RequirementMatch(
                    requirement_id=rid,
                    requirement_text=req.text,
                    category=req.category,
                    status=m.get("status", "missing"),
                    score=float(m.get("score") or 0.0),
                    reasoning=str(m.get("reasoning", "")),
                    evidence=evidences,
                    confidence=m.get("confidence", "medium"),
                )
            )

        must_scores = [
            m.score for m in matched if m.category == "must_have"
        ] or [0.0]
        nice_scores = [
            m.score for m in matched if m.category == "nice_to_have"
        ] or [0.0]

        overall = round(
            (sum(must_scores) / len(must_scores)) * 0.75
            + (sum(nice_scores) / len(nice_scores)) * 0.25,
            2,
        )

        missing = [m.requirement_text for m in matched if m.status == "missing"]
        strengths = [
            m.requirement_text for m in matched if m.status == "met" and m.score >= 75
        ]
        gaps = [
            m.requirement_text for m in matched if m.status == "partial"
        ]

        return CandidateMatch(
            candidate_id=profile.candidate_id,
            candidate_name=profile.name,
            overall_score=overall,
            matched_requirements=matched,
            missing_requirements=missing,
            gaps_to_validate=gaps,
            strengths=strengths,
            summary=(
                f"{profile.name} matches {len(strengths)} requirement(s) strongly, "
                f"has {len(gaps)} area(s) to validate, and is missing {len(missing)}."
            ),
        )

    def rank(self, matches: list[CandidateMatch]) -> list[CandidateMatch]:
        sorted_matches = sorted(
            matches, key=lambda m: m.overall_score, reverse=True
        )
        for i, m in enumerate(sorted_matches, start=1):
            m.rank = i
        return sorted_matches


matcher = Matcher()