<div align="center">

# 🔍 HireLens

### Evidence-backed hiring intelligence

**Every AI insight cites the exact resume line it came from.**

[![Live Demo](https://img.shields.io/badge/demo-live-success?style=flat-square)](https://hire-lens-blond.vercel.app)
[![API](https://img.shields.io/badge/api-render-blue?style=flat-square)](https://hirelens-backend.onrender.com/docs)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

</div>

---

## 📖 Overview

**HireLens** is an AI-powered recruitment intelligence agent that helps hiring teams screen candidates with **full transparency**. Unlike black-box screening tools, every score, gap, and recommendation is traced back to the exact source line in the candidate's resume.

> **Live:** [hire-lens-blond.vercel.app](https://hire-lens-blond.vercel.app)
> **API Docs:** [hirelens-backend.onrender.com/docs](https://hirelens-backend.onrender.com/docs)

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📄 **JD Parsing** | Upload a job description — LLM breaks it into atomic, testable requirements |
| 📑 **Resume Extraction** | Structured extraction of skills, experience, projects with source citations |
| 🎯 **Evidence-backed Matching** | Every requirement scored with a verbatim quote from the resume |
| 🏆 **Ranked Candidates** | Weighted scoring (75% must-have + 25% nice-to-have) |
| 🔎 **Natural Language Query** | Ask the candidate pool anything — get answers with cited sources |
| 🎤 **Interview Kits** | Role-specific questions (verify, probe, depth, behavioral) |
| 📝 **Interview Evaluation** | Post-interview notes → structured report with unanswered areas |
| 🔐 **Full Audit Trail** | Every AI claim links back to a source section |

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│                 │  HTTP   │                  │  API    │             │
│   Next.js 14    │ ──────► │   FastAPI        │ ──────► │    Groq     │
│   (Frontend)    │         │   (Backend)      │         │  (LLM)      │
│                 │         │                  │         │             │
└─────────────────┘         └──────────────────┘         └─────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │    ChromaDB      │
                            │  (Vector Store)  │
                            └──────────────────┘
```

### Tech Stack

**Backend**
- **FastAPI** — REST API framework
- **Groq** — LLM inference (`gpt-oss-120b`, `gpt-oss-20b`)
- **ChromaDB** — Vector store for semantic search
- **pdfplumber** — PDF text extraction
- **Pydantic** — Structured data validation

**Frontend**
- **Next.js 14** — App Router, React Server Components
- **TypeScript** — Type safety
- **Tailwind CSS** — Utility-first styling
- **Lucide Icons** — Icon set

**Deployment**
- **Render** — Backend hosting
- **Vercel** — Frontend hosting

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js 20+
- Groq API key ([get one free](https://console.groq.com/keys))

### Installation

```bash
git clone https://github.com/logiclayer0/Hire-Lens.git
cd Hire-Lens
```

**Backend**

```bash
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

**Frontend**

```bash
cd frontend
npm install
```

### Running

**Terminal 1 — Backend**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend**
```bash
cd frontend
npm run dev
```

**Terminal 3 — Seed demo data**
```bash
cd scripts
python seed_data.py
```

Open [http://localhost:3000](http://localhost:3000)

---

## 📁 Project Structure

```
HireLens/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # HTTP endpoints
│   │   ├── core/             # Business logic
│   │   │   ├── extractor.py  # Resume → structured profile
│   │   │   ├── jd_parser.py  # JD → requirements
│   │   │   ├── matcher.py    # Candidate ↔ JD scoring
│   │   │   ├── interviewer.py# Question generation
│   │   │   └── query_engine.py# NL query
│   │   ├── services/
│   │   │   ├── llm.py        # Groq wrapper
│   │   │   └── vector_store.py# ChromaDB
│   │   └── main.py           # FastAPI entry
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js routes
│   │   ├── components/       # UI primitives
│   │   └── lib/              # API client + types
│   └── package.json
├── data/
│   ├── samples/              # Demo JD + resumes
│   └── processed/            # Extracted JSON
├── scripts/
│   └── seed_data.py          # Demo data loader
└── docs/
    ├── architecture.md
    ├── api.md
    └── demo_script.md
```

---

## 🔌 API Reference

Base URL: `https://hirelens-backend.onrender.com`

### Upload

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload/jd` | Upload job description |
| `POST` | `/api/upload/resumes` | Upload multiple resumes |
| `GET`  | `/api/upload/status` | Check loaded data |
| `DELETE` | `/api/upload/reset` | Clear all data |

### Candidates

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/candidates/match` | Run matching against JD |
| `GET`  | `/api/candidates` | List ranked candidates |
| `GET`  | `/api/candidates/{id}` | Candidate detail with evidence |

### Query

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/query` | Natural language query |

### Interview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/interview/questions/{id}` | Generate interview kit |
| `POST` | `/api/interview/evaluate` | Evaluate interview notes |

Full Swagger docs: [`/docs`](https://hirelens-backend.onrender.com/docs)

---

## 🎯 How It Works

### 1. Job Description Parsing

The JD is broken into **atomic, testable requirements** categorized as `must_have` or `nice_to_have`:

```json
{
  "requirement_id": "req_1",
  "text": "5+ years of backend engineering experience",
  "category": "must_have",
  "skill": "backend engineering",
  "min_years": 5
}
```

### 2. Resume Extraction

Each resume is parsed into a structured profile where **every field carries an evidence object**:

```json
{
  "skill": "Python",
  "evidence": {
    "text": "Built 3 ML pipelines using Python at XYZ Company",
    "source": "resume_1.txt",
    "page": 1,
    "line": 12
  }
}
```

### 3. Evidence-backed Matching

For each requirement-candidate pair, the LLM decides `met`, `partial`, or `missing`, and **quotes the exact evidence**:

```json
{
  "requirement_id": "req_2",
  "status": "met",
  "score": 92,
  "reasoning": "Candidate built payment microservices in Python",
  "evidence": [
    {
      "text": "Led the design and rollout of a new payment processing microservice...",
      "source": "resume_1.txt"
    }
  ]
}
```

### 4. Scoring

```
overall_score = (avg_must_have_score × 0.75) + (avg_nice_to_have_score × 0.25)
```

---

## 🌐 Environment Variables

### Backend (`.env`)

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=openai/gpt-oss-120b
GROQ_FAST_MODEL=openai/gpt-oss-20b
APP_NAME=HireLens
APP_VERSION=1.0.0
DEBUG=False
UPLOAD_DIR=../data/uploads
PROCESSED_DIR=../data/processed
SAMPLES_DIR=../data/samples
CHROMA_DIR=../data/chroma
ALLOWED_ORIGINS=https://hire-lens-blond.vercel.app
```

### Frontend (`.env.local`)

```env
NEXT_PUBLIC_API_URL=https://hirelens-backend.onrender.com
```

---

## 🐳 Docker

```bash
docker-compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

---

## 🚢 Deployment

### Backend — Render

1. New Web Service → connect GitHub repo
2. Root Directory: `backend`
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Env vars: `GROQ_API_KEY`, `GROQ_MODEL`, `GROQ_FAST_MODEL`, `ALLOWED_ORIGINS`

### Frontend — Vercel

1. New Project → import GitHub repo
2. Root Directory: `frontend`
3. Env var: `NEXT_PUBLIC_API_URL=https://hirelens-backend.onrender.com`
4. Deploy

---

## 🧪 Testing

```bash
cd backend
pytest -q
```

---

## 🎬 Demo Flow

1. **Home** — Landing page with value prop
2. **Upload** — Drag JD + 3 resumes → "Upload & Analyze"
3. **Candidates** — Ranked list with scores
4. **Candidate Detail** — Requirement-by-requirement breakdown with evidence chips
5. **Ask Pool** — "Which candidates have led teams and worked on payments?"
6. **Interview** — Generate questions → paste notes → structured report

---

## 🛡️ Design Principles

- **Evidence-first** — No unsupported AI claims. Every score cites a source.
- **Human-in-the-loop** — AI suggests, humans decide.
- **Transparent** — Full audit trail for every insight.
- **Fast** — Groq LPU inference for sub-second responses.

---

## 🗺️ Roadmap

- [ ] Multi-language resume support
- [ ] Bias detection and mitigation
- [ ] Interview scheduling integration
- [ ] ATS integrations (Greenhouse, Lever)
- [ ] Team collaboration features
- [ ] PDF export for evaluation reports

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — Ultra-fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com) — Modern Python API framework
- [Next.js](https://nextjs.org) — React framework
- [ChromaDB](https://www.trychroma.com) — Vector database
- [Tailwind CSS](https://tailwindcss.com) — Utility-first CSS

---

<div align="center">

**Built for AI Agent Hackathon 2026**

⭐ Star this repo if you find it useful!

</div>
