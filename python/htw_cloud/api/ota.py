"""OTA Management API.

Creates upgrade jobs only. Edge validates version, installs, and rolls back.
Cloud must never force Provider/MCU upgrade without edge checks.
"""

from fastapi import APIRouter, Depends, HTTPException

from htw_cloud.api.deps import get_store
from htw_cloud.models.common import ApiResponse
from htw_cloud.models.robot import OtaCreateRequest, OtaRecord
from htw_cloud.store.memory import MemoryStore

router = APIRouter(tags=["ota"])


@router.post(
    "/robots/{robot_id}/ota",
    response_model=ApiResponse[OtaRecord],
)
def create_ota(
    robot_id: str,
    body: OtaCreateRequest,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[OtaRecord]:
    job = store.add_ota(robot_id, body)
    if job is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=job)


@router.get(
    "/robots/{robot_id}/ota",
    response_model=ApiResponse[list[OtaRecord]],
)
def list_ota(
    robot_id: str,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[list[OtaRecord]]:
    jobs = store.list_ota(robot_id)
    if jobs is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=jobs)
