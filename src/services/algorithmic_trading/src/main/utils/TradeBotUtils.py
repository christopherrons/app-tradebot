import argparse
import os
import smtplib
from configparser import ConfigParser
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from services.algorithmic_trading.src.main.exchange.ExchangeWebsocket import ExchangeWebsocket


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
    def get_script_config_attribute(parent: str, attribute: str) -> str:
        config = ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '../../resources/configs/script-config.ini')
        config.read(config_path)
        config_path = config.get('Paths', 'script_config_path')
        if not os.path.exists(config_path):
            raise ValueError(f'No configuration file exists. Expected file: {config_path}')

        config.read(config_path)
        return config.get(parent, attribute)

    @staticmethod
    def get_email_source() -> str:
        return TradeBotUtils.get_script_config_attribute('User', 'emailSource')

    @staticmethod
    def get_email_source_password() -> str:
        return TradeBotUtils.get_script_config_attribute('User', 'emailSourcePassword')

    @staticmethod
    def get_email_target() -> str:
        return TradeBotUtils.get_script_config_attribute('User', 'emailTarget')

    @staticmethod
    def get_kraken_api_secret() -> str:
        return TradeBotUtils.get_script_config_attribute('Kraken', 'apiSecret')

    @staticmethod
    def get_kraken_api_key() -> str:
        return TradeBotUtils.get_script_config_attribute('Kraken', 'apiKey')

    @staticmethod
    def get_bitstamp_api_secret() -> str:
        return TradeBotUtils.get_script_config_attribute('Bitstamp', 'apiSecret')

    @staticmethod
    def get_bitstamp_api_key() -> str:
        return TradeBotUtils.get_script_config_attribute('Bitstamp', 'apiKey')

    @staticmethod
    def get_bitstamp_customer_id() -> str:
        return TradeBotUtils.get_script_config_attribute('Bitstamp', 'customerID')

    @staticmethod
    def is_run_time_passed(current_time: datetime, run_stop_time: datetime) -> bool:
        return current_time > run_stop_time

    @staticmethod
    def live_run_checker(is_not_simulation: bool):
        if is_not_simulation:
            contract = input("WARNING LIVE RUN. If you want to trade sign the contract with: winteriscoming: ")
            if contract != "winteriscoming":
                print("ABORTING")
                exit()
            else:
                print("Contracted signed! Live run accepted!\n")

    @staticmethod
    def validate_args(args, minimum_interest: float):
        if args.initial_value < 1:
            raise ValueError(f'Initial Value {args.initial_value} is to low. Minimum value is 1')

        if args.interest < minimum_interest:
            raise ValueError(f'Interest {args.interest} is to low. Minimum value is 0.{minimum_interest}')

        if args.print_interval < 0:
            raise ValueError(f'Print Interval {args.print_interval} is to low. Minimum value is 0')

        if args.run_time_minutes < 1:
            raise ValueError(f'Run Time {args.run_time_minutes} is to low. Minimum value is 1')

        if args.run_time_minutes > 1000000:
            raise ValueError(f'Print Interval {args.run_time_minutes} is to high. Maximum value is 1000000')

    @staticmethod
    def set_initial_trade_price(exchange_websocket: ExchangeWebsocket, is_sell: bool) -> float:
        is_invalid_account_trade_price = True
        account_trade_price = 0
        while is_invalid_account_trade_price:
            market_bid_price = exchange_websocket.get_market_bid_price()
            market_ask_price = exchange_websocket.get_market_ask_price()
            print(f'Market bid: {market_bid_price} \nMarket ask: {market_ask_price}\n')

            if is_sell:
                account_trade_price = float(input('Set start account ASK price: '))
                is_invalid_account_trade_price = TradeBotUtils.is_invalid_account_ask_price(market_bid_price,
                                                                                            account_trade_price)
                if is_invalid_account_trade_price:
                    print("ERROR: Account ask price has to be larger than market bid price.\n")
                else:
                    print(f"Account Ask Price: {account_trade_price}\n")
            else:
                account_trade_price = float(input('Set start account BID price: '))
                is_invalid_account_trade_price = TradeBotUtils.is_invalid_account_bid_price(market_ask_price,
                                                                                            account_trade_price)
                if is_invalid_account_trade_price:
                    print("ERROR: Account bid price has to be smaller than market ask price.\n")
                else:
                    print(f"Account Bid Price: {account_trade_price}\n")

        return account_trade_price

    @staticmethod
    def is_invalid_account_bid_price(market_ask_price: float, account_bid_price: float) -> bool:
        return market_ask_price - account_bid_price < 0

    @staticmethod
    def is_invalid_account_ask_price(market_bid_price: float, account_ask_price: float) -> bool:
        return market_bid_price - account_ask_price > 0

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
            'USD': '$',
            'EUR': '€'
        }

    @staticmethod
    def get_permitted_crypto_currencies():
        return ['XRP']

    @staticmethod
    def get_permitted_cash_currencies():
        return ['USD', 'EUR']

    @staticmethod
    def get_permitted_trade_pairs():
        trading_pairs = []
        for crypto_currency in TradeBotUtils.get_permitted_crypto_currencies():
            for cash_currency in TradeBotUtils.get_permitted_cash_currencies():
                trading_pairs.append(crypto_currency + cash_currency)
        return trading_pairs

    @staticmethod
    def convert_epoch_time_to_timestamp(from_time: str) -> datetime:
        return datetime.fromtimestamp(float(from_time))
