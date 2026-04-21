---
name: open-spec
description: "独立 Spec 驱动开发（Open Spec）：仅依赖 Skill 完成从需求、规范、方案、任务、测试到发布复盘的闭环交付。"
argument-hint: "描述目标功能、约束、技术栈、交付边界和时间要求"
user-invocable: true
compatibility: "适用于新功能、功能变更、重构与跨模块协作场景。"
license: "MIT"
metadata: "version: 1.5.0, author: McCoy Zhang, lastUpdated: 2026-04-21"
---

# Open Spec 技能

## 定位

Open Spec 是一个“Skill 驱动 + Spec Agent Team 协作”的规范开发流程。由编排角色统一调度阶段子 Agent，避免单 Agent 长上下文导致的 token 膨胀和后程质量下降。

该技能为完全独立实现，不依赖任何外部或历史 SDD 技能定义。

默认执行模式：多 Agent 自动委派。

可选执行模式：在任务极小（单文档微调）时可退化为单执行者模式。

## 目标

将模糊需求转化为可执行规范，并通过“需求 -> 规范 -> 方案 -> 任务 -> 测试 -> 发布复盘”形成可追溯、可验证、可回滚的交付闭环。

## Reference 体系（详细执行指南）

为避免主技能文档过长且保证阶段执行质量，Open Spec 将阶段方法论沉淀在 `reference/` 目录。

- 总览：`reference/README.md`
- 需求分析：`reference/01-requirements-analysis-reference.md`
- 规范制定：`reference/02-specification-authoring-reference.md`
- 方案设计：`reference/03-solution-design-reference.md`
- 计划与实施：`reference/04-planning-and-implementation-reference.md`
- 测试与验证：`reference/05-testing-and-validation-reference.md`
- 发布与复盘：`reference/06-release-and-retrospective-reference.md`
- Handoff 样例：`reference/07-handoff-contract-example.md`

使用规则：

1. 每个阶段开始前，Workflow Lead 必须读取对应 reference 文件。
2. 每个阶段完成后，必须按 reference 中的自检清单执行一次自检。
3. 若阶段门禁失败，优先参考对应 reference 的“常见问题/自检清单”做最小修复。
4. 子 Agent 委派时，优先使用对应 reference 的 `Input Contract` / `Output Contract` 作为 handoff 模板。

## 关键交付物

- 需求功能清单（含优先级、范围边界、验收条件）
- 规范文档（业务规则、接口契约、异常语义、兼容策略）
- 技术方案（架构选型、模块划分、关键流程、风险与回滚）
- 存储设计（如适用：数据结构、索引策略、约束、迁移与回填）
- 开发任务安排（任务拆解、依赖、里程碑）
- 实施增量与任务完成状态（按 TASK 记录完成度、偏差与阻塞）
- 测试用例集（单元/集成/E2E，覆盖主路径与边界）
- 发布与复盘记录（变更说明、监控点、回滚策略、改进动作）

## 交付目录约束

默认输出目录：`docs/open-spec/<feature-slug>/`

- 变更场景必填：`00-change-request.md`
- 必填核心文件：
  - `01-requirements.md`
  - `02-specification.md`
  - `03-technical-solution.md`
  - `04-storage-design.md`（不涉及存储时标注 N/A）
  - `05-development-plan.md`
  - `06-test-cases.md`
  - `07-release-retrospective.md`
- 可选过程文件：
  - `08-stage-handoff.md`（阶段交接与续接摘要）

每个文档必须包含：

- 文档头（版本、作者、日期、状态）
- 修订记录表（修订号、日期、作者、变更摘要、关联 CR）
- 信息缺口清单
- 可追溯引用（FR/TASK/TC/CR/REV）

## ID 与版本规则

- 需求 ID：`FR-001`，非功能：`NFR-001`
- 任务 ID：`TASK-001`
- 测试 ID：`TC-001`
- 变更请求：`CR-001`
- 修订号：`REV-yyyymmdd-xx`

版本建议：`主版本.次版本.修订号`

- 重大变更：主版本 +1
- 向后兼容增强：次版本 +1
- 文案/细节修订：修订号 +1

## 记忆机制（独立执行）

为避免上下文膨胀，采用双层记忆：

- 详细记忆：`docs/open-spec/<feature-slug>/` 下 00-08 文档
- 摘要记忆：`docs/open-spec/memory/YYYY-MM-DD.md`

读取顺序：

1. 先读最近 7 天摘要记忆（近到远）
2. 按摘要中的 ID（FR/TASK/TC/CR/REV）加载详细文档章节
3. 仅在必要时回溯历史会话

写入时机：

- 每个阶段结束，更新 `08-stage-handoff.md`（可选但推荐）
- 每次阶段门禁结论后，回写当日 `memory/YYYY-MM-DD.md`

## Spec Agent Team（默认启用）

### 团队角色

- Workflow Lead（流程编排者）：负责分阶段计划、门禁验收、回退决策与最终汇总。
- Requirements Agent：负责 00（变更场景）与 01。
- Spec Agent：负责 02。
- Solution Agent：负责 03 与 04（或 N/A 说明）。
- Implementer Agent：负责 05 的迭代与开发计划、按计划推进具体开发、持续更新 TASK 完成状态与偏差说明。
- QA Agent：负责 06。
- Release Agent：负责 07。

### 内建角色标识（Open Spec 专用）

- `open-spec-lead`：Workflow Lead（流程编排者）
- `open-spec-requirements`：Requirements Agent
- `open-spec-spec`：Spec Agent
- `open-spec-solution`：Solution Agent
- `open-spec-implementer`：Implementer Agent（计划 + 实施 + TASK 跟踪）
- `open-spec-qa`：QA Agent
- `open-spec-release`：Release Agent

说明：上述标识是 Open Spec 工作流内部角色，不引用任何外部 agent 文件或既有映射。

### 自动委派规则

1. Workflow Lead 必须先完成当日记忆初始化与最近 7 天记忆预读。
2. 每进入新阶段，Workflow Lead 仅向对应子 Agent 传递最小输入包：

- 本阶段目标
- 上阶段 `08-stage-handoff.md` 摘要
- 必要文档路径与 ID 锚点（FR/TASK/TC/CR/REV）
- 本阶段模板路径

3. 子 Agent 完成后必须回传：

- 文档增量
- 门禁结论（PASS/FAIL）
- 新的 `08-stage-handoff.md` 摘要

4. Workflow Lead 合并记忆增量到当日记忆，再决定进入下一阶段或当前阶段返工。

### 严格上下文预算

- 禁止向子 Agent 传递全量历史对话。
- 子 Agent 输入包目标控制在 300-800 tokens（不含文档文件本体）。
- `08-stage-handoff.md` 摘要目标控制在 300-500 tokens。
- 跨阶段只传“摘要 + 必要文档引用 + ID 锚点”，不传冗余推理过程。

### 失败回退（Stage-local Rollback）

- 任一阶段门禁 FAIL，仅回退当前阶段，不回退已通过阶段。
- 回退单必须包含：失败门禁项、受影响文件、最小修复范围、阻塞问题。
- 修复后重新执行当前阶段门禁，PASS 后再继续。

## 阶段流（Team 自动编排）

1. 需求阶段

- 输出：00（变更场景）+ 01
- 门禁：FR/NFR 可测试、范围边界清晰、风险可见
- 默认执行者：Requirements Agent（`open-spec-requirements`）
- 参考：`reference/01-requirements-analysis-reference.md`

2. 规范阶段

- 输出：02
- 门禁：行为/数据/接口/异常完整，验收标准明确
- 默认执行者：Spec Agent（`open-spec-spec`）
- 参考：`reference/02-specification-authoring-reference.md`

3. 方案阶段

- 输出：03 + 04（或 N/A）
- 门禁：FR 可追溯、风险与回滚可执行
- 默认执行者：Solution Agent（`open-spec-solution`）
- 参考：`reference/03-solution-design-reference.md`

4. 计划与实施阶段

- 输出：05 + 实施增量 + TASK 完成状态更新
- 门禁：TASK 映射 FR 与方案章节，依赖与里程碑完整，实施偏差有记录且可解释
- 默认执行者：Implementer Agent（`open-spec-implementer`）
- 参考：`reference/04-planning-and-implementation-reference.md`

5. 测试阶段

- 输出：06
- 门禁：TC 映射 FR/TASK，边界与回归覆盖
- 默认执行者：QA Agent（`open-spec-qa`）
- 参考：`reference/05-testing-and-validation-reference.md`

6. 发布复盘阶段

- 输出：07
- 门禁：发布范围、回滚与监控明确，复盘动作有 owner 与截止日期
- 默认执行者：Release Agent（`open-spec-release`）
- 参考：`reference/06-release-and-retrospective-reference.md`

## Workflow Lead 执行协议（必须遵循）

1. 启动：初始化当日记忆文件，写入会话主题与初始续接点。
2. 计划：声明阶段顺序、每阶段入口条件与退出门禁。
3. 委派：按阶段自动调用子 Agent，不跨阶段混投。

- 仅使用 Open Spec 内建角色标识，不绑定外部技能或历史角色命名。

4. 验收：每阶段结束执行结构清单与追溯校验；在实施阶段额外校验 TASK 完成状态与偏差说明。
5. 记忆：将 handoff 的 Memory Delta 合并到当日记忆。
6. 收敛：输出最终交付摘要、剩余风险与下一步建议。

## 失败回退策略

- 任何门禁失败，仅回退当前阶段修订，不重跑全流程
- 修订时必须记录：失败项、影响文件、最小修复范围
- 修订完成后重新执行当前阶段门禁，再进入下一阶段
- Workflow Lead 负责判定是否需要二次委派同一子 Agent 执行返工

## 模板清单

- `templates/00-change-request-template.md`
- `templates/00-structure-checklist.md`
- `templates/01-requirements-template.md`
- `templates/02-specification-template.md`
- `templates/03-technical-solution-template.md`
- `templates/04-storage-design-template.md`
- `templates/05-development-plan-template.md`
- `templates/06-test-cases-template.md`
- `templates/07-release-retrospective-template.md`
- `templates/08-stage-handoff-template.md`
- `templates/09-daily-memory-template.md`

## 最小执行指令

- 新功能：Workflow Lead 按阶段自动委派，生成 01-07，并在实施阶段同步推进开发与 TASK 状态
- 变更需求：先生成 00，再自动委派更新 01-07 并同步 REV
- 每阶段结束都更新 `08-stage-handoff.md` 与当日记忆，确保可续接

## 快速调用示例

- `/open-spec 为订单服务新增取消原因与审计日志，要求向后兼容`
- `/open-spec 重构用户资料模块并补齐回归测试，限制两周内交付`
