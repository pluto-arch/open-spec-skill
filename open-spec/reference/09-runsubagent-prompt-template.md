# 09 runSubagent Prompt 模板（Workflow Lead）

## 用途

为 Workflow Lead 提供标准化 `runSubagent` 调用模板，确保每个阶段都真实触发临时子 Agent，会话输入最小化且结果可回收。

## 通用模板

将以下模板作为 `runSubagent` 的 `prompt`：

```text
[Role]
你是 Open Spec 的 <stage> 阶段临时子 Agent。

[Goal]
完成 <stage> 阶段目标，并输出可直接合并的文档增量与门禁结论。

[Required Inputs]
- Feature: <feature-slug>
- Stage Objective: <one-line objective>
- Required Docs:
  - <doc-path-1>
  - <doc-path-2>
- Upstream Handoff Summary:
  - <3-5 bullets>
- Required ID Anchors: <FR/TASK/TC/CR/REV...>

[Output Contract]
1) Document Delta
- file: <path>
- change summary: <what changed>
- key IDs: <ids>

2) Gate Result
- status: PASS | FAIL
- passed checks: <list>
- failed checks: <list>

3) Handoff Draft
- stage conclusion
- open risks
- next-stage required inputs
- memory delta

[Hard Constraints]
- 不要回放全量历史对话。
- 仅使用提供的输入和引用文档。
- 若信息不足，显式列出阻塞问题，不要编造。
```

建议 `description`：

```text
open-spec <stage> delegation
```

## 阶段模板（可直接粘贴）

### 1. 需求阶段

```text
你是 Open Spec 的 requirements 阶段临时子 Agent。
目标：产出 00/01 文档的可评审增量（变更场景需 00）。
必读：docs/<feature-slug>/00-change-request.md(如有), docs/<feature-slug>/01-requirements.md。
输出：文档增量 + PASS/FAIL + 08-stage-handoff 草稿。
门禁：FR/NFR 可测试；范围边界明确；信息缺口集中记录。
```

### 2. 规范阶段

```text
你是 Open Spec 的 specification 阶段临时子 Agent。
目标：产出 02 文档增量，完成行为/数据/接口/异常语义定义。
必读：docs/<feature-slug>/01-requirements.md, docs/<feature-slug>/02-specification.md。
输出：文档增量 + PASS/FAIL + 08-stage-handoff 草稿。
门禁：关键章节映射 FR；异常语义完整；兼容策略清晰。
```

### 3. 方案阶段

```text
你是 Open Spec 的 solution 阶段临时子 Agent。
目标：产出 03/04 文档增量（不涉及存储则在 04 标注 N/A）。
必读：docs/<feature-slug>/02-specification.md, docs/<feature-slug>/03-technical-solution.md, docs/<feature-slug>/04-storage-design.md。
输出：文档增量 + PASS/FAIL + 08-stage-handoff 草稿。
门禁：方案可追溯 FR；风险与回滚可执行；存储策略清晰或 N/A 合理。
```

### 4. 计划与实施阶段

```text
你是 Open Spec 的 implementation 阶段临时子 Agent。
目标：更新 05 并给出实施进展与 TASK 状态。
必读：docs/<feature-slug>/03-technical-solution.md, docs/<feature-slug>/04-storage-design.md, docs/<feature-slug>/05-development-plan.md。
输出：文档增量 + PASS/FAIL + 08-stage-handoff 草稿。
门禁：TASK 映射 FR/方案章节；里程碑完整；偏差记录可解释。
```

### 5. 测试阶段

```text
你是 Open Spec 的 testing 阶段临时子 Agent。
目标：更新 06 并形成可审计验证结果。
必读：docs/<feature-slug>/01-requirements.md, docs/<feature-slug>/02-specification.md, docs/<feature-slug>/05-development-plan.md, docs/<feature-slug>/06-test-cases.md。
输出：文档增量 + PASS/FAIL + 08-stage-handoff 草稿。
门禁：TC 映射 FR/TASK；失败与边界场景覆盖；执行证据完整。
```

### 6. 发布复盘阶段

```text
你是 Open Spec 的 release 阶段临时子 Agent。
目标：更新 07 并完成发布与复盘闭环。
必读：docs/<feature-slug>/05-development-plan.md, docs/<feature-slug>/06-test-cases.md, docs/<feature-slug>/07-release-retrospective.md。
输出：文档增量 + PASS/FAIL + 08-stage-handoff 草稿。
门禁：发布范围明确；回滚可执行；复盘动作有 owner 与 deadline。
```

## Workflow Lead 最小调用示例

```text
runSubagent(
  description="open-spec requirements delegation",
  prompt="<粘贴上面的阶段模板 + 当前 feature 输入 + 上阶段摘要>"
)
```

## 质量建议

- 每个阶段调用前先写一条 telemetry `stage_start`。
- 子 Agent 返回后立即写 `stage_end` 与 `gate_result`。
- FAIL 时仅返工当前阶段，并再次调用该阶段模板。
