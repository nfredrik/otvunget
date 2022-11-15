#!/usr/bin/env python
import time
import sys
from datetime import datetime, timedelta

from elspot_helper import ElSpotError, setup_logger, read_config, seconds_until_midnight, save_csv, CONFIG_FILE_NAME
from parser import ElSpotHTMLParser, ElSpotDataError
from repo import Repo
from scraper import Scraper, ElSpotCommError
from sleep_controller import SleepController


# The config file path is a file with the following name in the same directory as this script itself


def main(mock_scraper=None):
    config = read_config(config_filename=CONFIG_FILE_NAME)
    logger = setup_logger(config.loglevel, config.log_filename)

    scraper = mock_scraper or Scraper(logging=logger)
    sleep_controller = SleepController(config)
    elspot_parser = ElSpotHTMLParser(logger)
    repo = Repo(logger, config.json_filename)
    time_to_sleep = 0
    while True:
        try:
            time_to_sleep = sleep_controller.current_backoff()
            data = scraper.get_data()
            elspot_parser.feed(data)
            el_prices = elspot_parser.get_elprices()
            repo.save(el_prices)
        except ElSpotCommError as e:
            logger.debug('-- failure on communication, will backoff ' + str(time_to_sleep) + ' seconds' + str(e))

        except ElSpotDataError as e:
            logger.debug('-- failure on data, will backoff ' + str(time_to_sleep) + ' seconds' + str(e))
            del data

        except ElSpotError as e:
            logger.error('-- internal error... ' + str(e))

        except KeyboardInterrupt:
            logger.error('-- user killed the script!!...')
            return 1

        except Exception as e:
            logger.error('-- unknown error ' + str(e))

        if datetime.now().date() <= repo.saved_file_date():
            logger.debug('-- success, file saved')
            time_to_sleep = seconds_until_midnight() if not mock_scraper else 0
            sleep_controller.reset()
            save_csv(logger, config.csv_filename, el_prices)

        logger.debug('-- will sleep,  ' + str(timedelta(seconds=time_to_sleep)) + ' hours')
        time.sleep(time_to_sleep)


if __name__ == "__main__":
    sys.exit(main())
