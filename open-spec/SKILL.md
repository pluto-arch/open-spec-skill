---
name: open-spec
description: "Open Spec：Spec 驱动的开发流程编排技能，按五个阶段推进从需求到实施的交付闭环。"
argument-hint: "描述目标功能、约束、技术栈和交付边界"
user-invocable: true
---

# Open Spec 技能

## 定位

Open Spec 是一个 Spec 驱动的开发流程编排器。调度器按阶段将任务派发到对应 Agent，减少单一长上下文导致的质量下降。

## 工作流

固定五阶段，依次推进：

| # | 阶段     | Agent 文件                              | 主要产出                     |
|---|----------|-----------------------------------------|------------------------------|
| 1 | 需求分析 | `agents/01-requirements.agent.md`       | `01-requirements.md`         |
| 2 | 规范制定 | `agents/02-specification.agent.md`      | `02-specification.md`        |
| 3 | 方案设计 | `agents/03-solution-design.agent.md`    | `03-technical-solution.md`   |
| 4 | 开发计划 | `agents/04-development-plan.agent.md`   | `05-development-plan.md`     |
| 5 | 实施     | `agents/05-implementation.agent.md`     | 代码变更 + 任务状态           |

## 调度器职责

调度器（本文件定义的角色）负责：

1. **阶段识别**：根据用户输入判断进入哪个阶段，默认从阶段 1 开始，支持直接指定阶段。
2. **交接准备**：将前置阶段产出和当前阶段所需信息打包成 Handoff，传递给目标阶段 Agent。
3. **产出收集**：接收 Agent 输出，验证门禁状态。
4. **阶段推进**：当前阶段 `PASS` 后自动推进到下一阶段；遇到 `NEEDS_USER_INPUT` 时先等待用户补齐信息，不得跳过。

## 调度执行规则（必须真正执行）

调度器不能只“识别阶段”或只“告诉用户下一步该找哪个 Agent”。当阶段已确定且前置条件满足时，必须真正执行对应阶段 Agent 的任务。

固定执行顺序：

1. 识别目标阶段。
2. 读取对应 Agent 文件。
3. 组装 `dispatch_packet`。
4. 立即按该 Agent 的角色和步骤执行当前阶段任务。
5. 产出或更新该阶段文档。
6. 回收结构化 `handoff`。
7. 根据 `handoff.status` 决定继续下一阶段还是暂停。

如果只是输出“请切换到某个 Agent”但没有实际完成阶段任务，视为未遵循本技能。

## 兼容性说明

本技能设计为工具无关，支持两种执行模式，且两种模式都必须真正完成阶段执行：

- **原生子 Agent 模式**：如果工具支持子 Agent / 子会话 / Agent 切换，调度器直接加载 `agents/` 目录下对应的 Agent 文件并传入 `dispatch_packet`。
- **内联执行模式**：如果工具不支持子 Agent，调度器必须先读取对应 `agents/*.agent.md` 文件，然后在当前会话内“切换为该阶段 Agent 的角色”继续执行，完成阶段产出后再回到调度器身份继续调度。

只有在工具既不能调用子 Agent、也不能读取阶段 Agent 文件时，才允许退化为向用户展示手动执行说明。

默认优先级：

1. 原生子 Agent 模式
2. 内联执行模式
3. 用户手动执行说明（仅最后兜底）

因此，对大多数 AI coding 工具，本技能的标准行为应是：

- **能自动执行就自动执行**
- **不能起子会话就内联执行**
- **不要把“手动切换 Agent”当成默认路径**

## Dispatch Packet（调度输入包）

调度器在进入任一阶段前，必须构造并传入统一的 `dispatch_packet`：

```yaml
dispatch_packet:
  stage: <1-5>
  stage_name: <阶段名>
  agent_file: <agents/*.agent.md>
  objective: <本阶段目标>
  feature_slug: <feature-slug>
  user_request: <用户原始目标>
  required_inputs:
    - <文档路径或关键信息>
  upstream_handoff:
    from_phase: <上阶段编号或 START>
    summary: <上阶段结论摘要>
  expected_outputs:
    - <本阶段必须更新或生成的文档>
  execution_mode: native_subagent | inline
```

`required_inputs` 不足时，调度器必须先列出缺失项；满足时必须立即进入执行，不得停留在说明层。

## Stage Execution Record（阶段执行回传）

每个阶段 Agent 执行完成后，必须按以下顺序回传，便于调度器继续流转：

```yaml
stage_result:
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

每个阶段完成后，调度器必须输出以下标准格式的交接包：

```yaml
handoff:
  from_phase: <1-5>
  phase_name: <阶段名>
  status: PASS | NEEDS_USER_INPUT | BLOCKED
  next_phase: <2-5 或 DONE>
  artifacts:
    - path: <文档路径>
      summary: <一句话摘要>
  key_ids: <FR-xxx / ADR-xxx / TASK-xxx 等>
  open_risks: <未决风险列表>
  next_phase_inputs: <下一阶段所需的关键信息说明>
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

- `开始需求分析` / `进入需求阶段`
- `进入规范制定` / `开始写规范`
- `从方案设计开始` / `进入技术方案`
- `开发计划阶段` / `开始任务拆解`
- `直接进入实施` / `按任务开始开发`

调度器收到指定阶段指令后：

1. 读取已有前置文档（如 `01-requirements.md`）。
2. 若前置条件满足，立即执行目标阶段 Agent（原生子 Agent 或内联执行），并传入已有上下文。
3. 若前置条件不满足，返回缺失项列表并等待用户补充。

## 信息缺口处理

调度器和各阶段 Agent 统一使用三级缺口分类：

- `Blocker`：缺失后会直接影响核心决策，必须先问用户，不得继续后续阶段。
- `Assumption`：可临时假设，但必须在文档中明确标注，等待后续确认。
- `Nice-to-know`：不影响当前阶段主结论，进入未决项列表。

只有 `Blocker` 会触发 `NEEDS_USER_INPUT` 状态停止流程。

## 交付目录

产出文件默认存放在 `docs/<feature-slug>/`：

- `01-requirements.md`（需求分析）
- `02-specification.md`（规范制定）
- `03-technical-solution.md`（方案设计，含存储设计或标注 N/A）
- `04-storage-design.md`（可选，涉及存储时单独输出）
- `05-development-plan.md`（开发计划 + 实施进度）
- `08-handoff.md`（可选，阶段交接记录存档）

## 快速调用示例

```
/open-spec 为订单服务新增取消原因与审计日志，技术栈 ASP.NET Core + PostgreSQL
/open-spec 从方案设计开始，需求和规范文档已就绪
/open-spec 直接进入实施，按当前开发计划推进
```
