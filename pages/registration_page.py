from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    PATH = "/signup"

    class Locators:
        EMAIL = (By.XPATH, "//input[@id='email']")
        PASSWORD = (By.XPATH, "//input[@id='password']")
        BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(), 'Зарегистрироваться')]")
        INPUT_VALIDATION = (By.XPATH, "//div[contains(text(), 'Input payload validation failed')]")
        ALREADY_REGISTERED = (By.XPATH, "//div[contains(text(), 'is already registered')]")

    def __init__(self, driver, url):
        super().__init__(driver, f"{url}{self.PATH}")

    def get_email(self):
        return self.element_is_visible(self.Locators.EMAIL)

    def get_password(self):
        return self.element_is_visible(self.Locators.PASSWORD)

    def get_button(self):
        return self.element_is_clickable(self.Locators.BUTTON)

    def get_input_validation(self):
        return self.element_is_visible(self.Locators.INPUT_VALIDATION)

    def get_already_registered(self):
        return self.element_is_visible(self.Locators.ALREADY_REGISTERED)

    def get_current_url(self):
        return self.get_url()

    def set_email(self, email):
        return self.set_text(self.get_email(), email)

    def set_password(self, password):
        return self.set_text(self.get_password(), password)

    def click_on(self):
        self.click(self.get_button())

    def register(self, email, password):
        self.open_page()
        self.set_email(email)
        self.set_password(password)
        self.click_on()

