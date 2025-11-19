from testa.framework import test, TESTS
from testa.models.test_result import TestResult


@test("Debe registrar correctamente un test", category="unit")
def test_register(context):
    assert any(t["name"] == "test_register" for t in TESTS)


@test("Debe ejecutar correctamente un test que pasa", category="unit")
def test_passing(context):
    context.assert_equal(1 + 1, 2)


@test("Debe capturar una AssertionErrorDetailed", category="unit")
def test_failing(context):
    context.assert_equal(1 + 1, 3)
