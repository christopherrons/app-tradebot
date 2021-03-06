from Services.Runner.Exchange.KrakenApiImpl import KrakenApiImpl
from Services.Runner.Exchange.KrakenWebsocket import KrakenWebsocket
from Services.Runner.Utils.TradeBotUtils import TradeBotUtils


def main():
    exchange_api = KrakenApiImpl(KrakenWebsocket(),
                                 TradeBotUtils.get_kraken_api_key(),
                                 TradeBotUtils.get_kraken_api_secret())

    # TODO: How is order id returned
    # TODO: Check hwo to get the fee after trade


if __name__ == '__main__':
    main()
