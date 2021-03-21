import decimal
from datetime import datetime

import pandas.io.sql as sqlio
import psycopg2
from pandas import DataFrame

from applications.algorithmic_trading.src.main.calculators.CurrencyConverter import CurrencyConverter
from applications.algorithmic_trading.src.main.output_handlers.utils.PrinterUtils import PrinterUtils
from applications.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class SqlError(object):
    pass


class DatabaseService:
    def __init__(self):
        self.__conn = psycopg2.connect(
            host="db",
            database="postgres",
            user="postgres",
            password="password")
        self.__database_table_queries_path = TradeBotUtils.get_data_base_queries_path()
        self.__currency_converter = CurrencyConverter()

    def create_tables_if_not_exist(self):
        with open(self.__database_table_queries_path, 'r') as sql_file:
            queries = sql_file.read().strip().split(';')
        for query in [f'{query};' for query in queries]:
            self.__write_query(query=query, data=[])

        PrinterUtils.console_log(message=f'Query Executed: Created Tables if not Exist')

    def drop_all_tables(self):
        query = "SELECT table_name FROM information_schema.tables" \
                " WHERE table_schema = %s"
        data = ['trade_data']
        table_names = self.__read_query(query, data)
        table_names = ["trade_data." + table_name[0] for table_name in table_names]
        separator = ', '
        query = f"DROP TABLE {separator.join(table_names)}"
        data = []
        self.__write_query(query, data)
        PrinterUtils.console_log(message=f'Query Executed: Drop all Tables')

    def insert_trade_report(self, is_live: bool, exchange: str, trade_number: int, timestamp: datetime, order_id: str, buy: bool,
                            price: float, cash_currency: str, quantity: float, crypto_currency: str, fee: float,
                            gross_trade_value: float, net_trade_value: float):
        query = 'INSERT INTO trade_data.report(order_id, live, exchange,' \
                ' datetime, trade_number, buy, price, cash_currency,' \
                ' quantity, crypto_currency, fee, gross_trade_value, net_trade_value) ' \
                'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;'
        data = [order_id, is_live, exchange.lower(), timestamp, trade_number, buy,
                price, cash_currency.lower(), quantity, crypto_currency.lower(), fee, gross_trade_value, net_trade_value]

        self.__write_query(query=query, data=data)

        PrinterUtils.console_log(message=f'Query Executed: Insert Trade Report')

    def get_accrued_account_fees(self, exchange: str, cash_currency: str, is_live: bool) -> float:
        accrued_fee = 0
        for currency in TradeBotUtils.get_permitted_cash_currencies():
            query = "SELECT SUM(fee) from trade_data.report" \
                    " WHERE live = %s" \
                    " AND exchange = %s" \
                    " AND cash_currency = %s;"
            data = [is_live, exchange.lower(), currency.lower()]
            result = self.__read_query(query=query,
                                       data=data)[0][0]
            if result:
                accrued_fee += self.__currency_converter.convert_currency(value=float(result),
                                                                          from_currency=currency,
                                                                          to_currency=cash_currency)

        PrinterUtils.console_log(message=f'Query Executed: Get Accrued Account Fees')
        return float(accrued_fee)

    def get_nr_successful_trades(self, exchange: str, is_live: bool) -> int:
        query = "SELECT MAX(trade_number) from trade_data.report" \
                " WHERE live = %s" \
                " AND exchange = %s;"
        data = [is_live, exchange.lower()]
        result = self.__read_query(query=query, data=data)[0][0]

        PrinterUtils.console_log(message=f'Query Executed: Get nr of Successful Trade')
        return int(result) if result else 0

    def get_nr_successful_cycles(self, exchange: str, is_live: bool) -> int:
        query = "SELECT COUNT(trade_number) from trade_data.report" \
                " WHERE live = %s " \
                " AND buy = false" \
                " AND exchange = %s;"
        data = [is_live, exchange.lower()]
        result = self.__read_query(query=query, data=data)[0][0]
        PrinterUtils.console_log(message=f'Query Executed: Get nr of Successful Cycles')
        return int(result) if result else 0

    def get_transaction_as_dataframe(self, exchange: str, is_live: bool, cash_currency: str) -> DataFrame:  # TODO add currency converter
        query = "SELECT buy, cash_currency, net_trade_value, trade_number from trade_data.report" \
                " WHERE live = {}" \
                " AND exchange = '{}';" \
            .format(is_live, exchange.lower())
        transaction_df = self.__read_to_dataframe(query)
        transaction_df['net_trade_value'] = transaction_df.apply(
            lambda x: x['net_trade_value'] if x['cash_currency'] == cash_currency else
            self.__currency_converter.convert_currency(value=x['net_trade_value'], from_currency=x['cash_currency'], to_currency=cash_currency),
            axis=1)
        PrinterUtils.console_log(message=f'Query Executed: Get Transaction as DataFrame')
        return transaction_df

    def get_initial_account_value(self, exchange: str, is_live: bool, cash_currency: str) -> float:
        query = f"SELECT initial_account_value_{cash_currency.lower()} from trade_data.initial_account_value" \
                f" WHERE exchange = %s" \
                f" AND live = %s;"
        data = [exchange, is_live]
        result = self.__read_query(query=query, data=data)

        PrinterUtils.console_log(message=f'Query Executed: Get initial Account Value')
        return float(result[0][0]) if result else 0

    def insert_or_update_initial_account_value(self, exchange: str, is_live: bool, account_value: float, cash_currency: str):
        query = "INSERT INTO trade_data.initial_account_value(exchange, live, initial_account_value_usd, initial_account_value_eur)" \
                " VALUES(%s, %s, %s, %s)" \
                " ON CONFLICT (exchange, live) " \
                " DO UPDATE" \
                " SET" \
                " initial_account_value_usd = excluded.initial_account_value_usd," \
                " initial_account_value_eur = excluded.initial_account_value_eur;"
        data = [exchange, is_live, self.__currency_converter.convert_currency(account_value, cash_currency, 'usd'),
                self.__currency_converter.convert_currency(account_value, cash_currency, 'eur')]
        self.__write_query(query=query, data=data)

        PrinterUtils.console_log(message=f'Query Executed: Insert initial Account Value')

    def custom_read_query(self, query, data):
        result = self.__read_query(query, data)[0][0]
        if isinstance(result, decimal.Decimal):
            return float(result)
        if isinstance(result, str):
            return str(result)
        PrinterUtils.console_log(message=f'Custom Query Executed')
        return result

    def __read_to_dataframe(self, query: str) -> DataFrame:
        return sqlio.read_sql_query(query, self.__conn)

    def __read_query(self, query: str, data: list):
        cursor = self.__conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        self.__conn.commit()
        result = cursor.fetchall()
        cursor.close()
        return result

    def __write_query(self, query: str, data: list):
        cursor = self.__conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        self.__conn.commit()
        cursor.close()

    def close_connection(self):
        self.__conn.close()
