import json
import logging
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime, timedelta, date


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


def save_csv(logger, filename, data: dict) -> None:
    def saved_file_date(filename) -> date:
        return datetime.fromtimestamp(int(Path(filename).stat().st_mtime)).date() if Path(filename).exists() else datetime.fromtimestamp(0).date()

    if datetime.now().date() == saved_file_date(filename):
        logger.error('-- save_csv: date already saved! ' + str(datetime.now().date()))
        return

    file_exist = bool(Path(filename).exists())
    with open(filename, 'a') as fh:
        if not file_exist:
            fh.write('date time weekday price\n')
        sorted_by_hour = sorted(data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M"))

        for d in sorted_by_hour:
            the_date, price = d
            weekday = datetime.strptime(the_date, "%Y-%m-%d %H:%M").weekday()
            the_string = f'{the_date} {str(weekday)} ' + price.replace('.', ',') + '\n'
            fh.write(the_string)
