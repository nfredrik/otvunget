#!/usr/bin/env python
import asyncio
import logging

from elspot_helper import get_elspot_data, ElSpotHTMLParser, ElSpotError, get_elspot_mock, save_to_file, Config


async def the_main():
    config = Config()
    logging.basicConfig(filename='elspot.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=eval(f'logging.{config.loglevel}'))

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
            logging.error('--error, we failed going down...')
            exit(1)

        await asyncio.sleep(config.poll_frequency)


if __name__ == "__main__":
    asyncio.run(the_main())
