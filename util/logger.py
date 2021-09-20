import logging
import sys
from datetime import datetime

from util.singleton import Singleton

logging.basicConfig(filename="clicker.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logging.disable(logging.ERROR)
levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}
handler = logging.StreamHandler(sys.stdout)


class Logger(metaclass=Singleton):

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.propagate = False
        self.logger.setLevel(levels['info'])
        self.logger.addHandler(handler)

    def info(self, message):
        self._log(self.logger.info, message)

    def debug(self, message):
        self._log(self.logger.debug, message)

    def error(self, message):
        self._log(self.logger.error, message)

    @staticmethod
    def _log(method, message: str):
        output = '{} {}'.format(datetime.now(), message)
        if 'debug' not in method.__name__:
            with open('clicker.log', 'a') as f:
                f.write(output + '\n')
                print(output)
