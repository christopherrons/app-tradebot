from Services.Runner.Statistics.TradeBotOutput import TradeBotOutput


class TradeBotKing:
    def __init__(self, trade_bot_cache):
        self._trade_bot_cache = trade_bot_cache
        self._trade_bot_output = TradeBotOutput(self._trade_bot_cache)

    def print_and_log_current_formation(self, is_buy):
        self._trade_bot_output.print_and_log_current_formation(is_buy)

    def print_and_log_successful_trades(self, is_buy, fee):
        self._trade_bot_output.print_and_log_successful_trades(is_buy, fee)

    def send_email(self):
        self._trade_bot_output.send_email()
