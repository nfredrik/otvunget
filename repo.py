import json
from datetime import datetime
from pathlib import Path
from pprint import pprint

from elspot_helper import ElSpotError


class Repo:
    def __init__(self, logging, config):
        self.filename = config.filename
        self.logging = logging
        self.stdout = config.stdout

    @staticmethod
    def _today_date(d: dict):
        dates = [d.split()[0] for d in d]
        return any(datetime.now().strftime('%Y-%m-%d') == item for item in dates)

    def saved_file_date(self):
        return datetime.fromtimestamp(int(Path(self.filename).stat().st_ctime)).date() \
            if Path(self.filename).exists() else datetime.fromtimestamp(0).date()

    def save_2_file(self, data: dict) -> None:
        if not Repo._today_date(data):
            self.logging.error('-- error wrong date wait to save to file' + list(data.keys())[0])
            raise ElSpotError('Wrong date: ' + list(data.keys())[0])

        self.logging.info('-- save_to_file ...')
        with open(self.filename, "w") as outfile:
            json.dump(data, outfile, indent=2)

    @staticmethod
    def save_2_stdout(data: dict) -> None:
        pprint(data)

    def save(self, data: dict) -> None:
        return self.save_2_stdout(data) if bool(self.stdout) else self.save_2_file(data)
