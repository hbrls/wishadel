# Text-Only Agent 实施计划

## 📋 概述

在现有 `windows-app` 包中集成 **smolagents**，实现 Text-Only Agent Protocol。

---

## 🎯 核心目标

1. **输入/输出**：Markdown 文本
2. **LLM 核心**：MiniMax（MVP 阶段）
3. **Agent 管理**：role / system prompt / loop / 输出提取
4. **可选工具**：仅处理文本（text → text），无副作用
5. **Stateless**：每次请求独立，互不干扰
6. **Loop 用途**：质量验收，而非 schema 或自主推理
7. **Agent 架构**：拆分为 PolisherAgent 和 ValidatorAgent，独立职责

---

## 📝 实施步骤

### 阶段 1：项目初始化

- [x] 创建 `agent/` 目录结构（包含 `tools/` 子目录）

### 阶段 2：基础架构实现

- [x] 实现 `agent/minimax_provider.py`（MiniMax Provider for smolagents）
  - 实现 smolagents 的 Model 接口
  - 使用 Anthropic SDK 风格接口
  - 管理 API Key 和参数
  - 处理请求和响应
  - 在 `__call__` 返回前 strip 输出结果
  - 封装通用的后处理逻辑（如 strip、换行符处理）

- [x] 实现 `agent/charms.py`（Charm 定义）
  - 定义 `CHARM_POLISH`（润色用 system prompt）
  - 定义 `CHARM_POLISH_VALIDATE`（验证润色结果用 system prompt，引用 CHARM_POLISH）

- [x] 实现 `agent/core.py`（基于 smolagents 的 _TextAgent）
  - `_TextAgent` 类：自己控制循环，直接调用 model.generate()
  - 支持自定义 system_prompt、max_steps
  - 支持可选 tools 参数
  - 返回完整响应文本
  - **注意**：`_` 前缀表示只用于继承，不直接使用

- [x] 集成测试：polish → validate 流程验证
  - Step 1: 调用润色 (CHARM_POLISH)
  - Step 2: 调用验证 (CHARM_POLISH_VALIDATE)
  - 验证验证结果以 PASS 或 FAIL 开头

- [x] 编写单元测试

### 阶段 3：Agent 架构

**核心组件**：

- [x] 实现 `agent/agents/_text_agent.py`（_TextAgent 基类）
  - 基于 smolagents 的 Agent 抽象基类
  - 只用于继承，不直接使用

- [x] 实现 `agent/agents/validator_agent.py`（ValidatorAgent）
  - 继承 `_TextAgent`
  - 直接 import `CHARM_POLISH_VALIDATE`（不需要入参）
  - **MVP 简化**：不做循环，单次验证即可
  - `run(text: str) -> str`：返回 "PASS" 或 "FAIL: 原因"

- [x] 实现 `agent/agents/polisher_agent.py`（PolisherAgent）
  - 继承 `_TextAgent`
  - 传入 `validator_tool` 参数（使用 tools/validator）
  - 在 loop 中自动调用验证工具

- [x] 实现 `agent/tools/validator.py`（ValidatorTool）
  - 继承 smolagents `Tool` 接口
  - `name = "validate_polish_result"`
  - 无 init 入参，使用 `set_model()` 设置 model
  - `forward(text: str) -> str`：内部实例化 `ValidatorAgent` 并调用

- [x] 实现 `agent/core.py`（Wisadel 对外接口）
  - 内部使用 `PolisherAgent`
  - `agent/__init__.py` 只导出 `Wisadel`，不导出 `_TextAgent`

**调用关系**：

```
外部代码 → tools/validator (Tool 接口)
                 ↓
          实例化 ValidatorAgent
                 ↓
          调用 model 验证
                 ↓
          返回 "PASS" / "FAIL: 原因"

PolisherAgent.run()
                 ↓
     内部使用 tools/validator 作为工具
                 ↓
     每轮 loop 结束后调用验证工具
                 ↓
     PASS → 返回润色结果
     FAIL → messages 追加失败原因，继续循环
```

**验证工具工作流程**：

```
Loop 第 N 次:
  1. model.generate() → 润色结果
  2. 调用 validate_polish_result(润色结果)
  3. 如果返回 "PASS" → 返回润色结果，结束
  4. 如果返回 "FAIL: 原因" → 追加到 messages，继续循环

Messages 累积示例:
  messages = [
    {role: SYSTEM, content: "润色规则..."},
    {role: USER, content: "原始文本"},
    {role: ASSISTANT, content: "润色结果1"},
    {role: TOOL_RESPONSE, content: "FAIL: 原因"},
    {role: ASSISTANT, content: "润色结果2"},
    ...
  ]
```

**终止条件**：
- 验证返回 "PASS" → 立即返回
- 验证返回 "FAIL" → 继续 loop，messages 追加失败原因
- 达到 max_steps → 返回最后一次结果，print 失败原因
- 达到 token 限制 → 同上

### 阶段 4：集成到 GUI

- [x] 修改 `gui.py`，将"复制"按钮改为"润色"按钮
- [x] 点击"润色"时调用 Wisadel.run()
- [x] 将结果显示在右侧文本框
- [x] 测试完整流程

### 阶段 5：验证和优化

- [ ] 运行 MVP 验证指标测试
- [ ] 性能优化（如需要）
- [ ] 代码审查和重构

---

## ✅ MVP 验证指标

根据 spec，以下指标必须全部通过：

- [ ] **指标 1**：用户输入文本，调用 MiniMax 返回 Markdown 文本
- [ ] **指标 2**：loop 验收逻辑生效，最大步数限制可控制
- [ ] **指标 3**：多次请求独立执行，互不干扰
- [ ] **指标 4**：可选 text → text tool 能调用，执行结果正确
- [ ] **指标 5**：agent 本身保持"协议层"，能力由 MiniMax 提供

---

## 📅 预估时间

- 阶段 1：项目初始化 - 0.5 天
- 阶段 2：基础架构实现 - 0.5 天
- 阶段 3：Agent 架构 - 1 天
- 阶段 4：集成到 GUI - 1 天
- 阶段 5：验证和优化 - 0.5 天

**总计**：约 3.5 天

---

## 📌 注意事项

1. **API Key 安全**：使用环境变量，不硬编码
2. **错误处理**：完善的异常处理和重试机制
3. **日志记录**：记录关键操作和错误信息
4. **测试覆盖**：核心模块必须有单元测试
5. **最小化改动**：尽量不破坏现有 windows-app 的功能
6. **使用统一 venv**：与主应用使用同一个虚拟环境

---

## 🏗️ 项目结构

```
packages/windows-app/
├── agent/
│   ├── __init__.py          # 导出 Wisadel, MinimaxProvider
│   ├── core.py              # Wisadel 对外接口
│   ├── glm_provider.py      # 智谱 GLM Provider
│   ├── charms.py            # Charm 定义（CHARM_POLISH, CHARM_POLISH_VALIDATE）
│   ├── agents/              # Agent 实现（继承 _TextAgent）
│   │   ├── __init__.py
│   │   ├── _text_agent.py   # _TextAgent 基类（只用于继承）
│   │   ├── polisher_agent.py    # PolisherAgent - 润色 agent
│   │   └── validator_agent.py   # ValidatorAgent - 验证 agent（单次验证）
│   ├── tools/
│   │   ├── __init__.py
│   │   └── validator.py     # ValidatorTool（内部实例化 ValidatorAgent）
├── main.py                  # 主程序（已有，集成 agent 模块）
├── gui.py                   # GUI（已集成 agent）
└── requirements.txt         # 依赖清单
```

---

## 🔄 Agent 内部流程

```
用户输入文本
    ↓
Wisadel.run(input_text)
    ↓
构建 messages = [
    {role: SYSTEM, content: system_prompt},
    {role: USER, content: input_text}
]
    ↓
Loop (max_steps 次):
    ↓
    model.generate(messages) → 润色结果
    ↓
    如果有内置 validator_tool：
        ↓
        调用 validator_tool(润色结果)
        ↓
        ├─ "PASS" → 返回润色结果，结束
        └─ "FAIL: 原因" → messages 追加失败原因，继续循环
    ↓
    否则 → 直接返回润色结果
    ↓
如果达到 max_steps 限制：
    print("FAIL: 原因")
    返回最后一次润色结果
```

---

## 🎯 设计理念

- **Agent as Protocol**：smolagents 提供协议框架，MiniMax 提供能力
- **集成而非独立**：直接服务于 windows-app 的文本润色场景
- **最小化改动**：在现有架构基础上添加 agent 能力
