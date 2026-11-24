"""Pydantic models for HTW Cloud."""

from htw_cloud.models.common import ApiResponse
from htw_cloud.models.robot import (
    Devices,
    DiagnosticsInfo,
    HeartbeatRequest,
    Identity,
    OtaCreateRequest,
    OtaRecord,
    Platform,
    RobotRecord,
    RobotRegisterRequest,
    RuntimeInfo,
    StatusSnapshot,
    TaskCreateRequest,
    TaskRecord,
)

__all__ = [
    "ApiResponse",
    "Devices",
    "DiagnosticsInfo",
    "HeartbeatRequest",
    "Identity",
    "OtaCreateRequest",
    "OtaRecord",
    "Platform",
    "RobotRecord",
    "RobotRegisterRequest",
    "RuntimeInfo",
    "StatusSnapshot",
    "TaskCreateRequest",
    "TaskRecord",
]
