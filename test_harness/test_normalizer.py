import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from normalizer import TestCase, normalize_generation, parse_test_cases  # noqa: E402


class NormalizeGenerationTests(unittest.TestCase):
    def test_extracts_no_thinking_python_fence(self):
        result = normalize_generation(
            task_id="example/1",
            prediction="```python\nprint('ok')\n```",
            thinking=False,
            finish_reason="stop",
        )

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.extraction_method, "python_fence")
        self.assertEqual(result.code, "print('ok')")

    def test_extracts_fence_after_thinking_and_prose(self):
        result = normalize_generation(
            task_id="example/2",
            prediction=(
                "<think>reasoning</think>\n"
                "Here is the solution.\n"
                "```python\nimport sys\nprint(sys.stdin.read())\n```\n"
                "This is efficient."
            ),
            thinking=True,
            finish_reason="stop",
        )

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.code, "import sys\nprint(sys.stdin.read())")

    def test_rejects_unclosed_thinking(self):
        result = normalize_generation(
            task_id="example/3",
            prediction="<think>unfinished reasoning",
            thinking=True,
            finish_reason="length",
        )

        self.assertEqual(result.status, "incomplete_thinking")
        self.assertIsNone(result.code)

    def test_preserves_valid_plain_python(self):
        result = normalize_generation(
            task_id="example/4",
            prediction="x = 1\nprint(x)",
            thinking=False,
            finish_reason="stop",
        )

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.extraction_method, "plain_text")

    def test_reports_syntax_error(self):
        result = normalize_generation(
            task_id="example/5",
            prediction="```python\ndef broken(:\n    pass\n```",
            thinking=False,
            finish_reason="stop",
        )

        self.assertEqual(result.status, "syntax_error")
        self.assertIsNotNone(result.syntax_error)

    def test_generation_error_takes_priority(self):
        result = normalize_generation(
            task_id="example/6",
            prediction="",
            thinking=True,
            finish_reason="error",
            error="ReadTimeout: ",
        )

        self.assertEqual(result.status, "generation_error")
        self.assertIsNone(result.code)

    def test_prefers_syntactically_valid_fence(self):
        result = normalize_generation(
            task_id="example/7",
            prediction=(
                "```python\ndef invalid(:\n    this block is longer but invalid\n```\n"
                "```python\nprint(42)\n```"
            ),
            thinking=False,
            finish_reason="stop",
        )

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.code, "print(42)")


class ParseTestCasesTests(unittest.TestCase):
    def test_parses_lcb_test_list(self):
        result = parse_test_cases(
            '[{"input": "2\\n", "output": "4\\n"}]'
        )

        self.assertEqual(result, [TestCase(stdin="2\n", expected_stdout="4\n")])

    def test_parses_apps_parallel_lists(self):
        result = parse_test_cases(
            {
                "inputs": ["2\n", "3\n"],
                "outputs": ["4\n", "6\n"],
            }
        )

        self.assertEqual(
            result,
            [
                TestCase(stdin="2\n", expected_stdout="4\n"),
                TestCase(stdin="3\n", expected_stdout="6\n"),
            ],
        )

    def test_rejects_mismatched_apps_lists(self):
        with self.assertRaisesRegex(ValueError, "count mismatch"):
            parse_test_cases({"inputs": ["2\n"], "outputs": []})

    def test_rejects_function_call_tests(self):
        with self.assertRaisesRegex(ValueError, "function-call tests"):
            parse_test_cases({"inputs": [[1, 2]], "outputs": [3]})


if __name__ == "__main__":
    unittest.main()
