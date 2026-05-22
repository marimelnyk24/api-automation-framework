class Assert:
    @staticmethod
    def status_code(response, expected: int):
        assert response.status_code == expected, (
            f"Expected {expected}, got {response.status_code}"
        )

    @staticmethod
    def has_key(response_json, key: str):
        assert key in response_json, f"Missing key: {key}"

    @staticmethod
    def equals(actual, expected, field_name: str):
        assert actual == expected, (
            f"{field_name}: expected {expected}, got {actual}"
        )