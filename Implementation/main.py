#!/usr/bin/env python3.6
# ------------------------------------------------------------------------------
# Crypto Trading Bot
#
# (C) 2021 Christopher Herron, Thomas Brunner
# email: christopherherron09@gmail.com, tbrunner@kth.se
#
# ------------------------------------------------------------------------------
# TODO: Setup trading via api -  copy the simulation cache/trader and alter to live (easier to not miss changes)
# TODO: Strategy for start price

# Complete/Discuss Above tasks before doing these
# TODO: FIx email files
# TODO: Live run

# Nice to
# TODO: Add dynamic fee
# TODO: Optimize with threading
# TODO: Send email when trading or when orders are not going throug
# TODO: Add relevant visualisations
# TODO: Add database storage?
# TODO: Docker container
# TODO: Add flag to start trading buy being or selling. If selling we need to know how much we have on the account


from argparse import ArgumentParser
import sys

from BitstampAPIAction import BitstampAPIAction
from BitstampWebsocket import BitstampWebSocket
from Utils.TradebotUtils import TradeBotUtils
from SimulationTradeBot import SimulationTradeBot
from LiveTradeBot import LiveTradeBot


def main(argv):
    arg_parser = ArgumentParser(description='Run a crypto trading bot with the bitstamp api.',
                                formatter_class=TradeBotUtils.CustomFormatter,
                                epilog='(C) 2021 \nAuthors: Christopher Herron and Thomas Brunner \nEmails: christopherherron09@gmail.com and tbrunner@kth.se')
    arg_parser.add_argument('initial_value', help='Specify the amount of money to invest[$]', type=int)
    # arg_parser.add_argument('is_buy', help='Specify if buy or sell', default=True, action='store_false')
    arg_parser.add_argument('--interest', default=0.015, help='Specify the interest gain [%%]', type=float)
    arg_parser.add_argument('--run_time_minutes', default=1000000,
                            help='Specify the number of minutes the bot runs [min]', type=int)
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

    try:

        TradeBotUtils.validate_args(args)
        bitstamp_websocket = BitstampWebSocket(args.market)
        account_bid_price = TradeBotUtils.set_initial_trade_price(bitstamp_websocket)
        bitstamp_api = BitstampAPIAction(TradeBotUtils.get_customer_ID(),
                                         TradeBotUtils.get_api_key(),
                                         TradeBotUtils.get_api_secret())
        TradeBotUtils.live_run_checker(args.is_not_simulation)

        if args.is_not_simulation:
            crypto_trade_bot = LiveTradeBot(
                initial_value=args.initial_value,
                account_bid_price=account_bid_price,
                interest=args.interest,
                bitstamp_api=bitstamp_api,
                bitstamp_websocket=bitstamp_websocket,
                run_time_minutes=args.run_time_minutes,
                is_reinvesting_profits=args.is_reinvesting_profits,
                print_interval=args.print_interval,
                is_reset_logs=args.is_reset_logs,
                is_buy=True)
        else:
            crypto_trade_bot = SimulationTradeBot(
                initial_value=args.initial_value,
                account_bid_price=account_bid_price,
                interest=args.interest,
                bitstamp_websocket=bitstamp_websocket,
                run_time_minutes=args.run_time_minutes,
                is_reinvesting_profits=args.is_reinvesting_profits,
                print_interval=args.print_interval,
                is_reset_logs=args.is_reset_logs,
                is_buy=True)

        crypto_trade_bot.run()

    except ValueError as error_message:
        print(error_message)
    except KeyboardInterrupt:
        print("Keyboard Interrupted")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
