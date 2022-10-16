#!/usr/bin/env python
import time
from datetime import datetime

from elspot_helper import ElSpotError, setup_logger, read_config
from parser import ElSpotHTMLParser
from repo import Repo
from scraper import Scraper


def main():
    config = read_config()
    logger = setup_logger(config.loglevel)

    scraper = Scraper(config.mock, logger, config.attempts, config.interval)
    elspot_parser = ElSpotHTMLParser(logger)
    repo = Repo(config.filename, logger)

    while True:
        if datetime.now().date() > repo.saved_file_date():
            try:
                data = scraper.get_data()
                elspot_parser.feed(data)
                repo.save_to_file(elspot_parser.get_elprices())
            except ElSpotError as e:
                logger.error(f'-- Ough... {e}')

            except KeyboardInterrupt:
                logger.error('-- user killed the script!!...')
                exit(1)

        time.sleep(config.poll_frequency)


if __name__ == "__main__":
    main()
