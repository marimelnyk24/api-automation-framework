from core.response import Response


class UsersAPI:

    USERS = "/users"

    def __init__(self, client):
        self.client = client

    def get_users(self) -> Response:
        return self.client.get(self.USERS)

    def get_user(self, user_id: int) -> Response:
        return self.client.get(f"{self.USERS}/{user_id}")

    def filter_users(self, params: dict) -> Response:
        return self.client.get(self.USERS, params=params)