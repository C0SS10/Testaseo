from functools import wraps

TESTS = []

def test(description=None):
    if callable(description):
        # Caso @test
        func = description
        TESTS.append({"name": func.__name__, "func": func, "description": None})
        return func

    # Caso @test("descripción")
    def decorator(func):
        TESTS.append({"name": func.__name__, "func": func, "description": description})
        return func

    return decorator
