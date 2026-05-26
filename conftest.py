import pytest
from loguru import logger

from clients.api_client import APIClient
from endpoints.posts import PostsAPI
from config.settings import BASE_URL
from utils.logger import setup_logger

@pytest.fixture(scope="session", autouse=True)
def logger_setup():
    setup_logger()


@pytest.fixture(scope="module", autouse=True)
def log_module(request):
    module_name = request.node.module.__name__
    logger.info(f"START MODULE: {module_name}")
    yield
    logger.info(f"END MODULE: {module_name}")


@pytest.fixture(autouse=True)
def log_test(request):
    test_name = request.node.name
    logger.info(f"START TEST: {test_name}")
    yield
    logger.info(f"END TEST: {test_name}")


@pytest.fixture
def posts_api():
    client = APIClient(BASE_URL)
    return PostsAPI(client)