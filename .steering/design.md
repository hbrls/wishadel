# Design Principles

> updated_by: VSCode - Claude-Opus-4.6
> updated_at: 2026-02-21 14:48:00

## Design & Architecture

### Languages

| 用途 | 语言 | 版本 | 备注 |
|------|------|------|------|
| 主开发语言 | Python | 3.12 | 核心逻辑和 GUI |

### Frameworks

| 用途 | 框架 | 版本 | 备注 |
|------|------|------|------|
| 图形用户界面 | PySide6 | 最新稳定版 | 跨平台桌面 UI |
| AI Agent 框架 | smolagents | 最新稳定版 | Agent 编排框架 |

### Infrastructure

| 组件 | 设计选择 | 提供商 | 备注 |
|------|----------|--------|------|
| LLM 服务 | 可插拔设计 | 多种（MiniMax, OpenAI, Anthropic 等） | 通过 Provider 接口支持多种 LLM |
| 日志系统 | 文件 + 控制台 | loguru | 支持日志轮转 |
| 构建工具 | PyInstaller | - | Windows/macOS 打包 |

## Architecture Overview

Wisadel 采用分层架构设计：

```
┌─────────────────────────────────────┐
│           UI Layer (PySide6)        │
│  MainWindow │ SystemTray │ Worker  │
├─────────────────────────────────────┤
│         Agent Layer (smolagents)    │
│  Wisadel │ Polisher │ Validator     │
├─────────────────────────────────────┤
│        Provider Layer (Abstract)   │
│   MinimaxProvider │ OpenAIProvider │
├─────────────────────────────────────┤
│         Platform Layer             │
│  Hotkey │ Platform Utils │ Focus   │
└─────────────────────────────────────┘
```

### 核心组件

| 组件 | 职责 | 依赖 |
|------|------|------|
| `Wisadel` | 对外统一接口，协调 Agent 流程 | `PolisherAgent`, `ValidatorTool` |
| `PolisherAgent` | 文本润色核心逻辑 | `smolagents.Agent` |
| `ValidatorAgent` | 文本验证逻辑 | LLM |
| `Provider` | LLM 接口抽象层 | 各 LLM SDK |
| `MainWindow` | 主界面 | `PySide6` |
| `SystemTray` | 系统托盘 | `PySide6` |

## Dependencies

### External Services

| 服务 | 用途 | 关键性 | 备选方案 |
|------|------|--------|----------|
| MiniMax API | 默认 LLM 服务 | 高 | 可切换至其他 Provider |
| OpenAI API | 备选 LLM 服务 | 中 | 可作为替代 |
| Anthropic API | 备选 LLM 服务 | 中 | 可作为替代 |

### Python Dependencies

核心依赖（见 `requirements.txt`）：

- `PySide6` - 图形界面框架
- `smolagents` - Agent 框架
- `loguru` - 日志系统
- `pynput` - 全局键盘监听

## Development Environment

### Required Tools

- Python 3.12+
- pip / pipenv / poetry
- Git

### Setup

<!-- // 遵循团队统一的开发环境配置，如有特殊安装或启动步骤，在此说明。 -->

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `WISADEL_MINIMAX_API_KEY` | 是 | MiniMax API Key |
| `WISADEL_OPENAI_API_KEY` | 否 | OpenAI API Key |

## Design Decisions

### 必须使用

- **smolagents**: 作为 Agent 框架，提供工具调用和状态管理能力
- **PySide6**: 作为 GUI 框架，确保跨平台一致性

### 必须不使用

- **tkinter**: 不使用内置 tkinter，优先选择 PySide6
- **PyQt5**: 选择更新的 PySide6

### 推荐使用

- **loguru**: 优于标准 logging，提供更简洁的 API
- **类型注解**: 使用 Python 类型提示提高代码可维护性

## Design Debt

### Known Issues

| 问题 | 影响 | 优先级 | 计划 |
|------|------|--------|------|
| Linux 平台支持不完整 | Linux 下全局快捷键暂不支持 | 中 | 下个季度支持 |
| macOS 文本注入未实现 | macOS 版 Accept 仅隐藏窗口 | 低 | 后续版本评估 |

### Technical Debt Budget

- 每个 sprint 预留 **10%** 时间处理技术债务
- 大规模重构需要先撰写技术规格

## Architecture Decisions Records (ADRs)

| ADR | 标题 | 状态 | 日期 |
|-----|------|------|------|
| ADR-001 | 采用 smolagents 作为 Agent 框架 | 已通过 | 2026-01 |
| ADR-002 | 采用 PySide6 构建跨平台 GUI | 已通过 | 2026-01 |
| ADR-003 | Provider 接口抽象，支持多 LLM | 已通过 | 2026-01 |

## Changelog

<!-- // 这是一个 Living Document，如无必要，无需维护变更历史。 -->
