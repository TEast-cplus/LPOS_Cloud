# HTW Cloud Minimal Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在独立仓库 LPOS_Cloud 落地可本地启动的 HTW Cloud 最小骨架（FastAPI 六类 API stub + 内存 store + C++ 占位库）。

**Architecture:** 单体 FastAPI 应用，按六类 API 分路由模块；进程内 MemoryStore；C++ 仅 CMake 静态库占位，不参与 Python 运行时。

**Tech Stack:** Python 3.11+、FastAPI、Pydantic v2、Uvicorn、PyYAML、pytest、httpx；C++20、CMake。

## Global Constraints

- 仓库独立：仅改 `LPOS_Cloud`，不依赖 LPOS / LPOS_SDK 源码。
- Python 为主；C++ 为辅且首期仅占位。
- 云端不控制本地生存：OTA/任务只存记录，不强制端侧执行。
- API 前缀 `/api/v1`；响应包络 `code/message/data`。
- C++ 遵循 hantewin 命名/排版/注释；作者 `HTW_DEV`，日期 `2026-11-24`。

---

### Task 1: 工程元数据与配置

**Files:**
- Create: `requirements.txt`
- Create: `pyproject.toml`
- Create: `configs/default.yaml`
- Create: `python/htw_cloud/__init__.py`
- Create: `python/htw_cloud/config.py`
- Modify: `README.md`

**Interfaces:**
- Produces: `load_config(path: str | None) -> AppConfig`；`AppConfig` 含 `host`, `port`, `auth_enabled`

- [ ] **Step 1: 写入依赖与包元数据**
- [ ] **Step 2: 写入 default.yaml 与 config 加载**
- [ ] **Step 3: 更新 README 启动说明**

### Task 2: 数据模型与内存仓库

**Files:**
- Create: `python/htw_cloud/models/__init__.py`
- Create: `python/htw_cloud/models/robot.py`
- Create: `python/htw_cloud/models/common.py`
- Create: `python/htw_cloud/store/__init__.py`
- Create: `python/htw_cloud/store/memory.py`

**Interfaces:**
- Produces: Pydantic 模型 Identity/Platform/Devices/RuntimeInfo/DiagnosticsInfo/RobotRecord；`MemoryStore` 的 register/get/heartbeat/update_status/add_task/list_tasks/add_ota/list_ota/add_diagnostics/get_diagnostics

- [ ] **Step 1: 定义模型与 ApiResponse**
- [ ] **Step 2: 实现 MemoryStore**
- [ ] **Step 3: 单元测试 store**

### Task 3: 六类 API 路由与应用组装

**Files:**
- Create: `python/htw_cloud/api/*.py`（含 `__init__.py`）
- Create: `python/htw_cloud/app.py`
- Create: `python/htw_cloud/main.py`
- Create: `tests/test_api_flow.py`

**Interfaces:**
- Consumes: MemoryStore、模型、ApiResponse
- Produces: FastAPI `create_app()`；`GET /health`；六类路由

- [ ] **Step 1: 实现六类 router**
- [ ] **Step 2: create_app + main**
- [ ] **Step 3: pytest 主路径**

### Task 4: C++ 协议占位库

**Files:**
- Create: `cpp/CMakeLists.txt`
- Create: `cpp/include/htw_cloud/error_code.h`
- Create: `cpp/include/htw_cloud/robot_identity.h`
- Create: `cpp/src/error_code.cpp`

**Interfaces:**
- Produces: 命名空间 `Hantewin::HtwCloud`；枚举 `HTW_CLOUD_ERROR_E`；结构 `ROBOTIDENTITY_T`；库目标 `htw_cloud_protocol`

- [ ] **Step 1: 头文件与空实现**
- [ ] **Step 2: CMakeLists 可配置**

### Task 5: 验收

- [ ] **Step 1: pytest 全绿**
- [ ] **Step 2: 启动 uvicorn 并 curl /health**
