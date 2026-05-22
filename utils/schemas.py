class PostSchema:

    REQUIRED_SCHEMA = {
        "id": int,
        "title": str,
        "body": str,
        "userId": int
    }

    @staticmethod
    def validate(response_json: dict):
        missing = []
        wrong_type = []

        for key, expected_type in PostSchema.REQUIRED_SCHEMA.items():

            if key not in response_json:
                missing.append(key)
            elif not isinstance(response_json[key], expected_type):
                wrong_type.append(
                    f"{key}: expected {expected_type.__name__}, got {type(response_json[key]).__name__}"
                )

        assert not missing, f"Missing keys: {missing}"
        assert not wrong_type, f"Wrong types: {wrong_type}"