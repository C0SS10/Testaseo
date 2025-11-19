from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
import importlib
import os
from typing import Any, Dict, Iterable, List, Optional, Tuple
from testa.exceptions.assertion_error_detailed import AssertionErrorDetailed
from testa.framework import TESTS, BEFORE_ALL, AFTER_ALL, BEFORE_EACH, AFTER_EACH
from testa.models.colors import bold, green, red, yellow
from testa.models.test_context import TestContext
from testa.models.test_result import TestResult

def run_hooks(hooks: Iterable[Any], *args: Any) -> None:
    """
    Ejecuta una lista de hooks sin detener el flujo si uno falla.

    Args:
        hooks: Iterable con funciones hook.
        args: Argumentos que se pasan al hook.
    """
    for hook in hooks:
        try:
            hook(*args)
        except Exception:
            # Los errores de hooks no deben detener la ejecución
            continue


def run_single_test(test_info: Dict[str, Any]) -> TestResult:
    """
    Ejecuta un único test, incluyendo hooks before_each y after_each
    de la categoría asociada.

    Args:
        test_info: Diccionario con información del test.

    Returns:
        TestResult: Resultado de la prueba.
    """
    function = test_info["func"]
    name = test_info.get("description") or test_info.get("name")
    category = test_info.get("category", "unit")

    print(f"⏳ Starting: {name} [{category}]")

    context = TestContext()

    # Hooks before_each
    run_hooks(BEFORE_EACH.get(category, []), test_info)

    try:
        function(context)
        print(f"  {green('✓')} Finished: {name}")
        result = TestResult(name=name, passed=True)

    except AssertionErrorDetailed as error:
        print(f"  {red('✗')} Failed: {name}")
        result = TestResult(name=name, passed=False, error=str(error))

    except Exception as error:
        print(f"  {red('✗')} Error: {name}")
        result = TestResult(name=name, passed=False, error=f"Error inesperado:\n{error}")

    # Hooks after_each
    run_hooks(AFTER_EACH.get(category, []), test_info, result)

    return result


def run_all_tests(
    types: Optional[List[str]] = None,
    max_workers: int = 4,
    category_workers: Optional[Dict[str, int]] = None,
) -> List[TestResult]:
    """
    Ejecuta todas las pruebas, organizándolas por categoría y
    aplicando hooks before_all y after_all.

    Args:
        types: Lista de categorías a ejecutar o None para ejecutar todas.
        max_workers: Número de workers por defecto.
        category_workers: Configuración opcional workers por categoría.

    Returns:
        Lista ordenada de TestResult.
    """
    print(bold("⌛ Running tests...\n"))

    results: List[TestResult] = []

    # Filtrar pruebas según categorías indicadas
    tests_to_run = [
        t for t in TESTS
        if types is None or t.get("category") in types
    ]

    # Agrupar por categoría
    tests_by_cat: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for t in tests_to_run:
        category = t.get("category", "unit")
        tests_by_cat[category].append(t)

    # Ejecutores por categoría
    executors: Dict[str, ThreadPoolExecutor] = {}
    futures: List[Tuple[Future[TestResult], Dict[str, Any]]] = []

    # Asignar tareas por categoría
    for category, tests in tests_by_cat.items():

        run_hooks(BEFORE_ALL.get(category, []), category)

        workers = (category_workers or {}).get(category, max_workers)
        executor = ThreadPoolExecutor(max_workers=workers)
        executors[category] = executor

        for test in tests:
            future = executor.submit(run_single_test, test)
            futures.append((future, test))

    # Recolectar resultados
    for future, test in futures:
        try:
            results.append(future.result())
        except Exception as error:
            # Defensa: no debería ocurrir, run_single_test captura todo
            name = test.get("description") or test.get("name")
            results.append(TestResult(name=name, passed=False, error=str(error)))

    # Cierre de ejecutores + hooks after_all
    for category, executor in executors.items():
        executor.shutdown(wait=True)
        run_hooks(AFTER_ALL.get(category, []), category)

    # Orden por definición original
    results_sorted = sorted(
        results,
        key=lambda r: next(
            i for i, t in enumerate(TESTS)
            if (t.get("description") or t.get("name")) == r.name
        )
    )

    print_summary(results_sorted)

    return results_sorted

def print_summary(results: List[TestResult]) -> None:
    """Imprime el resumen, mostrando pruebas PASSED/FAILED y errores detallados."""
    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    print()

    for r in passed:
        print(f"🟩 {r.name} PASSED")

    for r in failed:
        print(f"🟥 {r.name} FAILED")

    print()

    for r in failed:
        print_failure(r)

    print(bold(f"Passed: {len(passed)}   Failed: {len(failed)}"))


def print_failure(result: TestResult) -> None:
    """Imprime detalles de un fallo de test."""
    print(yellow("─" * 50))
    print(red(f"🟥 FAIL: {result.name}"))
    print(bold(red("Assertion failed:\n")))
    print(result.error)
    print(yellow("─" * 50))
    print()


def discover_tests(directory: str = "tests") -> None:
    """
    Importa dinámicamente todos los archivos en un directorio cuyo nombre
    comience por 'test_' y termine en '.py'.

    Args:
        directory: Directorio donde buscar tests.
    """
    for filename in os.listdir(directory):
        if filename.startswith("test_") and filename.endswith(".py"):
            module_name = filename[:-3]
            importlib.import_module(f"{directory}.{module_name}")