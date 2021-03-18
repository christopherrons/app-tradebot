from datetime import datetime

import pandas.io.sql as sqlio
import psycopg2
from pandas import DataFrame

from services.algorithmic_trading.src.main.calculators.CurrencyConverter import CurrencyConverter
from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


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

        self.create_tables_if_not_exist()

    def create_tables_if_not_exist(self):
        with open(self.__database_table_queries_path, 'r') as sql_file:
            queries = sql_file.read().strip().split(';')
        for query in [f'{query};' for query in queries]:
            self.__write_query(query=query, data=[])

        print(f'\n--Query Executed: Created Tables if not Exist\n')

    def insert_trade_report(self, is_simulation: bool, exchange: str, timestamp: datetime, order_id: str, trade_number: int, buy: bool,
                            price: float, cash_currency: str, quantity: float, crypto_currency: str, fee: float,
                            gross_trade_value: float, net_trade_value: float):
        query = 'INSERT INTO trade_data.report(order_id, simulation, exchange,' \
                ' datetime, trade_number, buy, price, cash_currency,' \
                ' quantity, crypto_currency, fee, gross_trade_value, net_trade_value) ' \
                'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;'
        data = [order_id, is_simulation, exchange.lower(), timestamp, trade_number, buy,
                price, cash_currency.lower(), quantity, crypto_currency.lower(), fee, gross_trade_value, net_trade_value]

        self.__write_query(query=query, data=data)

        print(f'\n--Query Executed: Insert Trade Report\n')

    def get_accrued_account_fees(self, exchange: str, cash_currency: str, is_simulation: bool) -> float:
        accrued_fee = 0
        for currency in TradeBotUtils.get_permitted_cash_currencies():
            query = "SELECT SUM(fee) from trade_data.report WHERE simulation = %s AND exchange = %s AND cash_currency = %s;"
            data = [is_simulation, exchange.lower(), currency.lower()]
            result = self.__read_query(query=query,
                                       data=data)[0][0]
            if result:
                accrued_fee += self.__currency_converter.convert_currency(value=float(result),
                                                                          from_currency=currency,
                                                                          to_currency=cash_currency)

        print(f'\n--Query Executed: Get Accrued Account Fees\n')
        return accrued_fee

    def get_nr_successful_trades(self, exchange: str, is_simulation: bool) -> int:
        query = "SELECT MAX(trade_number) from trade_data.report WHERE simulation = %s AND exchange = %s;"
        data = [is_simulation, exchange.lower()]
        result = self.__read_query(query=query, data=data)[0][0]

        print(f'\n--Query Executed: Get nr of Successful Trade\n')
        return int(result) if result else 0

    def get_nr_successful_cycles(self, exchange: str, is_simulation: bool) -> int:
        query = "SELECT COUNT(trade_number) from trade_data.report WHERE simulation = %s AND buy = false AND exchange = %s;"
        data = [is_simulation, exchange.lower()]
        result = self.__read_query(query=query, data=data)[0][0]
        print(f'\n--Query Executed: Get nr of Successful Cycles\n')
        return int(result) if result else 0

    def get_transaction_as_dataframe(self, exchange: str, is_simulation: bool, cash_currency: str) -> DataFrame:  # TODO add currency converter
        query = "SELECT buy, cash_currency, net_trade_value, trade_number from trade_data.report WHERE simulation = {} AND exchange = '{}';" \
            .format(is_simulation, exchange.lower())
        transaction_df = self.__read_to_dataframe(query)
        transaction_df['net_trade_value'] = transaction_df.apply(
            lambda x: x['net_trade_value'] if x['cash_currency'] == cash_currency else
            self.__currency_converter.convert_currency(value=x['net_trade_value'], from_currency=x['cash_currency'], to_currency=cash_currency),
            axis=1)

        print(f'\n--Query Executed: Get Transaction as DataFrame\n')
        return transaction_df

    def get_initial_account_value(self, exchange: str, cash_currency: str) -> float:
        query = f"SELECT initial_account_value_{cash_currency.lower()} from trade_data.initial_account_value WHERE exchange = %s;"
        data = [exchange]
        result = self.__read_query(query=query, data=data)

        print(f'\n--Query Executed: Get initial Account Value \n')
        return result[0][0] if result else 0

    def insert_or_update_initial_account_value(self, exchange: str, account_value: float, cash_currency: str):
        query = "INSERT INTO trade_data.initial_account_value(exchange, initial_account_value_usd, initial_account_value_eur)" \
                " VALUES(%s, %s, %s) ON CONFLICT DO NOTHING;"
        data = [exchange, self.__currency_converter.convert_currency(account_value, cash_currency, 'usd'),
                self.__currency_converter.convert_currency(account_value, cash_currency, 'eur')]
        self.__write_query(query=query, data=data)

        print(f'\n--Query Executed: Insert initial Account Value \n')

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
