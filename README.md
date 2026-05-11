# Open Spec Skill

这是一个给 AI 编码工具（GitHub Copilot、Cursor 等）使用的 Spec 驱动开发技能仓库。

它把一个需求推进成完整的开发文档和代码实施，按五个固定阶段有序推进，每个阶段由独立 Agent 负责。

## 目录结构

```
open-spec/
  SKILL.md          # 调度器/编排器入口
agents/
  01-requirements.agent.md     # 需求分析 Agent
  02-specification.agent.md    # 规范制定 Agent
  03-solution-design.agent.md  # 方案设计 Agent
  04-development-plan.agent.md # 开发计划 Agent
  05-implementation.agent.md   # 实施 Agent
open-spec/reference/           # 各阶段详细执行参考
open-spec/templates/           # 各类文档模板
```

## 工作流（五阶段）

```
需求分析 → 规范制定 → 方案设计 → 开发计划 → 实施
```

| # | 阶段     | Agent                                   | 主要产出                   |
|---|----------|-----------------------------------------|----------------------------|
| 1 | 需求分析 | `agents/01-requirements.agent.md`       | `01-requirements.md`       |
| 2 | 规范制定 | `agents/02-specification.agent.md`      | `02-specification.md`      |
| 3 | 方案设计 | `agents/03-solution-design.agent.md`    | `03-technical-solution.md` |
| 4 | 开发计划 | `agents/04-development-plan.agent.md`   | `05-development-plan.md`   |
| 5 | 实施     | `agents/05-implementation.agent.md`     | 代码变更 + 任务状态        |

## 调度器 / 编排器

`open-spec/SKILL.md` 是调度器入口，负责：

- 判断当前应进入哪个阶段
- 将前置阶段产出打包成 Handoff，传递给目标阶段 Agent
- 收集 Agent 输出，验证门禁状态（`PASS` / `NEEDS_USER_INPUT`）
- 自动推进到下一阶段，或在缺少关键信息时暂停等待用户补充

## 使用方式

把 `open-spec/` 目录加入工具的技能目录（确保能识别到 `open-spec/SKILL.md`），然后直接描述需求：

```
/open-spec 为订单服务新增取消原因与审计日志，技术栈 ASP.NET Core + PostgreSQL
```

### 直接指定阶段

也可以跳到任意阶段开始，例如：

```
/open-spec 从方案设计开始
/open-spec 直接进入实施
```

调度器会读取已有前置文档，验证前置条件后直接进入目标阶段。

## agents/ 目录说明

每个 Agent 文件（`*.agent.md`）是独立的阶段指令文件，包含：

- 角色定位
- 输入 Contract（需要什么信息）
- 执行步骤
- 输出 Contract（产出什么文档）
- Handoff 输出格式（给调度器的结构化交接包）

Agent 文件可以被调度器自动加载，也可以被用户手动引用（在工具不支持子 Agent 调用时）。

## Handoff 机制

阶段之间通过标准化的 Handoff 包传递状态：

```yaml
handoff:
  from_phase: 1
  phase_name: 需求分析
  status: PASS
  next_phase: 2
  artifacts:
    - path: docs/order-cancel/01-requirements.md
      summary: 确认 3 条 FR、1 条 NFR，范围边界清晰
  key_ids: FR-001, FR-002, FR-003, NFR-001
  open_risks: 历史订单兼容策略待方案阶段确认
  next_phase_inputs: 规范制定阶段需要 01-requirements.md 全文
```

这个格式与工具无关，可以在任何 AI 编码工具中使用。

## 兼容性

本技能设计为工具无关：

- **支持子 Agent 调用的工具**（如 GitHub Copilot Agent Mode）：调度器自动加载 `agents/` 目录下的 Agent 文件并传入 Handoff 包。
- **不支持子 Agent 调用的工具**：调度器以文字指令通知用户"请手动切换到 `agents/02-specification.agent.md`，并传入以下 Handoff 包"，由用户手动切换上下文。

两种模式下工作流和 Handoff 格式完全一致。
