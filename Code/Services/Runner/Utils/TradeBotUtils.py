import argparse
import os
from configparser import ConfigParser


class TradeBotUtils:
    @staticmethod
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass

    @staticmethod
    def reset_logs():
        for file in [TradeBotUtils.get_trade_log_path(), TradeBotUtils.get_information_log_path()]:
            with open(file, 'a+') as f:
                f.truncate(0)

    @staticmethod
    def get_trade_log_path():
        return os.path.realpath(__file__).replace("Services/Runner/Utils/TradeBotUtils.py",
                                                  "logs/trades_logs.csv")

    @staticmethod
    def get_information_log_path():
        return os.path.realpath(__file__).replace("Services/Runner/Utils/TradeBotUtils.py",
                                                  "logs/current_formation_log.csv")

    @staticmethod
    def get_email_source():
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get('User', 'emailSource')

    @staticmethod
    def get_email_source_password():
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get('User', 'emailSourcePassword')

    @staticmethod
    def get_email_target():
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get('User', 'emailTarget')

    @staticmethod
    def get_bitstamp_api_secret():
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get('Bitstamp', 'apiSecret')

    @staticmethod
    def get_bitstamp_api_key():
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get('Bitstamp', 'apiKey')

    @staticmethod
    def get_bitstamp_customer_ID():
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get('Bitstamp', 'customerID')

    @staticmethod
    def is_run_time_passed(current_time, run_stop_time):
        return current_time > run_stop_time

    @staticmethod
    def live_run_checker(is_not_simulation):
        if is_not_simulation:
            contract = input("WARNING LIVE RUN. If you want to trade sign the contract with: winteriscoming: ")
            if contract != "winteriscoming":
                print("ABORTING")
                exit()
            else:
                print("Contracted signed! Live run accepted!\n")

    @staticmethod
    def validate_args(args, minimum_interest):
        if args.initial_value < 1:
            raise ValueError(f'Initial Value {args.initial_value} is to low. Minimum value is 1')

        if args.interest < minimum_interest :
            raise ValueError(f'Interest {args.interest} is to low. Minimum value is 0.{minimum_interest}')

        if args.print_interval < 0:
            raise ValueError(f'Print Interval {args.print_interval} is to low. Minimum value is 0')

        if args.run_time_minutes < 1:
            raise ValueError(f'Run Time {args.run_time_minutes} is to low. Minimum value is 1')

        if args.run_time_minutes > 1000000:
            raise ValueError(f'Print Interval {args.run_time_minutes} is to high. Maximum value is 1000000')

    @staticmethod
    def set_initial_trade_price(bitstamp_api, is_sell):
        is_invalid_account_trade_price = True
        while is_invalid_account_trade_price:
            market_bid_price = bitstamp_api.get_market_bid_price()
            market_ask_price = bitstamp_api.get_market_ask_price()
            print(f'Market bid: {market_bid_price} \nMarket ask: {market_ask_price}\n')

            if is_sell:
                account_trade_price = float(input('Set start account ASK price: '))
                is_invalid_account_trade_price = TradeBotUtils.is_invalid_account_ask_price(market_bid_price,
                                                                                            account_trade_price)
                if is_invalid_account_trade_price:
                    print("ERROR: Account ask price has to be larger than market bid price.\n")
                else:
                    print(f"Account Ask Price: {account_trade_price} [$].\n")
            else:
                account_trade_price = float(input('Set start account BID price: '))
                is_invalid_account_trade_price = TradeBotUtils.is_invalid_account_bid_price(market_ask_price,
                                                                                            account_trade_price)
                if is_invalid_account_trade_price:
                    print("ERROR: Account bid price has to be smaller than market ask price.\n")
                else:
                    print(f"Account Bid Price: {account_trade_price} [$].\n")

        return account_trade_price

    @staticmethod
    def is_invalid_account_bid_price(market_ask_price, account_bid_price):
        return market_ask_price - account_bid_price < 0

    @staticmethod
    def is_invalid_account_ask_price(market_bid_price, account_ask_price):
        return market_bid_price - account_ask_price > 0
