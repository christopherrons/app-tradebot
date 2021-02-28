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
# TODO: Transaction fee is not working properly eventhough the fee is available when i checke with the api. Maybe it didnt have time to register the transaction before the transaction_fee call
# TODO: Find smart way to set initial value other than memorizing
# TODO: Return quantity and price or only price from websocket?
# TODO: If possible trigger evant based on websocket rather than other way around

# Nice to
# TODO: Optimize with threading
# TODO: Add relevant visualisations
# TODO: Add database storage?
# TODO: Docker container

import sys
from argparse import ArgumentParser

from Application.Runner.TradeRunner import TradeRunner
from Services.Runner.CacheStorage.TradeBotCache import TradeBotCache
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
    arg_parser.add_argument('initial_value', help='Specify the amount of cash that was invested from the beginning [$]',
                            type=float)
    arg_parser.add_argument('exchange', choices=('Bitstamp', 'Kraken'),
                            type=str)
    arg_parser.add_argument('--is_sell', help='Specify if buy or sell', default=False, action='store_true')
    arg_parser.add_argument('--interest', default=0.015, help='Specify the interest gain [%%]', type=float)
    arg_parser.add_argument('--run_time_minutes', default=1000000,
                            help='Specify the number of minutes the bot runs [min]', type=int)
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

        TradeBotUtils.live_run_checker(args.is_not_simulation)

        if args.exchange == 'Bitstamp':
            print("Exchange Bitstamp is being used\n")
            exchange_websocket = BitstampWebsocket()
            exchange_api = BitstampAPIAction(TradeBotUtils.get_bitstamp_customer_ID(),
                                             TradeBotUtils.get_bitstamp_api_key(),
                                             TradeBotUtils.get_bitstamp_api_secret())
            exchange_fee = 0.005
            minimum_interest = 0.0100755031
        else:
            print("Exchange Kraken is being used\n")
            exchange_websocket = KrakenWebsocket()
            exchange_fee = 0.0026
            minimum_interest = 0.0052203505

        TradeBotUtils.validate_args(args, minimum_interest)

        if args.is_sell:
            account_bid_price = 0
            account_ask_price = TradeBotUtils.set_initial_trade_price(exchange_websocket, args.is_sell)
        else:
            account_bid_price = TradeBotUtils.set_initial_trade_price(exchange_websocket, args.is_sell)
            account_ask_price = 0

        if args.is_reset_logs:
            TradeBotUtils.reset_logs()

        if args.is_not_simulation:
            cache = TradeBotCache(initial_value=args.initial_value,
                                  cash_value=exchange_api.get_account_cash_value(),
                                  interest=args.interest,
                                  account_bid_price=account_bid_price,
                                  account_ask_price=account_ask_price,
                                  sell_quantity=exchange_api.get_account_quantity(),
                                  exchange_fee=exchange_fee,
                                  accrued_fees=exchange_api.get_accrued_account_fees(),
                                  success_ful_trades=exchange_api.get_successful_trades(),
                                  successful_cycles=exchange_api.get_successful_cycles())

            trade_bot_runner = TradeRunner(
                is_sell=args.is_sell,
                trade_bot_buyer=LiveTradeBotBuyer(exchange_api, exchange_websocket, cache),
                trade_bot_seller=LiveTradeBotSeller(exchange_api, exchange_websocket, cache),
                run_time_minutes=args.run_time_minutes,
                print_interval=args.print_interval)
        else:
            cache = TradeBotCache(initial_value=args.initial_value,
                                  cash_value=args.initial_value,
                                  interest=args.interest,
                                  account_bid_price=account_bid_price,
                                  account_ask_price=account_ask_price,
                                  sell_quantity=args.initial_value / ((1 - exchange_fee) * (account_ask_price / (
                                          1 + args.interest))) if not account_ask_price == 0 else 0,
                                  exchange_fee=exchange_fee,
                                  accrued_fees=0,
                                  success_ful_trades=0,
                                  successful_cycles=0)

            trade_bot_runner = TradeRunner(
                is_sell=args.is_sell,
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
