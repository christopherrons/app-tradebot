import time

from Services.Runner.Exchange.BitstampAPIAction import BitstampAPIAction
from Services.Runner.Utils.TradeBotUtils import TradeBotUtils


def main():
    exchange_api = BitstampAPIAction(TradeBotUtils.get_customer_ID(),
                                     TradeBotUtils.get_api_key(),
                                     TradeBotUtils.get_api_secret())

    # print(exchange_api.get_account_cash_value())
    print(exchange_api.get_transaction_fee(1332994931982336))
    # print(exchange_api.get_order_status(1332881377312771))


# print(exchange_api.get_open_orders())
# print(exchange_api.get_transaction_fee())

if __name__ == '__main__':
    main()
