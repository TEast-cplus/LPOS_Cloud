"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI

from htw_cloud import __version__
from htw_cloud.api import (
    diagnostics,
    heartbeat,
    ota,
    registration,
    status,
    task,
)
from htw_cloud.config import AppConfig, load_config
from htw_cloud.models.common import ApiResponse
from htw_cloud.store.memory import MemoryStore


def create_app(config: AppConfig | None = None) -> FastAPI:
    cfg = config or load_config()
    app = FastAPI(
        title="HTW Cloud",
        version=__version__,
        description=(
            "HTW Cloud skeleton. Cloud may query/dispatch; "
            "it does not control local robot survival."
        ),
    )
    app.state.config = cfg
    app.state.store = MemoryStore()

    prefix = cfg.api.prefix

    @app.get("/health", response_model=ApiResponse[dict])
    def health() -> ApiResponse[dict]:
        return ApiResponse(
            data={"status": "up", "version": __version__}
        )

    app.include_router(registration.router, prefix=prefix)
    app.include_router(heartbeat.router, prefix=prefix)
    app.include_router(status.router, prefix=prefix)
    app.include_router(task.router, prefix=prefix)
    app.include_router(ota.router, prefix=prefix)
    app.include_router(diagnostics.router, prefix=prefix)
    return app
