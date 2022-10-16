import json
import logging
from pathlib import Path
from types import SimpleNamespace


class ElSpotError(Exception):
    pass


def read_config(config_filename='elspot_config.json'):
    if not Path(config_filename).exists():
        raise ElSpotError('Could not find config file: ' + config_filename)

    with open(config_filename) as fh:
        return json.loads(fh.read(), object_hook=lambda d: SimpleNamespace(**d))


def setup_logger(level, filename='elspot.log'):
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=eval('logging.' + level))

    return logging.getLogger()
