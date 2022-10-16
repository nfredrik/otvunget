import json
import logging
from pathlib import Path
from types import SimpleNamespace


class ElSpotError(Exception):
    pass


def read_config():
    config = 'elspot_config.json'
    if not Path(config).exists():
        raise ElSpotError('Could not find config file: ' + config)

    with open('elspot_config.json') as fh:
        return json.loads(fh.read(), object_hook=lambda d: SimpleNamespace(**d))


def setup_logger(level):
    logging.basicConfig(filename='elspot.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=eval('logging.' + level))

    return logging.getLogger()