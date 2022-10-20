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

    scraper = Scraper(config.mock, logger, config.attempts, config.interval)
    elspot_parser = ElSpotHTMLParser(logger)
    repo = Repo(config.filename, logger, config.stdout)

    backoff = config.backoff_start

    while True:
#        if datetime.now().date() > repo.saved_file_date():
        if True:
            try:
                data = scraper.get_data()
                elspot_parser.feed(data)
                repo.save(elspot_parser.get_elprices())
                success = True
            except ElSpotError as e:
                logger.error('-- Ough... ' + str(e))
                success = False

            except KeyboardInterrupt:
                logger.error('-- user killed the script!!...')
                exit(1)

            if not success:
                logger.debug('backoff ' + str(backoff))
                time.sleep(backoff)
                backoff = backoff * config.backoff_multipel
                if backoff > config.backoff_stop:
                    backoff = config.backoff_stop
            else:
                logger.debug('success, will sleep until midnight')
                time.sleep(seconds_until_midnight())
                backoff = config.backoff_start

#        time.sleep(config.poll_frequency)


if __name__ == "__main__":
    main()
