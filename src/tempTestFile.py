import plotly.graph_objects as go
from plotly.subplots import make_subplots

from services.algorithmic_trading.src.main.calculators.CurrencyConverter import CurrencyConverter
from services.algorithmic_trading.src.main.database.DatabaseService import DatabaseService
from services.algorithmic_trading.src.main.output_handlers.PlotHandler import PlotHandler


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
    currency_converter = CurrencyConverter()
    database_service = DatabaseService()
    database_service.insert_or_update_initial_account_value('bitstamp', 100, 'usd')
    print(database_service.get_initial_account_value('bitstamp', 'eur'))


# print(currency_converter.convert_currency(10, 'usd', 'usd'))


if __name__ == '__main__':
    main()
