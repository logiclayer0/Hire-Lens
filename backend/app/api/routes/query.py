from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.models import CandidateProfile
from app.core.query_engine import query_engine
from app.utils.files import load_json

router = APIRouter(prefix="/api/query", tags=["query"])


class QueryRequest(BaseModel):
    question: str


def _load_profiles() -> list[CandidateProfile]:
    data = load_json("candidates_index") or []
    return [CandidateProfile(**c) for c in data]


@router.post("")
def ask(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty.")
    profiles = _load_profiles()
    if not profiles:
        raise HTTPException(status_code=400, detail="No candidates uploaded.")
    response = query_engine.query(req.question, profiles)
    return response.model_dump()