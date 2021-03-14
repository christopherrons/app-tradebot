from abc import ABC, abstractmethod

from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket
from services.algorithmic_trading.src.main.output_handlers.TradeBotOutputHandler import TradeBotOutputHandler


class VolatilityTradeBot(ABC):
    def __init__(self,
                 exchange_websocket: ExchangeWebsocket,
                 trade_out_put_handler: TradeBotOutputHandler,
                 trade_bot_cache: TradeBotCache):
        self._exchange_websocket = exchange_websocket
        self.__trade_bot_output_handler = trade_out_put_handler
        self._trade_bot_cache = trade_bot_cache

    @abstractmethod
    def is_buy(self) -> bool: pass

    @abstractmethod
    def is_account_price_matching_market_price(self) -> bool: pass

    @abstractmethod
    def execute_order(self) -> str: pass

    @abstractmethod
    def is_order_executed(self, order_id: str) -> bool: pass

    @abstractmethod
    def update_cache(self, order_id: str): pass

    @abstractmethod
    def run_post_trade_batch(self, order_id: str): pass

    def print_trading_formation(self, is_buy: bool):
        self.__trade_bot_output_handler.print_trading_formation(is_buy)

    def print_and_store_trade_report(self, is_buy: bool, fee: float):
        self.__trade_bot_output_handler.print_and_store_trade_report(is_buy, fee)

    def email_trade_reports(self):
        self.__trade_bot_output_handler.email_trade_reports()

    def create_visual_trade_report(self):
        self.__trade_bot_output_handler.create_visual_trade_report()
