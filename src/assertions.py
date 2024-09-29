import logging

from pages.main_page import MainPage
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage

logger = logging.getLogger("LOGGER_ASSERTIONS")


class Assertions:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def assert_the_price_is_correct(self):
        main_page = MainPage(self.driver, self.url)
        server_data = main_page.get_server_data()

        for data in server_data:
            expected_price = data['cpu'] ** 2 + data['ram'] * 2 + data['ssd'] / 4
            actual_price = data['price']
            try:
                assert actual_price == expected_price, (
                    f"The price for {data['name']} is ${actual_price}, expected ${expected_price}"
                )
            except AssertionError as e:
                raise e

    def assert_validation_message_appears(self):
        reg_page = RegistrationPage(self.driver, self.url)
        message = reg_page.get_input_validation()
        assert message is not None, "The alert message wasn't appeared"

    def assert_already_registered_message_appears(self):
        reg_page = RegistrationPage(self.driver, self.url)
        message = reg_page.get_already_registered()
        assert message is not None, "The alert message wasn't appeared"

    def assert_creds_dont_match(self):
        login_page = LoginPage(self.driver, self.url)
        message = login_page.get_alert_message()
        assert message is not None, "The alert message wasn't appeared"

    def assert_user_is_authorized(self):
        login_page = LoginPage(self.driver, self.url)
        assert "/profile" in login_page.get_current_url()


