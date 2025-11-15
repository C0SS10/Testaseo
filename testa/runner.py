from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib
import os
from testa.exceptions.assertion_error_detailed import AssertionErrorDetailed
from testa.framework import TESTS
from testa.models.colors import bold, green, red, yellow
from testa.models.test_context import TestContext
from testa.models.test_result import TestResult


def run_single_test(test_info):
    function = test_info["func"]
    name = test_info["description"] or test_info["name"]

    print(f"⏳ Starting: {name}")

    context = TestContext()

    try:
        function(context)
        print(f"  {green('✓')} Finished: {name}")
        return TestResult(name, True)

    except AssertionErrorDetailed as error:
        print(f"  {red('✗')} Failed: {name}")
        return TestResult(name, False, str(error))

    except Exception as error:
        print(f"  {red('✗')} Error: {name}")
        return TestResult(name, False, f"Error inesperado:\n{error}")


def run_all_tests(max_workers=4):
    print(bold("⌛ Running tests...\n"))

    results = []

    # Ejecutar tests con hilos y logs en tiempo real
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(run_single_test, test): test for test in TESTS}

        for future in as_completed(futures):
            results.append(future.result())

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