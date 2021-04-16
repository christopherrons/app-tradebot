import math
from datetime import date

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
        all_transactions = self.__get_transactions()
        k4_values = []
        for crypto_currency in all_transactions.crypto_currency.unique():
            PrinterUtils.console_log(f"Calculating for {crypto_currency}! --")
            transactions = all_transactions[all_transactions["crypto_currency"] == crypto_currency].reset_index(drop=True)
            self.__save_transactions(transactions, crypto_currency)

            total_overhead_value = 0
            avg_overhead_value = 0
            total_quantity = -self.reserved_xrp() if crypto_currency == "xrp" else 0
            total_profit = 0
            overhead_value_calculations = []
            for idx in transactions.index.values:
                transaction = transactions.iloc[idx]

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

                    if transaction["quantity"] >= math.pow(10, -5):
                        k4_values.append([transaction['datetime'],
                                          crypto_currency, transaction["quantity"],
                                          transaction['net_trade_value'],
                                          transaction["quantity"] * avg_overhead_value])

                overhead_value_calculations.append(
                    [transaction['datetime'],
                     "Köp" if transaction["buy"] else "Sälj",
                     total_quantity, total_overhead_value,
                     avg_overhead_value,
                     "" if profit <= math.pow(10, -5) else profit,
                     "" if profit <= math.pow(10, -5) else profit * self.__tax_percent, "", total_profit, total_profit * self.__tax_percent]
                )

            self.__save_overhead_value_calulations(overhead_value_calculations, crypto_currency)
            self.__print_current_values(total_quantity, total_overhead_value, avg_overhead_value, total_profit)

        if k4_values:
            self.__save_k4(k4_values)

    def __print_current_values(self, total_quantity: float, total_overhead_value: float, avg_overhead_value: float,
                               total_profit: float):
        headers = ["Date", "Total Quantity", "Total Overhead Value", "Average Overhead value", "Total Profit", "Total Tax"]
        output = [date.today(), total_quantity, total_overhead_value, avg_overhead_value, total_profit, total_profit * self.__tax_percent]
        PrinterUtils.console_log(message=f"Current State --")
        PrinterUtils.print_data_as_tabulate(headers=headers, output=output)

    def __save_k4(self, k4_values: list):
        headers = ["Datum", "Beteckning", "Antal", "Försäljningspris", "Omkostnadsbelopp"]
        k4_values_df = pd.DataFrame(k4_values, columns=headers)
        k4_df = k4_values_df.loc[k4_values_df['Datum'].dt.year == self._year]
        k4_df.to_csv(TaxManagementUtils.get_generated_file_path(f"k4_{self._year}.csv"))

    def __save_overhead_value_calulations(self, overhead_value_calculations: list, crypto_currency: str):
        headers = ["Datum", "Händelse", "Totalt Antal", "Total Omkostnadsbelopp [SEK]", "Genomsnittligt Omkostnadsbelopp [SEK]", "Vinst [SEK]",
                   "Skatt [SEK]", "", "Total Vinst [SEK]", "Total Skatt [SEK]"]
        overhead_value_calculations_df = pd.DataFrame(overhead_value_calculations, columns=headers)
        overhead_value_calculations_df.index.name = 'Transaktions Nr'
        overhead_value_calculations_df.to_csv(TaxManagementUtils.get_generated_file_path(f"overhead_value_calculations_{crypto_currency}_all.csv"))

        self.__save_tax_report_yearly_sales_per_crypto_currency(overhead_value_calculations_df, crypto_currency)

    def __save_tax_report_yearly_sales_per_crypto_currency(self, overhead_value_calculations_df: DataFrame, crypto_currency: str):
        calculated_sell_transactions_df = overhead_value_calculations_df.loc[overhead_value_calculations_df['Händelse'] == "Sälj"]
        overhead_value_calculations_df = calculated_sell_transactions_df.loc[calculated_sell_transactions_df['Datum'].dt.year == self._year]
        overhead_value_calculations_df.to_csv(
            TaxManagementUtils.get_generated_file_path(f"overhead_value_calculations_sales_{crypto_currency}_{self._year}.csv"))
        PrinterUtils.console_log(message=f"Tax Report {self._year} Saved for {crypto_currency}")

    def __get_transactions(self) -> DataFrame:
        PrinterUtils.console_log("Fetching Transactions from Database")
        query = f"SELECT * FROM tax_management.trades"
        transactions = self._database_service.custom_read_query_to_dataframe(query=query).sort_values(by=['datetime']).reset_index(drop=True)
        self.__convert_currencies(transactions)
        return transactions

    def __save_transactions(self, transactions: DataFrame, crypto_currency: str):
        transactions.index.name = 'Transaktions Nr'
        transactions.to_csv(TaxManagementUtils.get_generated_file_path(f"transaction_log_{crypto_currency}.csv"))

    def __convert_currencies(self, transactions: DataFrame):
        PrinterUtils.console_log(message="Converting values to SEK")
        columns_to_convert = ['fee', "gross_trade_value", "net_trade_value"]
        for column in columns_to_convert:
            transactions[column] = transactions.apply(lambda x:
                                                      x[column] if x['cash_currency'] == 'sek'
                                                      else self._currency_converter.convert_currency_from_api(value=x[column],
                                                                                                              from_currency=x['cash_currency'],
                                                                                                              to_currency='sek',
                                                                                                              date=x['datetime'].strftime(
                                                                                                                  "%Y-%m-%d")), axis=1)
