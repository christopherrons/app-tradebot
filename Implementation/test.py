#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Crypto Trading Bot
#
# (C) 2021 Christopher Herron, Thomas Brunner
# email: christopherherron09@gmail.com, tbrunner@kth.se
#
# ------------------------------------------------------------------------------
from argparse import ArgumentParser
import sys
from TradebotUtils import CustomFormatter, get_bitstamp_token


def main(argv):
    arg_parser = ArgumentParser(description='Run a crypto trading bot with the bitstamp api.',
                                formatter_class=CustomFormatter,
                                epilog='(C) 2021 \nAuthors: Christopher Herron and Thomas Brunner \nEmails: christopherherron09@gmail.com and tbrunner@kth.se')
    arg_parser.add_argument('initial_value', help='Specify the amount of money to invest[$]', type=int)
    arg_parser.add_argument('buy_price', help='Specify the buy price [$]', type=int)
    arg_parser.add_argument('interest', help='Specify the interest gain [%%]', type=int)
    arg_parser.add_argument('run_time_minutes', help='Specify the number of minutes the bot runs [min]', type=int)
    arg_parser.add_argument('--is_simulation', help='Flag if the trading is simulated based on the trading strategy',
                            default=True, action='store_false')

    args = arg_parser.parse_args()

    try:
        pass
    except KeyboardInterrupt:
        print("Keyboard Interrupted")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
