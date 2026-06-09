import pytest
from loguru import logger

from clients.api_client import APIClient
from endpoints.posts import PostsAPI
from endpoints.users import UsersAPI
from config.settings import BASE_URL
from utils.logger import setup_logger

@pytest.fixture(scope="session", autouse=True)
def logger_setup():
    setup_logger()

@pytest.fixture(autouse=True)
def log_context(request):
    test_name = request.node.name

    with logger.contextualize(
        test=test_name,
        test_module=request.node.module.__name__
    ):
        logger.info(f"START TEST: {test_name}")
        yield
        logger.info(f"END TEST: {test_name}")


@pytest.fixture
def api_client():
    return APIClient(BASE_URL)


@pytest.fixture
def posts_api(api_client):
    return PostsAPI(api_client)


@pytest.fixture
def users_api(api_client):
    return UsersAPI(api_client)