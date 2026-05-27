from loguru import logger


class APIResponse:
    def __init__(self, response):
        self._response = response
        self._json = None

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

    def assert_status_code(self, expected: int):
        assert self.status_code == expected, (
            f"Expected {expected}, got {self.status_code}"
        )
        return self

    def assert_schema(self, schema_class):
        logger.info(f"Validating schema: {schema_class.__name__}")

        schema_class.validate(self.json)
        return self

    def assert_is_list(self):
        assert isinstance(self.json, list), (
            f"Expected list, got {type(self.json).__name__}"
        )
        return self

    def assert_not_empty(self):
        assert self.json, "Response list is empty"
        return self

    def assert_each_schema(self, schema_class):
        self.assert_is_list()
        self.assert_not_empty()

        data = self.json

        logger.info(
            f"Validating schema for {len(data)} items using {schema_class.__name__}"
        )

        for index, item in enumerate(data):
            try:
                schema_class.validate(item)
            except AssertionError as e:
                raise AssertionError(
                    f"Schema validation failed at index {index}: {e}"
                )

        return self