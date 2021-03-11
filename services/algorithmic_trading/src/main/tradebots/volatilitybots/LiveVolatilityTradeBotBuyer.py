import time
from datetime import datetime

from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.exchange.ExchangeApi import ExchangeApi
from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket
from services.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotBuyer import VolatilityTradeBotBuyer


class LiveVolatilityTradeBotBuyer(VolatilityTradeBotBuyer):
    def __init__(self,
                 exchange_api: ExchangeApi,
                 exchange_websocket: ExchangeWebsocket,
                 trade_bot_cache: TradeBotCache):
        super().__init__(exchange_websocket, trade_bot_cache)
        self.__exchange_api = exchange_api

    def create_trade(self) -> str:
        return self.trade_action_buy()

    def trade_action_buy(self) -> str:
        return self.__exchange_api.buy_action(self._trade_bot_cache.market_ask_price,
                                              self._trade_bot_cache.buy_quantity)

    def is_trade_successful(self, order_id: str) -> bool:
        while self.__is_order_status_open(order_id):
            print(f"Order id {order_id} is still open")
            time.sleep(10)

        if self.__is_order_successful(order_id):
            return True
        else:
            print(f'\n--- {datetime.now()} - Order: {order_id} was not successful! \n')
            return False

    def update_cache(self, order_id: str):
        self._trade_bot_cache.increment_successful_trades()
        fee = self.__exchange_api.get_transaction_fee(order_id)
        self._trade_bot_cache.accrued_fee = fee
        self.print_successful_trades(self.is_buy(), fee)
        self._trade_bot_cache.sell_quantity = self.__exchange_api.get_account_quantity()
        self._trade_bot_cache.cash_value = self.__exchange_api.get_account_cash_value()
        self.update_ask_price()

    def __is_order_successful(self, order_id: str) -> bool:
        return self.__exchange_api.is_order_successful(order_id)

    def __is_order_status_open(self, order_id: str) -> bool:
        return self.__exchange_api.is_order_status_open(order_id)
