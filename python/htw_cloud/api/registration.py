"""Device Registration API."""

from fastapi import APIRouter, Depends

from htw_cloud.api.deps import get_store
from htw_cloud.models.common import ApiResponse
from htw_cloud.models.robot import RobotRecord, RobotRegisterRequest
from htw_cloud.store.memory import MemoryStore

router = APIRouter(tags=["registration"])


@router.post("/robots/register", response_model=ApiResponse[RobotRecord])
def register_robot(
    body: RobotRegisterRequest,
    store: MemoryStore = Depends(get_store),
) -> ApiResponse[RobotRecord]:
    record = store.register(body)
    return ApiResponse(data=record)
