from time import sleep
from testa.framework import test, before_all, after_all, before_each, after_each


def hook(message: str):
    """Print formatted hook messages."""
    print(f"[HOOK] {message}")


@before_all("unit")
def before_all_unit(category):
    hook(f"before_all para la categoría: {category}")


@after_all("unit")
def after_all_unit(category):
    hook(f"after_all para la categoría: {category}")


@before_each("unit")
def before_each_unit(test_info):
    hook(f"before_each: {test_info['name']}")


@after_each("unit")
def after_each_unit(test_info, result):
    hook(f"after_each: {test_info['name']} -> passed={result.passed}")

@test("unit fast 1", category="unit")
def test_unit_fast_1(context):
    sleep(0.1)
    context.assert_true(True)


@test("unit fast 2", category="unit")
def test_unit_fast_2(context):
    sleep(0.2)
    context.assert_true(True)


@test("integration slow", category="integration")
def test_integration_slow(context):
    sleep(0.6)  # Simula una tarea de integración tardandose
    context.assert_equal(1 + 1, 2)


@test("e2e failing", category="e2e")
def test_e2e_fail(context):
    sleep(0.1)
    context.assert_true(False)  # Se espera que falle
