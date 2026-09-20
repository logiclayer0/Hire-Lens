from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.interviewer import interviewer
from app.core.models import CandidateMatch, CandidateProfile, JobDescription
from app.utils.files import load_json

router = APIRouter(prefix="/api/interview", tags=["interview"])


class NotesRequest(BaseModel):
    candidate_id: str
    notes: str


def _load_jd() -> JobDescription:
    data = load_json("current_jd")
    if not data:
        raise HTTPException(status_code=400, detail="No JD uploaded.")
    return JobDescription(**data)


def _load_profiles() -> dict[str, CandidateProfile]:
    data = load_json("candidates_index") or []
    return {c["candidate_id"]: CandidateProfile(**c) for c in data}


def _load_matches() -> dict[str, CandidateMatch]:
    data = load_json("matches_index") or []
    return {m["candidate_id"]: CandidateMatch(**m) for m in data}


@router.get("/questions/{candidate_id}")
def get_questions(candidate_id: str):
    jd = _load_jd()
    profiles = _load_profiles()
    matches = _load_matches()
    if candidate_id not in profiles:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    if candidate_id not in matches:
        raise HTTPException(status_code=400, detail="Run matching first.")
    kit = interviewer.generate_questions(
        profiles[candidate_id], matches[candidate_id], jd
    )
    return kit.model_dump()


@router.post("/evaluate")
def evaluate(req: NotesRequest):
    jd = _load_jd()
    profiles = _load_profiles()
    if req.candidate_id not in profiles:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    if not req.notes.strip():
        raise HTTPException(status_code=400, detail="Notes are empty.")
    report = interviewer.evaluate(profiles[req.candidate_id], jd, req.notes)
    return report.model_dump()