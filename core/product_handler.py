import re
from time import sleep

from selenium.webdriver.common.by import By

from core.browser import Browser
from util.logger import Logger


class ProductHandler(object):

    def __init__(self):
        self.logger = Logger()
        self.browser = Browser()
        self.product_map = {}
        self.amount_cookies = 0

    def buy_product(self):
        """
        Buys the product with the best rate at the moment (if possible)

        """
        try:
            best_rate = 0
            chosen_product = None
            for name in self.product_map:
                product = self.product_map[name]
                if product.get('production') and product.get('price'):
                    rate = product['production'] / product['price']
                    if rate > best_rate:
                        best_rate = rate
                        chosen_product = name
                elif not product.get('production') and product.get('price') and product[
                    'price'] / 10 <= self.amount_cookies:
                    chosen_product = name
            if chosen_product:
                chosen_element = self.browser.get_element(chosen_product, By.ID)
                if 'enabled' in chosen_element.get_attribute('class'):
                    self.click_product(chosen_element)
                    self.load_products([chosen_product])  # reload that product value
        except Exception as exc:
            self.logger.error('main.buy_products -  {}: {}'.format(type(exc), str(exc)))

    def click_product(self, element):
        elem_id = element.get_attribute('id')
        self.browser.scroll_to_element(elem_id, By.ID)
        self.browser.hover_element(elem_id, By.ID)
        tooltip = self.browser.get_element('tooltip', By.ID)
        if tooltip:
            self.browser.click_element(elem_id, By.ID)
            p = self.browser.get_element('name', By.CLASS_NAME)
            p_name = ''
            if p:
                p_name = p.text
            self.logger.info('Bought "{}"!'.format(p_name))

    def load_products(self, specific: list = None):
        """
        Hovers over a list of products to popup their tooltips, showing percentages and production numbers.

        """
        try:
            if specific:
                self.populate_product_info(specific)
            else:
                products = self.browser.get_elements('product', By.CLASS_NAME, time=0)
                if products:
                    product_id_list = [x.get_attribute('id') for x in products]
                    self.populate_product_info(product_id_list)

        except Exception as exc:
            self.logger.error('main.load_products -  {}: {}'.format(type(exc), str(exc)))

    def populate_product_info(self, product_id_list: list):
        for product_id in product_id_list:
            product_metadata = {}
            elem_number = re.findall('\d+', product_id)[0]
            price = self.browser.get_element('productPrice{}'.format(elem_number), By.ID)
            if price and price.text:
                product_metadata['price'] = float(price.text.replace(',', ''))
            # self.browser.scroll_to_element(product_id, By.ID)
            # self.browser.hover_element(product_id, By.ID)
            # sleep(0.1)
            self.browser.js(
                "Game.tooltip.dynamic=1;Game.tooltip.draw(this,function(){return Game.ObjectsById[" + str(elem_number) + "].tooltip();},'store');Game.tooltip.wobble();")
            tooltip = self.browser.get_element('tooltip', By.ID)
            if tooltip:
                percentage = re.findall('\d*\.*\d+(?=%)', tooltip.text)
                if percentage:
                    product_metadata['percentage'] = float(percentage[0])
                production = re.findall('(?<=produces ).*(?= cookies per second)', tooltip.text)
                if production:
                    product_metadata['production'] = float(production[0].replace(',', ''))
            self.product_map[product_id] = product_metadata
        self.logger.info('Loaded products data!')

    def update_cookies_info(self):
        try:
            cookies_element = self.browser.get_element("cookies", By.ID, time=0)
            cookies_text = re.findall(r'.*(?=\n|cookie)', cookies_element.text)[0].replace('\n', '').replace(',', '').strip()
            self.amount_cookies = float(re.findall(r'.*\d+', cookies_text)[0].strip())
            self.logger.info('Cookies in bank: ' + str(self.amount_cookies))
        except Exception as exc:
            self.logger.error('main.update_cookies_info -  {}: {}'.format(type(exc), str(exc)))
