"""Unified robot data model (总体构建 · 云边协同)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Identity(BaseModel):
    robot_id: str = ""
    product_id: str = ""
    hardware_version: str = ""


class Platform(BaseModel):
    soc: str = ""
    os_version: str = ""
    htwos_version: str = ""


class Devices(BaseModel):
    camera: str = ""
    imu: str = ""
    motor: str = ""
    npu: str = ""


class RuntimeInfo(BaseModel):
    service_status: str = "unknown"
    task_status: str = "idle"
    model_status: str = "unknown"


class DiagnosticsInfo(BaseModel):
    cpu: float = 0.0
    memory: float = 0.0
    temperature: float = 0.0
    faults: list[str] = Field(default_factory=list)


class StatusSnapshot(BaseModel):
    devices: Devices = Field(default_factory=Devices)
    runtime: RuntimeInfo = Field(default_factory=RuntimeInfo)
    diagnostics: DiagnosticsInfo = Field(default_factory=DiagnosticsInfo)
    updated_at: datetime = Field(default_factory=utc_now)


class RobotRegisterRequest(BaseModel):
    product_id: str
    hardware_version: str = ""
    platform: Platform = Field(default_factory=Platform)
    devices: Devices = Field(default_factory=Devices)


class HeartbeatRequest(BaseModel):
    seq: int = 0
    extra: dict[str, Any] = Field(default_factory=dict)


class TaskCreateRequest(BaseModel):
    task_type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskRecord(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    task_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    status: str = "created"
    # Cloud creates tasks; edge decides whether/when to execute.
    created_at: datetime = Field(default_factory=utc_now)


class OtaCreateRequest(BaseModel):
    target: str  # os | provider | model | app
    version: str
    package_url: str = ""
    checksum: str = ""


class OtaRecord(BaseModel):
    ota_id: str = Field(default_factory=lambda: str(uuid4()))
    target: str
    version: str
    package_url: str = ""
    checksum: str = ""
    status: str = "pending"
    # Never force install without edge version check (cloud does not own survival).
    created_at: datetime = Field(default_factory=utc_now)


class RobotRecord(BaseModel):
    identity: Identity
    platform: Platform = Field(default_factory=Platform)
    devices: Devices = Field(default_factory=Devices)
    status: StatusSnapshot = Field(default_factory=StatusSnapshot)
    last_seen: datetime | None = None
    registered_at: datetime = Field(default_factory=utc_now)
    tasks: list[TaskRecord] = Field(default_factory=list)
    ota_jobs: list[OtaRecord] = Field(default_factory=list)
    diagnostics_history: list[DiagnosticsInfo] = Field(default_factory=list)
