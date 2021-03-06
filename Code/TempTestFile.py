from Services.Runner.Exchange.BitstampAPIAction import BitstampAPIAction
from Services.Runner.Utils.TradeBotUtils import TradeBotUtils


def main():
    exchange_api = BitstampAPIAction(TradeBotUtils.get_bitstamp_customer_ID(),
                                     TradeBotUtils.get_bitstamp_api_key(),
                                     TradeBotUtils.get_bitstamp_api_secret())

    print(exchange_api.get_successful_cycles())


# print(exchange_api.get_open_orders())
# print(exchange_api.get_transaction_fee())

if __name__ == '__main__':
    main()
