from __future__ import annotations

from typing import Callable, Dict, List, Optional, Any

# Tipos internos

TestFunction = Callable[..., Any]
HookFunction = Callable[..., Any]

TestInfo = Dict[str, Any]
HookRegistry = Dict[str, List[HookFunction]]


# Registro global de pruebas y hooks

TESTS: List[TestInfo] = []

BEFORE_ALL: HookRegistry = {}
AFTER_ALL: HookRegistry = {}
BEFORE_EACH: HookRegistry = {}
AFTER_EACH: HookRegistry = {}


def register_hook(store: HookRegistry, category: str, function: HookFunction) -> HookFunction:
    """
    Registra un hook dentro del diccionario correspondiente.

    Args:
        store: Diccionario de hooks agrupados por categoría.
        category: Categoría de test a la cual aplica el hook.
        function: Función hook.

    Returns:
        La misma función hook, para permitir encadenamiento de decoradores.
    """
    store.setdefault(category, []).append(function)
    return function


def before_all(category: str) -> Callable[[HookFunction], HookFunction]:
    """Registra un hook que se ejecuta una vez ANTES de todos los tests de `category`."""
    return lambda f: register_hook(BEFORE_ALL, category, f)


def after_all(category: str) -> Callable[[HookFunction], HookFunction]:
    """Registra un hook que se ejecuta una vez DESPUÉS de todos los tests de `category`."""
    return lambda f: register_hook(AFTER_ALL, category, f)


def before_each(category: str) -> Callable[[HookFunction], HookFunction]:
    """
    Registra un hook que se ejecuta ANTES de cada test de `category`.

    Firma esperada:
        hook(test_info: dict)
    """
    return lambda f: register_hook(BEFORE_EACH, category, f)


def after_each(category: str) -> Callable[[HookFunction], HookFunction]:
    """
    Registra un hook que se ejecuta DESPUÉS de cada test de `category`.

    Firma esperada:
        hook(test_info: dict, result: TestResult)
    """
    return lambda f: register_hook(AFTER_EACH, category, f)


def test(description: Optional[str] = None, *, category: str = "unit") -> Callable[[TestFunction], TestFunction] | TestFunction:
    """
    Registra una función de prueba.

    Formas de uso:

        @test
        def my_test(context): ...

        @test("Descripción opcional")
        def my_test(context): ...

        @test(category="integration")
        def my_test(context): ...

        @test("Desc", category="e2e")
        def my_test(context): ...

    Args:
        description: Descripción del test o None.
        category: Categoría del test (“unit” por defecto).

    Returns:
        El decorador correspondiente o la función decorada.
    """

    # Caso: @test sin paréntesis -> description es la función
    if callable(description):
        function = description
        TESTS.append({
            "name": function.__name__,
            "func": function,
            "description": None,
            "category": category,
        })
        return function

    # Caso: @test("desc") o @test(category="...") o ambos
    def decorator(function: TestFunction) -> TestFunction:
        desc = description if isinstance(description, str) else None
        TESTS.append({
            "name": function.__name__,
            "func": function,
            "description": desc,
            "category": category,
        })
        return function

    return decorator