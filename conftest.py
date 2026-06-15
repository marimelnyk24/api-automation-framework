import pytest
import pytest_html
from loguru import logger

from clients.api_client import APIClient
from core.request_context import get_last_response
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield

    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    response = get_last_response()

    if not response:
        return

    details = [
        "REQUEST",
        "-" * 50,
        f"Method: {response.request_method}",
        f"URL: {response.request_url}",
        "",
        f"Headers: {response.request_headers}",
        "",
        f"Body: {response.request_body}",
        "",
        "",
        "RESPONSE",
        "-" * 50,
        f"Status: {response.status_code}",
        "",
        f"Body: {response.text}",
    ]

    if not hasattr(report, "extras"):
        report.extras = []

    report.extras.append(
        pytest_html.extras.html(
            f"""
            <h3>API Request/Response</h3>
            <pre>
    {"\n".join(details)}
            </pre>
            """
        )
    )