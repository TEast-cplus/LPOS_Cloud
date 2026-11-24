"""Device Status API."""

from fastapi import APIRouter, Depends, HTTPException

from htw_cloud.api.deps import get_store
from htw_cloud.models.common import ApiResponse
from htw_cloud.models.robot import RobotRecord, StatusSnapshot
from htw_cloud.store.memory import MemoryStore

router = APIRouter(tags=["status"])


@router.get(
    "/robots/{robot_id}/status",
    response_model=ApiResponse[StatusSnapshot],
)
def get_status(
    robot_id: str,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[StatusSnapshot]:
    record = store.get(robot_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=record.status)


@router.put(
    "/robots/{robot_id}/status",
    response_model=ApiResponse[RobotRecord],
)
def put_status(
    robot_id: str,
    body: StatusSnapshot,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[RobotRecord]:
    record = store.update_status(robot_id, body)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=record)
