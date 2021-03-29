from abc import ABC

from applications.algorithmic_trading.src.main.cache_storage.TradingCache import TradingCache
from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBot import VolatilityTradeBot
from applications.common.src.main.exchanges import ExchangeWebsocket


class VolatilityTradeBotSeller(VolatilityTradeBot, ABC):

    def __init__(self, exchange_websocket: ExchangeWebsocket, trading_output_handler: TradingOutputHandler,
                 trade_bot_cache: TradingCache):
        super().__init__(exchange_websocket, trading_output_handler, trade_bot_cache)

    def is_account_order_matching_market_order(self) -> bool:
        market_bid_price, market_bid_quantity = self.get_market_bid_order()
        return self._trade_bot_cache.account_ask_price <= market_bid_price and self._trade_bot_cache.sell_quantity <= market_bid_quantity

    def get_market_bid_order(self) -> tuple:
        market_bid_price, market_bid_quantity = self._exchange_websocket.get_market_bid_order()
        self._trade_bot_cache.market_bid_price = market_bid_price
        return market_bid_price, market_bid_quantity

    def is_buy(self) -> bool:
        return False

    def update_bid_price(self):
        self._trade_bot_cache.account_bid_price = self._trade_bot_cache.market_bid_price / (1 + self._trade_bot_cache.interest)
