import json
import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

TOKENS_DIR = REPO_ROOT / "data" / "tokens"
UPLOADS_DIR = REPO_ROOT / "data" / "uploads"
PROFILES_DIR = REPO_ROOT / "data" / "profiles"

FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "dev-only-local-secret"

PINTEREST_CLIENT_ID = os.environ.get("PINTEREST_CLIENT_ID")
PINTEREST_CLIENT_SECRET = os.environ.get("PINTEREST_CLIENT_SECRET")
PINTEREST_REDIRECT_URI = os.environ.get("PINTEREST_REDIRECT_URI")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")


def require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing {name}. Set it in .env (see .env.example) before connecting this source."
        )
    return value


def token_path(provider: str) -> Path:
    TOKENS_DIR.mkdir(parents=True, exist_ok=True)
    return TOKENS_DIR / f"{provider}.json"


def load_token(provider: str) -> dict | None:
    path = token_path(provider)
    if not path.exists():
        return None
    return json.loads(path.read_text())


def save_token(provider: str, token: dict) -> None:
    token_path(provider).write_text(json.dumps(token, indent=2))
