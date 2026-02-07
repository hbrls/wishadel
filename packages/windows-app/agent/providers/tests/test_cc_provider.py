"""
Integration tests for CC Provider

使用真实 API 调用测试 CC Provider
需要设置环境变量：WISADEL_CC_API_KEY
"""

import os
import unittest


class TestCCProvider(unittest.TestCase):
    """CC Provider 集成测试（真实 API 调用）"""

    @classmethod
    def setUpClass(cls):
        """设置测试环境，从环境变量读取 API Key"""
        cls.api_key = os.environ.get("WISADEL_CC_API_KEY")
        if not cls.api_key:
            # raise unittest.SkipTest("WISADEL_CC_API_KEY environment variable not set")
            cls.api_key = 'cr_93203c865eec5054009cfe501be25d5dccfe8ae169e6171c1001769b88e1085eb9c8b1e'

    def test_call_returns_string(self):
        """Test that __call__ returns a non-empty string"""
        from agent.providers.cc_provider import CCProvider

        provider = CCProvider(api_key=self.api_key)

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."}
        ]

        response = provider(messages)

        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_call_with_simple_prompt(self):
        """Test __call__ with a simple prompt"""
        from agent.providers.cc_provider import CCProvider

        provider = CCProvider(api_key=self.api_key)

        messages = [
            {"role": "user", "content": "What is 1+1? Answer only with the number."}
        ]

        response = provider(messages)

        self.assertIsInstance(response, str)
        # Response should contain "2"
        self.assertIn("2", response)


if __name__ == '__main__':
    unittest.main()
