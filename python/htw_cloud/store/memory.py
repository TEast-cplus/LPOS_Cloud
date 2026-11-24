"""In-process memory store for the skeleton phase."""

from __future__ import annotations

from threading import Lock
from uuid import uuid4

from htw_cloud.models.robot import (
    DiagnosticsInfo,
    Identity,
    OtaCreateRequest,
    OtaRecord,
    RobotRecord,
    RobotRegisterRequest,
    StatusSnapshot,
    TaskCreateRequest,
    TaskRecord,
    utc_now,
)


class MemoryStore:
    """Thread-safe in-memory robot registry."""

    def __init__(self) -> None:
        self._robots: dict[str, RobotRecord] = {}
        self._lock = Lock()

    def register(self, request: RobotRegisterRequest) -> RobotRecord:
        robot_id = str(uuid4())
        record = RobotRecord(
            identity=Identity(
                robot_id=robot_id,
                product_id=request.product_id,
                hardware_version=request.hardware_version,
            ),
            platform=request.platform,
            devices=request.devices,
            last_seen=utc_now(),
        )
        with self._lock:
            self._robots[robot_id] = record
        return record

    def get(self, robot_id: str) -> RobotRecord | None:
        with self._lock:
            return self._robots.get(robot_id)

    def heartbeat(self, robot_id: str) -> RobotRecord | None:
        with self._lock:
            record = self._robots.get(robot_id)
            if record is None:
                return None
            record.last_seen = utc_now()
            return record

    def update_status(
        self, robot_id: str, status: StatusSnapshot
    ) -> RobotRecord | None:
        with self._lock:
            record = self._robots.get(robot_id)
            if record is None:
                return None
            status.updated_at = utc_now()
            record.status = status
            record.last_seen = status.updated_at
            return record

    def add_task(
        self, robot_id: str, request: TaskCreateRequest
    ) -> TaskRecord | None:
        with self._lock:
            record = self._robots.get(robot_id)
            if record is None:
                return None
            task = TaskRecord(
                task_type=request.task_type, payload=request.payload
            )
            record.tasks.append(task)
            return task

    def list_tasks(self, robot_id: str) -> list[TaskRecord] | None:
        with self._lock:
            record = self._robots.get(robot_id)
            if record is None:
                return None
            return list(record.tasks)

    def add_ota(
        self, robot_id: str, request: OtaCreateRequest
    ) -> OtaRecord | None:
        with self._lock:
            record = self._robots.get(robot_id)
            if record is None:
                return None
            job = OtaRecord(
                target=request.target,
                version=request.version,
                package_url=request.package_url,
                checksum=request.checksum,
            )
            record.ota_jobs.append(job)
            return job

    def list_ota(self, robot_id: str) -> list[OtaRecord] | None:
        with self._lock:
            record = self._robots.get(robot_id)
            if record is None:
                return None
            return list(record.ota_jobs)

    def add_diagnostics(
        self, robot_id: str, info: DiagnosticsInfo
    ) -> DiagnosticsInfo | None:
        with self._lock:
            record = self._robots.get(robot_id)
            if record is None:
                return None
            record.diagnostics_history.append(info)
            record.status.diagnostics = info
            record.last_seen = utc_now()
            return info

    def get_diagnostics(
        self, robot_id: str
    ) -> list[DiagnosticsInfo] | None:
        with self._lock:
            record = self._robots.get(robot_id)
            if record is None:
                return None
            return list(record.diagnostics_history)
