from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import upload, candidates, query, interview
from app.config import settings
from app.utils.files import ensure_dirs

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="HireLens — Evidence-backed hiring intelligence API powered by Groq.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(candidates.router)
app.include_router(query.router)
app.include_router(interview.router)


@app.on_event("startup")
def on_startup() -> None:
    ensure_dirs()


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return JSONResponse({"status": "healthy"})