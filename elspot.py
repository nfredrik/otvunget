#!/usr/bin/env python
import time
from datetime import datetime

from elspot_helper import ElSpotError, setup_logger, read_config, seconds_until_midnight, save_csv
from parser import ElSpotHTMLParser
from repo import Repo
from scraper import Scraper, SleepController


def main():
    config = read_config()
    logger = setup_logger(config.loglevel)

    scraper = Scraper(logger, config)
    sleep_controller = SleepController(logger, config)
    elspot_parser = ElSpotHTMLParser(logger)
    repo = Repo(logger, config)
    time_to_sleep = 0
    while True:
        try:
            time_to_sleep = sleep_controller.current_backoff()
            data = scraper.get_data()
            elspot_parser.feed(data)
            el_prices = elspot_parser.get_elprices()
            repo.save(el_prices)

        except ElSpotError as e:
            logger.error('-- ough... ' + str(e))

        except KeyboardInterrupt:
            logger.error('-- user killed the script!!...')
            exit(1)

        if datetime.now().date() <= repo.saved_file_date():
            logger.debug('-- success, will sleep until midnight')
            time_to_sleep = seconds_until_midnight()
            sleep_controller.reset()
            save_csv(config.filename, el_prices)


        time.sleep(time_to_sleep)


if __name__ == "__main__":
    main()
