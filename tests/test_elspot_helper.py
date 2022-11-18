import logging
import time
import json
from pathlib import Path

import pytest

from elspot_helper import seconds_until_midnight, save_csv, read_config,CONFIG_FILE_NAME,ElSpotError

JSON_FILE = 'nisse.json'
CSV_FILE = 'file.csv'
CONFIG_FILE = 'olle.json'

@pytest.fixture
def tempfile(tmpdir):
    return tmpdir + 'nisse.csv'

@pytest.fixture
def configfile(tmpdir):
    filename = f"{str(tmpdir)}/{CONFIG_FILE}"
    with open(filename, 'w') as fh:
        fh.write(json.dumps({'json_filename': JSON_FILE, 'csv_filename': CSV_FILE, 'loglevel': 'FATAL',
                             'log_filename': 'loggen.log', "backoff_start": 5,
                             "backoff_multiple": 2,
                             "backoff_stop": 3500}, indent=4))
    return CONFIG_FILE

def test_config_normal(configfile):
    mr = read_config(CONFIG_FILE_NAME)
    assert mr.loglevel == "DEBUG"

def test_config_no_config_file():
    with pytest.raises(ElSpotError):
        read_config('dummy.json')


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
