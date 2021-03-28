from abc import ABC, abstractmethod

from applications.common.src.main.converters.CurrencyConverter import CurrencyConverter
from applications.common.src.main.database.TaxManagementDao import TaxManagementDao
from applications.common.src.main.exchanges.BitstampApiImpl import BitstampApiImpl
from applications.common.src.main.exchanges.KrakenApiImpl import KrakenApiImpl
from applications.tax_management.src.main.utils.TaxManagementUtils import TaxManagementUtils


class TaxService(ABC):
    def __init__(self, year: str):
        self._year = int(year)
        self._database_service = TaxManagementDao()
        self._currency_converter = CurrencyConverter()

    @abstractmethod
    def tax_calculations(self):
        pass

    def init_tax_management_database_schema(self):
        self._database_service.run_queries_from_file(file_path=TaxManagementUtils.get_template_file_path("tax_management_database_schema.sql"))

    def insert_all_trades_to_database(self):
        trading_accounts = TaxManagementUtils.get_taxable_trading_accounts()
        for exchange in trading_accounts.keys():
            exchange_accounts = trading_accounts[exchange]
            for account in exchange_accounts.keys():
                account_data = exchange_accounts[account]
                if exchange == 'bitstamp':
                    BitstampApiImpl(cash_currency="",
                                    crypto_currency="",
                                    customer_id=account_data["customer_id"],
                                    api_key=account_data["api_key"],
                                    api_secret=account_data["api_secret"]).init_trades_to_database_from_exchange(self._database_service)

                elif exchange == 'kraken':
                    KrakenApiImpl(cash_currency="",
                                  crypto_currency="",
                                  api_key=account_data["api_key"],
                                  api_secret=account_data["api_secret"]).init_trades_to_database_from_exchange(self._database_service)
