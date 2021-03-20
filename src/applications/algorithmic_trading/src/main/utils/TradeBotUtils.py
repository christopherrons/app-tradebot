import argparse
import os
import smtplib
from configparser import ConfigParser
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import yaml


class TradeBotUtils:
    @staticmethod
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass

    @staticmethod
    def reset_logs(exchange_name: str):
        log_files = [TradeBotUtils.get_trade_log_path(exchange_name), TradeBotUtils.get_information_log_path(exchange_name)]
        if log_files:
            for file in log_files:
                with open(file, 'a+') as f:
                    f.truncate(0)

    @staticmethod
    def create_target_folder():
        if not os.path.exists(os.path.join(os.path.dirname(__file__), f"../../../target")):
            os.mkdir(os.path.join(os.path.dirname(__file__), f"../../../target"))
            os.mkdir(os.path.join(os.path.dirname(__file__), f"../../../target/generated"))

    @staticmethod
    def get_data_base_queries_path() -> str:
        return os.path.join(os.path.dirname(__file__), '../../resources/templates/algorithmic_trading_database_schema.sql')

    @staticmethod
    def get_trade_report_path(exchange: str) -> str:
        return os.path.join(os.path.dirname(__file__), f"../../../target/generated/{exchange.lower()}_trade_report.html")

    @staticmethod
    def get_trade_log_path(exchange: str) -> str:
        return os.path.join(os.path.dirname(__file__), f"../../../target/generated/{exchange.lower()}_successful_trade_log.csv")

    @staticmethod
    def get_information_log_path(exchange: str) -> str:
        return os.path.join(os.path.dirname(__file__), f"../../../target/generated/{exchange.lower()}_trading_formation_log.csv")

    @staticmethod
    def get_strategy_config_path() -> str:
        return os.path.join(os.path.dirname(__file__), '../../resources/configs/strategy-configs.yaml')

    @staticmethod
    def get_exchange_config_path() -> str:
        return os.path.join(os.path.dirname(__file__), '../../resources/configs/exchange-configs.yaml')

    @staticmethod
    def get_account_config_path() -> str:
        return os.path.join(os.path.dirname(__file__), '../../resources/configs/account-configs.ini')

    @staticmethod
    def get_script_config_attribute(parent: str, attribute: str) -> str:
        config = ConfigParser()
        config_path = TradeBotUtils.get_account_config_path()
        if not os.path.exists(config_path):
            raise ValueError(f'No configuration file exists. Expected file: {config_path}')

        config.read(config_path)
        return config.get(parent, attribute)

    @staticmethod
    def get_email_source() -> str:
        return TradeBotUtils.get_script_config_attribute('user', 'emailSource')

    @staticmethod
    def get_email_source_password() -> str:
        return TradeBotUtils.get_script_config_attribute('user', 'emailSourcePassword')

    @staticmethod
    def get_email_target() -> str:
        return TradeBotUtils.get_script_config_attribute('user', 'emailTarget')

    @staticmethod
    def get_kraken_api_secret() -> str:
        return TradeBotUtils.get_script_config_attribute('kraken', 'apiSecret')

    @staticmethod
    def get_kraken_api_key() -> str:
        return TradeBotUtils.get_script_config_attribute('kraken', 'apiKey')

    @staticmethod
    def get_bitstamp_api_secret() -> str:
        return TradeBotUtils.get_script_config_attribute('bitstamp', 'apiSecret')

    @staticmethod
    def get_bitstamp_api_key() -> str:
        return TradeBotUtils.get_script_config_attribute('bitstamp', 'apiKey')

    @staticmethod
    def get_bitstamp_customer_id() -> str:
        return TradeBotUtils.get_script_config_attribute('bitstamp', 'customerID')

    @staticmethod
    def is_run_time_passed(current_time: datetime, run_stop_time: datetime) -> bool:
        return current_time > run_stop_time

    @staticmethod
    def send_error_has_occurred_email(exchange: str, error: str):
        email_source = TradeBotUtils.get_email_source()
        email_source_password = TradeBotUtils.get_email_source_password()
        email_target = TradeBotUtils.get_email_target()

        message = MIMEMultipart()
        message['From'] = email_source
        message['To'] = email_target
        message['Subject'] = f"{exchange}: Error has occurred"
        message.attach(MIMEText(f'{error}'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(email_source, email_source_password)
        text = message.as_string()
        server.sendmail(email_source, email_target, text)
        server.quit()

    @staticmethod
    def get_cash_currency_symbols() -> dict:
        return {
            'usd': '$',
            'eur': '€'
        }

    @staticmethod
    def get_exchange_fee(exchange: str) -> float:
        with open(TradeBotUtils.get_exchange_config_path(), "r") as f:
            return yaml.safe_load(f)['exchange'][exchange]['fee']

    @staticmethod
    def get_minimum_interest(exchange: str) -> float:
        with open(TradeBotUtils.get_exchange_config_path(), "r") as f:
            return yaml.safe_load(f)['exchange'][exchange]['minimum_interest']

    @staticmethod
    def get_permitted_crypto_currencies() -> list:
        with open(TradeBotUtils.get_exchange_config_path(), "r") as f:
            return list(yaml.safe_load(f)['currency']['crypto_currencies'].values())

    @staticmethod
    def get_permitted_cash_currencies() -> list:
        with open(TradeBotUtils.get_exchange_config_path(), "r") as f:
            return list(yaml.safe_load(f)['currency']['cash_currencies'].values())

    @staticmethod
    def get_permitted_exchanges() -> list:
        with open(TradeBotUtils.get_exchange_config_path(), "r") as f:
            return list(yaml.safe_load(f)['exchange'].keys())

    @staticmethod
    def get_permitted_trade_pairs() -> list:
        trading_pairs = []
        for crypto_currency in TradeBotUtils.get_permitted_crypto_currencies():
            for cash_currency in TradeBotUtils.get_permitted_cash_currencies():
                trading_pairs.append(crypto_currency + cash_currency)
        return trading_pairs

    @staticmethod
    def convert_epoch_time_to_timestamp(from_time: str) -> datetime:
        return datetime.fromtimestamp(float(from_time))
