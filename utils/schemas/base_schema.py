class BaseSchema:

    REQUIRED_FIELDS = {}

    @classmethod
    def validate(cls, data: dict):
        missing = []
        wrong_type = []

        for field, expected_type in cls.REQUIRED_FIELDS.items():

            if field not in data:
                missing.append(field)
            elif not isinstance(data[field], expected_type):
                wrong_type.append(
                    f"{field}: expected {expected_type.__name__}, "
                    f"got {type(data[field]).__name__}"
                )

        assert not missing, f"Missing keys: {missing}"
        assert not wrong_type, f"Wrong types: {wrong_type}"