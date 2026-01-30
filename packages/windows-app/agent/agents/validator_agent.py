from smolagents.models import Model, ChatMessage, MessageRole
from smolagents.tools import Tool
from agent.charms import CHARM_POLISH_VALIDATE
from agent.agents._text_agent import _TextAgent


class _SimplePassFailValidator(Tool):
    """
    简单的 PASS/FAIL 格式校验工具
    
    检查验证结果格式：
    - 严格等于 "PASS" → True
    - 以 "FAIL: " 开头（英文冒号+空格）→ True
    - 其他 → False
    """
    
    name = "simple_passfail_validator"
    description = "检查验证结果是否是有效的 PASS 或 FAIL 格式，返回布尔值。"
    inputs = {
        "text": {
            "type": "string",
            "description": "需要检查的验证结果文本"
        }
    }
    output_type = "boolean"
    
    def forward(self, text: str) -> bool:
        """
        校验 PASS/FAIL 格式
        
        Args:
            text: 验证结果文本
            
        Returns:
            True 表示格式有效（PASS 或 FAIL: 原因），False 表示格式无效
        """
        if text == "PASS":
            return True
        if text.startswith("FAIL: "):
            return True
        return False


class ValidatorAgent(_TextAgent):
    """
    验证润色结果的 Agent
    
    继承 _TextAgent 的能力，使用 CHARM_POLISH_VALIDATE。
    内置 _SimplePassFailValidator 校验返回格式。
    """
    
    def __init__(self, model: Model):
        """
        初始化 ValidatorAgent
        
        Args:
            model: LLM Provider（MiniMax 等）
        """
        # 使用 _TextAgent 的循环能力
        super().__init__(
            model=model,
            system_prompt=CHARM_POLISH_VALIDATE,
            max_steps=3,  # 最多 3 次验证
            tools=[],
            validator_tool=_SimplePassFailValidator()
        )
    
    def run(self, text: str) -> str:
        """
        验证润色结果
        
        Args:
            text: 润色后的文本
            
        Returns:
            "PASS" 表示验证通过，"FAIL: 原因" 表示验证失败
        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=self.system_prompt),
            ChatMessage(role=MessageRole.USER, content=text)
        ]
        
        last_result = None
        
        for step in range(self.max_steps):
            # 调用 model 生成验证结果
            response = self.model.generate(messages)
            # 提取 content（可能是 str 或 ChatMessage）
            if hasattr(response, 'content'):
                result = response.content
            else:
                result = str(response)
            last_result = result
            
            # 使用内置工具收敛验证结果
            is_valid = self.validator_tool(result)
            
            # 始终返回 result（model 原始返回）
            if is_valid:
                return result
            
            # 验证失败，追加到 messages 继续循环
            messages.append(ChatMessage(
                role=MessageRole.ASSISTANT,
                content=result
            ))
            messages.append(ChatMessage(
                role=MessageRole.USER,
                content="请重新验证，仅返回 PASS 或 FAIL: 原因"
            ))
        
        # loop 超限
        print(f"验证失败: {last_result}")
        return last_result
