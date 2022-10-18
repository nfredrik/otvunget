import time
from urllib.error import URLError
from urllib.request import urlopen

from elspot_helper import ElSpotError


class Scraper:
    HTTP_OK = 200
    URL = 'https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm'

    def __init__(self, mock, logging, attempts, interval):
        self.mock = mock
        self.logging = logging
        self.attempts = attempts
        self.interval = interval

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
                logging.error('-- get_elspot data failure ' + e)

            time.sleep(interval)

        raise ElSpotError('Error: did not get a proper reply')

    @staticmethod
    def _get_elspot_mock(logging, attempts, interval):
        _ = attempts
        _ = interval
        logging.info('-- get_elspot mock data')
        with open('elspot_mock.html') as fh:
            tmp =  fh.read()

        return tmp

    def get_data(self):
        if bool(self.mock):
            return self._get_elspot_mock(self.logging, self.attempts, self.interval)

        return self._get_elspot_data(self.logging, self.attempts, self.interval)
