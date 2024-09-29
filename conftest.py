import logging
import pytest
import allure
import requests

from src.webdriver import DriverManager
from api.api_requests import ServersRequests

logger = logging.getLogger("LOGGER_FIXTURES")


def pytest_configure():
    logging.basicConfig(level=logging.DEBUG)


def pytest_addoption(parser):
    parser.addoption(
        "--url_ui",
        action="store",
        default="http://server:8081",
        help="Base url of main page"
    )

    parser.addoption(
        "--url_api",
        action="store",
        default="http://server:8081/api/v1",
        help="Base url for requests"
    )


@pytest.fixture(scope="session")
def chrome_driver():
    # driver = DriverManager().create_chrome_driver()
    driver = DriverManager().create_remote_driver()
    driver.maximize_window()
    yield driver
    driver.delete_all_cookies()
    DriverManager().close_driver(driver)


@pytest.fixture(scope="session")
def main_page_url(request):
    return request.config.getoption("--url_ui")

@pytest.fixture(scope="session")
def api_url(request):
    return request.config.getoption("--url_api")


@pytest.fixture(scope='class')
@allure.title("Getting a token...")
def bearer_token(register, api_url):
    email, password = register

    auth_url = f"{api_url}/auth/login"
    data = {
        "email": email,
        "password": password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    if not email or not password or not auth_url:
        raise ValueError(f"Required 'email' or 'password' or 'auth_url' is missing")

    try:
        response = requests.post(url=auth_url, data=data, headers=headers)
        token = response.json().get("access_token")
        if not token:
            raise ValueError("Fail to get bearer token")
        return token
    except requests.RequestException as e:
        logger.error(f"\nRequest error when receiving a token: {e}")
        raise
    except ValueError as e:
        logger.error(f"\nError when processing a token: {e}")
        raise

@pytest.fixture(scope='class')
@allure.title("Prepare HTTP client for requests")
def client(bearer_token, request):
    base_url = request.config.getoption("--url_api")

    _client = ServersRequests(
        base_url=base_url,
        token=bearer_token
    )

    _client.set_session_authentication()
    yield _client
    logger.info(f"\nSession was closed")
    _client.session.close()


