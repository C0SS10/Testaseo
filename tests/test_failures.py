from testa.framework import test


@test("Comparación simple que falla")
def test_simple_equal_fail(context):
    context.assert_equal(5, 10, "Los valores no coinciden: 5 != 10")


@test("Diff entre strings")
def test_string_diff_fail(context):
    esperado = "Hola mundo"
    recibido = "Hola Mundo!"
    context.assert_equal(esperado, recibido)


@test("Diff entre diccionarios")
def test_dict_diff_fail(context):
    esperado = {"name": "Rick", "alive": True}
    recibido = {"name": "Rik", "alive": False}
    context.assert_equal(esperado, recibido)


@test("assert_true fallando")
def test_true_fail(context):
    context.assert_true(False, "Se esperaba True y se obtuvo False")


@test("assert_false fallando")
def test_false_fail(context):
    context.assert_false(True, "Se esperaba False pero se obtuvo True")


@test("assert_raises no detecta excepción")
def test_raises_fail(context):
    def sumar(a, b):
        return a + b

    # Esto debería fallar porque sumar NO lanza ValueError
    context.assert_raises(ValueError, sumar, 2, 3)


@test("excepción inesperada")
def test_unexpected_exception(context):
    raise RuntimeError("Explosión inesperada")
