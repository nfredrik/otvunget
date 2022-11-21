from urllib.request import urlopen
from scraper import Scraper
from parser import ElSpotHTMLParser
import logging

def assert_content(response, content=None, mimetype="text/html"):
        msg = "No Content-Type header found"
        assert "Content-Type" in response.headers, msg


        content_type = response.headers["Content-Type"]
        msg =f"Incorrect Content Type set, expected:{mimetype}"
        assert mimetype in content_type, msg

        body = response.read()
        assert len(body) > 1, "Expected content size to be bigger than 1!"



def test_elspot_website_any_content():
        response = urlopen(Scraper.URL)
        assert response.getcode() == Scraper.HTTP_OK

        assert_content(response)
        response.close()


def test_elspot_website_compatible():
        response = urlopen(Scraper.URL)
        assert response.getcode() == Scraper.HTTP_OK
        tm = ElSpotHTMLParser(logging)
        body = response.read().decode("utf-8")
        response.close()
        tm.feed(body)
        it_all = tm.get_elprices()
        assert isinstance(it_all, dict)