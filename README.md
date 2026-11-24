# LPOS_Cloud / HTW Cloud

HTW Cloud 云端产品独立仓库：设备注册、心跳、状态、任务、OTA、诊断的 **最小可运行骨架**。

与 HTWOS Edge（`LPOS`）、SDK（`LPOS_SDK`）**无源码依赖**；仅通过 HTTPS API / 后续 MQTT 协议协同。原则：**云端不控制本地生存**。

## 技术栈

- **主：** Python 3.11+ · FastAPI · Pydantic v2 · Uvicorn
- **辅：** C++20 协议占位库（`cpp/`，不参与 Python 运行时）

## 快速启动

```bash
cd LPOS_Cloud
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .

python -m htw_cloud.main
```

- 健康检查：`GET http://127.0.0.1:8080/health`
- OpenAPI：`http://127.0.0.1:8080/docs`
- 配置：`configs/default.yaml`

## 六类 API（`/api/v1`）

| 能力 | 路径 |
|------|------|
| Device Registration | `POST /robots/register` |
| Heartbeat | `POST /robots/{robot_id}/heartbeat` |
| Device Status | `GET|PUT /robots/{robot_id}/status` |
| Task Management | `GET|POST /robots/{robot_id}/tasks` |
| OTA Management | `GET|POST /robots/{robot_id}/ota` |
| Diagnostics | `GET|POST /robots/{robot_id}/diagnostics` |

## 测试

```bash
pytest -q
```

## C++ 占位库

```bash
cd cpp
cmake -B build
cmake --build build
```

## 文档

- 设计：`docs/superpowers/specs/2026-11-24-htw-cloud-framework-design.md`
- 计划：`docs/superpowers/plans/2026-11-24-htw-cloud-framework.md`
