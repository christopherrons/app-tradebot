import psycopg2

from services.algorithmic_trading.src.main.utils.TradeBotUtils import TradeBotUtils


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
        queries = [f'{query};' for query in queries]
        self.__execute_query(queries)

    def insert_trade_report(self, exchange: str, timestamp, trade_number: int, buy: bool, sell: bool, price: float,
                            cash_currency: str, quantity: float, crypto_currency: str, fee: float,
                            gross_trade_value: float, net_trade_value: float):
        columns = f'INSERT INTO trade_data.report (trade_id, exchange,' \
                  f' datetime, trade_number, buy, sell, price, cash_currency,' \
                  f' quantity, crypto_currency,fee, gross_trade_value, net_trade_value)'
        data = f'VALUES ({exchange}, date {timestamp}, {trade_number}, {buy}, {sell}, {price}, {cash_currency},' \
               f' {quantity}, {crypto_currency}, {fee}, {gross_trade_value}, {net_trade_value});'

        query = [columns + data]
        self.__execute_query(query)

    def __execute_query(self, queries: list):
        cursor = self.__conn.cursor()
        for query in queries:
            cursor.execute(query)
            self.__conn.commit()
        cursor.close()
