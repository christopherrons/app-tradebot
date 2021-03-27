import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils
from applications.common.src.main.database import DatabaseService


class PlotHandler:
    def __init__(self, exchange: str, cash_currency: str, crypto_currency: str, database_service: DatabaseService, is_live: bool):
        self.__exchange = exchange
        self.__cash_currency = cash_currency
        self.__crypto_currency = crypto_currency
        self.__database_service = database_service
        self.__is_live = is_live

        self.__initial_value = database_service.custom_read_query(
            query=f"SELECT initial_account_value_{cash_currency} FROM trade_data.initial_account_value"
                  f" WHERE exchange = %s;",
            data=[exchange])

        self.__currency_symbols = TradeBotUtils.get_cash_currency_symbols()
        self.__subplot_rows = 3
        self.__subplot_columns = 1

    def create_visual_trade_report(self):
        fig1 = self.__plot_profits()
        fig2 = self.__plot_trade_values()
        self.__save_report(fig1, fig2)

    def __plot_profits(self):
        fig = make_subplots(rows=self.__subplot_rows, cols=self.__subplot_columns,
                            subplot_titles=(f'Cash Profit per Successful Cycle [{self.__currency_symbols[self.__cash_currency]}]',
                                            f'Percent Profit per Successful Cycle [%]'))

        transaction_df = self.__database_service.get_transactions_as_dataframe(self.__exchange, self.__is_live, self.__cash_currency, self.__crypto_currency)
        self.__plot_cash_profits(fig, transaction_df.loc[transaction_df['buy'] == False]['net_trade_value'].reset_index(drop=True))
        self.__plot_percent_profits(fig, transaction_df.loc[transaction_df['buy'] == False]['net_trade_value'].reset_index(drop=True))
        return fig

    def __plot_cash_profits(self, fig: Figure, net_sell_values: DataFrame):
        if not net_sell_values.empty:
            nr_successful_cycles = net_sell_values.index.to_list()
            cash_profits = net_sell_values.subtract(self.__initial_value).sort_values()
            self.__create_line_plot(fig=fig, x_axis=nr_successful_cycles, y_axis=cash_profits,
                                    line_name='Profit', x_axis_title='Successfully Cycle',
                                    y_axis_title=f'Profit [{self.__currency_symbols[self.__cash_currency]}]', mode='lines', row=1, col=1)

    def __plot_percent_profits(self, fig: Figure, net_sell_values: DataFrame):
        if not net_sell_values.empty:
            nr_successful_cycles = net_sell_values.index.to_list()
            percent_profits = net_sell_values.divide(self.__initial_value).subtract(1).multiply(100).sort_values()
            self.__create_line_plot(fig=fig, x_axis=nr_successful_cycles, y_axis=percent_profits,
                                    line_name='Profit', x_axis_title='Successful Cycle', y_axis_title='Profit [%]', mode='lines', row=2, col=1)

    def __plot_trade_values(self):
        transaction_df = self.__database_service.get_transactions_as_dataframe(self.__exchange, self.__is_live, self.__cash_currency, self.__crypto_currency)
        fig = px.scatter(transaction_df, x="trade_number", y="net_trade_value", color="buy",
                         title=f'Net Trade Values [{self.__currency_symbols[self.__cash_currency]}]')
        fig.update_xaxes(title_text='Successful Trade')
        fig.update_yaxes(title_text=f'Trade Value on {self.__exchange}]')
        return fig

    def __create_line_plot(self, fig: Figure, x_axis: list, y_axis: list, line_name: str, x_axis_title: str,
                           y_axis_title: str, mode: str, row: int, col: int):
        fig.add_trace(go.Scatter(x=x_axis, y=y_axis, mode=mode, name=line_name), row=row, col=col)
        fig.update_xaxes(title_text=x_axis_title, row=row, col=col)
        fig.update_yaxes(title_text=y_axis_title, row=row, col=col)

    def __save_report(self, fig1: Figure, fig2: Figure):
        with open(TradeBotUtils.get_trade_report_path(self.__exchange), 'w+') as f:
            f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
            f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
