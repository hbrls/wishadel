import os
import unittest


class TestWisadel(unittest.TestCase):
    """Wisadel 单元测试"""

    @classmethod
    def setUpClass(cls):
        """Set up test class with API key from environment"""
        cls.api_key = os.environ.get("WISADEL_MINIMAX_API_KEY")
        cls.model = os.environ.get("WISADEL_MINIMAX_MODEL")
        if not cls.api_key:
            raise unittest.SkipTest("WISADEL_MINIMAX_API_KEY environment variable not set")
        if not cls.model:
            raise unittest.SkipTest("WISADEL_MINIMAX_MODEL environment variable not set")

    def test_run_returns_string(self):
        """测试 run 方法返回字符串"""
        from agent import Wisadel, MinimaxProvider

        provider = MinimaxProvider(api_key=self.api_key, model=self.model)
        agent = Wisadel(model=provider)
        
        result = agent.run("这个项目需要尽快完成。")
        
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

if __name__ == "__main__":
    unittest.main()
