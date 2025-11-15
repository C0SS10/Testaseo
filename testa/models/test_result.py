class TestResult:
    def __init__(self, name, passed, error=None):
        self.name = name
        self.passed = passed
        self.error = error