import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("LOGGER_WEBDRIVER")


class DriverManager:
    def __init__(self):
        self._driver = None

    def _get_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return chrome_options

    def _get_chrome_driver(self):
        driver_path = ChromeDriverManager().install()
        driver = webdriver.Chrome(
            service=Service(driver_path),
            options=self._get_chrome_options()
        )
        return driver

    def _get_chrome_remote_driver(self):
        driver = webdriver.Remote(
            command_executor='http://standalone-chrome:4444',
            options=self._get_chrome_options()
        )
        return driver

    def create_chrome_driver(self):
        logger.debug("\nCreating chrome driver...")
        self._driver = self._get_chrome_driver()
        return self._driver

    def create_remote_driver(self):
        logger.debug("\nCreating remote driver...")
        self._driver = self._get_chrome_remote_driver()
        return self._driver

    def close_driver(self, driver):
        if driver:
            try:
                logger.debug("\nClosing browser window...")
                driver.close()
                logger.debug("\nBrowser window is closed.")
            except WebDriverException as w_e:
                logger.warning(f"\nError while closing browser window: {w_e}")

            try:
                logger.debug("\nClosing selenium driver...")
                driver.quit()
                logger.debug("\nSelenium driver is closed.")
            except WebDriverException as w_e:
                logger.warning(f"\nError while closing the driver: {w_e}")
        else:
            logger.debug("\nSelenium driver is already closed.")

    def get_browser_logs(self, driver):
        logs = driver.get_log("browser")
        for log in logs:
            logger.debug(f"\nBrowser console logs: {log}")
