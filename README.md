# Open Spec Skill

这是一个给 AI 编码工具使用的 Spec 驱动开发技能仓库。

当前版本采用 **三个顺序 task** 的执行方式：

```
需求变更分析 → 设计 → 开发
```

## 目录结构

```text
open-spec/
  SKILL.md                     # 主技能入口，负责按 task 推进流程
  reference/                   # 三个 task 的执行参考
  templates/                   # 对应模板
```

## 工作流（三阶段）

| # | Task | 主要产出 |
|---|------|----------|
| 1 | 需求变更分析 | `00-change-request.md`（如适用）、`01-change-analysis.md` |
| 2 | 设计 | `02-technical-design.md` |
| 3 | 开发 | `03-development.md`、代码变更 |

## SKILL 编排方式

`/tmp/workspace/pluto-arch/open-spec-skill/open-spec/SKILL.md` 是唯一入口，负责：

- 识别当前应进入哪个 task
- 检查前置文档是否齐备
- 直接执行当前 task
- 输出阶段结果与 handoff，决定继续还是暂停等待用户补充

每个环节都是一个 task，必须真正完成当前 task 的产出，不能只给说明或建议。

## 使用方式

把 `open-spec/` 加入技能目录后，直接描述需求：

```text
/open-spec 为订单服务新增取消原因与审计日志，技术栈 ASP.NET Core + PostgreSQL
```

也可以直接指定阶段：

```text
/open-spec 从设计开始
/open-spec 直接进入开发
```

系统会读取已有文档并校验前置条件，满足后直接执行对应 task。

## Handoff 机制

各 task 之间统一通过 `task_result + handoff` 传递状态：

```yaml
task_result:
  status: PASS
  completed_work:
    - 已完成变更范围确认
  updated_artifacts:
    - path: docs/order-cancel/01-change-analysis.md
      summary: 明确影响范围与验收标准
  blockers: []
```

```yaml
handoff:
  previous_task: 1
  task_name: 需求变更分析
  status: PASS
  next_task: 2
  artifacts:
    - path: docs/order-cancel/01-change-analysis.md
      summary: 已确认范围、约束与风险
  key_ids: CR-001, FR-001, NFR-001
  open_risks: 历史数据兼容策略待设计阶段确认
  next_task_inputs: 设计阶段需要需求变更分析文档全文
```

## 参考与模板

- `open-spec/reference/`：三个 task 的详细执行参考与 handoff 示例
- `open-spec/templates/`：变更请求、分析、设计、开发文档模板（存储设计并入主设计模板）

这个技能现在默认走 **task 编排**。
