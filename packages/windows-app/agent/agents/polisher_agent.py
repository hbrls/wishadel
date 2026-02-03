from typing import List, Optional
from smolagents.models import Model, ChatMessage, MessageRole
from smolagents.tools import Tool
from agent.charms import CHARM_POLISH
from agent.agents._text_agent import _TextAgent


class PolisherAgent(_TextAgent):
    """
    润色 Agent

    继承 _TextAgent 的能力，使用 CHARM_POLISH。
    可选内置验证工具进行质量验收：
    - 验证通过 → 返回润色结果
    - 验证失败 → 继续 loop
    - 超限 → 返回最后一次结果

    验证工具应通过 tools 列表传入，agent 会在运行时查找并使用。
    """

    def __init__(
        self,
        model: Model,
        max_steps: int = 3,
        tools: Optional[List[Tool]] = None
    ):
        """
        初始化 PolisherAgent

        Args:
            model: LLM Provider
            max_steps: 最大循环次数（默认 3）
            tools: 可选工具列表（包括验证工具）
        """
        super().__init__(
            model=model,
            system_prompt=CHARM_POLISH,
            max_steps=max_steps,
            tools=tools or []
        )

    def run(self, input_text: str) -> str:
        """
        执行润色，返回润色后的结果

        Args:
            input_text: 用户输入的原始文本

        Returns:
            润色后的文本
        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=self.system_prompt),
            ChatMessage(role=MessageRole.USER, content=input_text)
        ]

        last_result = None

        for step in range(self.max_steps):
            # 调用模型生成润色结果
            response = self.model.generate(messages)
            content = response.content

            # 保存润色结果
            last_result = content

            # 从 tools 列表中查找验证工具（目前只支持 validate 类型工具）
            validator_tool = next((t for t in self.tools if 'validate' in t.name.lower()), None)

            # 如果有验证工具，调用验证
            if validator_tool:
                # validator_tool 返回 "PASS" 或 "FAIL: 原因"
                validation_result = validator_tool(content)

                if validation_result.startswith("PASS"):
                    # 验证通过，返回润色结果
                    return content
                else:
                    # 验证失败，追加到 messages 继续循环
                    messages.append(ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=content
                    ))
                    messages.append(ChatMessage(
                        role=MessageRole.USER,
                        content=f"验证失败: {validation_result}"
                    ))
            else:
                # 没有验证工具，直接返回
                return content

        # 达到 max_steps 限制
        return last_result
