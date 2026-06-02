class SoftAssert:
    def __init__(self):
        self.errors = []

    def equals(self, actual, expected, field: str):
        if actual != expected:
            self.errors.append(
                f"{field}: expected {expected}, got {actual}"
            )
        return self

    def not_none(self, value, field: str):
        if value is None:
            self.errors.append(f"{field} is None")
        return self

    def assert_all(self):
        if self.errors:
            raise AssertionError("\n".join(self.errors))