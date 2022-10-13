import configparser
import json
import re
import time
import urllib
from datetime import datetime
from html.parser import HTMLParser
from urllib.error import URLError
from urllib.request import urlopen
from pathlib import Path


class ElSpotError(Exception):
    pass


def get_elspot_data(logging, attempts, interval) -> str:
    url = 'https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm'

    logging.info('-- get_elspot data')
    body = None
    for _ in range(attempts):
        try:
            response = urlopen(url)
            body = response.read()
            response.close()
            if response.getcode() == 200:
                break
            else:
                logging.error(f'-- get_elspot, error code: {response.getcode()}')

        except urllib.error.URLError as e:
            logging.error('-- get_elspot data failure')
            raise ElSpotError(f'Error: {e}') from e

        time.sleep(interval)

    return body.decode("utf-8")


def get_elspot_mock(logging, attempts, interval):
    logging.info('-- get_elspot mock data')
    with open('elspot_mock.html') as fh:
        return fh.read()


class ElSpotHTMLParser(HTMLParser):

    def __init__(self, logging):
        HTMLParser.__init__(self)
        self.logging = logging
        self._recording = False
        self._all = {}
        self._time = None

    @staticmethod
    def _td_tag(tag) -> bool:
        return tag == 'td'

    @staticmethod
    def _is_date(data) -> bool:
        return re.match("(\d{4})-(\d{2})-(\d{2})", data) != None

    def handle_starttag(self, tag, attrs):
        self._recording = self._td_tag(tag)

    def handle_endtag(self, tag):
        self._recording = not self._td_tag(tag) and self._recording

    def handle_data(self, data):
        if self._recording:
            if self._is_date(data):
                self._time = data
                return

            if self._time is None:
                self.logging.error('-- Error timestamp not inlcuded in data!!')
                raise ElSpotError('Error no date before price!')

            self._all[self._time] = data.split()[0]

    def get_elprices(self) -> dict:
        return self._all


def save_to_file(data, filename, logging):
    def file_saved_today(filename):
        return Path(filename).exists() and \
               (datetime.fromtimestamp(int(Path(filename).stat().st_ctime)).date() == datetime.now().date())

    def today_date(data):
        perhaps = datetime.fromisoformat(list(data.keys())[0])
        return datetime.now().date() == perhaps.date()

    if not today_date(data):
        logging.error('Error too old date wait to save to file')
        return

    if file_saved_today(filename):
        logging.error(f'a {filename} has been saved to day!')
    else:
        logging.error(f'No {filename} has been saved to day!')


    logging.info('--save_to_file ...')
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=2)
    logging.debug(data)


class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('elspot.ini')
        self.poll_frequency = int(config['default']['POLL_FREQUENCY'])
        self.mock = config['default']['MOCK'] == 'True'
        self.loglevel = config['default']['LOG_LEVEL']
        self.attempts = int(config['default']['ATTEMPTS'])
        self.interval = int(config['default']['INTERVAL'])
        self.filename = config['default']['FILENAME']
