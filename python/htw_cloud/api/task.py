"""Task Management API.

Cloud may create business tasks; HTWOS edge decides local execution.
Cloud does not control local survival.
"""

from fastapi import APIRouter, Depends, HTTPException

from htw_cloud.api.deps import get_store
from htw_cloud.models.common import ApiResponse
from htw_cloud.models.robot import TaskCreateRequest, TaskRecord
from htw_cloud.store.memory import MemoryStore

router = APIRouter(tags=["task"])


@router.post(
    "/robots/{robot_id}/tasks",
    response_model=ApiResponse[TaskRecord],
)
def create_task(
    robot_id: str,
    body: TaskCreateRequest,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[TaskRecord]:
    task = store.add_task(robot_id, body)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=task)


@router.get(
    "/robots/{robot_id}/tasks",
    response_model=ApiResponse[list[TaskRecord]],
)
def list_tasks(
    robot_id: str,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[list[TaskRecord]]:
    tasks = store.list_tasks(robot_id)
    if tasks is None:
        raise HTTPException(
            status_code=404,
            detail={"code": 40401, "message": "robot not found"},
        )
    return ApiResponse(data=tasks)
