from time import sleep

from selenium.webdriver.common.by import By

from core.browser import Browser
from util.logger import Logger


class UpgradeHandler(object):

    def __init__(self):
        self.logger = Logger()
        self.browser = Browser()

    def buy_upgrade(self):
        """
        Buys the first upgrade from the list of upgrades

        """
        try:
            self.browser.click_element_fast("//div[@id='upgrades']//div", By.XPATH)
            sleep(0.1)
            warning = self.browser.get_element('promptContent', By.ID, time=0)
            if warning and 'Warning' in warning.text:
                self.browser.get_element('promptOption1', By.ID, time=0).click()
        except Exception as exc:
            self.logger.error('main.buy_upgrades -  {}: {}'.format(type(exc), str(exc)))
