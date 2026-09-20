from fastapi import HTTPException
from app.utils.files import load_json


def require_jd() -> dict:
    data = load_json("current_jd")
    if not data:
        raise HTTPException(status_code=400, detail="No job description uploaded yet.")
    return data


def require_candidates() -> list[dict]:
    data = load_json("candidates_index")
    if not data:
        raise HTTPException(status_code=400, detail="No candidates uploaded yet.")
    return data