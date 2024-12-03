import json
from datetime import datetime, timedelta
from urllib.error import URLError
from urllib.request import urlopen


class ElSpotCommError(Exception):
    pass


class Scraper:
    HTTP_OK = 200

    def __init__(self, logging, urler=None):
        self.logging = logging
        self.urler = urler
        date_string = self.compute_date()
        prisklass = "SE3"
        self.build_url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_string}_{prisklass}.json"

    def compute_date(self, days: int = 1) -> datetime:
        next_day = datetime.now() + timedelta(days=days)
        month = str(next_day.month).zfill(2)
        day = str(next_day.day).zfill(2)
        return f"{next_day.year}/{month}-{day}"

    def ping_date(self) -> bool:
        try:
            response = self.urler or urlopen(self.build_url)
            if response.getcode() != Scraper.HTTP_OK:
                return False
            return True
        except URLError:
            return False

    def get_data(self) -> dict:
        self.logging.info("-- get_elspot data")
        try:
            response = self.urler or urlopen(self.build_url)
            if response.getcode() != Scraper.HTTP_OK:
                raise ElSpotCommError(
                    "Error: did not get a proper reply"
                    + str(response.getcode())
                )

        except URLError as e:
            self.logging.error("-- get_elspot com failure " + str(e))

            raise ElSpotCommError(
                "Error: did not get a proper reply " + str(e.reason)
            )

        except Exception as e:
            self.logging.error("-- get_elspot unknown error " + str(e))
            raise e

        body = response.read()
        response.close()
        all_day = json.loads(body)

        return {
            item["time_start"]
            .split("+")[0][:-3]
            .replace("T", " "): str(item["SEK_per_kWh"])
            for item in all_day
        }
