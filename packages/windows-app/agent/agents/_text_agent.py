from abc import ABC, abstractmethod
from typing import List, Optional
from smolagents.models import Model, ChatMessage, MessageRole
from smolagents.tools import Tool


class _TextAgent(ABC):
    """
    Text-Only Agent Protocol
    
    基于 smolagents 的 Agent 基类，提供文本处理能力。
    使用 system prompt + 用户输入的方式与 LLM 交互。
    
    **注意**：此类只用于继承，不直接使用。
    具体 Agent 应继承此类并实现 run() 方法。
    """
    
    def __init__(
        self,
        model: Model,
        system_prompt: str,
        max_steps: int = 10,
        tools: Optional[List[Tool]] = None,
        validator_tool: Optional[Tool] = None
    ):
        """
        初始化 TextAgent
        
        Args:
            model: LLM Provider（MiniMax 等）
            system_prompt: System prompt，描述优化思路和要求
            max_steps: 最大循环次数（默认 10）
            tools: 可选工具列表
            validator_tool: 可选的内置验证工具
        """
        self.model = model
        self.system_prompt = system_prompt
        self.max_steps = max_steps
        self.tools = tools or []
        self.validator_tool = validator_tool
    
    @abstractmethod
    def run(self, input_text: str) -> str:
        """
        执行 agent，返回润色/优化后的结果
        
        Args:
            input_text: 用户输入的原始文本
            
        Returns:
            优化后的文本
            
        Note:
            子类必须实现此方法
        """
        ...
