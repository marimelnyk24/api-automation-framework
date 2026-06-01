from loguru import logger

class ResponseSchema:
    def __init__(self, response):
        self.response = response

    def validate(self, schema_class, limit=None):
            data = self.response.json

            if isinstance(data, dict):
                schema_class.validate(data)
                return self

            if isinstance(data, list):
                items = data[:limit] if limit else data

                for i, item in enumerate(items):
                    try:
                        schema_class.validate(item)
                    except AssertionError as e:
                        raise AssertionError(f"Schema failed at index {i}: {e}")
                return self

            raise AssertionError(f"Unsupported type: {type(data)}")