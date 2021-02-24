from Services.Runner.TradeBots.TradeBotKing import TradeBotKing


class TradeBotBuyer(TradeBotKing):

    def __init__(self,
                 exchange_websocket,
                 trade_bot_cache):
        self._exchange_websocket = exchange_websocket
        super().__init__(trade_bot_cache)

    def is_trade_able(self):
        market_ask_price, market_ask_quantity = self.get_market_ask_price()
        return self._trade_bot_cache.account_bid_price >= market_ask_price and self._trade_bot_cache.buy_quantity <= market_ask_quantity

    def get_market_ask_price(self):
        market_ask_price, market_ask_quantity = self._exchange_websocket.get_market_ask_price_and_quantity()
        self._trade_bot_cache.market_ask_price = market_ask_price
        return market_ask_price, market_ask_quantity

    def is_buy(self):
        return True

    def update_ask_price(self):
        self._trade_bot_cache._account_ask_price = self._trade_bot_cache.market_bid_price * (
                1 + self._trade_bot_cache.interest)
