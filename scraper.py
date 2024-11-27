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
        next_day = datetime.now() + timedelta(days=0)
        date_string = f'{next_day.year}/{next_day.month}-{next_day.day}'
        prisklass ='SE3'
        self.build_url = f'https://www.elprisetjustnu.se/api/v1/prices/{date_string}_{prisklass}.json'

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

        return {item['time_start'].split('+')[0].replace('T', ' '): item['SEK_per_kWh'] for item in all_day}

