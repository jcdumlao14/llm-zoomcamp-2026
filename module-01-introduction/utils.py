import logging
import os
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

logger = logging.getLogger(__name__)


def load_env_file() -> None:
    """Load environment variables from .env if present."""
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        values = dotenv_values(env_path)
        for key, value in values.items():
            if value is not None and key not in os.environ:
                os.environ[key] = value


load_env_file()


def ensure_env_var(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_json(value: Any) -> str:
    return str(value)
