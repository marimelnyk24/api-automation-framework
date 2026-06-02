from core.response_schema import ResponseSchema
from core.response_assertions import ResponseAssertions


class Response:
    def __init__(self, api_response):
        self._response = api_response
        self._asserts = ResponseAssertions(api_response)
        self._schema = ResponseSchema(api_response)

    # -------------------
    # PROPERTIES
    # -------------------  
    @property
    def status_code(self):
        return self._response.status_code
    
    @property
    def json(self):
        return self._response.json
    
    @property
    def text(self):
        return self._response.text

    # -------------------
    # STATUS
    # -------------------
    def assert_status(self, code: int):
        self._asserts.assert_status_code(code)
        return self

    # -------------------
    # TYPE
    # -------------------
    def as_list(self):
        self._asserts.expect_list()
        return self

    def as_object(self):
        self._asserts.expect_object()
        return self

    # -------------------
    # COMMON CHECKS
    # -------------------
    def not_empty(self):
        self._asserts.not_empty()
        return self
    
    def is_empty(self):
        self._asserts.is_empty()
        return self

    def length(self, expected: int):
        self._asserts.expect_list_length(expected)
        return self

    # -------------------
    # SCHEMA
    # -------------------
    def validate(self, schema_class, limit=None):
        self._schema.validate(schema_class, limit)
        return self
    

    # -------------------
    # MODEL CONVERSION
    # -------------------
    def to_model(self, model_class):
        return self._response.to_model(model_class)

    def to_models(self, model_class):
        return self._response.to_models(model_class)