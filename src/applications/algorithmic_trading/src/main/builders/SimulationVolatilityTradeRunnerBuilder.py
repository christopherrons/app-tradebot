from applications.algorithmic_trading.src.main.builders.VolatilityTradeRunnerBuilder import VolatilityTradeRunnerBuilder
from applications.algorithmic_trading.src.main.cache.TradingCache import trading_cache
from applications.algorithmic_trading.src.main.config_parses.VolatilityTradingConfigParser import VolatilityTradingConfigParser
from applications.algorithmic_trading.src.main.output_handlers.TradingOutputHandler import TradingOutputHandler
from applications.algorithmic_trading.src.main.runners.VolatilityTradeRunner import VolatilityTradeRunner
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.SimulationVolatilityTradeBotBuyer import SimulationVolatilityTradeBotBuyer
from applications.algorithmic_trading.src.main.tradebots.volatilitybots.SimulationVolatilityTradeBotSeller import SimulationVolatilityTradeBotSeller
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.database.TradeDataDao import TradeDataDao
from applications.common.src.main.exchanges.ExchangeWebsocket import ExchangeWebsocket


class SimulationVolatilityTradeRunnerBuilder(VolatilityTradeRunnerBuilder):
    def __init__(self, configs: VolatilityTradingConfigParser, database_service: TradeDataDao):
        super().__init__(configs, database_service)

    def build(self) -> VolatilityTradeRunner:
        exchange_websocket = self._get_exchange_websocket()
        initial_value = self.__get_initial_value()
        account_ask_price = self._get_initial_ask_price(exchange_websocket)
        account_bid_price = self._get_initial_bid_price(exchange_websocket)
        self.__init_cache(initial_value, account_bid_price, account_ask_price)
        trading_output_handler = self._get_tradebot_output_handler()
        return self.__get_tradebot_runner(trading_output_handler, exchange_websocket)

    def __get_initial_value(self) -> float:
        return 100

    def __init_cache(self, initial_value: float, account_bid_price: float, account_ask_price: float):
        trading_cache.initial_value = initial_value
        trading_cache.cash_value = initial_value
        trading_cache.interest = self._configs.interest
        trading_cache.account_bid_price = account_bid_price
        trading_cache.account_ask_price = account_ask_price
        trading_cache.sell_quantity = initial_value / ((1 - TradeBotUtils.get_exchange_fee(self._configs.exchange)) *
                                                       (account_ask_price / (1 + self._configs.interest))) if not account_ask_price == 0 else 0
        trading_cache.exchange_fee = TradeBotUtils.get_exchange_fee(self._configs.exchange)
        trading_cache.accrued_fee = 0
        trading_cache.successful_trades = 0
        trading_cache.successful_cycles = 0

    def __get_tradebot_runner(self, trading_output_handler: TradingOutputHandler,
                              exchange_websocket: ExchangeWebsocket) -> VolatilityTradeRunner:
        return VolatilityTradeRunner(is_sell=self._configs.is_sell,
                                     trade_bot_buyer=SimulationVolatilityTradeBotBuyer(exchange_websocket, trading_output_handler),
                                     trade_bot_seller=SimulationVolatilityTradeBotSeller(exchange_websocket, trading_output_handler),
                                     run_time_minutes=self._configs.run_time_minutes,
                                     print_interval=self._configs.print_interval)
