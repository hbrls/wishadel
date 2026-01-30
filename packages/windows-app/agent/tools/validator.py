from typing import Optional
from smolagents.tools import Tool
from smolagents.models import Model


class ValidatorTool(Tool):
    """
    验证润色结果的 Tool
    
    用于验证润色结果的 Tool，内置在 PolisherAgent 中作为验收机制。
    纯包装，内部使用 ValidatorAgent。
    注意：model 需在外部设置（tool 本身无 init 入参）。
    """
    
    name = "validate_polish_result"
    description = """验证润色结果是否符合润色标准。
输入是润色后的文本，输出是 "PASS" 或 "FAIL: 原因"。"""
    inputs = {
        "text": {
            "type": "string",
            "description": "需要验证的润色结果文本"
        }
    }
    output_type = "string"
    
    def __init__(self):
        """初始化 ValidatorTool（无入参）"""
        self._model: Optional[Model] = None
        super().__init__()
    
    def set_model(self, model: Model):
        """设置验证用的 model"""
        self._model = model
    
    def forward(self, text: str) -> str:
        """
        验证润色结果
        
        Args:
            text: 润色后的文本
            
        Returns:
            "PASS" 表示验证通过，"FAIL: 原因" 表示验证失败
        """
        from agent.agents.validator_agent import ValidatorAgent
        
        if self._model is None:
            raise ValueError("ValidatorTool 需要先调用 set_model() 设置 model")
        
        validator_agent = ValidatorAgent(self._model)
        return validator_agent.run(text)
