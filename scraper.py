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

    def _get_elspot_data(self) -> str:

        self.logging.info('-- get_elspot data')
        for _ in range(self.attempts):
            try:
                response = urlopen(Scraper.URL)
                body = response.read()
                response.close()
                if response.getcode() == Scraper.HTTP_OK:
                    return body.decode("utf-8")
                else:
                    self.logging.error('-- get_elspot, error code: ' + response.getcode())
            except URLError as e:
                self.logging.error('-- get_elspot data failure ' + str(e))

            time.sleep(self.interval)

        raise ElSpotError('Error: did not get a proper reply')

    def _get_elspot_mock(self):
        self.logging.info('-- get_elspot mock data')
        return pathlib.Path('elspot_mock.html').read_text()

    def get_data(self):
        return self._get_data()


