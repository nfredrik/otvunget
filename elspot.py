#!/usr/bin/env python
import time
from datetime import datetime

from elspot_helper import ElSpotError, setup_logger, read_config, seconds_until_midnight
from parser import ElSpotHTMLParser
from repo import Repo
from scraper import Scraper


def main():
    config = read_config()
    logger = setup_logger(config.loglevel)

    scraper = Scraper(logger, config)
    elspot_parser = ElSpotHTMLParser(logger)
    repo = Repo(logger, config)
    time_to_sleep = 0
    while True:
        try:
            data, time_to_sleep = scraper.get_data()
            elspot_parser.feed(data)
            repo.save(elspot_parser.get_elprices())
        except ElSpotError as e:
            logger.error('-- ough... ' + str(e))

        except KeyboardInterrupt:
            logger.error('-- user killed the script!!...')
            exit(1)

        if datetime.now().date() <= repo.saved_file_date():
            logger.debug('-- success, will sleep until midnight')
            time_to_sleep = seconds_until_midnight()
            scraper.reset()

        time.sleep(time_to_sleep)


if __name__ == "__main__":
    main()
