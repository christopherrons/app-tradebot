CREATE SCHEMA IF NOT EXISTS trade_data;

CREATE TABLE IF NOT EXISTS trade_data.report (
  trade_id UUID NOT NULL,
  exchange VARCHAR(100) NOT NULL,
  datetime DATE NOT NULL,
  trade_number INT NOT NULL,
  buy BOOLEAN NOT NULL,
  sell BOOLEAN NOT NULL,
  price NUMERIC (10, 10) NOT NULL,
  cash_currency VARCHAR(100) NOT NULL,
  quantity NUMERIC (10, 10) NOT NULL,
  crypto_currency VARCHAR(100) NOT NULL,
  fee NUMERIC(10, 10) NOT NULL,
  gross_trade_value NUMERIC(10, 10) NOT NULL,
  net_trade_value NUMERIC(10, 10) NOT NULL
);

CREATE TABLE IF NOT EXISTS trade_data.run_session (
    trade_session UUID NOT NULL,
    datetime TIMESTAMP NOT NULL,
    initial_value NUMERIC(10, 10) NOT NULL,
    account_cash_value NUMERIC(10, 10) NOT NULL,
    cash_currency VARCHAR(100) NOT NULL,
    account_quantity NUMERIC(10, 10) NOT NULL,
    crypto_currency VARCHAR(100) NOT NULL,
    nr_successful_trades INT NOT NULL,
    nr_successful_cycles INT NOT NULL
)