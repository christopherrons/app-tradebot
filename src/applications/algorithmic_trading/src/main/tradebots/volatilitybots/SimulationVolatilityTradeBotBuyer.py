import time

from applications.algorithmic_trading.src.main.cache_storage.TradingCache import TradingCache
from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotBuyer import \
    VolatilityTradeBotBuyer
from applications.common.src.main.exchanges import ExchangeWebsocket
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class SimulationVolatilityTradeBotBuyer(VolatilityTradeBotBuyer):

    def __init__(self, exchange_websocket: ExchangeWebsocket,
                 trading_output_handler: TradingOutputHandler,
                 trade_bot_cache: TradingCache):
        super().__init__(exchange_websocket, trading_output_handler, trade_bot_cache)

    def execute_order(self) -> str:
        return "simulation"

    def is_order_executed(self, order_id: str) -> bool:
        return True

    def run_post_trade_tasks(self, order_id: str):
        fee = self._trade_bot_cache.cash_value * self._trade_bot_cache.exchange_fee
        self.update_cache(order_id, fee)
        self.create_visual_trade_report()
        self.email_trade_reports()
        PrinterUtils.console_log(message="Post Trade Task Finished!")

    def update_cache(self, order_id: str, fee: float):
        self._trade_bot_cache.increment_successful_trades()
        self._trade_bot_cache.accrued_fee = fee
        self.print_and_store_trade_report(self.is_buy(), fee, str(int(time.time() * 1e6)))
        self._trade_bot_cache.sell_quantity = self._trade_bot_cache.buy_quantity
        self.update_ask_price()
        self._trade_bot_cache.cash_value = 0
