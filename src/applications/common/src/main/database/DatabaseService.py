import decimal

import pandas.io.sql as sqlio
import psycopg2
from pandas import DataFrame

from applications.common.src.main.converters.CurrencyConverter import CurrencyConverter
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class SqlError(object):
    pass


class DatabaseService:
    def __init__(self):
        self.__conn = psycopg2.connect(
            host="db",
            database="postgres",
            user="postgres",
            password="password")
        self._currency_converter = CurrencyConverter()

    def run_queries_from_file(self, file_path):
        with open(file_path, 'r') as sql_file:
            queries = sql_file.read().strip().split(';')
        for query in [f'{query};' for query in queries]:
            self.write_query(query=query, data=[])

        PrinterUtils.console_log(message=f'Query Executed: Run Queries from File')

    def drop_schema_tables(self, schema: str):
        query = "SELECT table_name FROM information_schema.tables" \
                " WHERE table_schema = %s"
        data = [schema]
        table_names = self.read_query(query, data)
        table_names = [f"{schema}." + table_name[0] for table_name in table_names]
        separator = ', '
        query = f"DROP TABLE {separator.join(table_names)}"
        self.write_query(query=query, data=[])

        PrinterUtils.console_log(message=f'Query Executed: Drop all Schema Tables')

    def custom_read_query_to_dataframe(self, query: str) -> DataFrame:
        return self.read_to_dataframe(query)

    def custom_read_query(self, query: str, data: list):
        result = self.read_query(query, data)[0][0]
        if isinstance(result, decimal.Decimal):
            return float(result)
        if isinstance(result, str):
            return str(result)
        PrinterUtils.console_log(message=f'Custom Query Executed')
        return result

    def read_to_dataframe(self, query: str) -> DataFrame:
        return sqlio.read_sql_query(query, self.__conn)

    def read_query(self, query: str, data: list) -> list:
        cursor = self.__conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        self.__conn.commit()
        result = cursor.fetchall()
        cursor.close()
        return result

    def write_query(self, query: str, data: list):
        cursor = self.__conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        self.__conn.commit()
        cursor.close()

    def close_connection(self):
        self.__conn.close()
