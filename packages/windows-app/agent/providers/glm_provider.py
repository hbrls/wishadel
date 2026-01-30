"""
GLM Provider for smolagents

实现 smolagents 的 Model 接口，封装智谱 GLM API 调用
使用 zai 包（ZhipuAiClient）
"""

from typing import List, Dict, Any, Optional
from smolagents.models import Model, ChatMessage, MessageRole
from zai import ZhipuAiClient


class GLMProvider(Model):
    """
    智谱 GLM Provider

    实现 smolagents 的 Model 接口，封装智谱 GLM API 调用
    使用 zai 包（ZhipuAiClient）
    """

    API_URL = 'https://open.bigmodel.cn/api/paas/v4'

    def __init__(self, api_key: str, model: str = "GLM-4.7"):
        """
        初始化 GLM Provider

        Args:
            api_key: 智谱 API Key
            model: 模型名称（默认 GLM-4.7）
        """
        self.api_key = api_key
        self.model = model
        self._client: Optional[ZhipuAiClient] = None

    @property
    def client(self) -> ZhipuAiClient:
        """Lazy init client"""
        if self._client is None:
            self._client = ZhipuAiClient(
                api_key=self.api_key,
                base_url=self.API_URL
            )
        return self._client

    def generate(
        self,
        messages: List[ChatMessage],
        stop_sequences: Optional[List[str]] = None,
        response_format: Optional[Dict[str, str]] = None,
        tools_to_call_from: Optional[List] = None,
        **kwargs
    ) -> ChatMessage:
        """
        调用 GLM API，返回 ChatMessage

        Args:
            messages: 消息列表（smolagents ChatMessage 格式）
            stop_sequences: 停止序列（暂不支持）
            response_format: 响应格式（暂不支持）
            tools_to_call_from: 可用工具列表（暂不支持）
            **kwargs: 其他参数

        Returns:
            ChatMessage
        """
        # 转换 ChatMessage 为 API 格式
        api_messages: List[Dict[str, str]] = []

        for msg in messages:
            if msg.role == MessageRole.ASSISTANT:
                api_messages.append({
                    "role": "assistant",
                    "content": msg.content or ""
                })
            elif msg.role == MessageRole.USER:
                api_messages.append({
                    "role": "user",
                    "content": msg.content or ""
                })
            elif msg.role == MessageRole.SYSTEM:
                api_messages.append({
                    "role": "system",
                    "content": msg.content or ""
                })
            else:
                api_messages.append({
                    "role": str(msg.role),
                    "content": msg.content or ""
                })

        # 构建 API 调用参数
        api_params: Dict[str, Any] = {
            "model": self.model,
            "messages": api_messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        # 添加可选参数
        if kwargs.get("temperature") is not None:
            api_params["temperature"] = kwargs["temperature"]

        # 调用 API
        response = self.client.chat.completions.create(**api_params)

        # 提取文本内容
        text_content = ""
        if response.choices:
            text_content = response.choices[0].message.content or ""

        print(f"DEBUG: response = {response}")
        print(f"DEBUG: response.choices = {response.choices if hasattr(response, 'choices') else 'NO CHOICES'}")
        print(f"DEBUG: text_content = {repr(text_content)}")

        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content=text_content,
            raw=response
        )

    def __call__(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        调用 GLM API，返回完整响应文本

        Args:
            messages: 消息列表（dict 格式）
            temperature: 温度参数
            max_tokens: 最大 token 数
            **kwargs: 其他参数

        Returns:
            完整响应文本
        """
        try:
            # 转换为 ChatMessage 格式
            chat_messages = []
            for msg in messages:
                role = MessageRole(msg["role"]) if msg["role"] in ["user", "assistant", "system"] else MessageRole.USER
                chat_messages.append(ChatMessage(role=role, content=msg["content"]))

            # 调用 generate 方法
            response = self.generate(chat_messages, **kwargs)
            return response.content.strip()

        except Exception as e:
            raise RuntimeError(f"GLM API 调用失败: {str(e)}") from e
