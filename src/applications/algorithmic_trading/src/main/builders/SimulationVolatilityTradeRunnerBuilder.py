from applications.algorithmic_trading.src.main.builders.VolatilityTradeRunnerBuilder import VolatilityTradeRunnerBuilder
from applications.algorithmic_trading.src.main.cache_storage.TradingCache import TradingCache
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
        exchange_websocket = self.get_exchange_websocket()
        initial_value = self.__get_initial_value()
        account_ask_price = self.get_initial_ask_price(exchange_websocket)
        account_bid_price = self.get_initial_bid_price(exchange_websocket)
        trading_cache = self.__get_trading_cache(initial_value, account_bid_price, account_ask_price)
        trading_output_handler = self.get_tradebot_output_handler(trading_cache)
        return self.__get_tradebot_runner(trading_cache, trading_output_handler, exchange_websocket)

    def __get_initial_value(self) -> float:
        return 100

    def __get_trading_cache(self, initial_value: float, account_bid_price: float, account_ask_price: float) -> TradingCache:
        return TradingCache(initial_value=initial_value,
                            cash_value=initial_value,
                            interest=self._configs.interest,
                            account_bid_price=account_bid_price,
                            account_ask_price=account_ask_price,
                            sell_quantity=initial_value / ((1 - TradeBotUtils.get_exchange_fee(self._configs.exchange)) *
                                                           (account_ask_price / (1 + self._configs.interest)))
                            if not account_ask_price == 0 else 0,
                            exchange_fee=TradeBotUtils.get_exchange_fee(self._configs.exchange),
                            accrued_fees=0,
                            success_ful_trades=0,
                            successful_cycles=0)

    def __get_tradebot_runner(self, trading_cache: TradingCache, trading_output_handler: TradingOutputHandler,
                              exchange_websocket: ExchangeWebsocket) -> VolatilityTradeRunner:
        return VolatilityTradeRunner(is_sell=self._configs.is_sell,
                                     trade_bot_buyer=SimulationVolatilityTradeBotBuyer(exchange_websocket, trading_output_handler, trading_cache),
                                     trade_bot_seller=SimulationVolatilityTradeBotSeller(exchange_websocket, trading_output_handler, trading_cache),
                                     run_time_minutes=self._configs.run_time_minutes,
                                     print_interval=self._configs.print_interval)
