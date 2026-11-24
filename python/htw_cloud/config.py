"""Application configuration loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class ApiConfig(BaseModel):
    prefix: str = "/api/v1"


class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    auth_enabled: bool = False
    api: ApiConfig = Field(default_factory=ApiConfig)


def _default_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "configs" / "default.yaml"


def load_config(path: str | None = None) -> AppConfig:
    """Load YAML config; fall back to defaults when file missing."""
    config_path = Path(path) if path else _default_config_path()
    raw: dict[str, Any] = {}
    if config_path.is_file():
        with config_path.open("r", encoding="utf-8") as handle:
            loaded = yaml.safe_load(handle) or {}
            if isinstance(loaded, dict):
                raw = loaded
    return AppConfig.model_validate(raw)
