"""Heartbeat API."""

from fastapi import APIRouter, Depends, HTTPException

from htw_cloud.api.deps import get_store
from htw_cloud.models.common import ApiResponse
from htw_cloud.models.robot import HeartbeatRequest, RobotRecord
from htw_cloud.store.memory import MemoryStore

router = APIRouter(tags=["heartbeat"])


@router.post(
    "/robots/{robot_id}/heartbeat",
    response_model=ApiResponse[RobotRecord],
)
def post_heartbeat(
    robot_id: str,
    body: HeartbeatRequest,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[RobotRecord]:
    _ = body
    record = store.heartbeat(robot_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=record)
