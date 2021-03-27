import pandas as pd
from pandas import DataFrame

from applications.common.src.main.utils.PrinterUtils import PrinterUtils
from applications.tax_management.src.main.tax_services.TaxService import TaxService
from applications.tax_management.src.main.utils.TaxManagementUtils import TaxManagementUtils


class SwedishTaxService(TaxService):
    def __init__(self, year: str, crypto_currency: str):
        super().__init__(year, crypto_currency)
        self.__tax_percent = 0.3

    def create_yearly_tax_report(self):
        TaxManagementUtils.create_target_folder()
        self.init_tax_management_database_schema()
        self.insert_all_trades_to_database()
        calculated_transactions = self.tax_calculations()
        self.__save_tax_report(calculated_transactions)

    def tax_calculations(self) -> list:
        transactions = self.__get_transactions()
        self.__log_transactions(transactions)

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

            calculated_transactions.append([transaction['datetime'], "Köp" if transaction["buy"] else "Sälj", total_quantity, total_overhead_value,
                                            avg_overhead_value, "" if profit == 0 else profit,
                                            "" if profit == 0 else profit * self.__tax_percent, "", total_profit, total_profit * self.__tax_percent])

        return calculated_transactions

    def __save_tax_report(self, calculated_transactions: list):
        headers = ["Datum", "Händelse", "Totalt Antal", "Total Omkostnadsbelopp [SEK]", "Genomsnittligt Omkostnadsbelopp [SEK]", "Vinst [SEK]",
                   "Skatt [SEK]", "", "Total Vinst [SEK]", "Total Skatt [SEK]"]
        calculated_transactions_df = pd.DataFrame(calculated_transactions, columns=headers)
        calculated_transactions_df.to_csv(TaxManagementUtils.get_tax_report_log_path("All"))

        calculated_sell_transactions_df = calculated_transactions_df.loc[calculated_transactions_df['Händelse'] == "Sälj"]
        calculated_transactions_df = calculated_sell_transactions_df.loc[calculated_sell_transactions_df['Datum'].dt.year == self._year]
        calculated_transactions_df.to_csv(TaxManagementUtils.get_tax_report_log_path(self._year))
        PrinterUtils.console_log(message="Tax Report Saved")

    def __get_transactions(self) -> DataFrame:
        query = f"SELECT * FROM tax_management.trades WHERE crypto_currency = '{self._crypto_currency}'"
        transactions = self._database_service.custom_read_query_to_dataframe(query=query).sort_values(by=['datetime']).reset_index(drop=True)
        self.__convert_currencies(transactions)
        return transactions

    def __log_transactions(self, transactions: DataFrame):
        transactions.to_csv(TaxManagementUtils.get_transaction_log_path(self._year))

    def __convert_currencies(self, transactions: DataFrame):
        columns_to_convert = ['fee', "gross_trade_value", "net_trade_value"]
        for column in columns_to_convert:
            transactions[column] = transactions.apply(lambda x: x[column] if x['cash_currency'] == 'sek'
            else self._currency_converter.convert_currency(value=x[column], from_currency=x['cash_currency'], to_currency='sek',
                                                           date=x['datetime'].strftime("%Y-%m-%d")), axis=1)
