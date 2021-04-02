import random
import traceback

from applications.algorithmic_trading.src.main.builders.LiveVolatilityTradeRunnerBuilder import LiveVolatilityTradeRunnerBuilder
from applications.algorithmic_trading.src.main.builders.SimulationVolatilityTradeRunnerBuilder import SimulationVolatilityTradeRunnerBuilder
from applications.algorithmic_trading.src.main.config_parses.VolatilityTradingConfigParser import VolatilityTradingConfigParser
from applications.algorithmic_trading.src.main.runners.VolatilityTradeRunner import VolatilityTradeRunner
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.database.TradeDataDao import TradeDataDao
from applications.common.src.main.email.EmailHandler import EmailHandler
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class VolatilityTrading:

    def __init__(self):
        self.__configs = VolatilityTradingConfigParser()
        self.__database_service = TradeDataDao()
        self.__database_schema = "trade_data"

    def run(self):
        try:
            self.__run_setup_tasks()
            self.__get_trade_runner().run()
        except ValueError as error_message:
            print(error_message)
        except KeyboardInterrupt:
            print("Keyboard Interrupted")
        except Exception as error:
            print("\n--- ERROR ---")
            traceback.print_exc()
            EmailHandler().send_email_message(email_subject=f'ERROR: {self.__configs.exchange}', email_message=str(error))

    def __get_trade_runner(self) -> VolatilityTradeRunner:
        if self.__configs.is_live:
            return LiveVolatilityTradeRunnerBuilder(self.__configs, self.__database_service).build()
        else:
            return SimulationVolatilityTradeRunnerBuilder(self.__configs, self.__database_service).build()

    def __run_setup_tasks(self):
        self.__configs.validate_configs()
        self.__live_run_checker()
        TradeBotUtils.create_target_folder()
        if self.__configs.reset_database:
            self.__database_service.drop_schema_tables(schema=self.__database_schema)

        self.__database_service.run_queries_from_file(file_path=TradeBotUtils.get_template_file_path("algorithmic_trading_database_schema.sql"))

        if self.__configs.is_reset_logs:
            TradeBotUtils.reset_logs(self.__configs.exchange)

    def __live_run_checker(self):
        if self.__configs.is_live:
            contract_pin = random.randint(10000, 99999)
            signature = int(input(f"\nWARNING LIVE RUN. If you want to trade sign the contract by entering: {contract_pin}: "))
            if signature != int(contract_pin):
                PrinterUtils.console_log(message="ABORTING")
                exit()
            else:
                PrinterUtils.console_log(message="Contract signed! Live run accepted!")
