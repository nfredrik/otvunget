import json
from datetime import datetime
from pathlib import Path

from elspot_helper import ElSpotError


class Repo:
    def __init__(self, filename, logging):
        self.filename = filename
        self.logging = logging

    def saved_file_date(self):
        return datetime.fromtimestamp(int(Path(self.filename).stat().st_ctime)).date() if Path(self.filename).exists() else datetime.fromtimestamp(0).date()


    def save_to_file(self, data: dict) -> None:
        def today_date(data: dict):
            return datetime.now().strftime('%Y-%m-%d') == list(data.keys())[0].split()[0]

        if not today_date(data):
            self.logging.error('-- error too old date wait to save to file')
            raise ElSpotError('Wrong date: ' + list(data.keys())[0])

        self.logging.info('-- save_to_file ...')
        with open(self.filename, "w") as outfile:
            json.dump(data, outfile, indent=2)
