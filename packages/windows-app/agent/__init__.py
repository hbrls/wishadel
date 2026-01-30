"""
Text-Only Agent 模块

基于 smolagents 实现的 Text-Only Agent Protocol

注意：
- `_TextAgent` 是 Protocol 基类，只用于继承，不直接使用
- 具体 Agent 实现请从 `agent.agents` 导入（如 ValidatorAgent）
"""

from .core import Wisadel
from .providers.minimax_provider import MinimaxProvider

__all__ = [
    "Wisadel",
    "MinimaxProvider",
]
