from Services.Runner.TradeBots.TradeBotBuyer import TradeBotBuyer


class SimulationTradeBotBuyer(TradeBotBuyer):

    def __init__(self,
                 exchange_websocket,
                 trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)

    def create_trade(self):
        self.trade_action_buy()
        return True

    def trade_action_buy(self):
        self._trade_bot_cache.increment_successful_trades()
        fee = self._trade_bot_cache.cash_value * self._trade_bot_cache.exchange_fee
        self._trade_bot_cache.accrued_fee = fee
        self.print_and_log_successful_trades(self.is_buy(), fee)
        self._trade_bot_cache.sell_quantity = self._trade_bot_cache.buy_quantity
        self.update_ask_price()
        self.update_value()
        #self.send_email()

    def update_value(self):
        self._trade_bot_cache.cash_value = 0
