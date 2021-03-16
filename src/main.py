#!/usr/bin/env python3.6
# ------------------------------------------------------------------------------
# Crypto Trading Bot
#
# (C) 2021 Christopher Herron, Thomas Brunner
# email: christopherherron09@gmail.com, tbrunner@kth.se
#
# ------------------------------------------------------------------------------
# TODO: Clean up code
# TODO: Add kraken api and make api calls possible for both kraken and bitstamp
# TODO: If possible trigger evant based on websocket rather than other way around
# TODO: Trade in EUR or USD? Check which market is the most liquid
# TODO: Consider order could not be placed error from bitstamp
# TODO: Consider websocket connection loss error
# TODO: Clean up main file, how do we deal with if we add another tradebot (e.g. arbitrage)
# TODO: Docker container

# Nice to
# TODO: Optimize with threading
# TODO: Add relevant visualisations
# TODO: Strategy for start price
# TODO: Find smart way to set initial value other than memorizing

import sys
import traceback
from argparse import ArgumentParser

from application.algorithmic_trading.src.main.runners.VolatilityTradeRunner import VolatilityTradeRunner
from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.database.DatabaseService import DatabaseService
from services.algorithmic_trading.src.main.exchange.BitstampApiImpl import BitstampApiImpl
from services.algorithmic_trading.src.main.exchange.BitstampWebsocket import BitstampWebsocket
from services.algorithmic_trading.src.main.exchange.KrakenApiImpl import KrakenApiImpl
from services.algorithmic_trading.src.main.exchange.KrakenWebsocket import KrakenWebsocket
from services.algorithmic_trading.src.main.output_handlers.EmailHandler import EmailHandler
from services.algorithmic_trading.src.main.output_handlers.TradeBotOutputHandler import TradeBotOutputHandler
from services.algorithmic_trading.src.main.tradebots.volatilitybots.LiveVolatilityTradeBotBuyer import \
    LiveVolatilityTradeBotBuyer
from services.algorithmic_trading.src.main.tradebots.volatilitybots.LiveVolatilityTradeBotSeller import \
    LiveVolatilityTradeBotSeller
from services.algorithmic_trading.src.main.tradebots.volatilitybots.SimulationVolatilityTradeBotBuyer import \
    SimulationVolatilityTradeBotBuyer
from services.algorithmic_trading.src.main.tradebots.volatilitybots.SimulationVolatilityTradeBotSeller import \
    SimulationVolatilityTradeBotSeller
from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


def main(argv):
    arg_parser = ArgumentParser(description='Run a crypto trading bot with the bitstamp api.',
                                formatter_class=TradeBotUtils.CustomFormatter,
                                epilog='(C) 2021 \nAuthors: Christopher Herron and Thomas Brunner \nEmails: christopherherron09@gmail.com and tbrunner@kth.se')
    arg_parser.add_argument('initial_value', help='Specify the amount of cash that was invested from the beginning [$]', type=float) # TODO need to be converted to eur if required
    arg_parser.add_argument('exchange', choices=('Bitstamp', 'Kraken'), help='Choose exchange', type=str)
    arg_parser.add_argument('cash_currency', choices=('USD', 'EUR'), help='Choose Cash Currency', type=str)
    arg_parser.add_argument('crypto_currency', choices=('XRP'), help='Choose CryptoCurrency', type=str)
    arg_parser.add_argument('--is_sell', help='Specify if buy or sell', default=False, action='store_true')
    arg_parser.add_argument('--interest', default=0.015, help='Specify the interest gain [%%]', type=float)
    arg_parser.add_argument('--run_time_minutes', default=1000000, help='Specify the number of minutes the bot runs [min]', type=int)
    arg_parser.add_argument('--is_not_simulation', help='Flag if the trading is not simulated based on the trading strategy', default=False,
                            action='store_true')
    arg_parser.add_argument('--is_reset_logs', help='Flag to reset logs at start of run', default=False, action='store_true')
    arg_parser.add_argument('--print_interval', default=1, help='Specify the interval for current information data printing and logging [min]',
                            type=float)
    arg_parser.add_argument('--init_database_from_exchange',
                            help='Initialize the database with data from the exchange. Should only be required once. per exchange.', default=False,
                            action='store_true')
    args = arg_parser.parse_args()

    try:

        TradeBotUtils.live_run_checker(args.is_not_simulation)

        database_service = DatabaseService()
        database_service.create_tables_if_not_exist()

        print(f"Exchange {args.exchange} is being used for trading"
              f" {args.crypto_currency.upper()} in {args.cash_currency.upper()}\n")
        if args.exchange == 'Bitstamp':
            exchange_websocket = BitstampWebsocket(args.cash_currency, args.crypto_currency)
            exchange_api = BitstampApiImpl(cash_currency=args.cash_currency,
                                           crypto_currency=args.crypto_currency,
                                           customer_id=TradeBotUtils.get_bitstamp_customer_id(),
                                           api_key=TradeBotUtils.get_bitstamp_api_key(),
                                           api_secret=TradeBotUtils.get_bitstamp_api_secret())
            if args.init_database_from_exchange:
                print(f"Initializing Database from {args.exchange}!")
                trade_nr = 0
                for transaction in reversed(exchange_api.get_transactions()):
                    if transaction['type'] == '2':
                        database_service.insert_trade_report(order_id=transaction['order_id'],
                                                             is_simulation=False, exchange='bitstamp',
                                                             timestamp=exchange_api.get_transaction_timestamp(transaction),
                                                             trade_number=trade_nr + 1,
                                                             buy=exchange_api.is_transaction_buy(transaction),
                                                             cash_currency=exchange_api.get_transaction_cash_currency(transaction),
                                                             crypto_currency=exchange_api.get_transaction_crypto_currency(transaction),
                                                             fee=exchange_api.get_transaction_fee_from_transaction_dict(transaction),
                                                             price=exchange_api.get_transaction_price_per_quantity(transaction),
                                                             quantity=exchange_api.get_transaction_quantity(transaction),
                                                             gross_trade_value=exchange_api.get_transaction_gross_value(transaction),
                                                             net_trade_value=exchange_api.get_transaction_net_value(transaction))
                        trade_nr += 1

            exchange_fee = 0.005
            minimum_interest = 0.0100755031

        else:
            exchange_websocket = KrakenWebsocket(args.cash_currency, args.crypto_currency)
            exchange_api = KrakenApiImpl(cash_currency=args.cash_currency,
                                         crypto_currency=args.crypto_currency,
                                         api_key=TradeBotUtils.get_kraken_api_key(),
                                         api_secret=TradeBotUtils.get_kraken_api_secret())

            if args.init_database_from_exchange:
                print(f"Initializing Database from {args.exchange}!")
                closed_transactions = exchange_api.get_transactions()['closed']
                for idx, order_id in enumerate(closed_transactions.keys()):
                    database_service.insert_trade_report(order_id=order_id,
                                                         is_simulation=False, exchange='kraken',
                                                         timestamp=exchange_api.get_transaction_timestamp(closed_transactions[order_id]),
                                                         trade_number=idx + 1,
                                                         buy=exchange_api.is_transaction_buy(closed_transactions[order_id]),
                                                         cash_currency=exchange_api.get_transaction_cash_currency(closed_transactions[order_id]),
                                                         crypto_currency=exchange_api.get_transaction_crypto_currency(closed_transactions[order_id]),
                                                         fee=exchange_api.get_transaction_fee_from_transaction_dict(closed_transactions[order_id]),
                                                         price=exchange_api.get_transaction_price_per_quantity(closed_transactions[order_id]),
                                                         quantity=exchange_api.get_transaction_quantity(closed_transactions[order_id]),
                                                         gross_trade_value=exchange_api.get_transaction_gross_value(closed_transactions[order_id]),
                                                         net_trade_value=exchange_api.get_transaction_net_value(closed_transactions[order_id]))

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
            TradeBotUtils.reset_logs(args.exchange)

        if args.is_not_simulation:
            cache = TradeBotCache(initial_value=args.initial_value,
                                  cash_value=exchange_api.get_account_cash_value(),
                                  interest=args.interest,
                                  account_bid_price=account_bid_price,
                                  account_ask_price=account_ask_price,
                                  sell_quantity=exchange_api.get_account_quantity(),
                                  exchange_fee=exchange_fee,
                                  accrued_fees=database_service.get_accrued_account_fees(args.exchange, args.cash_currency, not args.is_not_simulation),
                                  success_ful_trades=database_service.get_nr_successful_trades(args.exchange, not args.is_not_simulation),
                                  successful_cycles=database_service.get_nr_successful_cycles(args.exchange, not args.is_not_simulation))

            trade_bot_output_handler = TradeBotOutputHandler(not args.is_not_simulation, args.exchange, cache,
                                                             database_service, args.cash_currency,
                                                             args.crypto_currency)

            trade_bot_runner = VolatilityTradeRunner(is_sell=args.is_sell,
                                                     trade_bot_buyer=LiveVolatilityTradeBotBuyer(exchange_api,
                                                                                                 exchange_websocket,
                                                                                                 trade_bot_output_handler,
                                                                                                 cache),
                                                     trade_bot_seller=LiveVolatilityTradeBotSeller(exchange_api,
                                                                                                   exchange_websocket,
                                                                                                   trade_bot_output_handler,
                                                                                                   cache),
                                                     run_time_minutes=args.run_time_minutes,
                                                     print_interval=args.print_interval)
        else:
            initial_value = 100
            cache = TradeBotCache(initial_value=initial_value,
                                  cash_value=args.initial_value,
                                  interest=args.interest,
                                  account_bid_price=account_bid_price,
                                  account_ask_price=account_ask_price,
                                  sell_quantity=initial_value / ((1 - exchange_fee) * (account_ask_price / (1 + args.interest)))
                                  if not account_ask_price == 0 else 0,
                                  exchange_fee=exchange_fee,
                                  accrued_fees=0,
                                  success_ful_trades=0,
                                  successful_cycles=0)
            trade_bot_output_handler = TradeBotOutputHandler(not args.is_not_simulation, args.exchange, cache,
                                                             database_service, args.cash_currency,
                                                             args.crypto_currency)

            trade_bot_runner = VolatilityTradeRunner(is_sell=args.is_sell,
                                                     trade_bot_buyer=SimulationVolatilityTradeBotBuyer(
                                                         exchange_websocket, trade_bot_output_handler, cache),
                                                     trade_bot_seller=SimulationVolatilityTradeBotSeller(
                                                         exchange_websocket, trade_bot_output_handler, cache),
                                                     run_time_minutes=args.run_time_minutes,
                                                     print_interval=args.print_interval)

        trade_bot_runner.run()

    except ValueError as error_message:
        print(error_message)
    except KeyboardInterrupt:
        print("Keyboard Interrupted")
    except Exception as error:
        print("\n--- ERROR ---")
        traceback.print_exc()
        EmailHandler().send_email_message(email_subject=args.exchange,
                                          email_message=str(error))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
