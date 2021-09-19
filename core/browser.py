from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from settings import BROWSER_HEIGHT, BROWSER_WIDTH, HEADLESS_BROWSER
from util.logger import Logger
from util.singleton import Singleton


class Browser(metaclass=Singleton):

    def __init__(self):
        self.logger = Logger()
        options = Options()
        options.headless = HEADLESS_BROWSER
        self.browser = webdriver.Firefox(options=options)
        self.browser.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)

    def control_s(self):
        ActionChains(self.browser).key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()

    def open_url(self, url):
        self.browser.get(url)

    def get_element(self, element, by, time=2):
        try:
            if time == 0:
                return self.browser.find_element(by, element)
            return WebDriverWait(self.browser, time).until(EC.presence_of_element_located((by, element)))
        except Exception as exc:
            self.logger.debug('browser.get_element -  {}: {}'.format(type(exc), str(exc)))
            return False

    def get_elements(self, element, by, time=2):
        try:
            if time == 0:
                return self.browser.find_elements(by, element)
            return WebDriverWait(self.browser, time).until(EC.presence_of_all_elements_located((by, element)))
        except Exception as exc:
            self.logger.debug('browser.get_elements -  {}: {}'.format(type(exc), str(exc)))
            return False

    def js(self, command, *args):
        self.browser.execute_script(command, *args)

    def scroll_to_element(self, element, by, time=2):
        try:
            e = self.get_element(element, by, time)
            self.js("arguments[0].scrollIntoView(true);", e)
        except Exception as exc:
            self.logger.error('browser.scroll_to_element -  {}: {}'.format(type(exc), str(exc)))

    def hover_element(self, element, by):
        try:
            e = self.get_element(element, by)
            hover = ActionChains(self.browser).move_to_element(e)
            hover.perform()
        except Exception as exc:
            self.logger.error('browser.hover_element -  {}: {}'.format(type(exc), str(exc)))

    def click_element(self, element, by, time=2):
        tries = 0
        while tries < 5:
            try:
                e = self.get_element(element, by, time)
                self.scroll_to_element(element, by, time)
                e.click()
                return
            except Exception as exc:
                self.logger.error('browser.click_element -  {}: {}'.format(type(exc), str(exc)))
                sleep(1)

    def click_element_fast(self, element, by):
        """
        Use cases:
            - no need to ensure it works
            - huge call rate
        """
        try:
            e = self.get_element(element, by, time=0)
            self.js('arguments[0].click();', e)
        except Exception as exc:
            self.logger.error('browser.click_element_fast -  {}: {}'.format(type(exc), str(exc)))

    def load_website(self):
        self.open_url('https://orteil.dashnet.org/cookieclicker/')
        self.click_element('statsButton', By.ID)  # wait for the page to load

    def dismiss_popups(self):
        try:
            self.get_element("//a[contains(text(), 'Got it!')]", By.XPATH, time=0).click()
        except Exception as exc:
            self.logger.error('main.dismiss_popups -  {}: {}'.format(type(exc), str(exc)))
