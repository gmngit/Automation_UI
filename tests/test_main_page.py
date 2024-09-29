from pages.main_page import MainPage
from src.assertions import Assertions


class TestMainPage:
    def test_the_price_correct(self, chrome_driver, main_page_url):
        """
        - Open the main page
        - Compare the price with expected result
        """

        main_page = MainPage(chrome_driver, main_page_url)
        assertion = Assertions(chrome_driver, main_page_url)

        # 1. Open the main page
        main_page.open_page()

        # 2. Compare the price with expected result
        assertion.assert_the_price_is_correct()
