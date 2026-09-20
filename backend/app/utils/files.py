import json
import uuid
from pathlib import Path
from typing import Any
import pdfplumber
from app.config import settings


def ensure_dirs() -> None:
    settings.resolve_path(settings.UPLOAD_DIR)
    settings.resolve_path(settings.PROCESSED_DIR)
    settings.resolve_path(settings.SAMPLES_DIR)
    settings.resolve_path(settings.CHROMA_DIR)


def new_id(prefix: str = "") -> str:
    raw = uuid.uuid4().hex[:12]
    return f"{prefix}{raw}" if prefix else raw


def safe_filename(name: str) -> str:
    keep = "-_. "
    cleaned = "".join(c for c in name if c.isalnum() or c in keep).strip()
    return cleaned.replace(" ", "_") or "file"


def save_upload(file_bytes: bytes, filename: str, subdir: str = "uploads") -> Path:
    target_dir = settings.resolve_path(
        settings.UPLOAD_DIR if subdir == "uploads" else settings.PROCESSED_DIR
    )
    safe = safe_filename(filename)
    path = target_dir / f"{new_id()}_{safe}"
    path.write_bytes(file_bytes)
    return path


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_text_from_pdf(path: Path) -> tuple[str, int]:
    parts: list[str] = []
    pages = 0
    with pdfplumber.open(str(path)) as pdf:
        pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                parts.append(f"[PAGE {i}]\n{text}")
    return "\n\n".join(parts), pages


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text, _ = extract_text_from_pdf(path)
        return text
    if suffix in {".txt", ".md"}:
        return read_text_file(path)
    try:
        return read_text_file(path)
    except Exception:
        return ""


def dump_json(data: Any, name: str) -> Path:
    target_dir = settings.resolve_path(settings.PROCESSED_DIR)
    path = target_dir / f"{name}.json"
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    return path


def load_json(name: str) -> Any:
    target_dir = settings.resolve_path(settings.PROCESSED_DIR)
    path = target_dir / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_json_files() -> list[Path]:
    target_dir = settings.resolve_path(settings.PROCESSED_DIR)
    return sorted(target_dir.glob("*.json"))