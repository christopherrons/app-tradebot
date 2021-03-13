import time
from datetime import datetime

from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.exchange.ExchangeApi import ExchangeApi
from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket
from services.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotBuyer import \
    VolatilityTradeBotBuyer


class LiveVolatilityTradeBotBuyer(VolatilityTradeBotBuyer):
    def __init__(self,
                 exchange_api: ExchangeApi,
                 exchange_websocket: ExchangeWebsocket,
                 trade_bot_cache: TradeBotCache):
        super().__init__(exchange_websocket, trade_bot_cache)
        self.__exchange_api = exchange_api

    def execute_order(self) -> str:
        return self.__exchange_api.execute_buy_order(self._trade_bot_cache.market_ask_price,
                                                     self._trade_bot_cache.buy_quantity)

    def is_order_executed(self, order_id: str) -> bool:
        while self.__is_order_status_open(order_id):
            print(f"Order id {order_id} is still open")
            time.sleep(10)

        if self.__is_order_executed(order_id):
            return True
        else:
            print(f'\n--- {datetime.now()} - Order: {order_id} was not executed! \n')
            return False

    def run_post_trade_batch(self, order_id: str):
        self.update_cache(order_id)
        self.create_visual_trade_report()
        self.email_trade_reports()

    def update_cache(self, order_id: str):
        self._trade_bot_cache.increment_successful_trades()
        fee = self.__exchange_api.get_transaction_fee(order_id)
        self._trade_bot_cache.accrued_fee = fee
        self.print_successful_trade(self.is_buy(), fee)
        self._trade_bot_cache.sell_quantity = self.__exchange_api.get_account_quantity()
        self._trade_bot_cache.cash_value = self.__exchange_api.get_account_cash_value()
        self.update_ask_price()

    def __is_order_executed(self, order_id: str) -> bool:
        return self.__exchange_api.is_order_successful(order_id)

    def __is_order_status_open(self, order_id: str) -> bool:
        return self.__exchange_api.is_order_status_open(order_id)
