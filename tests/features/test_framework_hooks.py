from testa.framework import before_all, after_all, before_each, after_each, test


STATE = {
    "before_all": 0,
    "after_all": 0,
    "before_each": 0,
    "after_each": 0,
    "tests_run": 0,
}


@before_all("hooks")
def hook_before_all(category):
    STATE["before_all"] += 1


@after_all("hooks")
def hook_after_all(category):
    STATE["after_all"] += 1


@before_each("hooks")
def hook_before_each(test_info):
    STATE["before_each"] += 1


@after_each("hooks")
def hook_after_each(test_info, result):
    STATE["after_each"] += 1


@test("Primer test con hooks", category="hooks")
def test_1(context):
    STATE["tests_run"] += 1
    assert True


@test("Segundo test con hooks", category="hooks")
def test_2(context):
    STATE["tests_run"] += 1
    assert True


@test("Validar ejecución de hooks", category="hooks")
def test_validate_hooks(context):
    # before_all: 1 vez
    assert STATE["before_all"] == 1  

    # after_all: todavía no ha corrido (solo corre al final)
    assert STATE["after_all"] == 0  

    # before_each y after_each por cada test ejecutado previamente
    assert STATE["before_each"] == 2  
    assert STATE["after_each"] == 2  

    assert STATE["tests_run"] == 2  
