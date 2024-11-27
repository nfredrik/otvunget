import logging
import re
from urllib.request import urlopen

from scraper import Scraper
import pytest


def assert_content(response, content=None, mimetype="application/json"):
    msg = "No Content-Type header found"
    assert "Content-Type" in response.headers, msg

    content_type = response.headers["Content-Type"]
    msg = f"Incorrect Content Type set, expected:{mimetype}"
    assert mimetype in content_type, msg

    body = response.read()
    assert len(body) > 1, "Expected content size to be bigger than 1!"


# @pytest.mark.integration
def test_elspot_website_any_content():
    logger = logging.getLogger()

    scraper = Scraper(logging=logger)
    response = urlopen(scraper.build_url)
    assert response.getcode() == Scraper.HTTP_OK

    assert_content(response)
    response.close()


# @pytest.mark.skip
def test_elspot_website_compatible():
    logger = logging.getLogger()
    scraper = Scraper(logging=logger)
    response = urlopen(scraper.build_url)
    assert response.getcode() == Scraper.HTTP_OK

    response.close()
    it_all = scraper.get_data()
    assert isinstance(it_all, dict)

    dates = it_all.keys()
    prices = it_all.values()
    date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    prices_pattern = re.compile(r"(-)?(\d{1,4}).(\d{1,4})(.*)")
    result = all(
        date_pattern.match(the_date) is not None for the_date in dates
    )
    assert result

    result2 = all(prices_pattern.match(price) is not None for price in prices)
    assert result2
