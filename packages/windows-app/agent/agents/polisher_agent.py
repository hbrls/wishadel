from smolagents.models import Model, ChatMessage, MessageRole
from smolagents.tools import Tool
from agent.charms import CHARM_POLISH
from agent.agents._text_agent import _TextAgent


class PolisherAgent(_TextAgent):
    """
    润色 Agent
    
    继承 _TextAgent 的能力，使用 CHARM_POLISH。
    可选内置 validator_tool 进行质量验收：
    - 验证通过 → 返回润色结果
    - 验证失败 → 继续 loop
    - 超限 → 返回最后一次结果
    """
    
    def __init__(
        self,
        model: Model,
        max_steps: int = 3,
        validator_tool: Tool = None
    ):
        """
        初始化 PolisherAgent
        
        Args:
            model: LLM Provider
            max_steps: 最大循环次数（默认 3）
            validator_tool: 可选的内置验证工具
        """
        super().__init__(
            model=model,
            system_prompt=CHARM_POLISH,
            max_steps=max_steps,
            tools=[],
            validator_tool=validator_tool
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
            # 提取 content（可能是 str 或 ChatMessage）
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            # 保存润色结果
            last_result = content
            
            # 如果有内置验证工具，调用验证
            if self.validator_tool:
                # validator_tool 返回 "PASS" 或 "FAIL: 原因"
                validation_result = self.validator_tool(content)
                
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
