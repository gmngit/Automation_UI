from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class ProfilePage(BasePage):
    PATH = "/profile"

    class Locators:
        ORDER_BUTTON = (By.XPATH, "//button[@type='button' and contains(text(), 'Заказать сервер')]")
        MODAL_CPU_INPUT = (By.XPATH, "//input[@id='cpu']")
        MODAL_RAM_1Gb = (By.XPATH, "//input[@type='radio' and @id='ram1']")
        MODAL_RAM_2Gb = (By.XPATH, "//input[@type='radio' and @id='ram2']")
        MODAL_RAM_4Gb = (By.XPATH, "//input[@type='radio' and @id='ram4']")
        MODAL_RAM_8Gb = (By.XPATH, "//input[@type='radio' and @id='ram8']")
        MODAL_RAM_16Gb = (By.XPATH, "//input[@type='radio' and @id='ram16']")
        MODAL_SSD_SLIDER = (By.XPATH, "//input[@type='range' and @id='ssd']")
        MODAL_LOCATION = (By.XPATH, "//select[@id='location']")
        MODAL_PERIOD = (By.XPATH, "//select[@id='period']")
        MODAL_DOMAIN = (By.XPATH, "//input[@id='info_url']")
        MODAL_BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(), 'Заказать')]")
        DELETE_BUTTONS = (By.XPATH, "//a[contains(text(), 'Удалить')]")
        SERVERS = (By.XPATH, "//div[@id='server-list']/div")
        INPUT_VALIDATION = (By.XPATH, "//div[contains(text(), 'Input payload validation failed')]")
        CLOSE_MODAL_BUTTON = (By.XPATH, "//button[@type='button' and @aria-label='Close']")

    def __init__(self, driver, url):
        super().__init__(driver, f"{url}{self.PATH}")

    def get_order_button(self):
        return self.element_is_clickable(self.Locators.ORDER_BUTTON)

    def get_modal_cpu(self):
        return self.element_is_visible(self.Locators.MODAL_CPU_INPUT)

    def get_modal_ram4(self):
        return self.element_is_visible(self.Locators.MODAL_RAM_4Gb)

    def get_modal_ram8(self):
        return self.element_is_visible(self.Locators.MODAL_RAM_8Gb)

    def get_modal_ram16(self):
        return self.element_is_visible(self.Locators.MODAL_RAM_16Gb)

    def get_ssd_slider(self):
        return self.element_is_clickable(self.Locators.MODAL_SSD_SLIDER)

    def get_location(self):
        return self.element_is_visible(self.Locators.MODAL_LOCATION)

    def get_period(self):
        return self.element_is_visible(self.Locators.MODAL_PERIOD)

    def get_domain(self):
        return self.element_is_visible(self.Locators.MODAL_DOMAIN)

    def get_button(self):
        return self.element_is_clickable(self.Locators.MODAL_BUTTON)

    def get_servers(self):
        return self.elements_are_present(self.Locators.SERVERS)

    def get_delete_buttons(self):
        return self.elements_are_visible(self.Locators.DELETE_BUTTONS)

    def get_total_servers(self):
        servers = self.get_servers()
        return len(servers)

    def get_input_validation(self):
        return self.element_is_visible(self.Locators.INPUT_VALIDATION)

    def get_close_modal_button(self):
        return self.element_is_clickable(self.Locators.CLOSE_MODAL_BUTTON)

    def set_modal_cpu(self, cpu):
        self.get_modal_cpu().clear()
        return self.set_text(self.get_modal_cpu(), cpu)

    def set_slider(self, value):
        return self.get_ssd_slider().send_keys(value)

    def set_location(self, location):
        select = Select(self.get_location())
        return select.select_by_value(location)

    def set_period(self):
        select = Select(self.get_period())
        return select.select_by_index(3)

    def set_domain(self, domain):
        self.get_domain().clear()
        return self.set_text(self.get_domain(), domain)

    def click_on_ram(self, ram):
        if ram == 4:
            self.click(self.get_modal_ram4())
        elif ram == 8:
            self.click(self.get_modal_ram8())
        elif ram == 16:
            self.click(self.get_modal_ram16())

    def click_on_button(self):
        self.click(self.get_button())

    def click_on_order_button(self):
        self.click(self.get_order_button())

    def close_modal_window(self):
        self.click(self.get_close_modal_button())

    def create_server(self, cpu, ram, location, domain):
        self.click_on_order_button()
        self.set_modal_cpu(cpu)
        self.click_on_ram(ram)
        self.set_location(location)
        self.set_domain(domain)
        self.click_on_button()

    def delete_server(self):
        delete_buttons = self.get_delete_buttons()
        self.click(delete_buttons[1])



