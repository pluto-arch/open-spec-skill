# 04 Handoff 契约示例（三阶段）

## 用途

展示当前 Agent 在各 task 间传递 `task_packet`，以及 task 完成后回传 `stage_result + handoff` 的标准格式。

示例场景：为订单服务新增“取消原因枚举 + 审计日志”。

## 阶段 1：需求变更分析

### Input Contract 示例

- 任务目标：产出变更分析、影响范围与可测试 FR/NFR。
- 必读输入：业务目标（新增取消原因与审计日志），兼容约束（向后兼容），交付时限（2 周）。
- 上游引用：无（新功能）。

### Task Packet 示例

```yaml
task_packet:
  stage: 1
  stage_name: 需求变更分析
  objective: 产出变更范围、FR/NFR 与验收标准
  user_request: 为订单服务新增取消原因枚举 + 审计日志
  required_inputs:
    - 向后兼容
    - 2 周交付
  upstream_handoff:
    from_phase: START
    summary: 新功能，从需求变更分析启动
  expected_outputs:
    - docs/order-cancel/00-change-request.md
    - docs/order-cancel/01-change-analysis.md
```

### Output Contract 示例

- 必交文档：`01-change-analysis.md`
- 必含内容：影响模块、FR-001 维护取消原因枚举，FR-002 记录取消审计日志，NFR-001 写入延迟 ≤ 500ms（95 分位）
- 交接摘要：风险（历史订单兼容策略待确认），下阶段输入（影响范围、FR 与验收标准）

### Stage Result 示例

```yaml
stage_result:
  status: PASS
  completed_work:
    - 明确范围边界
    - 识别受影响文档与模块
    - 产出 2 条 FR 和 1 条 NFR
  updated_artifacts:
    - path: docs/order-cancel/01-change-analysis.md
      summary: 完成变更分析初稿
  blockers: []
```

## 阶段 2：设计

### Input Contract 示例

- 任务目标：将变更分析落成可实施设计。
- 必读输入：`01-change-analysis.md`
- 上游引用：阶段 1 handoff 摘要

### Output Contract 示例

- 必交文档：`02-technical-design.md`，必要时 `02-storage-design.md`
- 必含内容：模块改造点（订单域 + 审计域），ADR-001（同步 vs 异步写日志），回滚触发条件
- 交接摘要：开发任务拆分建议与高风险点

## 阶段 3：开发

### Input Contract 示例

- 任务目标：形成开发任务并推进实际开发，持续更新状态。
- 必读输入：`02-technical-design.md`，`02-storage-design.md`（如有）
- 上游引用：阶段 2 handoff 摘要

### Output Contract 示例

- 产出：代码变更，更新后的 `03-development.md`（TASK 状态）
- 必含内容：已完成 TASK 列表，偏差说明（如有），阻塞项（如有）

## 最小模板

```yaml
task_packet:
  stage: <1-3>
  stage_name: <阶段名>
  objective: <本阶段目标>
  user_request: <用户请求>
  required_inputs:
    - <文档或关键信息>
  upstream_handoff:
    from_phase: <START 或上阶段编号>
    summary: <上游结论摘要>
  expected_outputs:
    - <产出文件>

stage_result:
  status: PASS | NEEDS_USER_INPUT | BLOCKED | PARTIAL
  completed_work:
    - <已完成动作>
  updated_artifacts:
    - path: <文档路径>
      summary: <更新摘要>
  blockers:
    - <阻塞项>

handoff:
  from_phase: <1-3>
  phase_name: <阶段名>
  status: PASS | NEEDS_USER_INPUT
  next_phase: <2-3 或 DONE>
  artifacts:
    - path: <文档路径>
      summary: <一句话摘要>
  key_ids: <FR/ADR/TASK ID 列表>
  open_risks: <未决风险>
  next_phase_inputs: <下一阶段所需关键信息>
```
