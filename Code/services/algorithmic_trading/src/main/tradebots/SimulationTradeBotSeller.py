from services.algorithmic_trading.src.main.tradebots.TradeBotSeller import TradeBotSeller


class SimulationTradeBotSeller(TradeBotSeller):

    def __init__(self,
                 exchange_websocket,
                 trade_bot_cache):
        super().__init__(exchange_websocket, trade_bot_cache)

    def create_trade(self):
        self.trade_action_sell()
        return True

    def trade_action_sell(self):
        self._trade_bot_cache.increment_successful_trades()
        self._trade_bot_cache.increment_successful_cycles()
        fee = self._trade_bot_cache.gross_position_value * self._trade_bot_cache.exchange_fee
        self._trade_bot_cache.accrued_fee = fee
        self._trade_bot_output.print_successful_trades('Simulation exchange', self.is_buy(), fee)
        self.update_bid_price()
        self.update_account_values()
        self.send_email_with_successful_trade('Simulation exchange')

    def update_account_values(self):
        self._trade_bot_cache.cash_value = self._trade_bot_cache.net_position_value
        self._trade_bot_cache.gross_position_value = 0
        self._trade_bot_cache.net_position_value = 0
