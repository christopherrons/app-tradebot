from applications.algorithmic_trading.src.main.builders.VolatilityTradeRunnerBuilder import VolatilityTradeRunnerBuilder
from applications.algorithmic_trading.src.main.cache.TradingCache import trading_cache
from applications.algorithmic_trading.src.main.config_parses.VolatilityTradingConfigParser import VolatilityTradingConfigParser
from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.algorithmic_trading.src.main.runners.VolatilityTradeRunner import VolatilityTradeRunner
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.LiveVolatilityTradeBotBuyer import LiveVolatilityTradeBotBuyer
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.LiveVolatilityTradeBotSeller import LiveVolatilityTradeBotSeller
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.database.TradeDataDao import TradeDataDao
from applications.common.src.main.exchanges.BitstampApi import BitstampApi
from applications.common.src.main.exchanges.ExchangeApi import ExchangeApi
from applications.common.src.main.exchanges.ExchangeWebsocket import ExchangeWebsocket
from applications.common.src.main.exchanges.KrakenApi import KrakenApi
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class LiveVolatilityTradeRunnerBuilder(VolatilityTradeRunnerBuilder):
    def __init__(self, configs: VolatilityTradingConfigParser, database_service: TradeDataDao):
        super().__init__(configs, database_service)

    def build(self) -> VolatilityTradeRunner:
        exchange_websocket = self._get_exchange_websocket()
        exchange_api = self.__get_exchange_api()
        initial_value = self.__get_initial_value(exchange_websocket, exchange_api)
        account_ask_price = self._get_initial_ask_price(exchange_websocket)
        account_bid_price = self._get_initial_bid_price(exchange_websocket)
        self.__init_cache(initial_value, exchange_api, account_bid_price, account_ask_price)
        trading_output_handler = self._get_tradebot_output_handler()
        return self.__get_tradebot_runner(exchange_api, trading_output_handler, exchange_websocket)

    def __get_exchange_api(self) -> ExchangeApi:
        PrinterUtils.console_log(message=f"Exchange {self._configs.exchange} Api is being used for trading {self._configs.crypto_currency}"
                                         f" in {self._configs.cash_currency} with interest: {self._configs.interest * 100}%")

        if self._configs.exchange == 'bitstamp':
            exchange_api = BitstampApi(cash_currency=self._configs.cash_currency,
                                       crypto_currency=self._configs.crypto_currency,
                                       customer_id=TradeBotUtils.get_bitstamp_customer_id(),
                                       api_key=TradeBotUtils.get_bitstamp_api_key(),
                                       api_secret=TradeBotUtils.get_bitstamp_api_secret())
        else:
            exchange_api = KrakenApi(cash_currency=self._configs.cash_currency,
                                     crypto_currency=self._configs.crypto_currency,
                                     api_key=TradeBotUtils.get_kraken_api_key(),
                                     api_secret=TradeBotUtils.get_kraken_api_secret())

        if self._configs.init_database_from_exchange:
            exchange_api.init_trades_to_database_from_exchange(database_service=self._database_service)

        return exchange_api

    def __get_initial_value(self, exchange_websocket: ExchangeWebsocket, exchange_api: ExchangeApi) -> float:
        if self._configs.override_initial_value:
            self._database_service.insert_or_update_initial_account_value(self._configs.exchange, self._configs.is_live,
                                                                          self._configs.override_initial_value, self._configs.cash_currency)
            return self._configs.override_initial_value

        initial_value = self._database_service.get_initial_account_value(self._configs.exchange, self._configs.is_live,
                                                                         self._configs.cash_currency)
        if initial_value == 0:
            initial_value = exchange_api.get_account_cash_value() + (
                    exchange_api.get_account_quantity() * exchange_websocket.get_market_bid_price()) * (
                                    1 - TradeBotUtils.get_exchange_fee(self._configs.exchange))

            self._database_service.insert_or_update_initial_account_value(self._configs.exchange, self._configs.is_live, initial_value,
                                                                          self._configs.cash_currency)
        return initial_value

    def __init_cache(self, initial_value: float, exchange_api: ExchangeApi, account_bid_price: float, account_ask_price: float):
        trading_cache.initial_value = initial_value
        trading_cache.cash_value = exchange_api.get_account_cash_value()
        trading_cache.interest = self._configs.interest
        trading_cache.account_bid_price = account_bid_price
        trading_cache.account_ask_price = account_ask_price
        trading_cache.sell_quantity = exchange_api.get_account_quantity()
        trading_cache.exchange_fee = TradeBotUtils.get_exchange_fee(self._configs.exchange)
        trading_cache.accrued_fee = self._database_service.get_accrued_account_fees(self._configs.exchange, self._configs.cash_currency,
                                                                                    self._configs.crypto_currency, self._configs.is_live)
        trading_cache.successful_trades = self._database_service.get_nr_successful_trades(self._configs.exchange, self._configs.crypto_currency,
                                                                                          self._configs.is_live)
        trading_cache.successful_cycles = self._database_service.get_nr_successful_cycles(self._configs.exchange, self._configs.crypto_currency,
                                                                                          self._configs.is_live)

    def __get_tradebot_runner(self, exchange_api: ExchangeApi, trading_output_handler: TradingOutputHandler,
                              exchange_websocket: ExchangeWebsocket) -> VolatilityTradeRunner:
        return VolatilityTradeRunner(is_sell=self._configs.is_sell,
                                     trade_bot_buyer=LiveVolatilityTradeBotBuyer(exchange_api, exchange_websocket, trading_output_handler),
                                     trade_bot_seller=LiveVolatilityTradeBotSeller(exchange_api, exchange_websocket, trading_output_handler),
                                     run_time_minutes=self._configs.run_time_minutes,
                                     print_interval=self._configs.print_interval)
