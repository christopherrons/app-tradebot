from datetime import datetime

from applications.common.src.main.database.DatabaseService import DatabaseService
from applications.common.src.main.utils.PrinterUtils import PrinterUtils


class TaxManagementDao(DatabaseService):
    def __init__(self):
        super().__init__()

    def insert_trade_report(self, is_live: bool, exchange: str, trade_number: int, timestamp: datetime, order_id: str, buy: bool, price: float,
                            cash_currency: str, quantity: float, crypto_currency: str, fee: float, gross_trade_value: float, net_trade_value: float):
        query = f'INSERT INTO tax_management.trades(order_id, live, exchange,' \
                ' datetime, trade_number, buy, price, cash_currency,' \
                ' quantity, crypto_currency, fee, gross_trade_value, net_trade_value) ' \
                'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;'
        data = [order_id, is_live, exchange.lower(), timestamp, trade_number, buy,
                price, cash_currency.lower(), quantity, crypto_currency.lower(), fee, gross_trade_value, net_trade_value]

        self.write_query(query=query, data=data)

        PrinterUtils.console_log(message=f'Query Executed: Insert Trade Report')
