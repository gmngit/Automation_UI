import time
import pytest

from pages.profile_page import ProfilePage
from src.assertions import Assertions
from src.assertion_base import BaseAssertion
from selenium.webdriver.common.alert import Alert
from http import HTTPStatus


class TestProfilePage:
    def test_create_3_servers_and_validate_total_count(
            self, login, chrome_driver, main_page_url, client
    ):
        """
         - Create 3 servers
         - Validate total number of servers via UI
         - Validate total number of servers via API
         """

        test_data = [
            (1, 4, "Berlin", "http://test1.com"),
            (2, 8, "Perm", "http://test2.com"),
            (4, 16, "Tokyo", "http://test3.com")
        ]

        profile_page = ProfilePage(chrome_driver, main_page_url)
        total_servers = []

        for cpu, ram, location, domain in test_data:
            server = profile_page.create_server(
                cpu=cpu,
                ram=ram,
                location=location,
                domain=domain
            )
            time.sleep(0.5)
            total_servers.append(server)

        # 2. Validate total number of servers
        assert len(total_servers) == profile_page.get_total_servers()


        # 3. Validate total number of servers via API
        response = client.get_servers_list()
        response_body = response.json()
        total = response_body['items']

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        assert len(total_servers) == len(total)

    # @pytest.mark.skip
    def test_delete_1_server_and_validate_total_count(
            self, login, chrome_driver, main_page_url, total_servers, client
    ):
        """
         - Delete 1 server
         - Validate total number of servers via UI
         - Validate total number of servers via API
         """

        profile_page = ProfilePage(chrome_driver, main_page_url)
        alert = Alert(chrome_driver)

        # 1. Delete 1 server
        profile_page.delete_server()
        alert.accept()
        time.sleep(1)

        # 2. Validate total number of servers via UI
        assert profile_page.get_total_servers() == 2

        # 3. Validate total number of servers via API
        response = client.get_servers_list()
        response_body = response.json()
        total = response_body['items']

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        assert len(total) == 2

    # @pytest.mark.skip
    def test_create_server_invalid_cpu(self, login, chrome_driver, main_page_url):
        """
         - Create a server
         - Validate payload message was appeared
         """

        profile_page = ProfilePage(chrome_driver, main_page_url)
        assertion = Assertions(chrome_driver, main_page_url)

        # 1. Create a server
        profile_page.create_server(
            cpu="XEON",
            ram=8,
            location="Tokyo",
            domain="http://test4.com"
        )

        # 2. Validate payload message was appeared
        assertion.assert_validation_message_appears()
        profile_page.close_modal_window()

    # @pytest.mark.skip
    def test_create_server_invalid_domain(self, login, chrome_driver, main_page_url):
        """
         - Create a server
         - Validate payload message was appeared
         """

        profile_page = ProfilePage(chrome_driver, main_page_url)
        assertion = Assertions(chrome_driver, main_page_url)

        # 1. Create a server
        profile_page.create_server(
            cpu=2,
            ram=8,
            location="Tokyo",
            domain="test5.com"
        )

        # 2. Validate payload message was appeared
        assertion.assert_validation_message_appears()
        profile_page.close_modal_window()

