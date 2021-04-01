import time

from applications.algorithmic_trading.src.main.cache.TradingCache import trading_cache
from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotSeller import \
    VolatilityTradeBotSeller
from applications.common.src.main.exchanges import ExchangeWebsocket
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class SimulationVolatilityTradeBotSeller(VolatilityTradeBotSeller):

    def __init__(self, exchange_websocket: ExchangeWebsocket,
                 trading_output_handler: TradingOutputHandler):
        super().__init__(exchange_websocket, trading_output_handler, )

    def execute_order(self) -> str:
        return "simulation"

    def is_order_executed(self, order_id: str) -> bool:
        return True

    def run_post_trade_tasks(self, order_id: str):
        fee = trading_cache.gross_position_value * trading_cache.exchange_fee
        self.update_cache(order_id, fee)
        self.create_visual_trade_report()
        self.email_trade_reports()
        PrinterUtils.console_log(message="Post Trade Task Finished!")

    def update_cache(self, order_id: str, fee: float):
        trading_cache.successful_trades = trading_cache.successful_trades + 1
        trading_cache.successful_cycles = trading_cache.successful_cycles + 1
        trading_cache.accrued_fee = fee
        self.print_and_store_trade_report(self.is_buy(), fee, str(int(time.time() * 1e6)))
        self.update_bid_price()
        trading_cache.cash_value = trading_cache.net_position_value
        trading_cache.gross_position_value = 0
        trading_cache.net_position_value = 0
