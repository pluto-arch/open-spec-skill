---
name: open-spec
description: "独立 Spec 驱动开发（Open Spec）：仅依赖 Skill 完成从需求、规范、方案、任务、测试到发布复盘的自动闭环交付，并支持用户从任意阶段显式触发继续执行。"
argument-hint: "描述目标功能、约束、技术栈、交付边界和时间要求"
user-invocable: true
compatibility: "适用于新功能、功能变更、重构与跨模块协作场景。"
license: "MIT"
metadata: "version: 1.12.0, author: McCoy Zhang, lastUpdated: 2026-04-22"
---

# Open Spec 技能

## 定位

Open Spec 是一个“Skill 驱动 + Spec Agent Team 协作”的规范开发流程。由编排角色统一调度阶段子 Agent，避免单 Agent 长上下文导致的 token 膨胀和后程质量下降。

本技能中的“子 Agent”指 Copilot 在当前会话中动态创建的临时 subagent 会话，不依赖任何预置 `*.agent.md` 文件。

默认执行模式：多 Agent 自动委派 + 默认自动闭环 + 关键阶段交互式门禁。

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
- runSubagent 模板：`reference/08-runsubagent-prompt-template.md`

使用规则：

1. 每个阶段开始前，Workflow Lead 必须读取对应 reference 文件。
2. 每个阶段完成后，必须按 reference 中的自检清单执行一次自检。
3. 若阶段门禁失败，优先参考对应 reference 的“常见问题/自检清单”做最小修复。
4. 子 Agent 委派时，优先使用对应 reference 的 `Input Contract` / `Output Contract` 作为 handoff 模板。
5. 进行阶段委派时，优先复制 `reference/08-runsubagent-prompt-template.md` 对应阶段模板。

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

默认输出目录：`docs/<feature-slug>/`

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

- 详细记忆：`docs/<feature-slug>/` 下 00-08 文档
- 摘要记忆：`docs/memory/YYYY-MM-DD.md`

读取顺序：

1. 先读最近 7 天摘要记忆（近到远）
2. 按摘要中的 ID（FR/TASK/TC/CR/REV）加载详细文档章节
3. 仅在必要时回溯历史会话

写入时机：

- 每个阶段结束，更新 `08-stage-handoff.md`（可选但推荐）
- 每次阶段门禁结论后，回写当日 `memory/YYYY-MM-DD.md`

## Spec Agent Team（默认启用）

说明：本章节定义的是“逻辑角色”，不是文件系统中的 agent 实体。

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

### 临时子 Agent 触发机制（强制）

为确保真正发生多子会话协作，Workflow Lead 必须按阶段调用 Copilot 的 `runSubagent`（不指定 `agentName`），创建临时子 Agent。

- 禁止将“阶段委派”仅停留在文档描述而不实际调用子会话。
- 每个阶段至少 1 次 `runSubagent` 调用；门禁失败返工阶段需再次调用。
- 临时子 Agent 只接收最小 handoff（Input/Output Contract + 必要文档引用 + ID 锚点）。
- 不得传递全量历史对话。

推荐调用约定：

- `description`：`open-spec <stage> delegation`
- `prompt`：包含阶段目标、输入契约、输出契约、门禁条件、回传格式

### 自动委派规则

1. Workflow Lead 必须先完成当日记忆初始化与最近 7 天记忆预读。
2. 每进入新阶段，Workflow Lead 仅向对应子 Agent 传递最小输入包：

- 本阶段目标
- 上阶段 `08-stage-handoff.md` 摘要
- 必要文档路径与 ID 锚点（FR/TASK/TC/CR/REV）
- 本阶段模板路径

3. 子 Agent 完成后必须回传：

- 文档增量
- 门禁结论（PASS/FAIL/NEEDS_USER_INPUT）
- 新的 `08-stage-handoff.md` 摘要

4. 若子 Agent 回传 `NEEDS_USER_INPUT`，Workflow Lead 必须先向用户发起补充问题并等待答复；在用户明确答复前，禁止进入下一阶段。

5. Workflow Lead 合并记忆增量到当日记忆，再决定进入下一阶段或当前阶段返工。

### 严格上下文预算

- 禁止向子 Agent 传递全量历史对话。
- 子 Agent 输入包目标控制在 300-800 tokens（不含文档文件本体）。
- `08-stage-handoff.md` 摘要目标控制在 300-500 tokens。
- 跨阶段只传“摘要 + 必要文档引用 + ID 锚点”，不传冗余推理过程。

### 失败回退（Stage-local Rollback）

- 任一阶段门禁 FAIL，仅回退当前阶段，不回退已通过阶段。
- 回退单必须包含：失败门禁项、受影响文件、最小修复范围、阻塞问题。
- 修复后重新执行当前阶段门禁，PASS 后再继续。

## 交互式信息补齐门禁（新增）

为避免流程在信息不足时继续向后扩散，Open Spec 对需求、规范、方案阶段启用强制交互门禁。

### 信息缺口分级

- `Blocker`：缺失后会直接影响 FR/AC、接口语义、技术选型、范围边界、风险回滚等核心决策，必须先问用户。
- `Assumption`：可以在文档中临时记录假设，但必须显式标注影响范围与待确认时间点。
- `Nice-to-know`：不影响当前阶段主结论，可进入未决项列表，不阻塞阶段完成。

### 必停阶段

- 需求阶段：业务目标、成功标准、范围边界、关键约束、外部依赖中存在 `Blocker` 时，阶段结果必须为 `NEEDS_USER_INPUT`。
- 规范阶段：行为规则、异常语义、接口契约、兼容策略中存在 `Blocker` 时，阶段结果必须为 `NEEDS_USER_INPUT`。
- 方案阶段：架构边界、关键 ADR、存储策略、风险与回滚方案中存在 `Blocker` 时，阶段结果必须为 `NEEDS_USER_INPUT`。

### Workflow Lead 交互协议

1. 每阶段结束先汇总信息缺口，按 `Blocker/Assumption/Nice-to-know` 分类。
2. 若存在 `Blocker`，只能输出“阶段结论 + 缺口摘要 + 待用户回答问题包”，不得继续调用下一阶段子 Agent。
3. 待用户回答问题包必须尽量短，优先给出 3-7 个高价值问题，并说明每个问题影响哪个文档或决策。
4. 用户答复后，Workflow Lead 先回写当前阶段文档与 `08-stage-handoff.md`，再重新执行当前阶段门禁。
5. 只有当前阶段状态变为 `PASS`，才能进入下一阶段。

## 阶段流（Team 自动编排）

1. 需求阶段

- 输出：00（变更场景）+ 01
- 门禁：FR/NFR 可测试、范围边界清晰、风险可见；若存在业务目标/范围/约束 `Blocker`，返回 `NEEDS_USER_INPUT`
- 默认执行者：Requirements Agent（`open-spec-requirements`）
- 参考：`reference/01-requirements-analysis-reference.md`

2. 规范阶段

- 输出：02
- 门禁：行为/数据/接口/异常完整，验收标准明确；若存在规则或接口语义 `Blocker`，返回 `NEEDS_USER_INPUT`
- 默认执行者：Spec Agent（`open-spec-spec`）
- 参考：`reference/02-specification-authoring-reference.md`

3. 方案阶段

- 输出：03 + 04（或 N/A）
- 门禁：FR 可追溯、风险与回滚可执行；若存在架构/选型/存储/发布策略 `Blocker`，返回 `NEEDS_USER_INPUT`
- 默认执行者：Solution Agent（`open-spec-solution`）
- 参考：`reference/03-solution-design-reference.md`

4. 计划与实施阶段

- 输出：05 + 实施增量 + TASK 完成状态更新 + 实际开发产出
- 门禁：TASK 映射 FR 与方案章节，依赖与里程碑完整，实施偏差有记录且可解释；当 05 已形成可执行计划且不存在 `Blocker` 时，Workflow Lead 必须自动续跑实施，不等待用户额外下达“开始开发”指令
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
2. 首轮识别：第一轮输出必须先完成场景判定、缺口分级和提问决策，不得直接创建完整阶段计划或直接进入需求文档铺写。
3. 计划：仅在首轮识别确认不存在 `Blocker`，或已拿到用户补充答复后，才声明阶段顺序、每阶段入口条件与退出门禁。
4. 委派：按阶段自动调用临时子 Agent（必须执行 `runSubagent`），不跨阶段混投。

- 若当前阶段退出门禁已满足，且下一阶段入口条件已满足，Workflow Lead 必须自动进入下一阶段，不等待用户手动说“继续”。

- 对计划与实施阶段，若 `05-development-plan.md` 已形成且实施前置条件齐备，Workflow Lead 必须立即继续委派 Implementer Agent 执行首批 TASK，并持续更新实施增量与 TASK 状态，直到进入测试入口条件或遇到新的 `Blocker`。

- 若用户显式指定起始阶段，则 Workflow Lead 必须将其视为阶段覆盖指令，从该阶段开始执行对应子 Agent，而不是退化为仅输出建议或停留在说明层。

- 仅使用 Open Spec 内建角色标识，不绑定外部技能或历史角色命名。

- 子 Agent 创建方式：使用临时 subagent（不依赖任何预置 `.agent.md`）。

5. 验收：每阶段结束执行结构清单与追溯校验；在实施阶段额外校验 TASK 完成状态与偏差说明。
6. 交互：需求/规范/方案阶段若回传 `NEEDS_USER_INPUT`，必须先向用户提出补充问题并等待答复，禁止直接续跑后续阶段。
7. 记忆：将 handoff 的 Memory Delta 合并到当日记忆。
8. 收敛：输出最终交付摘要、剩余风险与下一步建议。

### 用户主动指定起始阶段（新增）

Open Spec 默认自动闭环，但允许用户显式指定从某个阶段开始执行。

可识别的阶段触发示例：

- `开始需求分析`
- `开始规范设计`
- `开始技术方案`
- `开始进入开发实施`
- `开始测试验证`
- `开始发布复盘`

也支持等价表达，例如：

- `从实施阶段开始`
- `直接进入测试阶段`
- `只跑发布复盘`

### 阶段触发词归一化词表（新增）

Workflow Lead 在解析用户指令时，应先将自然语言表达归一化到标准阶段，再执行阶段前置检查与子 Agent 委派。

归一化要求：

1. 优先识别“开始/进入/继续/转到/切到/直接到/只跑”这类动作词。
2. 再识别对应阶段名、同义词、口语化表达和常见简称。
3. 若同一句中同时出现多个阶段，以最后一个明确阶段为准；若存在歧义，返回 `NEEDS_USER_INPUT`。
4. 若用户同时表达“只执行当前阶段”，则该轮执行结束后不自动流转到后续阶段。

标准阶段与建议匹配词：

1. 需求阶段

- 标准名：`需求阶段`
- 可匹配表达：`需求分析`、`需求梳理`、`开始需求`、`先做需求`、`进入需求阶段`、`回到需求阶段`

2. 规范阶段

- 标准名：`规范阶段`
- 可匹配表达：`规范设计`、`写规范`、`补规范`、`进入规范阶段`、`开始规格定义`、`开始接口规范`

3. 方案阶段

- 标准名：`方案阶段`
- 可匹配表达：`技术方案`、`方案设计`、`架构设计`、`开始方案`、`进入方案阶段`、`补技术方案`

4. 计划与实施阶段

- 标准名：`计划与实施阶段`
- 可匹配表达：`开始进入开发实施`、`开始开发`、`进入开发`、`进入实施`、`开始实施`、`继续开发`、`继续实施`、`开始编码`、`进入编码阶段`、`按任务开发`、`按 TASK 开发`、`落地实现`、`开始联调开发`

5. 测试阶段

- 标准名：`测试阶段`
- 可匹配表达：`开始测试`、`进入测试`、`开始验证`、`测试验证`、`回归测试`、`联调测试`、`进入验收测试`、`补测试用例`

6. 发布复盘阶段

- 标准名：`发布复盘阶段`
- 可匹配表达：`开始发布`、`进入发布`、`发布复盘`、`上线复盘`、`进入复盘`、`只跑发布`、`只跑复盘`

处理规则：

1. Workflow Lead 必须先解析用户显式指定的起始阶段。
2. Workflow Lead 必须读取该阶段所需的最小前置文档、最近 handoff 与当日记忆。
3. 若前置条件满足，必须立即调用该阶段对应子 Agent 开始执行。
4. 若前置条件不满足，必须仅报告缺失前置项并返回 `NEEDS_USER_INPUT`，不得假装已经执行该阶段。
5. 阶段执行完成后，除非遇到 `Blocker` 或用户明确要求“只执行当前阶段”，否则继续按默认自动闭环流转到后续阶段。

实施阶段特别规则：

- 当用户输入 `开始进入开发实施`、`从实施阶段开始` 或等价表达时，Workflow Lead 必须优先读取现有 `05-development-plan.md` 与最近的 `08-stage-handoff.md`。
- 若 `05-development-plan.md` 已存在且可执行，Implementer Agent 必须直接按 TASK 顺序或依赖关系推进实际开发，而不是仅复述计划。
- 若 `05-development-plan.md` 不存在，但 `03/04` 已齐备，则先生成 05，再在同一轮自动进入实际开发。
- 若 `03/04` 缺失导致无法实施，则返回缺失项并暂停在实施阶段。

### Workflow Lead 首轮启动要求（新增）

Workflow Lead 在接收到用户初始目标后，第一轮只能做以下四件事：

1. 判定场景：`new-feature` / `change-request` / `unknown`。
2. 提取已知输入：业务目标、范围、约束、技术栈、时间要求、依赖方、是否显式指定起始阶段。
3. 识别缺口：按 `Blocker/Assumption/Nice-to-know` 输出缺口清单。
4. 决定下一步：

- 若存在 `Blocker`，仅向用户提出 3-7 个高价值问题并暂停。
- 若不存在 `Blocker`，则进入用户指定阶段或默认需求阶段委派。

禁止行为：

- 在首轮识别前直接生成 01-07 全套文档计划。
- 在首轮识别前直接调用多个阶段子 Agent。
- 用默认假设替代用户尚未确认的核心输入。

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

- 新功能：Workflow Lead 按阶段自动委派，先完成需求/规范/方案的信息补齐与用户确认，再生成 01-07，并在实施阶段自动继续实际开发与 TASK 状态更新，不等待用户额外下达开始实施指令
- 变更需求：先生成 00，再按阶段补齐关键缺口，确认后更新 01-07 并同步 REV
- 定向触发：若用户显式指定某阶段，Workflow Lead 必须从该阶段开始调用对应子 Agent，并在前置条件满足时继续自动闭环
- 每阶段结束都更新 `08-stage-handoff.md` 与当日记忆；若阶段状态为 `NEEDS_USER_INPUT`，先暂停在当前阶段等待用户答复

## 未触发子 Agent 的常见原因

- 只写了“子 Agent 角色”但未实际调用 `runSubagent`。
- 将逻辑角色误当作预置 agent 名称，导致委派目标不存在。
- prompt 未包含“必须分阶段委派”的强约束，模型退化为单会话执行。
- 输入任务过小，命中“单执行者模式”分支。

## 快速调用示例

- `/open-spec 为订单服务新增取消原因与审计日志，要求向后兼容，并强制分阶段使用临时子agent`
- `/open-spec 重构用户资料模块并补齐回归测试，限制两周内交付，要求每阶段调用runSubagent`
- `/open-spec 开始进入开发实施`
- `/open-spec 继续开发，按当前 TASK 自动推进实现`
- `/open-spec 进入验收测试，继续当前 feature 的验证与回归`
- `/open-spec 从测试阶段开始，继续当前 feature 的验证与回归`
- `/open-spec 只跑发布复盘`

## 文档语言环境

文档默认使用中文撰写，确保团队成员的理解一致性和沟通效率。
