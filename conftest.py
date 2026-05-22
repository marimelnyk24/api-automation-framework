import pytest

from clients.api_client import APIClient
from endpoints.posts import PostsAPI
from config.settings import BASE_URL


@pytest.fixture
def posts_api():
    client = APIClient(BASE_URL)
    return PostsAPI(client)