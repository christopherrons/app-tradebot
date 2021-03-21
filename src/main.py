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
# TODO: Switch trade_nr back to before as serial wont work

# Nice to
# TODO: If possible trigger evant based on websocket rather than other way around
# TODO: Optimize with threading
# TODO: Strategy for start price
# TODO: Create tax calculator based on trades

import sys
from argparse import ArgumentParser

from applications.algorithmic_trading.src.main.strategies.VolatilityTrading import VolatilityTrading
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


def main(argv):
    arg_parser = ArgumentParser(description='Run a crypto trading bot with the bitstamp api.',
                                formatter_class=TradeBotUtils.CustomFormatter,
                                epilog='(C) 2021 \nAuthors: Christopher Herron and Thomas Brunner \nEmails: christopherherron09@gmail.com and tbrunner@kth.se')
    arg_parser.add_argument('strategy', choices=('Volatility',), help='Choose Trading Strategy', type=str)
    args = arg_parser.parse_args()

    if args.strategy == 'Volatility':
        VolatilityTrading().run()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
