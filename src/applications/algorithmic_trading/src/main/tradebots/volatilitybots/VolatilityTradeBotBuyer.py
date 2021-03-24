from abc import ABC

from applications.algorithmic_trading.src.main.cache_storage.TradingCache import TradingCache
from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBot import VolatilityTradeBot
from applications.common.src.main.exchanges import ExchangeWebsocket


class VolatilityTradeBotBuyer(VolatilityTradeBot, ABC):

    def __init__(self,
                 exchange_websocket: ExchangeWebsocket,
                 trading_output_handler: TradingOutputHandler,
                 trade_bot_cache: TradingCache):
        super().__init__(exchange_websocket, trading_output_handler, trade_bot_cache)

    def is_account_price_matching_market_price(self) -> bool:
        market_ask_price = self.get_market_ask_price()
        market_ask_quantity = self._exchange_websocket.get_market_ask_quantity()
        return self._trade_bot_cache.account_bid_price >= market_ask_price and self._trade_bot_cache.buy_quantity <= market_ask_quantity

    def get_market_ask_price(self) -> float:
        market_ask_price = self._exchange_websocket.get_market_ask_price()
        self._trade_bot_cache.market_ask_price = market_ask_price
        return market_ask_price

    def is_buy(self) -> bool:
        return True

    def update_ask_price(self):
        self._trade_bot_cache.account_ask_price = self._trade_bot_cache.market_ask_price * (1 + self._trade_bot_cache.interest)
