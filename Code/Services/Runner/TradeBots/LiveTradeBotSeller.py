import time
from datetime import datetime

from Services.Runner.TradeBots.TradeBotSeller import TradeBotSeller


class LiveTradeBotSeller(TradeBotSeller):

    def __init__(self,
                 exchange_api,
                 exchange_websocket,
                 trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)
        self.__exchange_api = exchange_api

    def create_trade(self):
        sell_order_id = self.trade_action_sell()

        while self.is_order_status_open(sell_order_id):
            print(f"Order id {sell_order_id} is still open")
            time.sleep(10)

        if self.is_order_successful(sell_order_id):
            self._trade_bot_cache.increment_successful_trades()
            self._trade_bot_cache.increment_successful_cycles()
            fee = self.__exchange_api.get_transaction_fee(sell_order_id)
            self._trade_bot_cache.accrued_fee = fee
            self.print_and_log_successful_trades(self.is_buy(), fee)
            self.update_account_quantity_values()
            self.update_bid_price()
            self.send_email()
            return True
        else:
            print(f'\n--- {datetime.now()} - Order: {sell_order_id} was not successful! \n')
            return False

    def trade_action_sell(self):
        return self.__exchange_api.sell_action(self._trade_bot_cache.market_bid_price,
                                               self._trade_bot_cache.sell_quantity)

    def update_account_quantity_values(self):
        self._trade_bot_cache.sell_quantity = self.__exchange_api.get_account_quantity()
        self._trade_bot_cache.cash_value = self.__exchange_api.get_account_cash_value()

    def is_order_successful(self, order_id):
        return self.__exchange_api.is_order_successful(order_id)

    def is_order_status_open(self, order_id):
        return self.__exchange_api.is_order_status_open(order_id)
