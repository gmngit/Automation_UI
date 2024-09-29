from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):

    class Locators:
        SERVERS = (By.XPATH, "//div[@id='Price']/div")
        SERVER_NAME = ".//div[@class='card-header']"
        DETAILS = ".//p[@class='card-text']"
        BUTTON = ".//a[@class='btn btn-primary']"

    def get_servers(self):
        return self.elements_are_present(self.Locators.SERVERS)

    def get_server_data(self):
        servers = self.get_servers()
        server_data = []
        for server in servers:
            server_name = server.find_element(By.XPATH, self.Locators.SERVER_NAME).text
            details = server.find_element(By.XPATH, self.Locators.DETAILS).text.strip().split('\n')
            price_text = server.find_element(By.XPATH, self.Locators.BUTTON).text
            cpu = int(details[0].split()[0])
            ram = int(details[1].split()[0])
            ssd = int(details[2].split()[0])
            price = int(price_text.split('$')[-1])
            server_data.append({
                'name': server_name,
                'cpu': cpu,
                'ram': ram,
                'ssd': ssd,
                'price': price
            })
        return server_data

