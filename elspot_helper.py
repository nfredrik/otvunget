import json
import logging
from datetime import datetime, timedelta, date
from pathlib import Path
from types import SimpleNamespace

WRITE_APPEND = "a"
CONFIG_FILE_NAME = "elspot_config.json"


# TODO: rewrite with better error handling ....
class ElSpotError(Exception):
    pass


def read_config(config_filename: str) -> dict:
    config_filename = str(Path(__file__).with_name(config_filename))

    if not Path(config_filename).exists():
        raise ElSpotError("Could not find config file: " + config_filename)

    with open(config_filename) as fh:
        return json.loads(
            fh.read(), object_hook=lambda d: SimpleNamespace(**d)
        )


def setup_logger(level, filename: str) -> logging.Logger:
    logging.basicConfig(
        filename=filename,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=eval("logging." + level),
    )

    return logging.getLogger()


def seconds_until_midnight() -> int:
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(
        year=tomorrow.year,
        month=tomorrow.month,
        day=tomorrow.day,
        hour=0,
        minute=0,
        second=10,
    )
    return int((midnight - datetime.now()).total_seconds())


def save_csv(logger: logging.Logger, filename: str, data: dict) -> None:
    def saved_file_date(filename) -> date:
        return (
            datetime.fromtimestamp(int(Path(filename).stat().st_mtime)).date()
            if Path(filename).exists()
            else datetime.fromtimestamp(0).date()
        )

    if datetime.now().date() == saved_file_date(filename):
        logger.error(
            "-- save_csv: date already saved! " + str(datetime.now().date())
        )
        return

    with open(filename, WRITE_APPEND) as fh:
        if not Path(filename).exists():
            fh.write("date time weekday price\n")
        sorted_by_hour = sorted(
            data.items(),
            key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M"),
        )

        for d in sorted_by_hour:
            the_date, price = d
            weekday = datetime.strptime(the_date, "%Y-%m-%d %H:%M").weekday()
            the_string = (
                the_date
                + " "
                + str(weekday)
                + " "
                + price.replace(".", ",")
                + "\n"
            )
            fh.write(the_string)
