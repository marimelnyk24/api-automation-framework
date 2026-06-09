from dataclasses import is_dataclass

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

        model_fields = model_class.__dataclass_fields__

        data = {}

        for field_name, field_def in model_fields.items():

            if field_name not in item:
                continue

            value = item[field_name]
            field_type = field_def.type

            if is_dataclass(field_type) and isinstance(value, dict):
                data[field_name] = self._map_item(
                    value,
                    field_type,
                    allow_extra_fields
                )
            else:
                data[field_name] = value

        if not allow_extra_fields:
            extra = set(item.keys()) - set(model_fields.keys())
            if extra:
                raise AssertionError(f"Unexpected fields: {extra}")

        return model_class(**data)

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