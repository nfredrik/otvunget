import os
import json
from pathlib import Path
import pytest
from datetime import datetime
from elspot import main, ERROR

DATA = f"""
 <!doctype html>
 <html lang="sv-SE">
 <body data-cmplz=1>
 <tbody>
                 <tr class="bg-gray-300 hover:bg-gray-100">
             <td class="text-left pt-2 pl-2">{datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
                                 <td class="text-right pt-2 pr-2">0,08 öre/kWh</td>
                             </tr>
                     <tr class="bg-gray-200 hover:bg-gray-100">
             <td class="text-left pt-2 pl-2">2022-10-11 01:00</td>
                                 <td class="text-right pt-2 pr-2">0,07 öre/kWh</td>
                             </tr>
                     <tr class="bg-gray-300 hover:bg-gray-100">
             <td class="text-left pt-2 pl-2">2022-10-11 02:00</td>
                                 <td class="text-right pt-2 pr-2">0,45 öre/kWh</td>                         
                           </tr>
                             </tbody>
 </body>
 </html>
 """


class ScraperMock():
    def __init__(self):
        self.cntr = 0

    def get_data(self) -> str:
        if self.cntr != 0:
            raise KeyboardInterrupt

        self.cntr += 1
        return DATA


@pytest.fixture
def configfile():
    filename = (Path.cwd().parent / 'olle.json').as_posix()
    with open(filename, 'w') as fh:
        fh.write(json.dumps({'json_filename': 'nisse.json', 'csv_filename': 'file.csv', 'loglevel': 'DEBUG',
                             'log_filename': 'loggen.log', "backoff_start": 5,
                             "backoff_multiple": 2,
                             "backoff_stop": 3600}, indent=4))
    return 'olle.json'


def test_main(configfile):
    scraper_mock = ScraperMock()
    rty = main(scraper_mock, config_filename=configfile)
    assert rty == ERROR
    assert (Path.cwd()/'nisse.json').exists()
    assert (Path.cwd()/'file.csv').exists()

    # assert that jsonfile and csvfile created!
