from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.extractor import extractor
from app.core.jd_parser import jd_parser
from app.core.models import CandidateProfile
from app.core.parser import parser
from app.utils.files import (
    dump_json,
    load_json,
    save_upload,
    ensure_dirs,
)

router = APIRouter(prefix="/api/upload", tags=["upload"])


def _upsert_candidate(profile: CandidateProfile) -> None:
    index = load_json("candidates_index") or []
    index = [c for c in index if c.get("candidate_id") != profile.candidate_id]
    index.append(profile.model_dump())
    dump_json(index, "candidates_index")


@router.post("/jd")
async def upload_jd(file: UploadFile = File(...)):
    ensure_dirs()
    try:
        content = await file.read()
        path = save_upload(content, file.filename or "jd.txt", subdir="uploads")
        parsed = parser.parse(path)
        jd = jd_parser.parse(parsed["text"])
        dump_json(jd.model_dump(), "current_jd")
        return {
            "status": "ok",
            "title": jd.title,
            "requirements_count": len(jd.requirements),
            "job_description": jd.model_dump(),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"JD upload failed: {exc}")


@router.post("/resumes")
async def upload_resumes(files: list[UploadFile] = File(...)):
    ensure_dirs()
    results = []
    for file in files:
        try:
            content = await file.read()
            path = save_upload(content, file.filename or "resume.txt", subdir="uploads")
            parsed = parser.parse(path)
            profile = extractor.extract(parsed["text"], parsed["filename"])
            extractor.index_in_vector_store(profile)
            _upsert_candidate(profile)
            results.append(
                {
                    "status": "ok",
                    "candidate_id": profile.candidate_id,
                    "name": profile.name,
                    "skills_count": len(profile.skills),
                }
            )
        except Exception as exc:
            results.append(
                {
                    "status": "error",
                    "filename": file.filename,
                    "detail": str(exc),
                }
            )
    return {"status": "ok", "results": results}


@router.get("/status")
def upload_status():
    jd = load_json("current_jd")
    candidates = load_json("candidates_index") or []
    return {
        "jd_loaded": bool(jd),
        "jd_title": jd.get("title") if jd else None,
        "candidates_loaded": len(candidates),
    }


@router.delete("/reset")
def reset_all():
    dump_json({}, "current_jd")
    dump_json([], "candidates_index")
    dump_json([], "matches_index")
    return {"status": "ok"}