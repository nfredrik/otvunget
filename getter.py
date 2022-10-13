import http
import time
from urllib.error import URLError
from urllib.request import urlopen

from elspot_helper import ElSpotError


def get_elspot_data(logging, attempts: int, interval: int) -> str:
    url = 'https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm'

    logging.info('-- get_elspot data')
    body = None
    for _ in range(attempts):
        try:
            response = urlopen(url)
            body = response.read()
            response.close()
            if response.getcode() == http.HTTPStatus.OK:
                break
            else:
                logging.error(f'-- get_elspot, error code: {response.getcode()}')

        except URLError as e:
            logging.error('-- get_elspot data failure')
            raise ElSpotError(f'Error: {e}') from e

        time.sleep(interval)

    return body.decode("utf-8")


def get_elspot_mock(logging, attempts, interval):
    _ = attempts
    _ = interval
    logging.info('-- get_elspot mock data')
    with open('elspot_mock.html') as fh:
        return fh.read()
