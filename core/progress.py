from selenium.webdriver.common.by import By

from core.browser import Browser
from settings import SAVE_FILE
from util.logger import Logger


class Progress(object):

    def __init__(self):
        self.logger = Logger()
        self.browser = Browser()

    def import_save(self):
        with open(SAVE_FILE, 'r') as f:
            save = f.readline()
        self.logger.info('Save imported: ' + save)
        self.browser.js('Game.ImportSave();')
        self.browser.get_element('textareaPrompt', By.ID).send_keys(save)
        self.browser.click_element('promptOption0', By.ID)

    def export_save(self):
        try:
            self.browser.control_s()
            self.browser.js('Game.ExportSave();')
            text = self.browser.get_element('textareaPrompt', By.ID).text
            with open(SAVE_FILE, 'w') as f:
                f.write(text)
            self.logger.info('Game saved: ' + text)
            self.browser.click_element('promptOption0', By.ID, time=0)

            self.browser.js('Game.CloseNotes();')
        except Exception as exc:
            self.logger.error('main.export_save -  {}: {}'.format(type(exc), str(exc)))
