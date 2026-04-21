# 07 Handoff 契约示例（全阶段）

## 用途

本示例用于展示 Workflow Lead 向子 Agent 委派时，如何按 `Input Contract` / `Output Contract` 组织最小必要上下文。

示例场景：为订单服务新增“取消原因枚举 + 审计日志”。

## 阶段 1：需求分析（open-spec-requirements）

### Input Contract 示例

- 任务目标：产出可测试 FR/NFR，并明确 In Scope / Out of Scope。
- 必读输入：业务目标（新增取消原因与审计日志），兼容约束（向后兼容），交付时限（2 周）。
- 上游引用：无（新功能）。
- 输出约束：FR/NFR 需编号并可验证。

### Output Contract 示例

- 必交文档：`01-requirements.md`。
- 必含内容：
  - FR-001 维护取消原因枚举
  - FR-002 记录取消审计日志
  - NFR-001 写入延迟 <= 500ms
- 追溯锚点：FR-001/FR-002/NFR-001
- 交接摘要：风险（历史订单兼容策略待确认）、下阶段输入（FR 与验收标准）。

## 阶段 2：规范制定（open-spec-spec）

### Input Contract 示例

- 任务目标：将 FR 转成行为/数据/接口/异常规范。
- 必读输入：`01-requirements.md`。
- 上游引用：阶段 1 handoff 摘要。
- 输出约束：规范覆盖 FR 且异常语义明确。

### Output Contract 示例

- 必交文档：`02-specification.md`。
- 必含内容：
  - 取消原因输入校验规则
  - 审计日志字段约束
  - 错误码与异常处理语义
- 追溯锚点：FR-001/FR-002/AC-001/AC-002
- 交接摘要：兼容策略确认项、方案阶段依赖清单。

## 阶段 3：方案设计（open-spec-solution）

### Input Contract 示例

- 任务目标：给出可实施技术方案与回滚路径。
- 必读输入：`02-specification.md`。
- 上游引用：阶段 2 handoff 摘要。
- 输出约束：模块边界、ADR、回滚策略必须可执行。

### Output Contract 示例

- 必交文档：`03-technical-solution.md`，必要时 `04-storage-design.md`。
- 必含内容：
  - 模块改造点（订单域 + 审计域）
  - ADR-001（同步写日志 vs 异步写日志）
  - 回滚触发条件与步骤
- 追溯锚点：FR-001/FR-002/ADR-001
- 交接摘要：实施阶段任务拆分建议与高风险点。

## 阶段 4：计划与实施（open-spec-implementer）

### Input Contract 示例

- 任务目标：形成 TASK 计划并推进实现，持续更新状态。
- 必读输入：`03-technical-solution.md`、`04-storage-design.md`（如有）。
- 上游引用：阶段 3 handoff 摘要。
- 输出约束：每个 TASK 必须映射 FR，且状态可追踪。

### Output Contract 示例

- 必交文档：`05-development-plan.md`。
- 必含内容：
  - TASK-001 新增取消原因枚举
  - TASK-002 接入审计日志写入
  - TASK-003 补齐兼容迁移处理
  - 每个 TASK 的状态/完成度/偏差说明
- 追溯锚点：TASK-001..003 对应 FR-001/FR-002
- 交接摘要：已完成 TASK、阻塞 TASK、偏差与纠偏动作。

## 阶段 5：测试与验证（open-spec-qa）

### Input Contract 示例

- 任务目标：验证实现满足 FR/TASK/规范。
- 必读输入：`01-requirements.md`、`02-specification.md`、`05-development-plan.md`。
- 上游引用：阶段 4 handoff 摘要。
- 输出约束：TC 需覆盖主路径、异常路径、边界与回归。

### Output Contract 示例

- 必交文档：`06-test-cases.md`。
- 必含内容：
  - TC-001 正常取消并写入日志
  - TC-002 非法取消原因校验失败
  - TC-003 历史订单兼容回归验证
- 追溯锚点：TC-001..003 -> FR/TASK
- 交接摘要：验收结论、未关闭风险、发布建议。

## 阶段 6：发布与复盘（open-spec-release）

### Input Contract 示例

- 任务目标：完成发布决策和复盘改进闭环。
- 必读输入：`06-test-cases.md`、`05-development-plan.md`。
- 上游引用：阶段 5 handoff 摘要。
- 输出约束：发布步骤、监控与回滚条件必须可执行。

### Output Contract 示例

- 必交文档：`07-release-retrospective.md`。
- 必含内容：
  - 发布范围与影响面
  - 回滚触发条件（错误率阈值、延迟阈值）
  - 复盘改进动作（owner + deadline）
- 追溯锚点：CR/REV/TC/风险项
- 交接摘要：最终发布结论、遗留风险、下一轮行动项。

## Workflow Lead 最小委派模板

可直接复制：

- 角色：<open-spec-\*>
- 阶段：<需求/规范/方案/计划与实施/测试/发布复盘>
- 任务目标：<一句话>
- 必读输入：<文档列表>
- 上游摘要：<上阶段 3-5 条增量>
- 输出要求：<必交文档 + 必含字段 + ID 锚点>
- 门禁标准：<PASS/FAIL 条件>
- 交接要求：更新 `08-stage-handoff.md` + 当日 memory 增量
