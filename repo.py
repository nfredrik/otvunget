import json
from datetime import datetime
from pathlib import Path
from pprint import pprint

from elspot_helper import ElSpotError


class Repo:
    def __init__(self, filename, logging, stdout=False):
        self.filename = filename
        self.logging = logging
        self.stdout = stdout

    @staticmethod
    def _today_date(d: dict):
            return datetime.now().strftime('%Y-%m-%d') == list(d.keys())[0].split()[0]

    def saved_file_date(self):
        return datetime.fromtimestamp(int(Path(self.filename).stat().st_ctime)).date() \
            if Path(self.filename).exists() else datetime.fromtimestamp(0).date()

    def save_2_file(self, data: dict) -> None:

        if not Repo._today_date(data):
            self.logging.error('-- error too old date wait to save to file')
            raise ElSpotError('Wrong date: ' + list(data.keys())[0])

        self.logging.info('-- save_to_file ...')
        with open(self.filename, "w") as outfile:
            json.dump(data, outfile, indent=2)

    def save_2_stdout(self, data:dict) -> None:
        pprint(data)

    def save(self, data: dict) -> None:
        return self.save_2_stdout(data) if bool(self.stdout) else self.save_2_file(data)