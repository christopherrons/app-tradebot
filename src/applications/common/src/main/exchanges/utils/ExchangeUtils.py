import os

import yaml


class ExchangeUtils:
    @staticmethod
    def get_config_file_path(file_name):
        return os.path.join(os.path.dirname(__file__), f'../../../resources/configs/{file_name}')

    @staticmethod
    def get_exchange_fee(exchange: str) -> float:
        with open(ExchangeUtils.get_config_file_path("exchange-configs.yaml"), "r") as f:
            return yaml.safe_load(f)['exchange'][exchange]['fee']

    @staticmethod
    def get_minimum_interest(exchange: str) -> float:
        with open(ExchangeUtils.get_config_file_path("exchange-configs.yaml"), "r") as f:
            return yaml.safe_load(f)['exchange'][exchange]['minimum_interest']

    @staticmethod
    def get_permitted_crypto_currencies() -> list:
        with open(ExchangeUtils.get_config_file_path("exchange-configs.yaml"), "r") as f:
            return list(yaml.safe_load(f)['currency']['crypto_currencies'].values())

    @staticmethod
    def get_permitted_cash_currencies() -> list:
        with open(ExchangeUtils.get_config_file_path("exchange-configs.yaml"), "r") as f:
            return list(yaml.safe_load(f)['currency']['cash_currencies'].values())

    @staticmethod
    def get_permitted_exchanges() -> list:
        with open(ExchangeUtils.get_config_file_path("exchange-configs.yaml"), "r") as f:
            return list(yaml.safe_load(f)['exchange'].keys())

    @staticmethod
    def get_permitted_trade_pairs() -> list:
        trading_pairs = []
        for crypto_currency in ExchangeUtils.get_permitted_crypto_currencies():
            for cash_currency in ExchangeUtils.get_permitted_cash_currencies():
                trading_pairs.append(crypto_currency + cash_currency)
        return trading_pairs
