# HireLens — API Reference

Base URL: `http://localhost:8000`

## Upload

### POST /api/upload/jd
Multipart: `file` (PDF/TXT).
Returns parsed JD with requirements.

### POST /api/upload/resumes
Multipart: `files` (multiple).
Returns per-file status + candidate_id.

### GET /api/upload/status
Returns `{ jd_loaded, jd_title, candidates_loaded }`.

### DELETE /api/upload/reset
Clears JD, candidates, matches.

## Candidates

### POST /api/candidates/match
Runs matching against current JD. Returns `{ status, count }`.

### GET /api/candidates
Returns `{ count, candidates: CandidateMatch[] }` ranked.

### GET /api/candidates/{candidate_id}
Returns full `CandidateMatch` with evidence.

## Query

### POST /api/query
Body: `{ "question": "..." }`
Returns `{ answer, sources[], matched_candidate_ids[] }`.

## Interview

### GET /api/interview/questions/{candidate_id}
Returns `InterviewKit`.

### POST /api/interview/evaluate
Body: `{ "candidate_id": "...", "notes": "..." }`
Returns `EvaluationReport`.

## Meta

- `GET /` — app info
- `GET /health` — health check
- `GET /docs` — Swagger UI