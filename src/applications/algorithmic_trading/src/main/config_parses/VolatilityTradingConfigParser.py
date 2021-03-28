import yaml

from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class VolatilityTradingConfigParser:
    def __init__(self):
        with open(TradeBotUtils.get_config_file_path("strategy-configs.yaml"), "r") as f:
            volatility_configs = yaml.safe_load(f)

            self.__is_sell = volatility_configs['volatility']['is_sell']['custom'] \
                if volatility_configs['volatility']['is_sell']['custom'] \
                else volatility_configs['volatility']['is_sell']['default']

            self.__is_reset_logs = volatility_configs['volatility']['is_reset_logs']['custom'] \
                if volatility_configs['volatility']['is_reset_logs']['custom'] \
                else volatility_configs['volatility']['is_reset_logs']['default']

            self.__init_database_from_exchange = volatility_configs['volatility']['init_database_from_exchange']['custom'] \
                if volatility_configs['volatility']['init_database_from_exchange']['custom'] \
                else volatility_configs['volatility']['init_database_from_exchange']['default']

            self.__reset_database = volatility_configs['volatility']['reset_database']['custom'] \
                if volatility_configs['volatility']['reset_database']['custom'] \
                else volatility_configs['volatility']['reset_database']['default']

            self.__is_live = volatility_configs['volatility']['is_live']['custom'] \
                if volatility_configs['volatility']['is_live']['custom'] \
                else volatility_configs['volatility']['is_live']['default']

            self.__override_initial_value = volatility_configs['volatility']['override_initial_value']['custom']

            self.__print_interval = volatility_configs['volatility']['print_interval']['custom'] \
                if volatility_configs['volatility']['print_interval']['custom'] else \
                volatility_configs['volatility']['print_interval']['default']

            self.__interest = volatility_configs['volatility']['interest']['custom'] \
                if volatility_configs['volatility']['interest']['custom'] \
                else volatility_configs['volatility']['interest']['default']

            self.__exchange = volatility_configs['volatility']['exchange']['custom'] \
                if volatility_configs['volatility']['exchange']['custom'] \
                else volatility_configs['volatility']['exchange']['default']

            self.__cash_currency = volatility_configs['volatility']['cash_currency']['custom'] \
                if volatility_configs['volatility']['cash_currency']['custom'] \
                else volatility_configs['volatility']['cash_currency']['default']

            self.__crypto_currency = volatility_configs['volatility']['crypto_currency']['custom'] \
                if volatility_configs['volatility']['crypto_currency']['custom'] \
                else volatility_configs['volatility']['crypto_currency']['default']

    def validate_configs(self):
        self.__validate_data_types()
        self.__validate_values()

    def __validate_data_types(self):
        if not isinstance(self.__is_sell, bool):
            raise ValueError(f'Config is_sell requires booleans got: {self.__is_sell} type {type(self.__is_sell)}')

        if not isinstance(self.__is_reset_logs, bool):
            raise ValueError(f'Config is_reset_logs requires booleans got: {self.__is_reset_logs} type {type(self.__is_reset_logs)}')

        if not isinstance(self.__init_database_from_exchange, bool):
            raise ValueError(
                f'Config init_database_from_exchange requires booleans got: {self.__init_database_from_exchange} type {type(self.__init_database_from_exchange)}')

        if not isinstance(self.__reset_database, bool):
            raise ValueError(
                f'Config reset_database requires booleans got: {self.__reset_database} type {type(self.__reset_database)}')

        if not isinstance(self.__is_live, bool):
            raise ValueError(f'Config is_not_simulation requires booleans got: {self.__is_live} type {type(self.__is_live)}')

        if self.__override_initial_value and not isinstance(self.__override_initial_value, float):
            raise ValueError(
                f'Config override_initial_value requires floats got: {self.__override_initial_value} type {type(self.__override_initial_value)}')

        if not isinstance(self.__print_interval, float):
            raise ValueError(f'Config print_interval requires floats got: {self.__print_interval} type {type(self.__print_interval)}')

        if not isinstance(self.__interest, float):
            raise ValueError(f'Config interest requires booleans got: {self.__interest} type {type(self.__interest)}')

        if not isinstance(self.__exchange, str):
            raise ValueError(f'Config exchanges requires str got: {self.__exchange} type {type(self.__exchange)}')

        if not isinstance(self.__cash_currency, str):
            raise ValueError(f'Config cash_currency requires str got: {self.__cash_currency} type {type(self.__cash_currency)}')

        if not isinstance(self.__crypto_currency, str):
            raise ValueError(f'Config crypto_currency requires str got: {self.__crypto_currency} type {type(self.__crypto_currency)}')

    def __validate_values(self):
        if self.__exchange not in TradeBotUtils.get_permitted_exchanges():
            raise ValueError(f'Exchange {self.__exchange} not in list {TradeBotUtils.get_permitted_exchanges()}')

        if self.__cash_currency not in TradeBotUtils.get_permitted_cash_currencies():
            raise ValueError(f'Cash Currency {self.__cash_currency}  not in list {TradeBotUtils.get_permitted_cash_currencies()}')

        if self.__crypto_currency not in TradeBotUtils.get_permitted_crypto_currencies():
            raise ValueError(f'Crypto Currency {self.__crypto_currency} not in list {TradeBotUtils.get_permitted_crypto_currencies()}')

        if self.__interest < TradeBotUtils.get_minimum_interest(self.__exchange):
            raise ValueError(f'Interest {self.__interest} is lower than allowed {TradeBotUtils.get_minimum_interest(self.__exchange)}')

    @property
    def is_sell(self) -> bool:
        return self.__is_sell

    @property
    def is_reset_logs(self) -> bool:
        return self.__is_reset_logs

    @property
    def init_database_from_exchange(self) -> bool:
        return self.__init_database_from_exchange

    @property
    def reset_database(self) -> bool:
        return self.__reset_database

    @property
    def is_live(self) -> bool:
        return self.__is_live

    @property
    def override_initial_value(self) -> float:
        return abs(self.__override_initial_value) if self.__override_initial_value else None

    @property
    def print_interval(self) -> float:
        return abs(self.__print_interval)

    @property
    def exchange(self) -> str:
        return self.__exchange

    @property
    def cash_currency(self) -> str:
        return self.__cash_currency

    @property
    def crypto_currency(self) -> str:
        return self.__crypto_currency

    @property
    def interest(self) -> float:
        return self.__interest

    @property
    def run_time_minutes(self) -> float:
        return 1000000
