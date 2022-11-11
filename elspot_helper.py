import json
import logging
from datetime import datetime, timedelta, date, timezone
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo


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


def seconds_until_midnight(logger):
    def summer_time(the_time=datetime.now()) -> bool:
        sweden_time = the_time.replace(tzinfo=ZoneInfo('Europe/Stockholm'))
        return sweden_time.hour == sweden_time.astimezone(ZoneInfo('Europe/Moscow')).hour + 1

    hour = 1 if summer_time() else 0
    logger.debug(f"-- we have {'summer' if summer_time() else 'winter'} time")

    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month,
                        day=tomorrow.day, hour=hour, minute=0, second=10)
    return int((midnight - datetime.now()).total_seconds())


def save_csv(logger, filename, data: dict) -> None:
    def saved_file_date(filename) -> date:
        return datetime.fromtimestamp(int(Path(filename).stat().st_mtime)).date() if Path(
            filename).exists() else datetime.fromtimestamp(0).date()

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
            the_string = the_date + ' ' + str(weekday) + ' ' + price.replace('.', ',') + '\n'
            fh.write(the_string)
