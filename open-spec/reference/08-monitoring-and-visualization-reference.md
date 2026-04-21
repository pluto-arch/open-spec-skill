# 08 执行监控与可视化参考

## 目标

通过事件日志 + 本地 Web 仪表盘监控 Open Spec 的阶段执行状态、门禁结果和进度变化。

## 组成

- 事件写入脚本：`scripts/emit_event.py`
- 可视化服务：`scripts/workflow_monitor_server.py`
- 一键启动（PowerShell）：`scripts/start_monitor.ps1`
- 前端资源目录：`scripts/wwwroot/`（`index.html` + `app.js` + `styles.css`，ReactJS）
- 默认日志：`docs/open-spec/telemetry/events.jsonl`

## 快速启动

1. 启动监控 WebHost

```powershell
./skills/open-spec/scripts/start_monitor.ps1
```

可选：指定自定义静态目录

```powershell
python ./skills/open-spec/scripts/workflow_monitor_server.py --static-dir ./skills/open-spec/scripts/wwwroot
```

2. 打开仪表盘

- `http://127.0.0.1:8765`

3. 发送一条测试事件

```powershell
python ./skills/open-spec/scripts/emit_event.py `
  --feature order-cancel-audit `
  --stage requirements `
  --role open-spec-requirements `
  --event stage_start `
  --status in_progress `
  --progress 10 `
  --message "需求阶段开始"
```

## 推荐埋点时机

- 每阶段开始：`event=stage_start`
- 每阶段结束：`event=stage_end`
- TASK 状态变化：`event=task_update`
- 门禁结果：`event=gate_result`
- 失败回退：`event=rollback`

## 推荐字段约束

- `feature`：feature slug
- `stage`：requirements/spec/solution/implementation/testing/release
- `role`：open-spec-\* 角色标识
- `status`：in_progress/completed/failed/info
- `progress`：0-100
- `ids`：逗号分隔的 FR/TASK/TC/CR/REV

## 与工作流协同

Workflow Lead 可在每次委派和验收时追加事件，形成一条可回放的执行轨迹。

建议最小集：

- 委派前写 `stage_start`
- 子 Agent 完成写 `stage_end`
- 门禁判定写 `gate_result`
- 失败修复写 `rollback`

## 注意事项

- 该监控是本地可视化，不自动上传外部服务。
- 日志文件为 JSONL，可直接纳入后续分析脚本。
- 若要长期保留，可按日期轮转日志文件。
