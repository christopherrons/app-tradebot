from services.algorithmic_trading.src.main.tradebots.TradeBotBuyer import TradeBotBuyer


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
        self.print_successful_trades('Simulation exchange', self.is_buy(), fee)
        self._trade_bot_cache.sell_quantity = self._trade_bot_cache.buy_quantity
        self.update_ask_price()
        self.update_account_values()
        self.send_email_with_successful_trade('Simulation exchange')

    def update_account_values(self):
        self._trade_bot_cache.cash_value = 0
