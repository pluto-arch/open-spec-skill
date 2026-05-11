# 07 Handoff 契约示例（五阶段）

## 用途

展示调度器向各阶段 Agent 传递 Handoff 包的标准格式。

示例场景：为订单服务新增"取消原因枚举 + 审计日志"。

## 阶段 1：需求分析

### Input Contract 示例

- 任务目标：产出可测试 FR/NFR，明确 In Scope / Out of Scope。
- 必读输入：业务目标（新增取消原因与审计日志），兼容约束（向后兼容），交付时限（2 周）。
- 上游引用：无（新功能）。

### Output Contract 示例

- 必交文档：`01-requirements.md`
- 必含内容：FR-001 维护取消原因枚举，FR-002 记录取消审计日志，NFR-001 写入延迟 ≤ 500ms（95 分位）
- 交接摘要：风险（历史订单兼容策略待确认），下阶段输入（FR 与验收标准）

## 阶段 2：规范制定

### Input Contract 示例

- 任务目标：将 FR 转成行为/数据/接口/异常规范。
- 必读输入：`01-requirements.md`
- 上游引用：阶段 1 handoff 摘要

### Output Contract 示例

- 必交文档：`02-specification.md`
- 必含内容：取消原因输入校验规则，审计日志字段约束，错误码与异常处理语义
- 交接摘要：兼容策略确认项，方案阶段依赖清单

## 阶段 3：方案设计

### Input Contract 示例

- 任务目标：给出可实施技术方案与回滚路径。
- 必读输入：`02-specification.md`
- 上游引用：阶段 2 handoff 摘要

### Output Contract 示例

- 必交文档：`03-technical-solution.md`，必要时 `04-storage-design.md`
- 必含内容：模块改造点（订单域 + 审计域），ADR-001（同步 vs 异步写日志），回滚触发条件
- 交接摘要：实施任务拆分建议与高风险点

## 阶段 4：开发计划

### Input Contract 示例

- 任务目标：形成 TASK 计划，为实施提供可跟踪的工作列表。
- 必读输入：`03-technical-solution.md`，`04-storage-design.md`（如有）
- 上游引用：阶段 3 handoff 摘要

### Output Contract 示例

- 必交文档：`05-development-plan.md`
- 必含内容：TASK-001 新增取消原因枚举，TASK-002 接入审计日志写入，TASK-003 兼容迁移处理
- 交接摘要：任务依赖顺序，高风险 TASK 清单

## 阶段 5：实施

### Input Contract 示例

- 任务目标：按 TASK 顺序推进实际开发，持续更新状态。
- 必读输入：`05-development-plan.md`，`03-technical-solution.md`
- 上游引用：阶段 4 handoff 摘要

### Output Contract 示例

- 产出：代码变更，更新后的 `05-development-plan.md`（TASK 状态）
- 必含内容：已完成 TASK 列表，偏差说明（如有），阻塞项（如有）

## 调度器最小委派模板

```yaml
handoff:
  from_phase: <1-5>
  phase_name: <阶段名>
  status: PASS | NEEDS_USER_INPUT
  next_phase: <2-5 或 DONE>
  artifacts:
    - path: <文档路径>
      summary: <一句话摘要>
  key_ids: <FR/ADR/TASK ID 列表>
  open_risks: <未决风险>
  next_phase_inputs: <下一阶段所需关键信息>
```
