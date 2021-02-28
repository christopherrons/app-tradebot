from Services.Runner.TradeBots.TradeBotKing import TradeBotKing


class TradeBotSeller(TradeBotKing):

    def __init__(self,
                 exchange_websocket,
                 trade_bot_cache):
        self._exchange_websocket = exchange_websocket
        super().__init__(trade_bot_cache)

    def is_trade_able(self):
        market_bid_price, market_bid_quantity = self.get_market_bid_price()
        return self._trade_bot_cache.account_ask_price <= market_bid_price and \
               self._trade_bot_cache.sell_quantity <= market_bid_quantity

    def get_market_bid_price(self):
        market_bid_price, market_bid_quantity = self._exchange_websocket.get_market_bid_price_and_quantity()
        self._trade_bot_cache.market_bid_price = market_bid_price
        return market_bid_price, market_bid_quantity

    def is_buy(self):
        return False

    def update_bid_price(self):
        self._trade_bot_cache.account_bid_price = self._trade_bot_cache.market_bid_price / (
                1 + self._trade_bot_cache.interest)
