import json

from testa.exceptions.assertion_error_detailed import AssertionErrorDetailed
from testa.models.colors import red, yellow


class TestContext:
    def format_diff(self, a, b):
        """Genera una salida tipo diff para strings y dicts."""
        if isinstance(a, dict) and isinstance(b, dict):
            a_json = json.dumps(a, indent=2, ensure_ascii=False)
            b_json = json.dumps(b, indent=2, ensure_ascii=False)
            return self.diff_text(a_json, b_json)

        if isinstance(a, str) and isinstance(b, str):
            return self.diff_text(a, b)

        return f"Se esperaba: {a}\nSe obtuvo:      {b}"


    def diff_text(self, a, b):
        import difflib
        diff = difflib.ndiff(a.splitlines(), b.splitlines())
        lines = []
        for line in diff:
            if line.startswith("+ "):
                lines.append(red(line))
            elif line.startswith("- "):
                lines.append(yellow(line))
            else:
                lines.append(line)
        return "\n".join(lines)


    def assert_equal(self, a, b, message=""):
        if a != b:
            details = message or self.format_diff(b, a)
            raise AssertionErrorDetailed(details)
    

    def assert_true(self, condition, message=""):
        if not condition:
            raise AssertionErrorDetailed(message or "Se esperaba True pero se obtuvo False")


    def assert_false(self, condition, message=""):
        if condition:
            raise AssertionErrorDetailed(message or "Se esperaba False pero se obtuvo True")


    def assert_raises(self, exception, function, *args, **kwargs):
        try:
            function(*args, **kwargs)
        except exception:
            return
        raise AssertionErrorDetailed(f"Se esperaba {exception} pero no se obtuvo")