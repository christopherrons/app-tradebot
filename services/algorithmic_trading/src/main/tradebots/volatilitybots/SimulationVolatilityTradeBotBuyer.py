from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket
from services.algorithmic_trading.src.main.output_handlers.TradeBotOutputHandler import TradeBotOutputHandler
from services.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotBuyer import \
    VolatilityTradeBotBuyer


class SimulationVolatilityTradeBotBuyer(VolatilityTradeBotBuyer):

    def __init__(self, exchange_websocket: ExchangeWebsocket,
                 trade_bot_output_handler: TradeBotOutputHandler,
                 trade_bot_cache: TradeBotCache):
        super().__init__(exchange_websocket, trade_bot_output_handler, trade_bot_cache)

    def execute_order(self) -> str:
        return "Simulation"

    def is_order_executed(self, order_id: str) -> bool:
        return True

    def run_post_trade_batch(self, order_id: str):
        self.update_cache(order_id)
        self.create_visual_trade_report()
        self.email_trade_reports()

    def update_cache(self, order_id: str):
        self._trade_bot_cache.increment_successful_trades()
        fee = self._trade_bot_cache.cash_value * self._trade_bot_cache.exchange_fee
        self._trade_bot_cache.accrued_fee = fee
        self.print_and_store_trade_report(self.is_buy(), fee)
        self._trade_bot_cache.sell_quantity = self._trade_bot_cache.buy_quantity
        self.update_ask_price()
        self._trade_bot_cache.cash_value = 0
