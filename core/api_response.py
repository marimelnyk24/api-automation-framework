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
    
    def _map_item(
        self,
        item: dict,
        model_class: Type[T],
        allow_extra_fields: bool = True
    ) -> T:
        model_fields = model_class.__dataclass_fields__.keys()

        if allow_extra_fields:
            item = {
                k: v
                for k, v in item.items()
                if k in model_fields
            }
        else:
            extra = set(item.keys()) - set(model_fields)
            if extra:
                raise AssertionError(f"Unexpected fields: {extra}")

        return model_class(**item)

    def to_model(
        self,
        model_class: Type[T],
        allow_extra_fields: bool = True
    ) -> T:
        return self._map_item(
            self.json,
            model_class,
            allow_extra_fields
        )

    def to_models(
        self,
        model_class: Type[T],
        allow_extra_fields: bool = True
    ) -> list[T]:
        return [
            self._map_item(
                item,
                model_class,
                allow_extra_fields
            )
            for item in self.json
        ]