import pytest

from pages.registration_page import RegistrationPage
from src.assertions import Assertions


class TestRegistrationPage:

    def test_registration_valid_email_and_valid_password(self, chrome_driver, main_page_url):
        """
        - Open the registration page
        - Enter valid email
        - Enter valid password
        - Click on the button
        """

        reg_page = RegistrationPage(chrome_driver, main_page_url)

        # 1. Open the main page
        reg_page.open_page()

        # 2. Enter valid email
        email = "test1@mail.ru"
        reg_page.set_email(email)

        # 3. Enter valid password
        password = "123"
        reg_page.set_password(password)

        # 4. Click on the button
        reg_page.click_on()

    # @pytest.mark.skip
    def test_registration_invalid_email_and_valid_password(self, chrome_driver, main_page_url):
        """
         - Open the registration page
         - Enter invalid email
         - Enter valid password
         - Click on the button
         - Validate the message was displayed
         """

        reg_page = RegistrationPage(chrome_driver, main_page_url)
        assertion = Assertions(chrome_driver, main_page_url)

        # 1. Open the main page
        reg_page.open_page()

        # 2. Enter invalid email
        email = "test_mail.ru"
        reg_page.set_email(email)

        # 3. Enter valid password
        password = "123"
        reg_page.set_password(password)

        # 4. Click on the button
        reg_page.click_on()

        # 5. Validate the message was displayed
        assertion.assert_validation_message_appears()

    # @pytest.mark.skip
    def test_registration_enter_name_and_password(self, chrome_driver, main_page_url):
        """
         - Open the registration page
         - Enter name in email field
         - Enter valid password
         - Click on the button
         - Validate the message was displayed
         """

        reg_page = RegistrationPage(chrome_driver, main_page_url)
        assertion = Assertions(chrome_driver, main_page_url)

        # 1. Open the main page
        reg_page.open_page()

        # 2. Enter invalid email
        email = "Vasya"
        reg_page.set_email(email)

        # 3. Enter valid password
        password = "123"
        reg_page.set_password(password)

        # 4. Click on the button
        reg_page.click_on()

        # 5. Validate the message was displayed
        assertion.assert_validation_message_appears()

    # @pytest.mark.skip
    def test_registration_enter_email_and_empty_password(self, chrome_driver, main_page_url):
        """
         - Open the registration page
         - Enter valid email
         - Click on the button
         - Validate the current url
         """

        reg_page = RegistrationPage(chrome_driver, main_page_url)

        # 1. Open the main page
        reg_page.open_page()

        # 2. Enter valid email
        email = "test2@mail.ru"
        reg_page.set_email(email)

        # 3. Click on the button
        reg_page.click_on()

        # 4. Validate the current url
        expected_url = f"{main_page_url}/signup"
        assert reg_page.get_current_url() == expected_url

    # @pytest.mark.skip
    def test_registration_the_same_creds(self, chrome_driver, main_page_url):
        """
         - Register
         - Register one more time with the same creds
         - Validate the message was displayed
         """

        reg_page = RegistrationPage(chrome_driver, main_page_url)
        assertion = Assertions(chrome_driver, main_page_url)
        email = "test5@mail.ru"
        password = "123"

        # 1. Register
        reg_page.register(email, password)

        # 2. Register one more time with the same creds
        reg_page.register(email, password)

        # 3. Validate the message was displayed
        assertion.assert_already_registered_message_appears()
