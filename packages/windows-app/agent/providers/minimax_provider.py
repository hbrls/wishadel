"""
Minimax Provider for smolagents

实现 smolagents 的 Model 接口，封装 MiniMax API 调用
使用 Anthropic SDK 风格的接口，但调用 MiniMax 服务
"""

from typing import List, Dict, Any
from smolagents.models import Model
import anthropic
import anthropic.types


class MinimaxProvider(Model):
    """
    MiniMax Provider
    
    实现 smolagents 的 Model 接口，封装 MiniMax API 调用
    使用 Anthropic SDK 风格的接口
    """
    
    API_URL = "https://api.minimaxi.com/anthropic"
    
    def __init__(self, api_key: str, model: str = "MiniMax-M2.1"):
        """
        初始化 MiniMax Provider
        
        Args:
            api_key: MiniMax API Key
            model: 模型名称（默认 MiniMax-M2.1）
        """
        self.api_key = api_key
        self.model = model
    
    def __call__(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        调用 MiniMax API，返回完整响应文本
        
        Args:
            messages: 消息列表（smolagents 格式）
            temperature: 温度参数
            max_tokens: 最大 token 数
            **kwargs: 其他参数
            
        Returns:
            完整响应文本
        """
        try:
            # 使用 Anthropic SDK 构建消息格式
            system_message = None
            anthropic_messages: List[anthropic.types.MessageParam] = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    anthropic_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # 使用 Anthropic SDK 调用 MiniMax
            client = anthropic.Anthropic(
                api_key=self.api_key,
                base_url=self.API_URL
            )
            
            # 构建 API 调用参数
            api_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": anthropic_messages
            }
            
            if system_message:
                api_params["system"] = system_message
            
            if temperature != 0.7:
                api_params["temperature"] = temperature
            
            response = client.messages.create(**api_params)
            
            # 提取文本内容
            text_content = ""
            for block in response.content:
                if block.type == "text":
                    text_content += block.text
            
            return text_content
        except anthropic.APIError as e:
            raise RuntimeError(f"MiniMax API 调用失败: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"MiniMax 处理响应失败: {str(e)}") from e
