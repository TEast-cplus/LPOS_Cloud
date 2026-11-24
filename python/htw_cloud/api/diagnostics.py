"""Diagnostics API."""

from fastapi import APIRouter, Depends, HTTPException

from htw_cloud.api.deps import get_store
from htw_cloud.models.common import ApiResponse
from htw_cloud.models.robot import DiagnosticsInfo
from htw_cloud.store.memory import MemoryStore

router = APIRouter(tags=["diagnostics"])


@router.post(
    "/robots/{robot_id}/diagnostics",
    response_model=ApiResponse[DiagnosticsInfo],
)
def post_diagnostics(
    robot_id: str,
    body: DiagnosticsInfo,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[DiagnosticsInfo]:
    info = store.add_diagnostics(robot_id, body)
    if info is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=info)


@router.get(
    "/robots/{robot_id}/diagnostics",
    response_model=ApiResponse[list[DiagnosticsInfo]],
)
def get_diagnostics(
    robot_id: str,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[list[DiagnosticsInfo]]:
    history = store.get_diagnostics(robot_id)
    if history is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=history)
