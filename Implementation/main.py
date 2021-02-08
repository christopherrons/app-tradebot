#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Crypto Trading Bot
#
# (C) 2021 Christopher Herron, Thomas Brunner
# email: christopherherron09@gmail.com, tbrunner@kth.se
#
# ------------------------------------------------------------------------------
# TODO: Add fees to output. Fees are available through the API
# TODO: ADd input checker, e.g. that interest is not below 0.00105..
# TODO: Get current market price before start
# TODO: Add flag to start trading buy being or selling
# TODO: Setup trading via api
# TODO: Check options on hwo to setup accounts
# TODO: Live run
# TODO: Add relevant visualisations
# TODO: Add database storage
# TODO: Optimize with threading
# TODO: Strategy for start price


from argparse import ArgumentParser
import sys
from TradebotUtils import TradeBotUtils
from SimulationTradeBot import SimulationTradeBot
from LiveTradeBot import LiveTradeBot


def main(argv):
    arg_parser = ArgumentParser(description='Run a crypto trading bot with the bitstamp api.',
                                formatter_class=TradeBotUtils.CustomFormatter,
                                epilog='(C) 2021 \nAuthors: Christopher Herron and Thomas Brunner \nEmails: christopherherron09@gmail.com and tbrunner@kth.se')
    arg_parser.add_argument('initial_value', help='Specify the amount of money to invest[$]', type=int)
    arg_parser.add_argument('account_bid_price', help='Specify the buy price [$]', type=float)
    arg_parser.add_argument('interest', help='Specify the interest gain [%%]', type=float)
    arg_parser.add_argument('--run_time_minutes', default=10000000000, help='Specify the number of minutes the bot runs [min]', type=int)
    arg_parser.add_argument('--market', default="xrpusd", help='Specify the trading market ', type=str)
    arg_parser.add_argument('--is_reinvesting_profits', help='Flag if the profits are reinvested',
                            default=True, action='store_false')
    arg_parser.add_argument('--is_not_simulation',
                            help='Flag if the trading is not simulated based on the trading strategy',
                            default=False, action='store_true')
    arg_parser.add_argument('--is_reset_logs',
                            help='Flag to reset logs at start of run',
                            default=False, action='store_true')
    arg_parser.add_argument('--print_interval', default=1,
                            help='Specify the interval for current information data printing and logging [min]',
                            type=float)

    args = arg_parser.parse_args()

    TradeBotUtils.live_run_checker(args.is_not_simulation)

    try:
        if args.is_not_simulation:
            crypto_trade_bot = LiveTradeBot(
                initial_value=args.initial_value,
                account_bid_price=args.account_bid_price,
                interest=args.interest,
                bitstamp_token=TradeBotUtils.get_bitstamp_token(),
                run_time_minutes=args.run_time_minutes,
                is_reinvesting_profits=args.is_reinvesting_profits,
                print_interval=args.print_interval,
                is_reset_logs=args.is_reset_logs,
                is_buy=True)
        else:
            crypto_trade_bot = SimulationTradeBot(
                initial_value=args.initial_value,
                account_bid_price=args.account_bid_price,
                interest=args.interest,
                bitstamp_token=TradeBotUtils.get_bitstamp_token(),
                market=args.market,
                run_time_minutes=args.run_time_minutes,
                is_reinvesting_profits=args.is_reinvesting_profits,
                print_interval=args.print_interval,
                is_reset_logs=args.is_reset_logs,
                is_buy=True)

        crypto_trade_bot.run()

    except KeyboardInterrupt:
        print("Keyboard Interrupted")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
