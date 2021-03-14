from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


def main():
    #  exchange_api = KrakenApiImpl('EUR',
    #                               'XRP',
    #                               KrakenWebsocket('USD', 'XRP', ),
    #                                TradeBotUtils.get_kraken_api_key(),
    #                                TradeBotUtils.get_kraken_api_secret())

    # TODO: How is order id returned
    # TODO: Check hwo to get the fee after trade

    # print(exchange_api.get_accrued_account_fees())
    # print(TradeBotUtils.get_information_log_path("t"))

    print(TradeBotUtils.convert_epoch_time_to_timestamp('1615042047.4079'))


if __name__ == '__main__':
    main()
