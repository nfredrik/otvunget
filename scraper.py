import pathlib
import time
from urllib.error import URLError
from urllib.request import urlopen

from elspot_helper import ElSpotError


class Scraper:
    HTTP_OK = 200
    URL = 'https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm'

    def __init__(self, logging, config):
        self.logging = logging
        self.attempts = config.attempts
        self.interval = config.interval
        self._get_data = self._get_elspot_mock if bool(config.mock) else self._get_elspot_data

    @staticmethod
    def _get_elspot_data(logging, attempts: int, interval: int) -> str:

        logging.info('-- get_elspot data')
        for _ in range(attempts):
            try:
                response = urlopen(Scraper.URL)
                body = response.read()
                response.close()
                if response.getcode() == Scraper.HTTP_OK:
                    return body.decode("utf-8")
                else:
                    logging.error('-- get_elspot, error code: ' + response.getcode())
            except URLError as e:
                logging.error('-- get_elspot data failure ' + str(e))

            time.sleep(interval)

        raise ElSpotError('Error: did not get a proper reply')

    @staticmethod
    def _get_elspot_mock(logging, attempts, interval):
        _ = attempts
        _ = interval
        logging.info('-- get_elspot mock data')
        return pathlib.Path('elspot_mock.html').read_text()

    def get_data(self):
        return self._get_data(self.logging, self.attempts, self.interval)


class SleepController:
    def __init__(self, logging, config):
        self.logging = logging
        self.backoff = self.backoff_start = config.backoff_start
        self.backoff_stop = config.backoff_stop
        self.backoff_multipel = config.backoff_multipel

    def current_backoff(self):
#        self.logging.debug('-- backoff ' + str(self.backoff))
        current_backoff = self.backoff
        self.backoff *= self.backoff_multipel
        self.backoff = self.backoff_stop if self.backoff > self.backoff_stop else self.backoff
        return current_backoff

    def reset(self):
        self.backoff = self.backoff_start
