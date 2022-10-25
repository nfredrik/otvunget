import json
import logging
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime, timedelta


class ElSpotError(Exception):
    pass


def read_config(config_filename='elspot_config.json'):
    if not Path(config_filename).exists():
        raise ElSpotError('Could not find config file: ' + config_filename)

    with open(config_filename) as fh:
        return json.loads(fh.read(), object_hook=lambda d: SimpleNamespace(**d))


def setup_logger(level, filename):
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=eval('logging.' + level))

    return logging.getLogger()


def seconds_until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month,
                        day=tomorrow.day, hour=0, minute=0, second=10)
    return (midnight - datetime.now()).seconds


def save_csv(filename, data: dict) -> None:
    file_exist = bool(Path(filename).exists())

    with open(filename, 'a') as fh:
        if not file_exist:
            fh.write('date time weekday price\n')

        for d in data.items():
            the_date, price = d
            weekday = datetime.strptime(the_date, "%Y-%m-%d %H:%M").weekday()
            the_string = the_date + ' ' + str(weekday) + ' ' + price.replace('.', ',') + '\n'

            fh.write(the_string)
