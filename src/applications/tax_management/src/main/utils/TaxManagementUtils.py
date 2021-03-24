import os

import yaml


class TaxManagementUtils:

    @staticmethod
    def create_target_folder():
        if not os.path.exists(os.path.join(os.path.dirname(__file__), f"../../../target")):
            os.mkdir(os.path.join(os.path.dirname(__file__), f"../../../target"))
            os.mkdir(os.path.join(os.path.dirname(__file__), f"../../../target/generated"))

    @staticmethod
    def get_tax_report_log_path(year) -> str:
        return os.path.join(os.path.dirname(__file__), f"../../../target/generated/tax_report_{year}.csv")

    @staticmethod
    def get_transaction_log_path(year) -> str:
        return os.path.join(os.path.dirname(__file__), f"../../../target/generated/transaction_log_{year}.csv")

    @staticmethod
    def get_tax_management_init_queries() -> str:
        return os.path.join(os.path.dirname(__file__), '../../resources/templates/tax_management_database_schema.sql')

    @staticmethod
    def get_trading_accounts_config_path():
        return os.path.join(os.path.dirname(__file__), '../../resources/configs/taxable_account-configs.yaml')

    @staticmethod
    def get_taxable_trading_accounts() -> dict:
        with open(TaxManagementUtils.get_trading_accounts_config_path(), "r") as f:
            return yaml.safe_load(f)['exchange']
