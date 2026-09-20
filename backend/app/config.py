from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_FAST_MODEL: str = "llama-3.1-8b-instant"

    APP_NAME: str = "HireLens"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    UPLOAD_DIR: str = "../data/uploads"
    PROCESSED_DIR: str = "../data/processed"
    SAMPLES_DIR: str = "../data/samples"
    CHROMA_DIR: str = "../data/chroma"

    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    @property
    def base_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    def resolve_path(self, relative: str) -> Path:
        p = Path(relative)
        if p.is_absolute():
            return p
        resolved = (self.base_dir / p).resolve()
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved


settings = Settings()