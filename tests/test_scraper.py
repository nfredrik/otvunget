import pytest
from unittest.mock import MagicMock, patch
from urllib.error import URLError
import json

# Assuming the classes are in a module named scraper_module
from scraper import Scraper, ElSpotCommError


@pytest.fixture
def mock_logging():
    return MagicMock()


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.getcode.return_value = 200
    mock.read.return_value = json.dumps(
        [
            {"time_start": "2024-11-27T00:00:00+01:00", "SEK_per_kWh": 0.5},
            {"time_start": "2024-11-27T01:00:00+01:00", "SEK_per_kWh": 0.6},
        ]
    ).encode("utf-8")
    return mock


def test_get_data_success(mock_logging, mock_response):
    scraper = Scraper(logging=mock_logging, urler=mock_response)
    data = scraper.get_data()
    assert data == {"2024-11-27 00:00:00": "0.5", "2024-11-27 01:00:00": "0.6"}
    mock_logging.info.assert_called_with("-- get_elspot data")


def test_get_data_http_error(mock_logging):
    mock_response = MagicMock()
    mock_response.getcode.return_value = 500
    scraper = Scraper(logging=mock_logging, urler=mock_response)
    with pytest.raises(
        ElSpotCommError, match="Error: did not get a proper reply500"
    ):
        scraper.get_data()
    mock_logging.info.assert_called_with("-- get_elspot data")


def test_get_data_url_error(mock_logging):
    scraper = Scraper(logging=mock_logging)
    with patch("scraper.urlopen", side_effect=URLError("Test URL Error")):
        with pytest.raises(
            ElSpotCommError,
            match="Error: did not get a proper reply Test URL Error",
        ):
            scraper.get_data()
    mock_logging.info.assert_called_with("-- get_elspot data")
    mock_logging.error.assert_called_with(
        "-- get_elspot com failure <urlopen error Test URL Error>"
    )


def test_get_data_unknown_error(mock_logging):
    scraper = Scraper(logging=mock_logging)
    with patch("scraper.urlopen", side_effect=Exception("Test Unknown Error")):
        with pytest.raises(Exception, match="Test Unknown Error"):
            scraper.get_data()
    mock_logging.info.assert_called_with("-- get_elspot data")
    mock_logging.error.assert_called_with(
        "-- get_elspot unknown error Test Unknown Error"
    )
