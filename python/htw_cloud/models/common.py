"""Common API envelope types."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Unified response envelope for all HTW Cloud HTTP APIs."""

    code: int = 0
    message: str = "ok"
    data: T | None = None


class ErrorBody(BaseModel):
    detail: str = Field(default="")
