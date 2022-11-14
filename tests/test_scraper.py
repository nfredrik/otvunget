import logging
from dataclasses import dataclass
from unittest.mock import Mock
from urllib.error import URLError
from urllib.request import urlopen

import pytest

from scraper import Scraper, ElSpotCommError


@pytest.mark.skip
def test_scraper():
    xr = Scraper(logging=logging, urler=urlopen(Scraper.URL))
    assert isinstance(xr.get_data(), str)


def test_scraper_okay():
    class Nisse:
        def read(self):
            return 'hello'.encode('utf-8')

        def getcode(self):
            return 200

        def close(self):
            ...

    urlopen = Nisse()
    xr = Scraper(logging=logging, urler=urlopen)
    assert 'hello', xr.get_data()


def test_scraper_not_okay():
    class Nisse:
        def read(self):
            return 'hello'.encode('utf-8')

        def getcode(self):
            return 500

        def close(self):
            ...

    urlopen = Nisse()

    xr = Scraper(logging=logging, urler=urlopen)
    with pytest.raises(ElSpotCommError):
        xr.get_data()


def test_scraper_error():
    class Nisse:
        def read(self):
            raise URLError(reason='Aj')

        def getcode(self):
            return 200

        def close(self):
            ...

    urlopen = Nisse()

    xr = Scraper(logging=logging, urler=urlopen)
    with pytest.raises(ElSpotCommError):
        xr.get_data()


def test_scraper_no_encode():
    class Nisse:
        def read(self):
            return 'helloa'

        def getcode(self):
            return 200

        def close(self):
            ...

    urlopen = Nisse()

    xr = Scraper(logging=logging, urler=urlopen)
    with pytest.raises(Exception):
        xr.get_data()
