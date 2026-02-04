# Text-Only Agent Spec (MVP)

## 1️⃣ 核心目标

在现有 Python 项目中引入一个**干净、Text-only Agent Protocol**：

* 输入 / 输出 Markdown 文本（内部可含轻量结构，但主要是文本）
* 以 **智谱 GLM** 为能力核心（MVP 阶段）
* Agent 管理：**role / system prompt / loop / 输出提取**
* 可选工具仅处理文本（text → text），不产生副作用
* 每次请求独立（stateless），互不干扰
* Loop 用于**质量验收**，而非 schema 或自主推理

> 成功判定：一次请求完整跑通，返回提取结果，loop 限制生效，后续请求独立。

---

## 2️⃣ Goals / Non-Goals

### ✅ Goals

1. Agent 协议：role + system prompt + loop 管理
2. 文本 I/O：用户输入 → GLM → 提取 `<RESULT>` 作为返回
3. Stateless 请求：每次请求互不影响，loop 内状态仅在当前请求期间存在
4. 可选工具：text → text，纯逻辑处理，无副作用
5. Loop / 质量验收：基于输出文本质量判断是否继续
6. GLM 接入（MVP 阶段）
7. Agent as Protocol：确保 agent 是协议壳，能力由 LLM 提供

### ❌ Non-Goals

* 多模型并行（Minimax 暂不实现）
* 强 schema 校验
* IDE / filesystem / OS side-effect 操作
* 自动调用现实世界工具（write_file / grep / shell 等）
* 长期记忆 / RAG
* 复杂 planner / critic 架构
* 输出结构过度强制化

---

## 3️⃣ 选型决策

| 框架             | 状态       | 原因                                                                       |
| -------------- | -------- | ------------------------------------------------------------------------ |
| mini-swe-agent | ❌ 不适合    | 强 world tool + 强任务范式 + LLM 适配成本高                                         |
| pydantic-ai    | ⚠️ 可用但偏离 | 偏向 schema / typed output，输出正确性 loop，不符合文本 agent 协议需求                     |
| **smolagents** | ✅ 最匹配    | Text-first agent protocol + provider-neutral + 可选工具；支持 stateless 请求和文本输出 |

> **最终选型**：**smolagents**
> 理由：符合 “Agent as Protocol, not Agent as Intelligence”，干净、可验证、MVP 可落地。

---

## 4️⃣ 核心约束

| 约束        | 描述                                        |
| --------- | ----------------------------------------- |
| 输入        | Markdown / 自然语言文本                         |
| 输出        | Markdown 文本，摘取 `<RESULT>` 部分作为返回          |
| LLM       | 调用智谱 GLM API，带 system prompt 和参数          |
| Loop      | 最大步数限制（如 3），用于质量验收，不做 schema 校验           |
| Stateless | 每次请求独立；loop 内状态在请求结束后释放                   |
| Tools     | 可选，仅 text → text，纯函数，无副作用                 |
| 内置验证工具   | TextAgent 可内置 ValidatorTool，作为 loop 验收机制；<br>验证工具使用独立的 model 和 prompt，验证结果（PASS/FAIL）追加到 messages context；<br>验证失败时，失败原因会回传给主 model 用于改进 |
| Agent     | 管理 role、prompt、loop 和输出提取，不承担能力本身         |
| 可扩展性      | 后续可接 Minimax 或其他 LLM Provider，但 MVP 阶段不实现 |
| Agent 架构   | `_TextAgent` 为 Protocol 基类（只用于继承，不直接使用）；<br>`PolisherAgent` 继承 `_TextAgent`，负责润色任务；<br>`ValidatorAgent` 继承 `_TextAgent`，负责单次验证；<br>`ValidatorTool` 封装 `ValidatorAgent`，暴露 Tool 接口；<br>外部代码只知道 `tools/validator`，不知道 `ValidatorAgent` |

---

## 5️⃣ Agent 内部流程（正向场景）

```
+------------------+
|   User Input     |
| Markdown / Text  |
+------------------+
          |
          v
+-------------------------------+
|        Agent Protocol         |
|  - Add role / system prompt   |
|  - Configure parameters       |
+-------------------------------+
          |
          v
+------------------+
|   GLM API Call   |
+------------------+
          |
          v
+---------------------------+
| Extract <RESULT> Section  |
+---------------------------+
          |
          v
+-------------------------------+
| Quality Check / Loop Control  |
| - Max N retries               |
| - Optional text-processing    |
|   tools: rewrite_text, etc.   |
+-------------------------------+
   |           |
   | Fail      | Pass
   |           v
   |       +--------------------+
   |       | Return Final Output|
   |       |  Extracted Result  |
   |       +--------------------+
   |
   +--> Retry loop (back to GLM API Call)
```

### 流程说明

* **Optional Tool**：在 loop 内可调用，仅处理文本
* **Stateless**：每次请求独立，loop 内状态仅在当前请求有效
* **Loop / Quality Check**：关注输出质量，非 schema 校验
* **Output**：Markdown 文本，摘取 `<RESULT>` 部分

---

## 6️⃣ MVP 验证指标（Definition of Done）

* [ ] 用户输入文本，调用 GLM 返回 Markdown 文本
* [ ] 成功提取 `<RESULT>` 部分作为返回
* [ ] loop 验收逻辑生效，最大步数限制可控制
* [ ] 多次请求独立执行，互不干扰
* [ ] 可选 text → text tool 能调用，执行结果正确
* [ ] agent 本身保持“协议层”，能力由 GLM 提供

---

## 7️⃣ Agent 核心原则写入 Spec

* **Agent as Protocol, not Agent as Intelligence**
* **选型**：smolagents
* **职责**：协议管理 + 输出提取 + loop / role 控制
* **能力**：由 LLM 提供
* **MVP 范围**：正向场景，stateless，text-only
