"""
Integration tests for GLM Provider

使用真实 API 调用测试 GLM Provider
需要设置环境变量：WISADEL_GLM_API_KEY
"""

import os
import unittest


class TestGLMProvider(unittest.TestCase):
    """GLM Provider 集成测试（真实 API 调用）"""

    @classmethod
    def setUpClass(cls):
        """设置测试环境，从环境变量读取 API Key"""
        cls.api_key = os.environ.get("WISADEL_GLM_API_KEY")
        if not cls.api_key:
            raise unittest.SkipTest(
                "WISADEL_GLM_API_KEY 环境变量未设置\n"
                "请设置环境变量：export WISADEL_GLM_API_KEY='your-api-key'"
            )

    def test_call_returns_string(self):
        """Test that __call__ returns a non-empty string"""
        from agent.providers.glm_provider import GLMProvider

        provider = GLMProvider(api_key=self.api_key, model="GLM-4.7")

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."}
        ]

        response = provider(messages)

        print(f"Response: {repr(response)}")
        print(f"Response length: {len(response)}")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_call_with_simple_prompt(self):
        """Test __call__ with a simple prompt"""
        from agent.providers.glm_provider import GLMProvider

        provider = GLMProvider(api_key=self.api_key, model="GLM-4.7")

        messages = [
            {"role": "user", "content": "What is 1+1? Answer only with the number."}
        ]

        response = provider(messages)

        self.assertIsInstance(response, str)
        # Response should contain "2"
        self.assertIn("2", response)


if __name__ == '__main__':
    unittest.main()
