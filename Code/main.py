#!/usr/bin/env python3.6
# ------------------------------------------------------------------------------
# Crypto Trading Bot
#
# (C) 2021 Christopher Herron, Thomas Brunner
# email: christopherherron09@gmail.com, tbrunner@kth.se
#
# ------------------------------------------------------------------------------
# TODO: Strategy for start price
# TODO: Clean up code
# TODO: Add kraken api and make api calls possible for both kraken and bitstamp

# Nice to
# TODO: Optimize with threading
# TODO: Add relevant visualisations
# TODO: Add database storage?
# TODO: Docker container
# TODO: Add flag to start trading buy being or selling. If selling we need to know how much we have on the account
# TODO: Transaction fee is not working properly eventhough the fee is available when i checke with the api. Maybe it didnt have time to register the transaction before the transaction_fee call

import sys
from argparse import ArgumentParser

from Application.Runner.TradeRunner import TradeRunner
from Services.Runner.CacheStorage.LiveCache import LiveCache
from Services.Runner.CacheStorage.SimulationCache import SimulationCache
from Services.Runner.Exchange.BitstampAPIAction import BitstampAPIAction
from Services.Runner.Exchange.BitstampWebsocket import BitstampWebsocket
from Services.Runner.Exchange.KrakenWebsocket import KrakenWebsocket
from Services.Runner.TradeBots.LiveTradeBotBuyer import LiveTradeBotBuyer
from Services.Runner.TradeBots.LiveTradeBotSeller import LiveTradeBotSeller
from Services.Runner.TradeBots.SimulationTradeBotBuyer import SimulationTradeBotBuyer
from Services.Runner.TradeBots.SimulationTradeBotSeller import SimulationTradeBotSeller
from Services.Runner.Utils.TradeBotUtils import TradeBotUtils


def main(argv):
    arg_parser = ArgumentParser(description='Run a crypto trading bot with the bitstamp api.',
                                formatter_class=TradeBotUtils.CustomFormatter,
                                epilog='(C) 2021 \nAuthors: Christopher Herron and Thomas Brunner \nEmails: christopherherron09@gmail.com and tbrunner@kth.se')
    arg_parser.add_argument('initial_value', help='Specify the amount of money to invest[$]', type=int)
    arg_parser.add_argument('--exchange', default="Kraken", help='Type Bitstamp to use their API and WEbsocket', type=str)
    arg_parser.add_argument('--is_buy', help='Specify if buy or sell', default=True, action='store_false')
    arg_parser.add_argument('--interest', default=0.015, help='Specify the interest gain [%%]', type=float)
    arg_parser.add_argument('--run_time_minutes', default=1000000,
                            help='Specify the number of minutes the bot runs [min]', type=int)
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
        TradeBotUtils.live_run_checker(args.is_not_simulation)

        if args.exchange == 'Bitstamp':
            print("Exchange Bitstamp is being used\n")
            exchange_websocket = BitstampWebsocket()
            exchange_api = BitstampAPIAction(TradeBotUtils.get_customer_ID(),
                                             TradeBotUtils.get_api_key(),
                                             TradeBotUtils.get_api_secret())
        else:
            print("Exchange Kraken is being used\n")
            exchange_websocket = KrakenWebsocket()

        account_bid_price = TradeBotUtils.set_initial_trade_price(exchange_websocket)

        if args.is_reset_logs:
            TradeBotUtils.reset_logs()

        if args.is_not_simulation:
            cache = LiveCache(initial_value=exchange_api.get_account_cash_value(),
                              interest=args.interest,
                              account_bid_price=account_bid_price,
                              is_reinvesting_profits=args.is_reinvesting_profits)

            trade_bot_runner = TradeRunner(
                is_buy=args.is_buy,
                trade_bot_buyer=LiveTradeBotBuyer(exchange_api, exchange_websocket, cache),
                trade_bot_seller=LiveTradeBotSeller(exchange_api, exchange_websocket, cache),
                run_time_minutes=args.run_time_minutes,
                print_interval=args.print_interval)
        else:
            cache = SimulationCache(initial_value=args.initial_value,
                                    interest=args.interest,
                                    account_bid_price=account_bid_price,
                                    is_reinvesting_profits=args.is_reinvesting_profits)

            trade_bot_runner = TradeRunner(
                is_buy=args.is_buy,
                trade_bot_buyer=SimulationTradeBotBuyer(exchange_websocket, cache),
                trade_bot_seller=SimulationTradeBotSeller(exchange_websocket, cache),
                run_time_minutes=args.run_time_minutes,
                print_interval=args.print_interval)

        trade_bot_runner.run()

    except ValueError as error_message:
        print(error_message)
    except KeyboardInterrupt:
        print("Keyboard Interrupted")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
