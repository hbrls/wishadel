import os
import unittest


class TestSimplePassFailValidator(unittest.TestCase):

    def test_validator_pass_returns_true(self):
        """测试严格等于 'PASS' 返回 True"""
        from agent.agents.validator_agent import _SimplePassFailValidator
        validator = _SimplePassFailValidator()
        self.assertTrue(validator("PASS"))
        # PASS 有后续内容是无效的
        self.assertFalse(validator("PASS 额外内容"))

    def test_validator_fail_with_space_returns_true(self):
        """测试 'FAIL: ' 开头返回 True"""
        from agent.agents.validator_agent import _SimplePassFailValidator
        validator = _SimplePassFailValidator()
        self.assertTrue(validator("FAIL: 格式不正确"))

    def test_validator_invalid_returns_false(self):
        """测试无效格式返回 False"""
        from agent.agents.validator_agent import _SimplePassFailValidator
        validator = _SimplePassFailValidator()
        # FAIL 没有冒号空格是无效的
        self.assertFalse(validator("FAIL"))
        self.assertFalse(validator("FAIL:无空格"))
        self.assertFalse(validator("无效结果"))
        self.assertFalse(validator("通过"))


class TestValidatorAgent(unittest.TestCase):

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
        from agent.agents import ValidatorAgent

        provider = MinimaxProvider(api_key=self.api_key, model=self.model)
        agent = ValidatorAgent(provider)

        result = agent.run("润色后的文本")
        self.assertIsInstance(result, str)

    def test_agent_result_starts_with_pass_or_fail(self):
        """测试结果以 PASS 或 FAIL 开头"""
        from agent import MinimaxProvider
        from agent.agents import ValidatorAgent

        provider = MinimaxProvider(api_key=self.api_key, model=self.model)
        agent = ValidatorAgent(provider)

        result = agent.run("润色后的文本")
        stripped = result.strip()
        self.assertTrue(
            stripped.startswith("PASS") or stripped.startswith("FAIL"),
            f"结果应该以 PASS 或 FAIL 开头，实际: {result}"
        )


if __name__ == "__main__":
    unittest.main()
