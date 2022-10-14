#!/usr/bin/env python
import time
import logging

from elspot_helper import ElSpotError, save_to_file, Config, setup_logging
from elspot_scrape import get_elspot_data, get_elspot_mock
from parser import ElSpotHTMLParser


def the_main():
    config = Config()
    setup_logging(config.loglevel)

    elspot_parser = ElSpotHTMLParser(logging)
    get_data = get_elspot_mock if config.mock else get_elspot_data
    last_update = (datetime.datetime.now() - timedelta(days=1)).date
    while True:

        current = datetime.datetime.now().date()
        if current > last_update:
            try:
                data = get_data(logging, config.attempts, config.interval)
                elspot_parser.feed(data)
                save_to_file(data=elspot_parser.get_elprices(), filename=config.filename, logging=logging)
                last_update = current
            except ElSpotError:
                ...

            except KeyboardInterrupt:
                logging.error('--User killed the script!!...')
                exit(1)

        time.sleep(config.poll_frequency)


if __name__ == "__main__":
    the_main()
