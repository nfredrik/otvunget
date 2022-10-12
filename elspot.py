#!/usr/bin/env python

import argparse
import logging
import sys

from elspot_helper import get_elspot_data, ElSpotHTMLParser, ElSpotError, get_elspot_mock, save_to_file

SUCCESS, ERROR = 0, 1


def the_main(args):
    logging.basicConfig(level=logging.INFO)
    elspot_parser = ElSpotHTMLParser()

    try:
        logging.info('--get data')
        data = get_elspot_mock() if args.mock else get_elspot_data()
        logging.info('--parse data')
        elspot_parser.feed(data)
    except ElSpotError:
        return ERROR

    logging.info('--save data to file')
    save_to_file(data=elspot_parser.get_elprices(), filename='elspot.json')
    logging.debug(elspot_parser.get_elprices())
    return SUCCESS


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract prices', prog='elspot',
                                     usage='%(prog)s [options]')
    parser.add_argument('-l', '--loglevel', type=eval, choices=['FATAL', 'WARN', 'INFO', 'DEBUG'], required=False,
                        help='log level')

    parser.add_argument('-m', '--mock', action='store_true', help='enable the mocked data')

    arguments = parser.parse_args()

    sys.exit(the_main(arguments))
