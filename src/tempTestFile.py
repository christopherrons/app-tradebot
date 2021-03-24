from applications.common.src.main.exchanges.KrakenApiImpl import KrakenApiImpl


def main():
    #  exchange_api = KrakenApiImpl('usd',
    #                               'xrp',
    #                               KrakenWebsocket('usd', 'xrp', ),
    #                                TradeBotUtils.get_kraken_api_key(),
    #                                TradeBotUtils.get_kraken_api_secret())

    # TODO: How is order id returned
    # TODO: Check hwo to get the fee after trade

    KrakenApiImpl().crypto_currency()


# print(currency_converter.convert_currency(10, 'usd', 'usd'))


if __name__ == '__main__':
    main()
