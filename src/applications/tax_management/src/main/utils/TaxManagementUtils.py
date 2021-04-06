import os

import yaml


class TaxManagementUtils:

    @staticmethod
    def create_target_folder():
        if not os.path.exists(os.path.join(os.path.dirname(__file__), f"../../../target")):
            os.mkdir(os.path.join(os.path.dirname(__file__), f"../../../target"))
            os.mkdir(os.path.join(os.path.dirname(__file__), f"../../../target/generated"))

    @staticmethod
    def get_generated_file_path(file_name):
        return os.path.join(os.path.dirname(__file__), f"../../../target/generated/{file_name}")

    @staticmethod
    def get_config_file_path(file_name):
        return os.path.join(os.path.dirname(__file__), f'../../resources/configs/{file_name}')

    @staticmethod
    def get_template_file_path(file_name):
        return os.path.join(os.path.dirname(__file__), f'../../resources/templates/{file_name}')

    @staticmethod
    def get_number_of_trading_exchanges():
        return len(TaxManagementUtils.get_taxable_trading_accounts().keys())

    @staticmethod
    def get_taxable_trading_accounts() -> dict:
        with open(TaxManagementUtils.get_config_file_path("taxable_account-configs.yaml"), "r") as f:
            return yaml.safe_load(f)['exchange']
