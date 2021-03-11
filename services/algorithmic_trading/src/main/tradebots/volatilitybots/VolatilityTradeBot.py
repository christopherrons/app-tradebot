from abc import ABC, abstractmethod

from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.data_output_handler.TradeBotOutput import TradeBotOutput
from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket


class VolatilityTradeBot(ABC):
    def __init__(self,
                 exchange_websocket: ExchangeWebsocket,
                 trade_bot_cache: TradeBotCache):
        self._exchange_websocket = exchange_websocket
        self._trade_bot_cache = trade_bot_cache
        self._trade_bot_output = TradeBotOutput(exchange_websocket.exchange_name,
                                                self._trade_bot_cache,
                                                exchange_websocket.cash_currency,
                                                exchange_websocket.crypto_currency)

    @abstractmethod
    def is_buy(self) -> bool: pass

    @abstractmethod
    def is_trade_able(self) -> bool: pass

    @abstractmethod
    def create_trade(self) -> str: pass

    @abstractmethod
    def is_trade_successful(self, order_id: str) -> bool: pass

    @abstractmethod
    def update_cache(self, order_id: str): pass

    def print_trading_formation(self, is_buy: bool):
        self._trade_bot_output.print_trading_formation(is_buy)

    def print_successful_trades(self, is_buy: bool, fee: float):
        self._trade_bot_output.print_successful_trades(is_buy, fee)

    def send_email_with_successful_trade(self):
        self._trade_bot_output.send_email_with_successful_trade()
