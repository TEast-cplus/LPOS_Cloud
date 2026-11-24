"""Shared FastAPI dependencies."""

from fastapi import Request

from htw_cloud.store.memory import MemoryStore


def get_store(request: Request) -> MemoryStore:
    return request.app.state.store
