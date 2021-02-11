import argparse
import os
from configparser import ConfigParser


class TradeBotUtils:
    @staticmethod
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass

    @staticmethod
    def get_bitstamp_token():
        if not os.path.exists(os.path.expanduser('~') + '/.script-config'):
            raise ValueError('No configuration file exists. Expected file: ~/.script-config')

        config = ConfigParser()
        config.read(os.path.expanduser('~') + '/.script-config')
        return config.get('Bitstamp', 'Token')

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
    def validate_args(args):
        if args.initial_value < 1:
            raise ValueError(f'Initial Value {args.initial_value} is to low. Minimum value is 1')

        if args.interest < 0.0100755031:
            raise ValueError(f'Interest {args.interest} is to low. Minimum value is 0.0100755031')

        if args.print_interval < 0:
            raise ValueError(f'Print Interval {args.print_interval} is to low. Minimum value is 0')

        if args.run_time_minutes < 1:
            raise ValueError(f'Run Time {args.run_time_minutes} is to low. Minimum value is 1')

        if args.run_time_minutes > 1000000:
            raise ValueError(f'Print Interval {args.run_time_minutes} is to high. Maximum value is 1000000')

        markets = ["xrpusd"]
        if args.market not in markets:
            raise ValueError(f'Market {args.market} is incorrect. Choose from {markets}')

    @staticmethod
    def set_initial_trade_price(bitstamp_api):
        account_bid_price = float('inf')
        bid_percent_diff = float('inf')
        is_invalid_account_bid_price = bitstamp_api.get_market_ask_price() - account_bid_price < 0 or bid_percent_diff > 0.03
        while is_invalid_account_bid_price:
            market_bid_price = bitstamp_api.get_market_bid_price()
            market_ask_price = bitstamp_api.get_market_ask_price()
            print(f'Market bid: {market_bid_price} \nMarket ask: {market_ask_price}\n')
            account_bid_price = float(input('Set start account bid price: '))
            bid_percent_diff = abs(1 - (market_bid_price / account_bid_price))
            is_invalid_account_bid_price = market_ask_price - account_bid_price < 0 or bid_percent_diff > 0.02
            if is_invalid_account_bid_price:
                print("ERROR: Account bid price has to be smaller than market ask price and max 3% diff from market price.")
            print("")

        print(
            f"Account Bid Price: {account_bid_price} [$]. \nNet Diff Market Ask: {bitstamp_api.get_market_ask_price() - account_bid_price} [$]."
            f"\nPercent Diff Market Ask {100 * ((bitstamp_api.get_market_ask_price() / account_bid_price) - 1)} [%]\n")
        return account_bid_price
