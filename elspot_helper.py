import configparser
import json
import logging
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace


class ElSpotError(Exception):
    pass


def saved_file_date(filename:str) -> datetime:
    return datetime.fromtimestamp(int(Path(filename).stat().st_ctime)) if Path(filename).exists() else datetime.fromtimestamp(0)

def save_to_file(data: dict, filename: str, logging) -> None:
    def today_date(data: dict):
        return datetime.now().strftime('%Y-%m-%d') == list(data.keys())[0].split()[0]

    if not today_date(data):
        logging.error('-- error too old date wait to save to file')
        raise ElSpotError('Wrong date: ' + list(data.keys())[0])

    logging.info('-- save_to_file ...')
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=2)

def read_config():
    config = 'elspot_config.json'
    if not Path(config).exists():
        raise ElSpotError('Could not find config file: ' + config)

    with open('elspot_config.json') as fh:
       return json.loads(fh.read(), object_hook=lambda d: SimpleNamespace(**d))


# TODO: Use wrapping functionality
def setup_logging(level):
    logging.basicConfig(filename='elspot.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=eval('logging.' + level))
