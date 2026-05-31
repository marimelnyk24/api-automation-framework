from loguru import logger


class APIResponse:
    def __init__(self, response):
        self._response = response
        self._json = None
        self._is_list = False

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def json(self):
        if self._json is None:
            self._json = self._response.json()
        return self._json

    @property
    def text(self):
        return self._response.text

    # -------------------------
    # STATUS
    # -------------------------
    def assert_status_code(self, expected: int):
        assert self.status_code == expected, (
            f"Expected {expected}, got {self.status_code}"
        )
        return self

    # -------------------------
    # TYPE EXPECTATION
    # -------------------------
    def expect_list(self):
        assert isinstance(self.json, list), (
            f"Expected list, got {type(self.json).__name__}"
        )
        self._is_list = True
        return self

    def expect_object(self):
        assert isinstance(self.json, dict), (
            f"Expected dict, got {type(self.json).__name__}"
        )
        self._is_list = False
        return self

    # -------------------------
    # COMMON CHECKS
    # -------------------------
    def not_empty(self):
        assert self.json, "Response is empty"
        return self
    
    def expect_list_length(self, expected_length: int):
        actual_length = len(self.json)
        assert actual_length == expected_length, (
            f"Expected list length {expected_length}, got {actual_length}"
        )
        return self

    # -------------------------
    # SCHEMA VALIDATION
    # -------------------------
    def schema(self, schema_class):
        logger.info(f"Validating schema: {schema_class.__name__}")

        schema_class.validate(self.json)
        return self

    def each_schema(self, schema_class, limit=None):
        items = self.json if limit is None else self.json[:limit]

        logger.info(
            f"Validating schema for {len(items)} items using {schema_class.__name__}"
        )

        for index, item in enumerate(items):
            try:
                schema_class.validate(item)
            except AssertionError as e:
                raise AssertionError(
                    f"Schema validation failed at index {index}: {e}"
                )

        return self