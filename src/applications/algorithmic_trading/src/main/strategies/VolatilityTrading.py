import random
import traceback

from applications.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from applications.algorithmic_trading.src.main.config_parses.VolatilityTradingConfigParser import VolatilityTradingConfigParser
from applications.algorithmic_trading.src.main.database.DatabaseService import DatabaseService
from applications.algorithmic_trading.src.main.exchange.BitstampApiImpl import BitstampApiImpl
from applications.algorithmic_trading.src.main.exchange.BitstampWebsocket import BitstampWebsocket
from applications.algorithmic_trading.src.main.exchange.KrakenApiImpl import KrakenApiImpl
from applications.algorithmic_trading.src.main.exchange.KrakenWebsocket import KrakenWebsocket
from applications.algorithmic_trading.src.main.output_handlers.EmailHandler import EmailHandler
from applications.algorithmic_trading.src.main.output_handlers.TradeBotOutputHandler import TradeBotOutputHandler
from applications.algorithmic_trading.src.main.output_handlers.utils.PrinterUtils import PrinterUtils
from applications.algorithmic_trading.src.main.runners.VolatilityTradeRunner import VolatilityTradeRunner
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.LiveVolatilityTradeBotBuyer import LiveVolatilityTradeBotBuyer
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.LiveVolatilityTradeBotSeller import LiveVolatilityTradeBotSeller
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.SimulationVolatilityTradeBotBuyer import SimulationVolatilityTradeBotBuyer
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.SimulationVolatilityTradeBotSeller import SimulationVolatilityTradeBotSeller
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class VolatilityTrading:

    def __init__(self):
        self.__configs = VolatilityTradingConfigParser()
        self.__database_service = DatabaseService()
        self.__exchange_websocket = None
        self.__exchange_api = None
        self.__account_bid_price = 0
        self.__account_sell_price = 0
        self.__trade_bot_runner = None

    def run(self):
        try:
            self.__run_setup_tasks()
            self.__trade_bot_runner.run()
        except ValueError as error_message:
            print(error_message)
        except KeyboardInterrupt:
            print("Keyboard Interrupted")
        except Exception as error:
            print("\n--- ERROR ---")
            traceback.print_exc()
            EmailHandler().send_email_message(email_subject=f'ERROR: {self.__configs.exchange}', email_message=str(error))

    def __run_setup_tasks(self):
        self.__live_run_checker()
        self.__configs.validate_configs()
        TradeBotUtils.create_target_folder()
        self.__set_exchange_services()

        if self.__configs.is_reset_logs:
            TradeBotUtils.reset_logs(self.__configs.exchange)

        if self.__configs.init_database_from_exchange:
            self.__exchange_api.init_database_from_exchange(self.__database_service)

        self.__set_initial_trade_price()

        if self.__configs.is_live:
            self.__set_live_trade_runner()
        else:
            self.__set_simulation_runner()

    def __set_exchange_services(self):
        PrinterUtils.console_log(message=f"Exchange {self.__configs.exchange} is being used for trading {self.__configs.cash_currency}"
              f" in {self.__configs.cash_currency}")
        if self.__configs.exchange == 'bitstamp':
            self.__exchange_websocket = BitstampWebsocket(self.__configs.cash_currency, self.__configs.crypto_currency)
            self.__exchange_api = BitstampApiImpl(cash_currency=self.__configs.cash_currency,
                                                  crypto_currency=self.__configs.crypto_currency,
                                                  customer_id=TradeBotUtils.get_bitstamp_customer_id(),
                                                  api_key=TradeBotUtils.get_bitstamp_api_key(),
                                                  api_secret=TradeBotUtils.get_bitstamp_api_secret())
        else:
            self.__exchange_websocket = KrakenWebsocket(self.__configs.cash_currency, self.__configs.crypto_currency)
            self.__exchange_api = KrakenApiImpl(cash_currency=self.__configs.cash_currency,
                                                crypto_currency=self.__configs.crypto_currency,
                                                api_key=TradeBotUtils.get_kraken_api_key(),
                                                api_secret=TradeBotUtils.get_kraken_api_secret())

    def __set_initial_trade_price(self):
        is_invalid_account_trade_price = True
        while is_invalid_account_trade_price:
            market_bid_price = self.__exchange_websocket.get_market_bid_price()
            market_ask_price = self.__exchange_websocket.get_market_ask_price()
            print(f'\nMarket bid: {market_bid_price} \nMarket ask: {market_ask_price}')

            if self.__configs.is_sell:
                account_trade_price = float(input('Set start account ASK price: '))
                self.__account_bid_price = 0
                self.__account_ask_price = account_trade_price
                is_invalid_account_trade_price = market_bid_price - account_trade_price > 0
                if is_invalid_account_trade_price:
                    PrinterUtils.console_log(message="ERROR: Account ask price has to be larger than market bid price.")
                else:
                    PrinterUtils.console_log(message=f"Account Ask Price: {account_trade_price}")

            else:
                account_trade_price = float(input('Set start account BID price: '))
                self.__account_bid_price = account_trade_price
                self.__account_ask_price = 0
                is_invalid_account_trade_price = market_ask_price - account_trade_price < 0
                if is_invalid_account_trade_price:
                    PrinterUtils.console_log(message="ERROR: Account bid price has to be smaller than market ask price.")
                else:
                    PrinterUtils.console_log(message=f"Account Bid Price: {account_trade_price}")

    def __set_simulation_runner(self):
        initial_value = 100
        cache = TradeBotCache(initial_value=initial_value,
                              cash_value=initial_value,
                              interest=self.__configs.interest,
                              account_bid_price=self.__account_bid_price,
                              account_ask_price=self.__account_ask_price,
                              sell_quantity=initial_value / (
                                      (1 - TradeBotUtils.get_exchange_fee(self.__configs.exchange)) * (
                                      self.__account_ask_price / (1 + self.__configs.interest)))
                              if not self.__account_ask_price == 0 else 0,
                              exchange_fee=TradeBotUtils.get_exchange_fee(self.__configs.exchange),
                              accrued_fees=0,
                              success_ful_trades=0,
                              successful_cycles=0)

        trade_bot_output_handler = TradeBotOutputHandler(self.__configs.is_live, self.__configs.exchange, cache,
                                                         self.__database_service, self.__configs.cash_currency, self.__configs.crypto_currency)

        self.__trade_bot_runner = VolatilityTradeRunner(is_sell=self.__configs.is_sell,
                                                        trade_bot_buyer=SimulationVolatilityTradeBotBuyer(self.__exchange_websocket,
                                                                                                          trade_bot_output_handler,
                                                                                                          cache),
                                                        trade_bot_seller=SimulationVolatilityTradeBotSeller(self.__exchange_websocket,
                                                                                                            trade_bot_output_handler,
                                                                                                            cache),
                                                        run_time_minutes=self.__configs.run_time_minutes,
                                                        print_interval=self.__configs.print_interval)

    def __set_live_trade_runner(self):
        if self.__configs.override_initial_value:
            self.__database_service.insert_or_update_initial_account_value(self.__configs.exchange, self.__configs.override_initial_value,
                                                                           self.__configs.cash_currency)

        initial_value = self.__database_service.get_initial_account_value(self.__configs.exchange, self.__configs.cash_currency)
        if initial_value == 0:
            initial_value = self.__exchange_api.get_account_cash_value() + \
                            (self.__exchange_api.get_account_quantity() * self.__exchange_websocket.get_market_bid_price()) * (
                                    1 - TradeBotUtils.get_exchange_fee(self.__configs.exchange))
            self.__database_service.insert_or_update_initial_account_value(self.__configs.exchange, initial_value, self.__configs.cash_currency)

        cache = TradeBotCache(initial_value=initial_value,
                              cash_value=self.__exchange_api.get_account_cash_value(),
                              interest=self.__configs.interest,
                              account_bid_price=self.__account_bid_price,
                              account_ask_price=self.__account_ask_price,
                              sell_quantity=self.__exchange_api.get_account_quantity(),
                              exchange_fee=TradeBotUtils.get_exchange_fee(self.__configs.exchange),
                              accrued_fees=self.__database_service.get_accrued_account_fees(self.__configs.exchange, self.__configs.cash_currency,
                                                                                            self.__configs.is_live),
                              success_ful_trades=self.__database_service.get_nr_successful_trades(self.__configs.exchange,
                                                                                                  self.__configs.is_live),
                              successful_cycles=self.__database_service.get_nr_successful_cycles(self.__configs.exchange,
                                                                                                 self.__configs.is_live))

        trade_bot_output_handler = TradeBotOutputHandler(self.__configs.is_live, self.__configs.exchange, cache,
                                                         self.__database_service, self.__configs.cash_currency, self.__configs.crypto_currency)

        self.__trade_bot_runner = VolatilityTradeRunner(is_sell=self.__configs.is_sell,
                                                        trade_bot_buyer=LiveVolatilityTradeBotBuyer(self.__exchange_api, self.__exchange_websocket,
                                                                                                    trade_bot_output_handler, cache),
                                                        trade_bot_seller=LiveVolatilityTradeBotSeller(self.__exchange_api, self.__exchange_websocket,
                                                                                                      trade_bot_output_handler, cache),
                                                        run_time_minutes=self.__configs.run_time_minutes,
                                                        print_interval=self.__configs.print_interval)

    def __live_run_checker(self):
        if self.__configs.is_live:
            contract_pin = random.randint(10000, 99999)
            signature = int(input(f"\nWARNING LIVE RUN. If you want to trade sign the contract by entering: {contract_pin}: "))
            if signature != int(contract_pin):
                PrinterUtils.console_log(message="ABORTING")
                exit()
            else:
                PrinterUtils.console_log(message="Contracted signed! Live run accepted!")
