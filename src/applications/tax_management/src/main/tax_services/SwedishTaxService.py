import math

import pandas as pd
from pandas import DataFrame

from applications.common.src.main.utils.PrinterUtils import PrinterUtils
from applications.tax_management.src.main.tax_services.TaxService import TaxService
from applications.tax_management.src.main.utils.TaxManagementUtils import TaxManagementUtils


class SwedishTaxService(TaxService):
    def __init__(self, year: str):
        super().__init__(year)
        self.__tax_percent = 0.3

    def create_yearly_tax_report(self):
        TaxManagementUtils.create_target_folder()
        self.init_tax_management_database_schema()
        self.insert_all_trades_to_database()
        self.tax_calculations()

    def tax_calculations(self):
        PrinterUtils.console_log("Calculating!")
        all_transactions = self.__get_transactions()
        for crypto_currency in all_transactions.crypto_currency.unique():
            transactions = all_transactions[all_transactions["crypto_currency"] == crypto_currency].reset_index(drop=True)
            self.__save_transactions(transactions, crypto_currency)

            total_overhead_value = 0
            avg_overhead_value = 0
            total_quantity = 0
            total_profit = 0
            calculated_transactions = []
            for idx in transactions.index.values:
                transaction = transactions.iloc[idx]

                if idx == 0:
                    total_quantity += transaction["quantity"]
                    total_overhead_value += transaction['net_trade_value']
                    avg_overhead_value = total_overhead_value / total_quantity
                    profit = 0
                else:
                    if transaction['buy']:
                        total_quantity += transaction["quantity"]
                        total_overhead_value += transaction['net_trade_value']
                        avg_overhead_value = total_overhead_value / total_quantity
                        profit = 0
                    else:
                        total_quantity -= transaction["quantity"]
                        total_overhead_value -= avg_overhead_value * transaction['quantity']
                        profit = transaction['net_trade_value'] - transaction['quantity'] * avg_overhead_value
                        total_profit += profit

                calculated_transactions.append(
                    [transaction['datetime'], "Köp" if transaction["buy"] else "Sälj", total_quantity, total_overhead_value,
                     avg_overhead_value, "" if profit <= math.pow(10, -5) else profit,
                     "" if profit <= math.pow(10, -5) else profit * self.__tax_percent, "", total_profit, total_profit * self.__tax_percent])

            self.__save_tax_report(calculated_transactions, crypto_currency)

    def __save_tax_report(self, calculated_transactions: list, crypto_currency: str):
        headers = ["Datum", "Händelse", "Totalt Antal", "Total Omkostnadsbelopp [SEK]", "Genomsnittligt Omkostnadsbelopp [SEK]", "Vinst [SEK]",
                   "Skatt [SEK]", "", "Total Vinst [SEK]", "Total Skatt [SEK]"]
        calculated_transactions_df = pd.DataFrame(calculated_transactions, columns=headers)
        calculated_transactions_df.index.name = 'Transaktions Nr'
        calculated_transactions_df.to_csv(TaxManagementUtils.get_generated_file_path(f"tax_report_{crypto_currency}_all.csv"))

        self.__save_tax_report_yearly_sales_per_crypto_currency(calculated_transactions_df, crypto_currency)

    def __save_tax_report_yearly_sales_per_crypto_currency(self, calculated_transactions_df: DataFrame, crypto_currency: str):
        calculated_sell_transactions_df = calculated_transactions_df.loc[calculated_transactions_df['Händelse'] == "Sälj"]
        calculated_transactions_df = calculated_sell_transactions_df.loc[calculated_sell_transactions_df['Datum'].dt.year == self._year]
        calculated_transactions_df.to_csv(TaxManagementUtils.get_generated_file_path(f"tax_report_{crypto_currency}_{self._year}.csv"))
        PrinterUtils.console_log(message=f"Tax Report Saved for {crypto_currency}")

    def __get_transactions(self) -> DataFrame:
        query = f"SELECT * FROM tax_management.trades"
        transactions = self._database_service.custom_read_query_to_dataframe(query=query).sort_values(by=['datetime']).reset_index(drop=True)
        self.__convert_currencies(transactions)
        return transactions

    def __save_transactions(self, transactions: DataFrame, crypto_currency: str):
        transactions.index.name = 'Transaktions Nr'
        transactions.to_csv(TaxManagementUtils.get_generated_file_path(f"transaction_log_{crypto_currency}.csv"))

    def __convert_currencies(self, transactions: DataFrame):
        columns_to_convert = ['fee', "gross_trade_value", "net_trade_value"]
        for column in columns_to_convert:
            transactions[column] = transactions.apply(lambda x: x[column] if x['cash_currency'] == 'sek'
            else self._currency_converter.convert_currency(value=x[column], from_currency=x['cash_currency'], to_currency='sek',
                                                           date=x['datetime'].strftime("%Y-%m-%d")), axis=1)
