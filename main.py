from threading import Thread
from time import sleep

from selenium.webdriver.common.by import By

from core.browser import Browser
from core.product_handler import ProductHandler
from core.progress import Progress
from core.upgrade_handler import UpgradeHandler
from settings import NUMBER_OF_COOKIE_THREADS, SAVE_INTERVAL
from util import util
from util.logger import Logger


class Main(object):

    def __init__(self):
        self.logger = Logger()
        self.browser = Browser()
        self.progress = Progress()
        self.product_handler = ProductHandler()
        self.upgrade_handler = UpgradeHandler()
        self.actions = [
            {'action': self.click_big_cookie, 'threads': NUMBER_OF_COOKIE_THREADS},
            {'action': self.click_golden_cookie, 'interval': 0.1},
            {'action': self.progress.export_save, 'interval': SAVE_INTERVAL},
            {'action': self.upgrade_handler.buy_upgrade, 'interval': 60},
            {'action': self.product_handler.update_cookies_info, 'interval': 5},
            {'action': self.product_handler.load_products, 'interval': 60},
            {'action': self.product_handler.buy_product, 'interval': 5},
        ]

    def click_big_cookie(self):
        self.browser.click_element_fast('bigCookie', By.ID)

    def click_golden_cookie(self):
        try:
            golden_cookie = self.browser.get_element('shimmer', By.CLASS_NAME, time=0)
            if golden_cookie:
                golden_cookie.click()
                self.logger.info('Clicked golden cookie!')
        except Exception as exc:
            self.logger.error('main.click_golden_cookie -  {}: {}'.format(type(exc), str(exc)))

    def execute(self, method, interval: float = 0, num_of_threads: int = 1):
        for index in range(num_of_threads):
            self.logger.info("main.execute - method: {}: create and start thread {}.".format(method.__name__, index))
            x = Thread(target=util.start_custom_thread, args=(method, interval,))
            x.start()

    def start(self):
        self.browser.load_website()
        self.progress.import_save()
        self.browser.dismiss_popups()
        try:
            for action in self.actions:
                self.execute(
                    method=action['action'],
                    num_of_threads=action.get('threads', 1),
                    interval=action.get('interval', 0)
                )
            while True:
                sleep(5)

        except Exception as exc:
            self.logger.error('main.start -  {}: {}'.format(type(exc), str(exc)))


if __name__ == '__main__':
    Main().start()
