import csv
import os

from tabulate import tabulate


class PrinterUtils:

    @staticmethod
    def print_data_as_tabulate(headers: list, output: list):
        tabulated_output = tabulate([output], headers=headers)
        print("\n" + tabulated_output + "\n\n\n\n\n")

    @staticmethod
    def log_data(headers: list, output: list, file_path: str):
        with open(file_path, 'a+') as f:
            writer = csv.writer(f)
            if os.stat(file_path).st_size == 0:
                writer.writerow(headers)
                writer.writerow(output)
            else:
                writer.writerow(output)

    @staticmethod
    def console_log(message: str):
        print(f'\n-- {message}')
