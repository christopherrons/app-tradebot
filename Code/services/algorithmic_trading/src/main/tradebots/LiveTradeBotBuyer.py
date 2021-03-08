import time
from datetime import datetime

from services.algorithmic_trading.src.main.tradebots.TradeBotBuyer import TradeBotBuyer


class LiveTradeBotBuyer(TradeBotBuyer):

    def __init__(self,
                 exchange_api,
                 exchange_websocket,
                 trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)
        self.__exchange_api = exchange_api

    def create_trade(self):
        buy_action_id = self.trade_action_buy()

        while self.is_order_status_open(buy_action_id):
            print(f"Order id {buy_action_id} is still open")
            time.sleep(10)

        if self.is_order_successful(buy_action_id):
            self._trade_bot_cache.increment_successful_trades()
            fee = self.__exchange_api.get_transaction_fee(buy_action_id)
            self._trade_bot_cache.accrued_fee = fee
            self.print_successful_trades(self.__exchange_api.get_exchange_name(), self.is_buy(), fee)
            self.update_account_values()
            self.update_ask_price()
            self.send_email_with_successful_trade(self.__exchange_api.get_exchange_name())
            return True
        else:
            print(f'\n--- {datetime.now()} - Order: {buy_action_id} was not successful! \n')
            return False

    def trade_action_buy(self):
        return self.__exchange_api.buy_action(self._trade_bot_cache.market_ask_price,
                                              self._trade_bot_cache.buy_quantity)

    def update_account_values(self):
        self._trade_bot_cache.sell_quantity = self.__exchange_api.get_account_quantity()
        self._trade_bot_cache.cash_value = self.__exchange_api.get_account_cash_value()

    def is_order_successful(self, order_id):
        return self.__exchange_api.is_order_successful(order_id)

    def is_order_status_open(self, order_id):
        return self.__exchange_api.is_order_status_open(order_id)