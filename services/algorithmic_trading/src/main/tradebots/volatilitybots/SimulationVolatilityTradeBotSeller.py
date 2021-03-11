from services.algorithmic_trading.src.main.cache_storage.TradeBotCache import TradeBotCache
from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket
from services.algorithmic_trading.src.main.tradebots.volatilitybots.VolatilityTradeBotSeller import VolatilityTradeBotSeller


class SimulationVolatilityTradeBotSeller(VolatilityTradeBotSeller):

    def __init__(self,
                 exchange_websocket: ExchangeWebsocket,
                 trade_bot_cache: TradeBotCache):
        super().__init__(exchange_websocket, trade_bot_cache)

    def create_trade(self) -> str:
        return self.trade_action_sell()

    def trade_action_sell(self) -> str:
        return "Simulation"

    def is_trade_successful(self, order_id: str) -> bool:
        return True

    def update_cache(self, order_id: str):
        self._trade_bot_cache.increment_successful_trades()
        self._trade_bot_cache.increment_successful_cycles()
        fee = self._trade_bot_cache.gross_position_value * self._trade_bot_cache.exchange_fee
        self._trade_bot_cache.accrued_fee = fee
        self._trade_bot_output.print_successful_trades(self.is_buy(), fee)
        self.update_bid_price()
        self._trade_bot_cache.cash_value = self._trade_bot_cache.net_position_value
        self._trade_bot_cache.gross_position_value = 0
        self._trade_bot_cache.net_position_value = 0
