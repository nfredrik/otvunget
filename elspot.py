#!/usr/bin/env python
import asyncio
import logging

from elspot_helper import ElSpotError, save_to_file, Config, setup_logging
from getter import get_elspot_data, get_elspot_mock
from parser import ElSpotHTMLParser


async def the_main():
    config = Config()
    setup_logging(config.loglevel)

    elspot_parser = ElSpotHTMLParser(logging)
    get_data = get_elspot_mock if config.mock else get_elspot_data
    while True:
        try:
            data = get_data(logging, config.attempts, config.interval)
            elspot_parser.feed(data)
            save_to_file(data=elspot_parser.get_elprices(), filename=config.filename, logging=logging)
        except ElSpotError:
            ...

        except KeyboardInterrupt:
            logging.error('--User killed the script!!...')
            exit(1)

        await asyncio.sleep(config.poll_frequency)


if __name__ == "__main__":
    asyncio.run(the_main())
