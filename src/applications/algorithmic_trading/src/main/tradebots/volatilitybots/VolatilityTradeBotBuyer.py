from abc import ABC

from applications.algorithmic_trading.src.main.cache.TradingCache import trading_cache
from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBot import VolatilityTradeBot
from applications.common.src.main.exchanges import ExchangeWebsocket


class VolatilityTradeBotBuyer(VolatilityTradeBot, ABC):

    def __init__(self,
                 exchange_websocket: ExchangeWebsocket,
                 trading_output_handler: TradingOutputHandler):
        super().__init__(exchange_websocket, trading_output_handler)

    def is_account_order_matching_market_order(self) -> bool:
        market_ask_price, market_ask_quantity = self.__get_market_ask_order()
        return trading_cache.account_bid_price >= market_ask_price and trading_cache.buy_quantity <= market_ask_quantity

    def __get_market_ask_order(self) -> tuple:
        market_ask_price, market_ask_quantity = self._exchange_websocket.get_market_ask_order()
        trading_cache.market_ask_price = market_ask_price
        return market_ask_price, market_ask_quantity

    def is_buy(self) -> bool:
        return True

    def _update_ask_price(self):
        trading_cache.account_ask_price = trading_cache.market_ask_price * (1 + trading_cache.interest)
