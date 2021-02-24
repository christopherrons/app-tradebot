from Services.Runner.TradeBots.TradeBotBuyer import TradeBotBuyer


class SimulationTradeBotBuyer(TradeBotBuyer):

    def __init__(self,
                 exchange_websocket,
                 trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)

    def create_trade(self):
        self.trade_action_buy()

    def trade_action_buy(self):
        self._trade_bot_cache.accrued_fee = self._trade_bot_cache.buy_fee()
        self.print_and_log_successful_trades(self.is_buy(), self._trade_bot_cache.buy_fee())
        self._trade_bot_cache.sell_quantity = self._trade_bot_cache.buy_quantity
        self.update_ask_price()
        self.update_values()
        self.send_email()

    def update_values(self):
        self._trade_bot_cache.position_value = 0
        self._trade_bot_cache.cash_value = self._trade_bot_cache.position_value - self._trade_bot_cache.sell_fee()


