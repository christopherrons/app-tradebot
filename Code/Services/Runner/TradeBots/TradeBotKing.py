from Services.Runner.Statistics.TradeBotOutput import TradeBotOutput


class TradeBotKing:
    def __init__(self, exchange_websocket, trade_bot_cache):
        self._exchange_websocket = exchange_websocket
        self._trade_bot_cache = trade_bot_cache
        self._trade_bot_output = TradeBotOutput(self._trade_bot_cache,
                                                exchange_websocket.cash_currency,
                                                exchange_websocket.crypto_currency)

    def print_and_log_current_formation(self, is_buy):
        self._trade_bot_output.print_and_log_current_formation(is_buy)

    def print_and_log_successful_trades(self, exchange_name, is_buy, fee):
        self._trade_bot_output.print_and_log_successful_trades(exchange_name, is_buy, fee)

    def send_email(self, exchange_name):
        self._trade_bot_output.send_email(exchange_name)
