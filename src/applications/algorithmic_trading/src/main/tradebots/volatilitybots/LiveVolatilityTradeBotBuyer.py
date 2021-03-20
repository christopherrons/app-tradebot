import time
from datetime import datetime

from applications.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from applications.algorithmic_trading.src.main.exchange.ExchangeApi import ExchangeApi
from applications.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket
from applications.algorithmic_trading.src.main.output_handlers.TradeBotOutputHandler import TradeBotOutputHandler
from applications.algorithmic_trading.src.main.output_handlers.utils.PrinterUtils import PrinterUtils
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotBuyer import \
    VolatilityTradeBotBuyer


class LiveVolatilityTradeBotBuyer(VolatilityTradeBotBuyer):
    def __init__(self,
                 exchange_api: ExchangeApi,
                 exchange_websocket: ExchangeWebsocket,
                 trade_bot_output_handler: TradeBotOutputHandler,
                 trade_bot_cache: TradeBotCache):
        super().__init__(exchange_websocket, trade_bot_output_handler, trade_bot_cache)
        self.__exchange_api = exchange_api

    def execute_order(self) -> str:
        return self.__exchange_api.execute_buy_order(self._trade_bot_cache.market_ask_price, self._trade_bot_cache.buy_quantity)

    def is_order_executed(self, order_id: str) -> bool:
        while self.__is_order_status_open(order_id):
            PrinterUtils.console_log(message=f"Order id {order_id} is still open")
            time.sleep(10)

        if self.__is_order_executed(order_id):
            return True
        else:
            PrinterUtils.console_log(message=f'{datetime.now()} - Order: {order_id} was not executed!')
            return False

    def run_post_trade_tasks(self, order_id: str):
        fee = self.__exchange_api.get_transaction_fee(order_id)
        self.update_cache(order_id, fee)
        self.create_visual_trade_report()
        self.email_trade_reports()
        PrinterUtils.console_log(message="Post Trade Task Finished!")

    def update_cache(self, order_id: str, fee: float):
        self._trade_bot_cache.increment_successful_trades()
        self._trade_bot_cache.accrued_fee = fee
        self.print_and_store_trade_report(self.is_buy(), fee, order_id)
        self._trade_bot_cache.sell_quantity = self.__exchange_api.get_account_quantity()
        self._trade_bot_cache.cash_value = self.__exchange_api.get_account_cash_value()
        self.update_ask_price()

    def __is_order_executed(self, order_id: str) -> bool:
        return self.__exchange_api.is_order_successful(order_id)

    def __is_order_status_open(self, order_id: str) -> bool:
        return self.__exchange_api.is_order_status_open(order_id)