import json
import urllib
from html.parser import HTMLParser
from urllib.error import URLError
from urllib.request import urlopen


class ElSpotError(Exception):
    pass

def get_elspot_data() -> str:
    url = 'https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm'

    try:
        response = urlopen(url)
        body = response.read()
        response.close()
    except urllib.error.URLError as e:
        print(f'Error {e}')
        raise ElSpotError(f'Error: {e}') from e

    return body.decode("utf-8")

def get_elspot_mock():
    with open('elspot_mock.html') as fh:
        return fh.read()

class ElSpotHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._recording = False
        self._all = {}
        self._time = None

    @staticmethod
    def _td_tag(tag) -> bool:
        return tag == 'td'

    @staticmethod
    def _is_date(data) -> bool:
        return data.find(':') != -1  # parsa att det är timestamp! use re!


    def handle_starttag(self, tag, attrs):
        self._recording = self._td_tag(tag)

    def handle_endtag(self, tag):
        self._recording = not self._td_tag(tag) and self._recording


    def handle_data(self, data):
        if self._recording:
            if self._is_date(data):
                self._time = data
                return

            if self._time is None:
               raise ElSpotError('Error no date before price!')

            self._all[self._time] = data.split()[0]

    def get_elprices(self) -> dict:
        return self._all


# TODO save formatted!
def save_to_file(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile)
