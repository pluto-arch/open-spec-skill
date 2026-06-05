---
name: open-spec
description: "Open Spec：Spec 驱动的开发流程技能，按三个 task 推进需求变更分析、设计与开发。"
argument-hint: "描述目标功能、约束、技术栈和交付边界"
user-invocable: true
---

# Open Spec 技能

## 定位

Open Spec 是一个 Spec 驱动的开发流程技能。

执行时按三个顺序 task 推进，并在每个 task 完成后产出标准 handoff。

下文统一使用 `task` 表示工作流任务。

## 工作流

固定三个 task，依次推进：

| # | Task | 主要产出 |
|---|------|----------|
| 1 | 需求变更分析 | `00-change-request.md`（如适用）、`01-change-analysis.md` |
| 2 | 设计 | `02-technical-design.md` |
| 3 | 开发 | `03-development.md`、代码变更 |

## 执行原则

执行本技能时必须遵守：

1. **Task 识别**：根据用户输入判断进入哪个 task，默认从 task 1 开始。
2. **直接执行**：识别后立即执行当前 task，不得只解释流程。
3. **文档落盘**：每个 task 必须更新对应文档或代码。
4. **Task 推进**：当前 task `PASS` 后自动推进下一 task；`NEEDS_USER_INPUT` 时暂停。

## Task 执行规则

执行顺序固定如下：

1. 识别目标 task。
2. 检查前置输入与已有文档。
3. 组装 `task_packet`。
4. 立即执行该 task。
5. 产出或更新该 task 文档 / 代码。
6. 回收结构化 `handoff`。
7. 根据 `handoff.status` 决定继续下一 task 还是暂停。

必须完成当前 task 的实际工作。仅输出“下一步请继续做某个 task”视为未遵循本技能。

## Task Packet（执行输入包）

进入任一 task 前，必须构造统一的 `task_packet`：

```yaml
task_packet:
  task: <1-3>
  task_name: <任务名>
  objective: <本 task 目标>
  feature_slug: <feature-slug>
  user_request: <用户原始目标>
  required_inputs:
    - <文档路径或关键信息>
  upstream_handoff:
    previous_task: <START 或上游 task 编号>
    summary: <上一个 task 结论摘要>
  expected_outputs:
    - <本 task 必须更新或生成的文档>
```

`required_inputs` 的处理规则固定如下：

- 输入不完整：先列出缺失项。
- 输入完整：立即进入执行，不得停留在说明层。

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

标准回传顺序固定为 `task_result` → `handoff` → `user_questions`。`user_questions` 是独立的顶层输出结构，仅在 `status: NEEDS_USER_INPUT` 时追加在 `handoff` 之后。

## Handoff 格式

每个 task 完成后，必须输出以下标准格式的交接包：

```yaml
handoff:
  previous_task: <1-3>
  task_name: <任务名>
  status: PASS | NEEDS_USER_INPUT | BLOCKED
  next_task: <2-3 或 DONE>
  artifacts:
    - path: <文档路径>
      summary: <一句话摘要>
  key_ids: <FR-xxx / ADR-xxx / TASK-xxx 等>
  open_risks: <未决风险列表>
  next_task_inputs: <下一 task 所需的关键信息说明>
```

仅在 `status: NEEDS_USER_INPUT` 时追加的 `user_questions` 结构如下：

```yaml
# 仅在 status: NEEDS_USER_INPUT 时追加
user_questions:
  - question: <问题>
    reason: <为什么需要这个信息>
    impact: <哪个文档或决策受影响>
```

## 直接指定 Task

支持跳过已完成 task，直接从指定 task 开始。用户可以说：

- `开始需求变更分析` / `进入需求变更分析`
- `从设计开始` / `进入设计 task`
- `直接进入开发` / `开始开发 task`

收到指定 task 指令后，按以下规则执行：

1. 读取已有前置文档（如 `01-change-analysis.md`）。
2. 前置条件齐备：立即执行目标 task，并传入已有上下文。
3. 前置条件缺失：返回缺失项列表并等待用户补充。

## 信息缺口处理

统一使用三级缺口分类：

- `Blocker`：缺失后会直接影响核心决策，必须先问用户，不得继续后续 task。
- `Assumption`：可临时假设，但必须在文档中明确标注，等待后续确认。
- `Nice-to-know`：不影响当前 task 主结论，进入未决项列表。

只有 `Blocker` 会触发 `NEEDS_USER_INPUT` 状态停止流程。

## 交付目录

产出文件默认存放在 `docs/<feature-slug>/`：

- `00-change-request.md`（可选，变更场景）
- `01-change-analysis.md`（需求变更分析）
- `02-technical-design.md`（设计主文档，如适用时包含存储设计内容）
- `03-development.md`（开发任务、实施进展、验证记录）
- `08-task-handoff.md`（可选，任务交接记录存档）

## 快速调用示例（三种入口）

```text
/open-spec 为订单服务新增取消原因与审计日志，技术栈 ASP.NET Core + PostgreSQL
/open-spec 从设计开始，分析文档已就绪
/open-spec 直接进入开发，按现有设计推进
```
