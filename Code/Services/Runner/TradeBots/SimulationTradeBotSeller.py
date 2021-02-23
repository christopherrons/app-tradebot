from Services.Runner.TradeBots.TradeBotSeller import TradeBotSeller


class SimulationTradeBotSeller(TradeBotSeller):

    def __init__(self,
                 exchange_websocket,
                 trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)

    def create_trade(self):
        self.trade_action_sell()

    def trade_action_sell(self):
        self._trade_bot_cache.increment_successful_cycles()
        self._trade_bot_cache.accrued_fee = self._trade_bot_cache.sell_fee()
        self._trade_bot_output.print_and_log_successful_trades(self.is_buy(), self._trade_bot_cache.sell_fee())
        self.update_bid_price()
        self.update_value()
        self.send_email()

    def update_value(self):
        self._trade_bot_cache.cash_value = 0
