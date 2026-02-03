from smolagents.models import Model
from smolagents.tools import Tool
from typing import List, Optional


class Wisadel:
    """
    Wisadel Agent 对外接口

    内部使用 PolisherAgent 实现润色功能。
    """

    def __init__(
        self,
        model: Model,
        max_steps: int = 3,
        tools: Optional[List[Tool]] = None
    ):
        """
        初始化 Wisadel

        Args:
            model: LLM Provider
            max_steps: 最大循环次数（默认 3）
            tools: 可选工具列表
        """
        from agent.agents import PolisherAgent
        from agent.tools import ValidatorTool

        self.model = model
        self.max_steps = max_steps
        self._tools = tools or []

        validator_tool = ValidatorTool()
        validator_tool.set_model(model)

        # 将验证工具添加到 tools 列表
        agent_tools = list(self._tools) + [validator_tool]

        self._agent = PolisherAgent(
            model=model,
            max_steps=max_steps,
            tools=agent_tools
        )

    def run(self, input_text: str) -> str:
        """
        执行润色

        Args:
            input_text: 用户输入的原始文本

        Returns:
            润色后的文本
        """
        return self._agent.run(input_text)
