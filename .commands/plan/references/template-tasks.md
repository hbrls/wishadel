---
name: template-tasks
version: 0.0.1
---

# Tasks

## 执行模式 (AI Agent 必读)

**仅支持阶段模式（Phase）：**

触发词：'执行第一阶段'、'execute setup'

行为：执行一个阶段（Phase）内的所有事项，然后等待用户确认再进入下一阶段

## Completion Checklist（AI Agent 义务，不是勾选模板）

{以下事项是你作为 AI Agent 在交付/收尾时应主动遵守的检查点；它们不是任务清单的一部分，不用于勾选，也不用于记录历史状态。}

- 确认所有 Story/Task 已按预期完成并在文档中标注完成状态
- 确认测试已通过（如有测试）
- 确认关键变更已完成 review（如适用）
- 确认必要的文档已更新（README/接口文档等）
- 确认 Changelog（如有）已更新
- 确认已通知相关 Stakeholders（如适用）
- 确认最终产物已按约定归档到 `.spec-flow/archive/{feature-name}/`

**所有模式必须遵守：**
1. ✅ 严格按顺序执行 - 从第一个 `- [ ]` 开始
2. ✅ 检查依赖 - 执行前确认依赖任务已完成 (`- [x]`)
3. ✅ 更新状态 - 完成后将 `- [ ]` 改为 `- [x]`
4. ✅ 报告进度 - 显示 (N/Total)
5. ✅ 遇错即停 - 出错时立即停止，等待用户指示

**禁止行为：**
- ❌ 跳过任务
- ❌ 不按顺序执行
- ❌ 执行任务列表之外的工作
- ❌ 出错后继续执行

## 概览

| Phase           | Tasks   | Completed | Progress |
|-----------------|---------|-----------|----------|
| Setup           | {{n}}   | 0         | 0%       |
| Implementation  | {{n}}   | 0         | 0%       |
| Testing         | {{n}}   | 0         | 0%       |
| Documentation   | {{n}}   | 0         | 0%       |
| **Total**       | **{{n}}** | **0**     | **0%**   |

## Dependencies & Blockers
 
 {默认情况下，所有 Story 与 Task 都应按文档从上到下依次执行，因此常规依赖关系天然由顺序表达；本章节不列出这些“普通依赖”，以保持信息密度与见解。这里只记录那些可能与从上到下的自然顺序不同、需要特殊关注的依赖/阻塞点（例如需要提前准备、需要并行协调、或会反向阻塞后续执行的事项）。}

{建议只记录以下“异常点”类型：}

- {需要提前准备的前置条件：权限/账号/环境/证书/配额/外部依赖等}
- {需要跨团队并行协调的对齐点：接口联调窗口、发布节奏、数据口径确认等}
- {顺序反转或回流：后置事项反向阻塞前置推进，或需要回到上游调整 Requirements/Specs}
- {高不确定性/高风险路径：一旦失败会导致大范围返工或阻塞的关键点}
- {需要显式停下确认的决策点：需要用户/owner 做选择才能继续}

 ```mermaid
 graph LR
     %% Only list exceptions that deviate from the top-to-bottom order
     TASK-XXX[TASK-XXX] --> TASK-YYY[TASK-YYY]
 ```

 **Blockers**

 - **Blocker**: {blocker description}
 - **Blocking Items**: {TASK-XXX / STORY-XXX}
 - **Raised**: {date}
 - **Owner**: {name}
 - **Status**: Open/Resolved
 - **Resolution**: {resolution}

## Changelog

{我们以“最新的设计/决策”为准，不需要维护面向历史版本的变更记录；大多数更新应直接体现在 Specs 中。此处仅用于记录少量适合放在 Tasks 侧的 memory，例如关键场景、容易误解的边界、踩坑与注意事项，用于帮助后续执行与对齐。}

{date}: {memory}

{date}: {memory}

## Task Breakdown

### Phase 1: Setup

- [ ] **TASK-001**: {{task description}}
  - **Complexity**: Low
  - **Files**: `{{path/to/file}}`
  - **Dependencies**: None
  - **Notes**: {{additional context}}

- [ ] **STORY-001**: {{story description}}
  - **Complexity**: Low
  - **Files**: `{{path/to/file}}`
  - **Dependencies**: TASK-001
  - **Notes**:

  - [ ] **TASK-002**: {{task description}}
    - **Complexity**: Low
    - **Files**: `{{path/to/file}}`
    - **Dependencies**: TASK-001
    - **Notes**:

  - [ ] **TASK-003**: {{task description}}
    - **Complexity**: Low
    - **Files**: `{{path/to/file}}`
    - **Dependencies**: TASK-002
    - **Notes**:

### Phase 2: Core Implementation

- [ ] **TASK-004**: {{task description}}
  - **Complexity**: Medium
  - **Files**:
    - `{{path/to/file1}}`
    - `{{path/to/file2}}`
  - **Dependencies**: STORY-001
  - **Notes**:

- [ ] **STORY-002**: {{story description}}
  - **Complexity**: High
  - **Files**: `{{path/to/file}}`
  - **Dependencies**: TASK-004
  - **Notes**:

  - [ ] **TASK-005**: {{task description}}
    - **Complexity**: Medium
    - **Files**: `{{path/to/file}}`
    - **Dependencies**: TASK-004
    - **Notes**:

  - [ ] **TASK-006**: {{task description}}
    - **Complexity**: Medium
    - **Files**: `{{path/to/file}}`
    - **Dependencies**: TASK-005
    - **Notes**:

- [ ] **TASK-007**: {{task description}}
  - **Complexity**: Medium
  - **Files**: `{{path/to/file}}`
  - **Dependencies**: TASK-004
  - **Notes**:

### Phase 3: Integration

- [ ] **TASK-008**: {{task description}}
  - **Complexity**: Medium
  - **Files**: `{{path/to/file}}`
  - **Dependencies**: STORY-002, TASK-007
  - **Notes**:

- [ ] **STORY-003**: {{story description}}
  - **Complexity**: Medium
  - **Files**: `{{path/to/file}}`
  - **Dependencies**: TASK-008
  - **Notes**:

  - [ ] **TASK-009**: {{task description}}
    - **Complexity**: Medium
    - **Files**: `{{path/to/file}}`
    - **Dependencies**: TASK-008
    - **Notes**:

  - [ ] **TASK-010**: {{task description}}
    - **Complexity**: Medium
    - **Files**: `{{path/to/file}}`
    - **Dependencies**: TASK-009
    - **Notes**:

### Phase 4: Testing

- [ ] **TASK-011**: Write unit tests for {{component}}
  - **Complexity**: Medium
  - **Files**: `{{path/to/test/file}}`
  - **Dependencies**: TASK-008
  - **Notes**: Target coverage: {{percentage}}%

- [ ] **STORY-004**: {{story description}}
  - **Complexity**: Medium
  - **Files**: `{{path/to/test/file}}`
  - **Dependencies**: TASK-011
  - **Notes**:

  - [ ] **TASK-012**: {{task description}}
    - **Complexity**: Medium
    - **Files**: `{{path/to/test/file}}`
    - **Dependencies**: TASK-011
    - **Notes**:

  - [ ] **TASK-013**: {{task description}}
    - **Complexity**: Medium
    - **Files**: `{{path/to/test/file}}`
    - **Dependencies**: TASK-012
    - **Notes**:

- [ ] **TASK-014**: Manual QA testing
  - **Complexity**: Low
  - **Files**: N/A
  - **Dependencies**: STORY-004
  - **Notes**: Test cases: {{list}}

### Phase 5: Documentation

- [ ] **TASK-015**: Update API documentation
  - **Complexity**: Low
  - **Files**: `docs/{{file}}.md`
  - **Dependencies**: TASK-008
  - **Notes**:

- [ ] **STORY-005**: {{story description}}
  - **Complexity**: Low
  - **Files**: `README.md`, `CHANGELOG.md`
  - **Dependencies**: TASK-015
  - **Notes**:

  - [ ] **TASK-016**: {{task description}}
    - **Complexity**: Low
    - **Files**: `{{path/to/file}}`
    - **Dependencies**: TASK-015
    - **Notes**:

  - [ ] **TASK-017**: {{task description}}
    - **Complexity**: Low
    - **Files**: `{{path/to/file}}`
    - **Dependencies**: TASK-016
    - **Notes**: