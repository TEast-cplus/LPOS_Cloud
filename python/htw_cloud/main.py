"""Uvicorn entrypoint: python -m htw_cloud.main"""

from __future__ import annotations

import uvicorn

from htw_cloud.app import create_app
from htw_cloud.config import load_config


def main() -> None:
    config = load_config()
    app = create_app(config)
    uvicorn.run(
        app,
        host=config.server.host,
        port=config.server.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
