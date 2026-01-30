import os
import unittest


class TestPolisherAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test class with API key from environment"""
        cls.api_key = os.environ.get("WISADEL_MINIMAX_API_KEY")
        cls.model = os.environ.get("WISADEL_MINIMAX_MODEL")
        if not cls.api_key:
            raise unittest.SkipTest("WISADEL_MINIMAX_API_KEY environment variable not set")
        if not cls.model:
            raise unittest.SkipTest("WISADEL_MINIMAX_MODEL environment variable not set")

    def test_agent_run_returns_string(self):
        """测试 run 方法返回字符串"""
        from agent import MinimaxProvider
        from agent.agents import PolisherAgent

        provider = MinimaxProvider(api_key=self.api_key, model=self.model)
        agent = PolisherAgent(provider, max_steps=1)

        result = agent.run("这个项目需要尽快完成。")
        self.assertIsInstance(result, str)

    def test_agent_without_validator_tool(self):
        """测试不带 validator_tool 的 PolisherAgent"""
        from agent import MinimaxProvider
        from agent.agents import PolisherAgent

        provider = MinimaxProvider(api_key=self.api_key, model=self.model)
        agent = PolisherAgent(provider, max_steps=1)

        # 没有验证工具，应该直接返回结果
        result = agent.run("这个项目需要尽快完成。")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_agent_with_validator_tool(self):
        """测试带 validator_tool 的 PolisherAgent"""
        # TODO: test_core 会覆盖这个用例


if __name__ == "__main__":
    unittest.main()
