import re
from html.parser import HTMLParser

from elspot_helper import ElSpotError


class ElSpotHTMLParser(HTMLParser):

    def __init__(self, logging):
        HTMLParser.__init__(self)
        self.logging = logging
        self._recording = False
        self._all = {}
        self._time = None

    @staticmethod
    def _td_tag(tag) -> bool:
        return tag == 'td'

    @staticmethod
    def _is_date(data) -> bool:
        return re.match("(\d{4})-(\d{2})-(\d{2})", data) != None

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
                self.logging.error('-- Error timestamp not inlcuded in data!!')
                raise ElSpotError('Error no date before price!')

            self._all[self._time] = data.split()[0]

    def get_elprices(self) -> dict:
        return self._all
