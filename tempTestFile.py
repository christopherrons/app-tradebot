from services.algorithmic_trading.src.main.output_handlers.PlotHandler import PlotHandler


def main():
    #  exchange_api = KrakenApiImpl('EUR',
    #                               'XRP',
    #                               KrakenWebsocket('USD', 'XRP', ),
    #                             TradeBotUtils.get_kraken_api_key(),
    #                             TradeBotUtils.get_kraken_api_secret())

    # TODO: How is order id returned
    # TODO: Check hwo to get the fee after trade

    # print(exchange_api.get_accrued_account_fees())
    # print(TradeBotUtils.get_information_log_path("t"))
    plot_handler = PlotHandler(100, 0.1, 'Bitstamp', 'usd', 'xrp')
    plot_handler.create_visual_trade_report()


if __name__ == '__main__':
    main()
