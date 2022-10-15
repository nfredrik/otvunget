import configparser
import json
import logging
from datetime import datetime
from pathlib import Path


class ElSpotError(Exception):
    pass


def save_to_file(data: dict, filename: str, logging) -> None:
    def file_saved_today(filename: str) -> bool:
        return Path(filename).exists() and datetime.fromtimestamp(
            int(Path(filename).stat().st_ctime)).date() == datetime.now().date()

    def today_date(data: dict):
        return datetime.now().strftime('%Y-%m-%d') == list(data.keys())[0].split()[0]

    if not today_date(data):
        logging.error('-- error too old date wait to save to file')
        raise ElSpotError(f'Wrong date: {list(data.keys())[0]}')

    logging.info('-- save_to_file ...')
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=2)


class Config:
    INI_FILE = 'elspot.ini'

    def __init__(self):
        config = configparser.ConfigParser()
        if not Path(self.INI_FILE).exists():
            raise ElSpotError('Error not file called: " + self.INI_FILE)

        config.read(self.INI_FILE)
        self.poll_frequency = int(config['default']['POLL_FREQUENCY'])
        self.mock = config['default']['MOCK'] == 'True'
        self.loglevel = config['default']['LOG_LEVEL']
        self.attempts = int(config['default']['ATTEMPTS'])
        self.interval = int(config['default']['INTERVAL'])
        self.filename = config['default']['FILENAME']


# TODO: Use wrapping functionality
def setup_logging(level):
    logging.basicConfig(filename='elspot.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=eval(f'logging.{level}'))
