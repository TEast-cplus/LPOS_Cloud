# HTW Cloud 最小框架设计

**日期:** 2026-11-24  
**仓库:** LPOS_Cloud（独立 Git，与 HTWOS Edge / SDK 解耦）  
**状态:** 已批准（方案 1 · 首期范围 A）

## 1. 目标

在 `LPOS_Cloud` 内搭建 **HTW Cloud** 可本地启动的最小骨架：统一机器人数据模型、六类 HTTPS API stub、内存存储、C++ 协议占位库。不引入真实 MQTT、数据库、Web 控制台。

## 2. 原则（来自总体构建）

云端可以：查询状态、下发业务任务、调整允许远程修改的参数、发布升级任务、收集日志与故障。

云端不可以：绕过本地安全策略控制电机；断网导致机器人无法安全运行；直接操作底层寄存器；未经版本检查强制升级 Provider/MCU。

代码与注释中固定表达：**云端不控制本地生存**。

## 3. 技术选型

| 层级 | 技术 |
|------|------|
| 主语言 | Python 3.11+ |
| HTTP | FastAPI + Pydantic v2 + Uvicorn |
| 配置 | YAML（`configs/default.yaml`） |
| 存储（首期） | 进程内内存仓库 |
| 辅语言 | C++20 + CMake（仅占位库） |
| 测试 | pytest + httpx |

## 4. 仓库结构

```
LPOS_Cloud/
├── README.md
├── requirements.txt
├── pyproject.toml
├── configs/default.yaml
├── python/htw_cloud/
│   ├── __init__.py
│   ├── main.py              # uvicorn 入口
│   ├── app.py               # FastAPI 组装
│   ├── config.py
│   ├── models/robot.py      # 统一机器人数据模型
│   ├── api/                 # 六类路由
│   │   ├── registration.py
│   │   ├── heartbeat.py
│   │   ├── status.py
│   │   ├── task.py
│   │   ├── ota.py
│   │   └── diagnostics.py
│   └── store/memory.py
├── tests/
├── cpp/                     # C++ 占位，不参与 Python 运行
│   ├── CMakeLists.txt
│   ├── include/htw_cloud/
│   └── src/
└── docs/superpowers/
```

## 5. 数据模型

对应总体构建第十章：

- `Identity`：`robot_id`, `product_id`, `hardware_version`
- `Platform`：`soc`, `os_version`, `htwos_version`
- `Devices`：`camera`, `imu`, `motor`, `npu`（字符串状态摘要，首期不深挖）
- `Runtime`：`service_status`, `task_status`, `model_status`
- `Diagnostics`：`cpu`, `memory`, `temperature`, `faults`

聚合类型：`RobotRecord`（注册信息 + 最近心跳 + 状态快照）。

## 6. 六类 API（`/api/v1`）

| 模块 | 方法与路径 | 行为（stub） |
|------|------------|--------------|
| Device Registration | `POST /robots/register` | 写入内存，返回 `robot_id` |
| Heartbeat | `POST /robots/{robot_id}/heartbeat` | 更新 last_seen |
| Device Status | `GET/PUT /robots/{robot_id}/status` | 读/写状态快照 |
| Task Management | `POST/GET /robots/{robot_id}/tasks` | 创建/列出任务（不下发到端） |
| OTA Management | `POST/GET /robots/{robot_id}/ota` | 创建/查询升级任务（不强制安装） |
| Diagnostics | `POST/GET /robots/{robot_id}/diagnostics` | 上报/查询诊断 |

另：`GET /health` 健康检查。

统一响应包络：`{ "code": 0, "message": "ok", "data": ... }`；未找到机器人 `code=40401`。

## 7. 数据流

1. 机器人（或模拟客户端）`POST /robots/register` → 内存 store。
2. 周期 `heartbeat` → 更新存活时间。
3. `status` / `diagnostics` 上报；云端 `GET` 查询。
4. 云端创建 `task` / `ota` 记录；**首期不推送到端侧**（为后续 MQTT 留扩展点）。

## 8. 错误处理

- Pydantic 校验失败 → HTTP 422。
- 业务：机器人不存在 → HTTP 404 + 业务码。
- 不在 stub 中实现鉴权；配置预留 `auth_enabled: false`。

## 9. C++ 占位

- 命名空间 `Hantewin::HtwCloud`
- 头文件：错误码枚举、与 Python 对齐的基础类型声明（占位）
- 静态库目标 `htw_cloud_protocol`，可空实现
- 遵循 hantewin C++ 命名/排版/注释规范

## 10. 非目标（首期不做）

真实 MQTT、DB、Redis、鉴权、Web UI、Cloud Agent、与 LPOS/LPOS_SDK 代码依赖、强制 OTA。

## 11. 验收

1. `pip install -r requirements.txt` 后 `python -m htw_cloud.main` 可启动。
2. OpenAPI：`/docs` 可见六类接口。
3. pytest 覆盖注册→心跳→状态→任务→OTA→诊断主路径。
4. `cpp/` 可独立 `cmake` 配置（允许无安装依赖时跳过构建）。
5. 仓库无对 Edge/SDK 源码树的硬依赖。
