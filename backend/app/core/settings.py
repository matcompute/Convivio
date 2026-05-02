import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel


backend_root = Path(__file__).resolve().parents[2]
load_dotenv(backend_root / ".env")


class Settings(BaseModel):
    project_name: str = "Convivio API"
    api_prefix: str = "/api"
    demo_password: str = "Convivio123!"
    llm_provider: str = os.getenv("LLM_PROVIDER", "mock").lower()
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
    gemini_api_base: str = os.getenv(
        "GEMINI_API_BASE",
        "https://generativelanguage.googleapis.com/v1beta",
    )
    llm_timeout_seconds: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "45"))
    allowed_origins: list[str] = [
        "http://127.0.0.1:4203",
        "http://localhost:4203",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ]


settings = Settings()
