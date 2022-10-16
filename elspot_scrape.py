import time
from urllib.error import URLError
from urllib.request import urlopen

from elspot_helper import ElSpotError

HTTP_OK = 200

def get_elspot_data(logging, attempts: int, interval: int) -> str:
    url = 'https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm'

    logging.info('-- get_elspot data')
    for _ in range(attempts):
        try:
            response = urlopen(url)
            body = response.read()
            response.close()
            if response.getcode() == HTTP_OK:
                return body.decode("utf-8")
            else:
                logging.error('-- get_elspot, error code: ' + response.getcode())
        except URLError as e:
            logging.error('-- get_elspot data failure ' + e)

        time.sleep(interval)

    raise ElSpotError('Error: did not get a proper reply')


def get_elspot_mock(logging, attempts, interval):
    _ = attempts
    _ = interval
    logging.info('-- get_elspot mock data')
    with open('elspot_mock.html') as fh:
        return fh.read()
