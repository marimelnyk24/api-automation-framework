from loguru import logger

from typing import Type, TypeVar

T = TypeVar("T")



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

    def to_model(self, model_class: Type[T]) -> T:
        return model_class(**self.json)

    def to_models(self, model_class: Type[T]) -> list[T]:
        return [
            model_class(**item)
            for item in self.json
        ]