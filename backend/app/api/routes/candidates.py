from fastapi import APIRouter, HTTPException

from app.core.matcher import matcher
from app.core.models import CandidateProfile, CandidateMatch, JobDescription
from app.utils.files import dump_json, load_json

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


def _load_jd() -> JobDescription:
    data = load_json("current_jd")
    if not data:
        raise HTTPException(status_code=400, detail="No JD uploaded.")
    return JobDescription(**data)


def _load_profiles() -> list[CandidateProfile]:
    data = load_json("candidates_index") or []
    return [CandidateProfile(**c) for c in data]


def _load_matches() -> list[CandidateMatch]:
    data = load_json("matches_index") or []
    return [CandidateMatch(**m) for m in data]


@router.post("/match")
def run_matching():
    jd = _load_jd()
    profiles = _load_profiles()
    if not profiles:
        raise HTTPException(status_code=400, detail="No candidates uploaded.")

    results: list[CandidateMatch] = []
    for p in profiles:
        results.append(matcher.match_candidate(p, jd))

    ranked = matcher.rank(results)
    dump_json([m.model_dump() for m in ranked], "matches_index")
    return {"status": "ok", "count": len(ranked)}


@router.get("")
def list_candidates():
    matches = _load_matches()
    return {
        "count": len(matches),
        "candidates": [m.model_dump() for m in matches],
    }


@router.get("/{candidate_id}")
def get_candidate(candidate_id: str):
    matches = _load_matches()
    for m in matches:
        if m.candidate_id == candidate_id:
            return m.model_dump()
    raise HTTPException(status_code=404, detail="Candidate not found.")