from applications.algorithmic_trading.src.main.cache_storage.TradingCache import TradingCache
from applications.algorithmic_trading.src.main.config_parses.VolatilityTradingConfigParser import VolatilityTradingConfigParser
from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.common.src.main.database.TradeDataDao import TradeDataDao
from applications.common.src.main.exchanges.BitstampWebsocket import BitstampWebsocket
from applications.common.src.main.exchanges.ExchangeWebsocket import ExchangeWebsocket
from applications.common.src.main.exchanges.KrakenWebsocket import KrakenWebsocket
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class VolatilityTradeRunnerBuilder:
    def __init__(self, configs: VolatilityTradingConfigParser, database_service: TradeDataDao):
        self._configs = configs
        self._database_service = database_service

    def get_exchange_websocket(self) -> ExchangeWebsocket:
        PrinterUtils.console_log(message=f"Exchange {self._configs.exchange} WebSocket is being used for trading {self._configs.crypto_currency}"
                                         f" in {self._configs.cash_currency}")
        if self._configs.exchange == 'bitstamp':
            return BitstampWebsocket(self._configs.cash_currency, self._configs.crypto_currency)
        else:
            return KrakenWebsocket(self._configs.cash_currency, self._configs.crypto_currency)

    def get_initial_ask_price(self, exchange_websocket: ExchangeWebsocket) -> float:
        if not self._configs.is_sell:
            return 0

        is_invalid_account_ask_price = True
        account_ask_price = 0
        while is_invalid_account_ask_price:
            market_bid_price = exchange_websocket.get_market_bid_price()
            market_ask_price = exchange_websocket.get_market_ask_price()
            print(f'\nMarket bid: {market_bid_price} \nMarket ask: {market_ask_price}')

            account_ask_price = float(input('Set start account ASK price: '))
            is_invalid_account_ask_price = market_bid_price - account_ask_price > 0
            if is_invalid_account_ask_price:
                PrinterUtils.console_log(message="ERROR: Account ask price has to be larger than market bid price.")
            else:
                PrinterUtils.console_log(message=f"Account Ask Price: {account_ask_price}")

        return account_ask_price

    def get_initial_bid_price(self, exchange_websocket: ExchangeWebsocket) -> float:
        if self._configs.is_sell:
            return 0

        is_invalid_account_bid_price = True
        account_bid_price = 0
        while is_invalid_account_bid_price:
            market_bid_price = exchange_websocket.get_market_bid_order()
            market_ask_price = exchange_websocket.get_market_ask_price()
            print(f'\nMarket bid: {market_bid_price} \nMarket ask: {market_ask_price}')

            account_bid_price = float(input('Set start account BID price: '))
            is_invalid_account_bid_price = market_ask_price - account_bid_price < 0
            if is_invalid_account_bid_price:
                PrinterUtils.console_log(message="ERROR: Account bid price has to be smaller than market ask price.")
            else:
                PrinterUtils.console_log(message=f"Account Bid Price: {account_bid_price}")

        return account_bid_price

    def get_tradebot_output_handler(self, trading_cache: TradingCache) -> TradingOutputHandler:
        return TradingOutputHandler(self._configs.is_live, self._configs.exchange, trading_cache, self._database_service, self._configs.cash_currency,
                                    self._configs.crypto_currency)
