from services.algorithmic_trading.src.main.data_output_handler.TradeBotOutput import TradeBotOutput


class TradeBotKing:
    def __init__(self, exchange_websocket, trade_bot_cache):
        self._exchange_websocket = exchange_websocket
        self._trade_bot_cache = trade_bot_cache
        self._trade_bot_output = TradeBotOutput(exchange_websocket.get_exchange_name(),
                                                self._trade_bot_cache,
                                                exchange_websocket.cash_currency,
                                                exchange_websocket.crypto_currency)

    def print_trading_formation(self, is_buy):
        self._trade_bot_output.print_trading_formation(is_buy)

    def print_successful_trades(self, exchange_name, is_buy, fee):
        self._trade_bot_output.print_successful_trades(exchange_name, is_buy, fee)

    def send_email_with_successful_trade(self, exchange_name):
        self._trade_bot_output.send_email_with_successful_trade(exchange_name)
