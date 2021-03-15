from datetime import datetime

import psycopg2

from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


class SqlError(object):
    pass


class DatabaseService:
    def __init__(self):
        self.__conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="root321",
            port='5432')
        self.__database_table_queries_path = TradeBotUtils.get_data_base_queries_path()

    def create_tables_if_not_exist(self):
        with open(self.__database_table_queries_path, 'r') as sql_file:
            queries = sql_file.read().strip().split(';')

        self.__execute_query(queries=[f'{query};' for query in queries],
                             data=[],
                             message='Created Tables if not Exist')

    def insert_trade_session(self):
        pass

    def insert_trade_report(self, is_simulation: bool, exchange: str, timestamp: datetime, order_id: str, trade_number: int, buy: bool,
                            price: float, cash_currency: str, quantity: float, crypto_currency: str, fee: float,
                            gross_trade_value: float, net_trade_value: float):
        query = 'INSERT INTO trade_data.report(order_id, simulation, exchange,' \
                ' datetime, trade_number, buy, price, cash_currency,' \
                ' quantity, crypto_currency, fee, gross_trade_value, net_trade_value) ' \
                'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;'
        data = [order_id, is_simulation, exchange.lower(), timestamp, trade_number, buy,
                price, cash_currency.lower(), quantity, crypto_currency.lower(), fee, gross_trade_value, net_trade_value]

        self.__execute_query(queries=[query],
                             data=data,
                             message="Insert Trade Report")

    def get_accrued_account_fees(self, exchange: str) -> float:
        query = "SELECT SUM(fee) from trade_data.report WHERE simulation = false AND exchange = %s;"
        data = exchange.lower()
        return float(self.__execute_query(queries=[query],
                                          data=[data],
                                          message="Get Accrued Account Fees")[0][0])

    def get_nr_successful_trades(self, exchange: str) -> int:
        query = "SELECT MAX(trade_number) from trade_data.report WHERE simulation = false AND exchange = %s;"
        data = exchange.lower()
        return int(self.__execute_query(queries=[query],
                                        data=[data],
                                        message="Get nr of Successful Trade")[0][0])

    def get_nr_successful_cycles(self, exchange: str) -> int:
        query = "SELECT COUNT(trade_number) from trade_data.report WHERE simulation = false AND buy = false AND exchange = %s;"
        data = exchange.lower()
        return int(self.__execute_query(queries=[query],
                                        data=[data],
                                        message="Get nr of Successful Cycles")[0][0])

    def __execute_query(self, queries: list, data: list, message: str):
        cursor = self.__conn.cursor()
        result = ""
        for query in queries:
            print(query)
            print(data)
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.__conn.commit()
        result = cursor.fetchall()
        cursor.close()
        print(result)
        print(f'\n--Query Executed: {message}\n')
        return result
