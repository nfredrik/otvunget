#!/usr/bin/env python
import logging
import time
from datetime import datetime

from elspot_helper import ElSpotError, save_to_file, setup_logging, saved_file_date, read_config
from elspot_scrape import get_elspot_data, get_elspot_mock
from parser import ElSpotHTMLParser


def the_main():
    config = read_config()
    setup_logging(config.loglevel)

    elspot_parser = ElSpotHTMLParser(logging)
    get_data = get_elspot_mock if config.mock == 'True' else get_elspot_data
    while True:
        if datetime.now().date() > saved_file_date(config.filename).date():
            try:
                data = get_data(logging, config.attempts, config.interval)
                elspot_parser.feed(data)
                save_to_file(data=elspot_parser.get_elprices(), filename=config.filename, logging=logging)
            except ElSpotError as e:
                logging.error(f'-- Ough... {e}')

            except KeyboardInterrupt:
                logging.error('-- user killed the script!!...')
                exit(1)

        else:
            logging.info('-- ping')

        time.sleep(config.poll_frequency)


if __name__ == "__main__":
    the_main()
