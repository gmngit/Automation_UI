import time
import pytest

from pages.login_page import LoginPage
from src.assertions import Assertions


class TestLoginPage:

    def test_login_valid_creds(self, chrome_driver, main_page_url, register):
        """
         - Login with valid creds
         - Assert the user is authorized
         """
        email, password = register
        login_page = LoginPage(chrome_driver, main_page_url)
        assertion = Assertions(chrome_driver, main_page_url)

        # 1. Login with valid creds
        login_page.login(email, password)
        time.sleep(0.5)

        # 2. Assert the user is authorized
        assertion.assert_user_is_authorized()

    def test_login_invalid_creds(self, chrome_driver, main_page_url):
        """
         - Login with invalid creds
         - Validate the alert message
         """

        login_page = LoginPage(chrome_driver, main_page_url)
        assertion = Assertions(chrome_driver, main_page_url)
        email = "test_test@mail.ru"
        password = "1234"

        # 1. Login with invalid creds
        login_page.login(email, password)
        time.sleep(0.5)

        # 2. Validate the alert message
        assertion.assert_creds_dont_match()

    def test_compare_cookie(self, chrome_driver, main_page_url):
        """
         - Get access_token
         - Login with valid creds
         - Compare access_token cookie
         """

        login_page = LoginPage(chrome_driver, main_page_url)
        email = "test1@mail.ru"
        password = "123"

        # 1. Get access_token
        cookie_name = "access_token"
        access_token_before = login_page.get_cookie(cookie_name)

        # 2. Login with valid creds
        login_page.login(email, password)
        time.sleep(0.5)

        # 3. Compare access_token cookie
        access_token_after = login_page.get_cookie(cookie_name)
        assert access_token_after != access_token_before



