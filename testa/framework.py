"""Minimal test registration, tagging and simple AOP-style hooks.

This module exposes:
- `test` decorator which can be used as `@test`, `@test("desc")`, or
  `@test(category="integration")`.
- Hook decorators: `before_all`, `after_all`, `before_each`, `after_each` that
  register functions to run around tests for a given category.

Tests are registered in the `TESTS` list as dicts with keys:
  name, func, description, category

The runner imports these globals to filter and execute tests.
"""

from typing import Callable, Optional

# Central registry of tests
TESTS = []

# Hooks stored per category (string -> list[callable])
BEFORE_ALL = {}
AFTER_ALL = {}
BEFORE_EACH = {}
AFTER_EACH = {}


def _register_hook(store: dict, category: str, func: Callable):
    store.setdefault(category, []).append(func)
    return func


def before_all(category: str):
    """Decorator: register a function to run once before all tests of `category`."""
    return lambda f: _register_hook(BEFORE_ALL, category, f)


def after_all(category: str):
    """Decorator: register a function to run once after all tests of `category`."""
    return lambda f: _register_hook(AFTER_ALL, category, f)


def before_each(category: str):
    """Decorator: register a function to run before each test of `category`.

    Hook signature: func(test_info) — receives the test dict.
    """
    return lambda f: _register_hook(BEFORE_EACH, category, f)


def after_each(category: str):
    """Decorator: register a function to run after each test of `category`.

    Hook signature: func(test_info, result) — receives the test dict and result.
    """
    return lambda f: _register_hook(AFTER_EACH, category, f)


def test(description: Optional[str] = None, category: str = "unit"):
    """Register a test.

    Usage:
      @test
      def t(ctx): ...

      @test("desc")
      def t(ctx): ...

      @test(category="integration")
      def t(ctx): ...

      @test("desc", category="e2e")
      def t(ctx): ...
    """

    # Case: used as @test without parentheses -> description is the callable
    if callable(description):
        func = description
        TESTS.append({
            "name": func.__name__,
            "func": func,
            "description": None,
            "category": category,
        })
        return func

    # Otherwise return a decorator that captures description and category
    def decorator(func: Callable):
        desc = description if isinstance(description, str) else None
        TESTS.append({
            "name": func.__name__,
            "func": func,
            "description": desc,
            "category": category,
        })
        return func

    return decorator
