#!/usr/bin/env python3.6
# ------------------------------------------------------------------------------
# Crypto Trading Bot
#
# (C) 2021 Christopher Herron, Thomas Brunner
# email: christopherherron09@gmail.com, tbrunner@kth.se
#
# ------------------------------------------------------------------------------
# TODO: Clean up code
# TODO: Trade in eur or usd? Check which market is the most liquid
# TODO: Remove sensitive information fromm docker files and database service class
# TODO: Fix file permissions docker
# TODO: USe pandas df to csv instead of appending
# TODO Check all queries and see if they can be more general
# TODO: Create tax report based on skatteverkt config
# TODO: Config file vs args parser
# TODO: Fix taxable account before push  + remove old branches


# Nice to
# TODO: If possible trigger evant based on websocket rather than other way around
# TODO: Optimize with threading
# TODO: Strategy for start price
# TODO: Create tax calculator based on trades

import sys
from argparse import ArgumentParser

from applications.algorithmic_trading.src.main.strategies.VolatilityTrading import VolatilityTrading
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.tax_management.src.main.tax_services.SwedishTaxService import SwedishTaxService


def main(argv):
    arg_parser = ArgumentParser(description='Run Algorithmic Trading or Generate Tax Reports',
                                formatter_class=TradeBotUtils.CustomFormatter,
                                epilog='(C) 2021 \nAuthors: Christopher Herron and Thomas Brunner \nEmails: christopherherron09@gmail.com and tbrunner@kth.se')
    subparsers = arg_parser.add_subparsers(help='Pick Application to run', dest='subparser_name')

    parse_algorithmic_trading = subparsers.add_parser('algorithmic_trading', help='Run algorithmic trading app')
    parse_algorithmic_trading.add_argument('strategy', choices=('volatility',), help='Choose trading strategy', type=str)

    parse_tax_management = subparsers.add_parser('tax_management', help='Run tax management app')
    parse_tax_management.add_argument('year', help='Enter Tax Year', type=str)
    parse_tax_management.add_argument('--init_database_from_exchange', default=False, help='Flag to init database form exchange', action="store_true")
    parse_tax_management.add_argument('tax_service', choices=('swedish',), help='Choose tax service', type=str)

    args = arg_parser.parse_args()

    if args.subparser_name == "algorithmic_trading":
        if args.strategy == 'volatility':
            VolatilityTrading().run()

    elif args.subparser_name == "tax_management":
        if args.tax_service == "swedish":
            SwedishTaxService(args.year).create_yearly_tax_report()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
