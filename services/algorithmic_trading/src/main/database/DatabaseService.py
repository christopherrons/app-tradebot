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
            queries = sql_file.read().strip().split(";")
        queries = [f'{query};' for query in queries]
        cursor = self.__conn.cursor()
        for query in queries:
            print(query)
            cursor.execute(query)
            self.__conn.commit()
        cursor.close()


    def get_connection(self):
        pass


    def create_tables_if_not_exists(self):
        pass
