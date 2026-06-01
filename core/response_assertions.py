class ResponseAssertions:
    def __init__(self, response):
        self.response = response

    # -------------------------
    # STATUS
    # -------------------------
    def assert_status_code(self, expected: int):
        assert self.response.status_code == expected, (
            f"Expected {expected}, got {self.response.status_code}"
        )
        return self

    # -------------------------
    # TYPE EXPECTATION
    # -------------------------
    def expect_list(self):
        assert isinstance(self.response.json, list), (
            f"Expected list, got {type(self.response.json).__name__}"
        )
        self.response._is_list = True
        return self

    def expect_object(self):
        assert isinstance(self.response.json, dict), (
            f"Expected dict, got {type(self.response.json).__name__}"
        )
        self.response._is_list = False
        return self

    # -------------------------
    # COMMON CHECKS
    # -------------------------
    def not_empty(self):
        assert self.response.json, "Response is empty"
        return self
    
    def is_empty(self):
        assert not self.response.json, f"Expected empty response, got length {len(self.response.json)}"
        return self

    def expect_list_length(self, expected_length: int):
        actual_length = len(self.response.json)
        assert actual_length == expected_length, (
            f"Expected list length {expected_length}, got {actual_length}"
        )
        return self