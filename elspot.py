#!/usr/bin/env python
import sys
import time
from datetime import datetime, timedelta

from elspot_helper import (
    ElSpotError,
    setup_logger,
    read_config,
    seconds_until_midnight,
    save_csv,
    CONFIG_FILE_NAME,
)
from repo import Repo
from scraper import Scraper, ElSpotCommError
from sleep_controller import SleepController

# The config file path is a file with the following name in the same directory as this script itself

ERROR = 42


def main(mock_scraper=None, config_filename=CONFIG_FILE_NAME):
    config = read_config(config_filename=config_filename)
    logger = setup_logger(config.loglevel, config.log_filename)

    scraper = mock_scraper or Scraper(logging=logger)
    sleep_controller = SleepController(config)
    repo = Repo(logger, config.json_filename)
    time_to_sleep = 0
    while True:
        try:
            time_to_sleep: int = sleep_controller.current_backoff()
            el_prices: dict = scraper.get_data()
            repo.save(el_prices)
        except (ElSpotCommError, ElSpotError) as e:
            logger.debug(
                "-- failure , will backoff "
                + str(time_to_sleep)
                + " seconds"
                + str(e)
            )
            del el_prices

        except KeyboardInterrupt:
            logger.error("-- user killed the script!!...")
            return ERROR

        except Exception as e:
            logger.error("-- unknown error " + str(e))

        if datetime.now().date() <= repo.saved_file_date():
            logger.debug("-- success, file saved")
            time_to_sleep: int = (
                seconds_until_midnight() if not mock_scraper else 0
            )
            sleep_controller.reset()
            save_csv(logger, config.csv_filename, el_prices)

        logger.debug(
            "-- will sleep,  "
            + str(timedelta(seconds=time_to_sleep))
            + " hours"
        )
        time.sleep(time_to_sleep)


if __name__ == "__main__":
    sys.exit(main())
