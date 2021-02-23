from Services.Runner.TradeBots.TradeBotBuyer import TradeBotBuyer


class LiveTradeBotBuyer(TradeBotBuyer):

    def __init__(self,
                 exchange_api,
                 exchange_websocket,
                 trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)
        self.__exchange_api = exchange_api

    def create_trade(self):
        self.trade_action_buy()

    def trade_action_buy(self):
        buy_action_id = self.__exchange_api.buy_action(self._trade_bot_cache.market_ask_price,
                                                       self._trade_bot_cache.buy_quantity)
        while not self.is_order_status_finished(buy_action_id):
            # TODO add logic for printing while waiting
            pass

        fee = self.__exchange_api.get_transaction_fee()
        self._trade_bot_cache.accrued_fee = fee
        self.print_and_log_successful_trades(self.is_buy(), fee)
        self.update_account_quantity_values()
        self.update_ask_price()
        self.send_email()

    def is_buy(self):
        return True

    def update_account_quantity_values(self):
        self._trade_bot_cache.sell_quantity = self.__exchange_api.get_account_quantity()
        self._trade_bot_cache.cash_value = self.__exchange_api.get_account_cash_value()

    def update_ask_price(self):
        self._trade_bot_cache._account_ask_price = self._trade_bot_cache.market_bid_price * (
                1 + self._trade_bot_cache.interest)

    def is_order_status_finished(self, order_id):
        return self.__exchange_api.get_order_status(order_id) == "Finished"