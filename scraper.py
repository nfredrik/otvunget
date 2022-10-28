import pathlib
from urllib.error import URLError
from urllib.request import urlopen


class ElSpotCommError(Exception): pass


class Scraper:
    HTTP_OK = 200
    URL = 'https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm'

    def __init__(self, logging, config):
        self.logging = logging
        self._get_data = self._get_elspot_mock if bool(config.mock) else self._get_elspot_data

    def _get_elspot_data(self) -> str:

        self.logging.info('-- get_elspot data')
        try:
            response = urlopen(Scraper.URL)
            body = response.read()
            response.close()
            if response.getcode() == Scraper.HTTP_OK:
                return body.decode("utf-8")

            self.logging.error('-- get_elspot, error code: ' + response.getcode())

        except URLError as e:
            self.logging.error('-- get_elspot com failure ' + str(e))

        raise ElSpotCommError('Error: did not get a proper reply')


    def _get_elspot_mock(self) -> str:
        self.logging.info('-- get_elspot mock data')
        return pathlib.Path('elspot_mock.html').read_text()


    def get_data(self):
        return self._get_data()
