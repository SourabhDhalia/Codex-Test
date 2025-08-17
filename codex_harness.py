#!/usr/bin/env python3
"""Simple harness to evaluate Codex on small programming tasks."""
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple, Any

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - best effort import
    openai = None  # type: ignore


@dataclass
class Task:
    prompt: str
    function: str
    tests: Sequence[Tuple[Sequence[Any], Any]]


def generate_code(prompt: str) -> str:
    if openai is None:
        raise RuntimeError("openai package is not installed")
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        max_tokens=256,
        temperature=0,
    )
    return response.choices[0].text


def evaluate_code(code: str, func_name: str, tests: Sequence[Tuple[Sequence[Any], Any]]) -> bool:
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    func = namespace.get(func_name)
    if not callable(func):
        raise ValueError(f"Function {func_name!r} not defined in generated code")
    for args, expected in tests:
        result = func(*args)
        if result != expected:
            raise AssertionError(f"For {func_name}{args}, expected {expected!r} but got {result!r}")
    return True


def run_task(task: Task, dry_run: bool = False) -> bool:
    print(f"\nTask: {task.prompt}")
    if dry_run:
        print("Dry run; skipping OpenAI API call")
        return True
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    code = generate_code(task.prompt)
    print("Generated code:\n", code)
    return evaluate_code(code, task.function, task.tests)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls and just display tasks")
    args = parser.parse_args()

    tasks: List[Task] = [
        Task(
            prompt="Write a Python function `add` that returns the sum of two numbers a and b.",
            function="add",
            tests=[((1, 2), 3), ((5, -1), 4)],
        ),
        Task(
            prompt="Implement a function `reverse_string` that returns the reverse of its input string.",
            function="reverse_string",
            tests=[(("abc",), "cba"), (("",), "")],
        ),
        Task(
            prompt="Create a function `factorial` that returns n! for a non-negative integer n.",
            function="factorial",
            tests=[((5,), 120), ((0,), 1)],
        ),
    ]

    success = True
    for t in tasks:
        try:
            run_task(t, dry_run=args.dry_run)
        except Exception as exc:  # pragma: no cover - display errors
            success = False
            print("Error:", exc)
    return 0 if success else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
