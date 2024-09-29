from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/signin"

    class Locators:
        EMAIL = (By.XPATH, "//input[@id='email']")
        PASSWORD = (By.XPATH, "//input[@id='password']")
        BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(), 'Войти')]")
        CREDS_DONT_MATCH = (By.XPATH, "//div[contains(text(), 'email or password does not match')]")

    def __init__(self, driver, url):
        super().__init__(driver, f"{url}{self.PATH}")

    def get_email(self):
        return self.element_is_visible(self.Locators.EMAIL)

    def get_password(self):
        return self.element_is_visible(self.Locators.PASSWORD)

    def get_button(self):
        return self.element_is_clickable(self.Locators.BUTTON)

    def get_current_url(self):
        return self.get_url()

    def get_alert_message(self):
        return self.element_is_visible(self.Locators.CREDS_DONT_MATCH)

    def get_cookie(self, cookie_name):
        cookie = self.driver.get_cookie(cookie_name)
        return cookie['value']

    def set_email(self, email):
        return self.set_text(self.get_email(), email)

    def set_password(self, password):
        return self.set_text(self.get_password(), password)

    def click_on(self):
        self.click(self.get_button())

    def login(self, email, password):
        self.open_page()
        self.set_email(email)
        self.set_password(password)
        self.click_on()
