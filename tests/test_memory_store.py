"""Unit tests for MemoryStore."""

from htw_cloud.models.robot import RobotRegisterRequest
from htw_cloud.store.memory import MemoryStore


def test_register_and_get() -> None:
    store = MemoryStore()
    record = store.register(
        RobotRegisterRequest(product_id="p1", hardware_version="h1")
    )
    robot_id = record.identity.robot_id
    assert store.get(robot_id) is not None
    assert store.get("nope") is None
