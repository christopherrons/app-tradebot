import csv
import os

from tabulate import tabulate


class PrinterUtils:

    @staticmethod
    def print_data_as_tabulate(headers, output):
        tabulated_output = tabulate([output], headers=headers)
        print(tabulated_output + "\n\n\n\n\n\n")

    @staticmethod
    def log_data(headers, output, file_path):
        with open(file_path, 'a+') as f:
            writer = csv.writer(f)
            if os.stat(file_path).st_size == 0:
                writer.writerow(headers)
                writer.writerow(output)
            else:
                writer.writerow(output)
