# Code Structure

> updated_by: VSCode - Claude-Opus-4.6
> updated_at: 2026-02-21 14:47:00

## Project Layout

Wisadel 项目采用 monorepo 结构，主要代码位于 `packages/windows-app/` 目录下：

```
wishadel/
├── .steering/               # 项目公约文档
│   ├── constitution.md     # 项目治理原则
│   ├── product.md          # 产品愿景
│   ├── structure.md        # 代码结构规范
│   └── design.md           # 设计原则
├── .plans/                 # 项目计划文档
│   ├── 001-windows-app.md  # Windows 应用计划
│   └── 002-mac-app.md     # macOS 应用计划
├── packages/
│   └── windows-app/        # Windows/macOS 桌面应用
│       ├── agent/           # AI Agent 核心模块
│       │   ├── agents/     # Agent 实现
│       │   │   └── tests/  # Agent 测试
│       │   ├── providers/  # LLM 提供商
│       │   │   └── tests/  # Provider 测试
│       │   ├── tools/      # 工具函数
│       │   └── tests/      # 核心模块测试
│       ├── ui/             # 图形界面模块
│       │   ├── assets/     # UI 资源（图标等）
│       │   └── tests/      # UI 测试
│       ├── main.py         # 应用入口
│       ├── focus.py        # 焦点管理与文本注入（Windows）
│       ├── hotkey_manager.py    # 全局快捷键管理
│       ├── platform_utils.py     # 平台检测工具
│       ├── logger_config.py     # 日志配置
│       ├── Wisadel.spec   # PyInstaller 配置
│       ├── build.bat       # Windows 构建脚本
│       └── requirements.txt     # Python 依赖
├── AGENTS.md              # AI 协作规范
└── README.md               # 项目说明
```

## Module Organization

### 模块职责

| 模块 | 职责 | 主要组件 |
|------|------|----------|
| `agent` | AI 润色和验证核心逻辑 | `Wisadel`, `PolisherAgent`, `ValidatorAgent` |
| `agent/providers` | LLM 提供商接口 | `MinimaxProvider` |
| `agent/tools` | Agent 工具函数 | `ValidatorTool` |
| `ui` | 图形用户界面 | `MainWindow`, `SystemTrayIcon`, `PolishWorker` |
| 根目录 | 平台相关功能 | `hotkey_manager`, `platform_utils` |

### Naming Conventions

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件/目录 | snake_case | `hotkey_manager.py`, `polisher_agent.py` |
| 类名 | PascalCase | `Wisadel`, `MainWindow`, `SystemTrayIcon` |
| 函数/方法 | snake_case | `register_global_hotkey`, `on_accept` |
| 常量 | UPPER_SNAKE_CASE | `DEFAULT_MAX_STEPS` |
| 私有方法/属性 | _snake_case（单下划线前缀） | `_agent`, `_tools` |

### Import Order

Python 代码中的导入顺序应遵循以下规范：

1. **标准库导入** - Python 内置模块
2. **第三方库导入** - 外部包（如 `PySide6`, `loguru`, `smolagents`）
3. **本地应用导入** - 项目内部模块

```python
# 标准库
import os
import sys
from typing import List, Optional

# 第三方库
from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import QApplication
from loguru import logger
from smolagents.models import Model

# 本地应用导入
from agent import Wisadel, MinimaxProvider
from ui.main_window import MainWindow
from ui.system_tray import SystemTrayIcon
from hotkey_manager import register_global_hotkey
```

### Import 分组规则

在每个分组内，按字母顺序排列导入。对于本地导入，按层级从深到浅排序：

```python
# 第三方库
from pynput import keyboard

# 本地导入 - 先按模块层级
from agent import Wisadel
from agent.agents import PolisherAgent
from agent.providers import MinimaxProvider
from agent.tools import ValidatorTool
from ui.main_window import MainWindow
from ui.polish_worker import PolishWorker
```

## Code Patterns

### Component Structure

Agent 模块的标准结构：

```python
"""模块描述"""

from typing import Optional
from loguru import logger


class ComponentName:
    """
    组件描述

    详细说明组件的功能和使用方法。
    """

    def __init__(self, param1: str, param2: Optional[int] = None):
        """
        初始化组件

        Args:
            param1: 参数1说明
            param2: 参数2说明（可选）
        """
        self.param1 = param1
        self.param2 = param2
        logger.debug(f"ComponentName 初始化: {param1}")

    def method_name(self, arg: str) -> str:
        """
        方法描述

        Args:
            arg: 参数说明

        Returns:
            返回值说明
        """
        logger.debug(f"method_name 被调用: {arg}")
        return f"result_{arg}"
```

### Error Handling

使用 try-except 块进行错误处理，并记录日志：

```python
from loguru import logger


def risky_operation():
    try:
        result = do_something()
        logger.debug(f"操作成功: {result}")
        return result
    except ValueError as e:
        logger.warning(f"值错误: {e}")
        raise
    except Exception as e:
        logger.error(f"未知错误: {e}")
        raise
```

### Logging

使用 `loguru` 进行日志记录：

```python
from loguru import logger

# 在模块顶部配置日志（logger_config.py）
logger.add("app.log", rotation="500 MB", level="INFO")

# 在代码中使用
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
```

## Testing Conventions

### Test File Location

测试文件放置在对应模块的 `tests/` 目录下：

```
agent/
├── agents/
│   ├── tests/
│   │   ├── test_polisher_agent.py
│   │   └── test_validator_agent.py
│   └── polisher_agent.py
├── providers/
│   ├── tests/
│   │   └── test_minimax_provider.py
│   └── minimax_provider.py
└── tests/
    └── test_core.py
```

### Test Naming

使用 `test_` 前缀命名测试文件，测试函数使用 `test_` 前缀：

```
test_module_name.py
test_function_name_scenario.py
```

### Test Structure

```python
"""测试模块名称"""

import pytest
from agent.module import ClassName


class TestClassName:
    """测试目标类"""

    def test_method_name_success(self):
        """测试方法在正常情况下的行为"""
        # Arrange
        obj = ClassName(param="test")

        # Act
        result = obj.method_name("input")

        # Assert
        assert result == "expected_output"

    def test_method_name_with_invalid_input(self):
        """测试方法在输入无效时的行为"""
        # Arrange
        obj = ClassName(param="test")

        # Act & Assert
        with pytest.raises(ValueError):
            obj.method_name("")
```

### Test Coverage

根据 `constitution.md` 中的要求，测试覆盖率最低要求为 **60%**。

## Documentation Standards

### 代码注释

- 使用注释解释 **为什么**，而不是 **是什么**
- 公共 API 必须使用 docstring 文档化
- 保持注释与代码同步更新

### Docstring 格式

```python
def function_name(param1: str, param2: int = 10) -> bool:
    """
    函数简短描述

    详细描述函数的功能、参数和返回值。

    Args:
        param1: 参数1的描述
        param2: 参数2的描述，默认值为 10

    Returns:
        返回值的描述

    Raises:
        ValueError: 当参数无效时抛出

    Example:
        >>> result = function_name("test", 5)
        >>> print(result)
        True
    """
    pass
```

## Dependency Management

### 添加依赖流程

1. 检查现有依赖是否已包含相似功能
2. 评估安全性（使用 `pip audit` 或 `safety` 检查）
3. 检查维护状态（最后更新时间、Issue 数量）
4. 在 PR 中说明添加依赖的原因

### 版本锁定

- 生产环境使用精确版本
- 开发环境允许小版本更新
- 主版本更新需明确审查

## Performance Guidelines

### 代码级优化

- 避免 N+1 查询问题
- 大数据使用懒加载
- 缓存昂贵计算结果
- 优化前先进行性能分析

### 响应时间目标

| 操作 | 目标响应时间 |
|------|-------------|
| 界面唤起 | < 100ms |
| 润色请求发送 | < 200ms |
| 整体流程 | < 5秒 |

## Changelog

<!-- // 这是一个 Living Document，如无必要，无需维护变更历史。 -->
