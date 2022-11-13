import time
import logging
from elspot_helper import seconds_until_midnight, save_csv
from pathlib import Path
import pytest
@pytest.fixture
def tempfile(tmpdir):
    return tmpdir + 'nisse.csv'


def test_midnight():
    first = seconds_until_midnight()
    time.sleep(1)
    second = seconds_until_midnight()
    assert first > second

# TODO: Use a tempfile or file object. Veridy file content??
# check saved only once a day.
# check of sorted on time!
def test_save_csv(tempfile):
    save_csv(logger=logging, filename=tempfile, data={"2022-11-11 06:00": "0.90"})
    assert Path(tempfile).exists()
