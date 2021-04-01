from abc import ABC, abstractmethod

from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.common.src.main.exchanges import ExchangeWebsocket


class VolatilityTradeBot(ABC):
    def __init__(self, exchange_websocket: ExchangeWebsocket,
                 trade_out_put_handler: TradingOutputHandler):
        self._exchange_websocket = exchange_websocket
        self.__trading_output_handler = trade_out_put_handler

    @abstractmethod
    def is_buy(self) -> bool: pass

    @abstractmethod
    def is_account_order_matching_market_order(self) -> bool: pass

    @abstractmethod
    def execute_order(self) -> str: pass

    @abstractmethod
    def is_order_executed(self, order_id: str) -> bool: pass

    @abstractmethod
    def update_cache(self, order_id: str, fee: float): pass

    @abstractmethod
    def run_post_trade_tasks(self, order_id: str): pass

    def reconnect_websocket(self):
        self._exchange_websocket.reconnect()

    def print_trading_data(self, is_buy: bool):
        self.__trading_output_handler.print_trading_data(is_buy)

    def print_and_store_trade_report(self, is_buy: bool, fee: float, order_id: str):
        self.__trading_output_handler.print_and_store_trade_report(is_buy, fee, order_id)

    def email_trade_reports(self):
        self.__trading_output_handler.email_trade_reports()

    def create_visual_trade_report(self):
        self.__trading_output_handler.create_visual_trade_report()
