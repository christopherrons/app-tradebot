from datetime import datetime

import psycopg2

from services.algorithmic_trading.src.main.calculators.CurrencyConverter import CurrencyConverter
from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class SqlError(object):
    pass


class DatabaseService:
    def __init__(self):
        self.__conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="root321",  # TODO move to file
            port='5432')
        self.__database_table_queries_path = TradeBotUtils.get_data_base_queries_path()
        self.__currency_converter = CurrencyConverter()

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

    def get_accrued_account_fees(self, exchange: str, cash_currency: str, is_simulation:bool) -> float:
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

    def get_transaction_net_value(self, exchange: str, is_simulation: bool, is_buy: bool) -> list: # TODO add currency converter
        query = "SELECT net_trade_value from trade_data.report WHERE buy = %s AND simulation = %s AND exchange = %s;"
        data = [is_buy, is_simulation, exchange.lower()]
        result = self.__read_query(query=query, data=data)

        print(f'\n--Query Executed: Get Transaction Net Value\n')
        return result

    def __read_query(self, query: str, data: list):
        cursor = self.__conn.cursor()
        print(query)
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
