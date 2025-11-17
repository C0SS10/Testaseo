from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib
import os
from testa.exceptions.assertion_error_detailed import AssertionErrorDetailed
from testa.framework import TESTS, BEFORE_ALL, AFTER_ALL, BEFORE_EACH, AFTER_EACH
from testa.models.colors import bold, green, red, yellow
from testa.models.test_context import TestContext
from testa.models.test_result import TestResult


def run_single_test(test_info):
    """Run one test and honor before_each/after_each hooks for its category."""
    function = test_info["func"]
    name = test_info["description"] or test_info["name"]
    category = test_info.get("category", "unit")

    print(f"⏳ Starting: {name} [{category}]")

    context = TestContext()

    # Run before_each hooks
    for hook in BEFORE_EACH.get(category, []):
        try:
            hook(test_info)
        except Exception:
            # hook errors should not stop tests
            pass

    try:
        function(context)
        print(f"  {green('✓')} Finished: {name}")
        result = TestResult(name, True)

    except AssertionErrorDetailed as error:
        print(f"  {red('✗')} Failed: {name}")
        result = TestResult(name, False, str(error))

    except Exception as error:
        print(f"  {red('✗')} Error: {name}")
        result = TestResult(name, False, f"Error inesperado:\n{error}")

    # Run after_each hooks
    for hook in AFTER_EACH.get(category, []):
        try:
            hook(test_info, result)
        except Exception:
            pass

    return result


def run_all_tests(types=None, max_workers=4, category_workers: dict = None):
    """Run tests optionally filtered by `types` (list of categories).

    Execution model:
      - Group tests by category.
      - For each category: run BEFORE_ALL hooks, then execute that category's
        tests in a dedicated ThreadPoolExecutor (workers controlled via
        `category_workers`), then run AFTER_ALL hooks.

    Parameters:
      types: list or None -> categories to run (None == all)
      max_workers: default workers when category_workers not provided
      category_workers: optional dict mapping category->workers
    """
    print(bold("⌛ Running tests...\n"))

    results = []

    # Filter tests by requested types
    tests_to_run = [t for t in TESTS if types is None or t.get("category") in types]

    # Group by category
    from collections import defaultdict

    tests_by_cat = defaultdict(list)
    for t in tests_to_run:
        tests_by_cat[t.get("category", "unit")].append(t)

    # For each category create a dedicated executor and submit its tests
    category_executors = {}
    all_futures = []

    for category, tests in tests_by_cat.items():
        # run before_all hooks
        for hook in BEFORE_ALL.get(category, []):
            try:
                hook(category)
            except Exception:
                pass

        workers = (category_workers or {}).get(category, max_workers)
        executor = ThreadPoolExecutor(max_workers=workers)
        category_executors[category] = executor

        for test in tests:
            future = executor.submit(run_single_test, test)
            all_futures.append((future, test))

    # Collect results as they complete
    for future, test in all_futures:
        try:
            results.append(future.result())
        except Exception as e:
            # Shouldn't happen because run_single_test handles exceptions, but
            # be defensive.
            results.append(TestResult(test.get("description") or test.get("name"), False, str(e)))

    # After all futures finished, call after_all hooks and shutdown executors
    for category, executor in category_executors.items():
        # shutdown executor to free threads
        executor.shutdown(wait=True)

        for hook in AFTER_ALL.get(category, []):
            try:
                hook(category)
            except Exception:
                pass

    # Ordenar por orden de definición
    results_sorted = sorted(
        results,
        key=lambda r: next(
            i for i, t in enumerate(TESTS)
            if (t["description"] or t["name"]) == r.name
        )
    )

    passed = [r for r in results_sorted if r.passed]
    failed = [r for r in results_sorted if not r.passed]

    print()

    # Mostrar PASSED
    for result in passed:
        print(f"🟩 {result.name} PASSED")

    # Mostrar FAILED (solo título)
    for result in failed:
        print(f"🟥 {result.name} FAILED")

    # Explicación detallada de errores
    print()
    for result in failed:
        _print_failure(result)

    # Resumen
    print(bold(f"Passed: {len(passed)}   Failed: {len(failed)}"))

    return results_sorted

def _print_failure(result):
    print(yellow("─" * 50))
    print(red(f"🟥 FAIL: {result.name}"))
    print(bold(red("Assertion failed:\n")))
    print(result.error)
    print(yellow("─" * 50))
    print()

def discover_tests(directory="tests"):
    """ Función para descubrir y ejecutar todos los tests en el directorio "tests". """
    for filename in os.listdir(directory):
        if filename.startswith("test_") and filename.endswith(".py"):
            module_name = filename[:-3]
            importlib.import_module(f"{directory}.{module_name}")