from time import sleep
from testa.framework import test, before_all, after_all, before_each, after_each

@before_all("unit")
def setup_unit(cat):
    print(f"[HOOK] before_all for {cat}")

@after_all("unit")
def teardown_unit(cat):
    print(f"[HOOK] after_all for {cat}")

@before_each("unit")
def before_unit(test_info):
    print(f"[HOOK] before_each: {test_info['name']}")

@after_each("unit")
def after_unit(test_info, result):
    print(f"[HOOK] after_each: {test_info['name']} -> passed={result.passed}")


@test("unit fast 1", category="unit")
def unit_fast_1(ctx):
    sleep(0.1)
    ctx.assert_true(True)


@test("unit fast 2", category="unit")
def unit_fast_2(ctx):
    sleep(0.2)
    ctx.assert_true(True)


@test("integration slow", category="integration")
def integration_slow(ctx):
    # simulate longer integration-like work
    sleep(0.6)
    ctx.assert_equal(1 + 1, 2)


@test("e2e failing", category="e2e")
def e2e_fail(ctx):
    sleep(0.1)
    ctx.assert_true(False)  # will fail
