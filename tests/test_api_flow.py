"""End-to-end stub flow: register → heartbeat → status → task → ota → diagnostics."""

from fastapi.testclient import TestClient

from htw_cloud.app import create_app


def test_full_api_flow() -> None:
    client = TestClient(create_app())

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["code"] == 0

    reg = client.post(
        "/api/v1/robots/register",
        json={
            "product_id": "htw-bot-demo",
            "hardware_version": "v1",
            "platform": {
                "soc": "rk3588",
                "os_version": "ubuntu-22.04",
                "htwos_version": "0.1.0",
            },
        },
    )
    assert reg.status_code == 200
    robot_id = reg.json()["data"]["identity"]["robot_id"]
    assert robot_id

    hb = client.post(
        f"/api/v1/robots/{robot_id}/heartbeat",
        json={"seq": 1},
    )
    assert hb.status_code == 200
    assert hb.json()["data"]["last_seen"] is not None

    put_status = client.put(
        f"/api/v1/robots/{robot_id}/status",
        json={
            "runtime": {
                "service_status": "running",
                "task_status": "idle",
                "model_status": "ready",
            }
        },
    )
    assert put_status.status_code == 200

    get_status = client.get(f"/api/v1/robots/{robot_id}/status")
    assert get_status.status_code == 200
    assert get_status.json()["data"]["runtime"]["service_status"] == "running"

    task = client.post(
        f"/api/v1/robots/{robot_id}/tasks",
        json={"task_type": "patrol", "payload": {"zone": "A"}},
    )
    assert task.status_code == 200
    assert task.json()["data"]["status"] == "created"

    tasks = client.get(f"/api/v1/robots/{robot_id}/tasks")
    assert tasks.status_code == 200
    assert len(tasks.json()["data"]) == 1

    ota = client.post(
        f"/api/v1/robots/{robot_id}/ota",
        json={
            "target": "app",
            "version": "1.0.1",
            "package_url": "https://example.invalid/pkg",
        },
    )
    assert ota.status_code == 200
    assert ota.json()["data"]["status"] == "pending"

    diag = client.post(
        f"/api/v1/robots/{robot_id}/diagnostics",
        json={
            "cpu": 12.5,
            "memory": 40.0,
            "temperature": 55.0,
            "faults": [],
        },
    )
    assert diag.status_code == 200

    history = client.get(f"/api/v1/robots/{robot_id}/diagnostics")
    assert history.status_code == 200
    assert len(history.json()["data"]) == 1


def test_robot_not_found() -> None:
    client = TestClient(create_app())
    resp = client.post(
        "/api/v1/robots/missing/heartbeat", json={"seq": 0}
    )
    assert resp.status_code == 404
