from applications.algorithmic_trading.src.main.config_parses.VolatilityTradingConfigParser import VolatilityTradingConfigParser
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


def main():
    #  exchange_api = KrakenApiImpl('usd',
    #                               'xrp',
    #                               KrakenWebsocket('usd', 'xrp', ),
    #                                TradeBotUtils.get_kraken_api_key(),
    #                                TradeBotUtils.get_kraken_api_secret())

    # TODO: How is order id returned
    # TODO: Check hwo to get the fee after trade

    print(TradeBotUtils.get_exchange_fee('bitstamp'))



# print(currency_converter.convert_currency(10, 'usd', 'usd'))


if __name__ == '__main__':
    main()
