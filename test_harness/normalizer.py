from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from typing import Any


CODE_FENCE_RE = re.compile(
    r"```[ \t]*(?P<language>[^\n`]*)\n(?P<code>.*?)```",
    re.IGNORECASE | re.DOTALL,
)

PYTHON_LANGUAGES = {"", "py", "python", "python3"}


@dataclass(frozen=True)
class NormalizedProgram:
    task_id: str
    code: str | None
    status: str
    extraction_method: str | None
    syntax_error: str | None = None


@dataclass(frozen=True)
class TestCase:
    stdin: str
    expected_stdout: str


def parse_test_cases(raw_tests: Any) -> list[TestCase]:
    """Convert LCB or APPS stdin/stdout tests to one common representation."""
    try:
        tests = json.loads(raw_tests) if isinstance(raw_tests, str) else raw_tests
    except json.JSONDecodeError as exc:
        raise ValueError(f"Tests contain invalid JSON: {exc.msg}") from exc

    if isinstance(tests, list):
        pairs = []
        for index, case in enumerate(tests):
            if not isinstance(case, dict) or "input" not in case or "output" not in case:
                raise ValueError(
                    f"LCB test {index} must contain 'input' and 'output'"
                )
            pairs.append((case["input"], case["output"]))
    elif isinstance(tests, dict):
        inputs = tests.get("inputs")
        outputs = tests.get("outputs")
        if not isinstance(inputs, list) or not isinstance(outputs, list):
            raise ValueError("APPS tests must contain 'inputs' and 'outputs' lists")
        if len(inputs) != len(outputs):
            raise ValueError(
                "APPS test input/output count mismatch: "
                f"{len(inputs)} inputs and {len(outputs)} outputs"
            )
        pairs = list(zip(inputs, outputs, strict=True))
    else:
        raise ValueError("Tests must decode to an LCB list or an APPS dictionary")

    if not pairs:
        raise ValueError("No test cases found")

    test_cases = []
    for index, (test_input, expected_output) in enumerate(pairs):
        if not isinstance(test_input, str) or not isinstance(expected_output, str):
            raise ValueError(
                f"Test {index} is not a stdin/stdout string test; "
                "function-call tests need a separate evaluator"
            )
        test_cases.append(
            TestCase(
                stdin=test_input,
                expected_stdout=expected_output,
            )
        )

    return test_cases


def normalize_generation(
    *,
    task_id: str,
    prediction: str,
    thinking: bool,
    finish_reason: str,
    error: str | None = None,
) -> NormalizedProgram:
    if finish_reason == "error" or error:
        return NormalizedProgram(
            task_id=task_id,
            code=None,
            status="generation_error",
            extraction_method=None,
        )

    text = (prediction or "").strip()
    if not text:
        return NormalizedProgram(
            task_id=task_id,
            code=None,
            status="empty_prediction",
            extraction_method=None,
        )

    if thinking:
        if "</think>" not in text:
            return NormalizedProgram(
                task_id=task_id,
                code=None,
                status="incomplete_thinking",
                extraction_method=None,
            )
        text = text.rsplit("</think>", 1)[1].strip()

    fenced_candidates: list[str] = []
    for match in CODE_FENCE_RE.finditer(text):
        language = match.group("language").strip().lower()
        if language in PYTHON_LANGUAGES:
            fenced_candidates.append(match.group("code").strip())

    if fenced_candidates:
        valid_candidates = [
            candidate for candidate in fenced_candidates if is_valid_python(candidate)
        ]
        candidates = valid_candidates or fenced_candidates
        code = max(candidates, key=len)
        method = "python_fence"
    else:
        code = text
        method = "plain_text"

    code = code.strip().lstrip("\ufeff")
    if not code:
        return NormalizedProgram(
            task_id=task_id,
            code=None,
            status="empty_code",
            extraction_method=method,
        )

    try:
        ast.parse(code)
    except SyntaxError as exc:
        return NormalizedProgram(
            task_id=task_id,
            code=code,
            status="syntax_error",
            extraction_method=method,
            syntax_error=f"{exc.msg} at line {exc.lineno}",
        )

    return NormalizedProgram(
        task_id=task_id,
        code=code,
        status="ok",
        extraction_method=method,
    )


def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
    except SyntaxError:
        return False

    return True
