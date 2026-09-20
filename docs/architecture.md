# HireLens — Architecture

## Overview

HireLens is a two-service application:

- **Backend** (FastAPI + Groq): parses documents, extracts structured data, matches candidates, powers natural-language queries.
- **Frontend** (Next.js 14): recruiter interface for uploading, viewing ranked candidates, asking questions, and generating interview kits.

## Data Flow

1. Recruiter uploads a JD → `POST /api/upload/jd`
2. Backend parses PDF/text, calls Groq to break JD into atomic requirements, saves to `data/processed/current_jd.json`.
3. Recruiter uploads resumes → `POST /api/upload/resumes`
4. Backend extracts structured candidate profile per resume with evidence citations, indexes chunks in ChromaDB, saves to `data/processed/candidates_index.json`.
5. Recruiter triggers `POST /api/candidates/match` → per candidate, per requirement scoring with evidence.
6. `GET /api/candidates` returns ranked list.
7. `POST /api/query` runs vector search + Groq to answer recruiter questions with cited snippets.
8. `GET /api/interview/questions/{id}` generates role-specific questions.
9. `POST /api/interview/evaluate` turns notes into a structured report.

## Key Design Decisions

- **Evidence-first**: every AI claim carries an `Evidence` object with verbatim text + source.
- **Groq for speed**: llama-3.3-70b for quality, llama-3.1-8b for fast tasks.
- **ChromaDB local persistence**: no external vector DB needed.
- **JSON file storage**: zero-config for hackathon; swap for Postgres later.

## Directory Layout

- `backend/app/api/routes` — HTTP endpoints
- `backend/app/core` — parsing, extraction, matching, interviewing, query
- `backend/app/services` — LLM wrapper, vector store
- `backend/app/utils` — file helpers
- `frontend/src/app` — Next.js routes
- `frontend/src/components` — UI primitives
- `data/samples` — demo JD + resumes