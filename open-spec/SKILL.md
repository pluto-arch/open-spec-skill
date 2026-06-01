---
name: open-spec
description: "Open Spec：Spec 驱动的开发流程技能，按三个 task 推进需求变更分析、设计与开发。"
argument-hint: "描述目标功能、约束、技术栈和交付边界"
user-invocable: true
---

# Open Spec 技能

## 定位

Open Spec 是一个 Spec 驱动的开发流程技能。

它不再依赖 subagent。执行时始终由当前 Agent 直接推进三个顺序 task，并在每个 task 完成后产出标准 handoff。

## 工作流

固定三个 task，依次推进：

| # | 阶段 | 执行方式 | 主要产出 |
|---|------|----------|----------|
| 1 | 需求变更分析 | 当前 Agent 的 task 1 | `00-change-request.md`（如适用）、`01-change-analysis.md` |
| 2 | 设计 | 当前 Agent 的 task 2 | `02-technical-design.md` |
| 3 | 开发 | 当前 Agent 的 task 3 | `03-development.md`、代码变更 |

## 执行原则

执行本技能时必须遵守：

1. **阶段识别**：根据用户输入判断进入哪个 task，默认从 task 1 开始。
2. **直接执行**：识别后立即执行当前 task，不得只解释流程。
3. **文档落盘**：每个 task 必须更新对应文档或代码。
4. **阶段推进**：当前 task `PASS` 后自动推进下一 task；`NEEDS_USER_INPUT` 时暂停。
5. **禁止 subagent**：不要加载、切换、模拟或引用任何 subagent 机制。

## Task 执行规则

执行顺序固定如下：

1. 识别目标 task。
2. 检查前置输入与已有文档。
3. 组装 `task_packet`。
4. 在当前会话内立即执行该 task。
5. 产出或更新该 task 文档 / 代码。
6. 回收结构化 `handoff`。
7. 根据 `handoff.status` 决定继续下一阶段还是暂停。

如果只是输出“下一步请继续做某个 task”而没有完成该 task 的实际工作，视为未遵循本技能。

## Task Packet（执行输入包）

进入任一 task 前，必须构造统一的 `task_packet`：

```yaml
task_packet:
  task: <1-3>
  task_name: <阶段名>
  objective: <本阶段目标>
  feature_slug: <feature-slug>
  user_request: <用户原始目标>
  required_inputs:
    - <文档路径或关键信息>
  upstream_handoff:
    previous_task: <START 或上游 task 编号>
    summary: <上阶段结论摘要>
  expected_outputs:
    - <本阶段必须更新或生成的文档>
```

`required_inputs` 不足时，必须先列出缺失项；满足时必须立即进入执行，不得停留在说明层。

## Task Execution Record（任务执行回传）

每个 task 完成后，必须按以下顺序回传，便于继续流转：

```yaml
task_result:
  status: PASS | NEEDS_USER_INPUT | BLOCKED | PARTIAL
  completed_work:
    - <本轮完成的动作>
  updated_artifacts:
    - path: <文件路径>
      summary: <更新摘要>
  blockers:
    - <阻塞项，没有则空>
```

然后再输出标准 `handoff`；若需用户补充，再附 `user_questions`。

## Handoff 格式

每个阶段完成后，必须输出以下标准格式的交接包：

```yaml
handoff:
  previous_task: <1-3>
  task_name: <阶段名>
  status: PASS | NEEDS_USER_INPUT | BLOCKED
  next_task: <2-3 或 DONE>
  artifacts:
    - path: <文档路径>
      summary: <一句话摘要>
  key_ids: <FR-xxx / ADR-xxx / TASK-xxx 等>
  open_risks: <未决风险列表>
  next_task_inputs: <下一阶段所需的关键信息说明>
```

若 `status: NEEDS_USER_INPUT`，附加：

```yaml
user_questions:
  - question: <问题>
    reason: <为什么需要这个信息>
    impact: <哪个文档或决策受影响>
```

## 直接指定阶段

支持跳过已完成阶段，直接从某阶段开始。用户可以说：

- `开始需求变更分析` / `进入分析阶段`
- `从设计开始` / `进入技术设计`
- `直接进入开发` / `开始落地开发`

收到指定阶段指令后：

1. 读取已有前置文档（如 `01-change-analysis.md`）。
2. 若前置条件满足，立即执行目标 task，并传入已有上下文。
3. 若前置条件不满足，返回缺失项列表并等待用户补充。

## 信息缺口处理

统一使用三级缺口分类：

- `Blocker`：缺失后会直接影响核心决策，必须先问用户，不得继续后续阶段。
- `Assumption`：可临时假设，但必须在文档中明确标注，等待后续确认。
- `Nice-to-know`：不影响当前阶段主结论，进入未决项列表。

只有 `Blocker` 会触发 `NEEDS_USER_INPUT` 状态停止流程。

## 交付目录

产出文件默认存放在 `docs/<feature-slug>/`：

- `00-change-request.md`（可选，变更场景）
- `01-change-analysis.md`（需求变更分析）
- `02-technical-design.md`（设计主文档，包含存储设计内容）
- `03-development.md`（开发任务、实施进展、验证记录）
- `08-handoff.md`（可选，阶段交接记录存档）

## 快速调用示例

以下示例分别对应默认起步、从设计续跑、以及直接进入开发三种常见用法：

```text
/open-spec 为订单服务新增取消原因与审计日志，技术栈 ASP.NET Core + PostgreSQL
/open-spec 从设计开始，分析文档已就绪
/open-spec 直接进入开发，按现有设计推进
```
