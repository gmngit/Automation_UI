import pytest
import time

from faker import Faker
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.profile_page import ProfilePage


@pytest.fixture(scope="class")
def register(chrome_driver, main_page_url):
    reg_page = RegistrationPage(chrome_driver, main_page_url)
    fake = Faker()
    email = fake.email()
    password = fake.password(
        length=6,
        special_chars=False,
        digits=True,
        upper_case=True,
        lower_case=True)

    # Register
    reg_page.register(email, password)
    time.sleep(0.5)
    return email, password


@pytest.fixture(scope="class")
def login(chrome_driver, main_page_url, register):
    login_page = LoginPage(chrome_driver, main_page_url)
    email, password = register

    # Login
    login_page.login(email, password)
    time.sleep(0.5)


@pytest.fixture(scope="function")
def total_servers(chrome_driver, main_page_url):
    profile_page = ProfilePage(chrome_driver, main_page_url)
    return profile_page.get_total_servers()



