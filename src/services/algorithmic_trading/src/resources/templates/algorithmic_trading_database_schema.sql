CREATE SCHEMA IF NOT EXISTS trade_data;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" SCHEMA trade_data;

CREATE TABLE IF NOT EXISTS trade_data.report (
  order_id VARCHAR(100) DEFAULT trade_data.uuid_generate_v4() NOT NULL,
  simulation BOOLEAN NOT NULL,
  exchange VARCHAR(100) NOT NULL,
  datetime TIMESTAMP NOT NULL,
  trade_number INT NOT NULL,
  buy BOOLEAN NOT NULL,
  price NUMERIC (20, 10) NOT NULL,
  cash_currency VARCHAR(100) NOT NULL,
  quantity NUMERIC (20, 10) NOT NULL,
  crypto_currency VARCHAR(100) NOT NULL,
  fee NUMERIC(20, 10) NOT NULL,
  gross_trade_value NUMERIC(20, 10) NOT NULL,
  net_trade_value NUMERIC(20, 10) NOT NULL,
  PRIMARY KEY(order_id, exchange, datetime)
);

CREATE TABLE IF NOT EXISTS trade_data.run_session (
    trade_session UUID NOT NULL,
    datetime TIMESTAMP NOT NULL,
    initial_value NUMERIC(20, 10) NOT NULL,
    account_cash_value NUMERIC(20, 10) NOT NULL,
    cash_currency VARCHAR(100) NOT NULL,
    account_quantity NUMERIC(20, 10) NOT NULL,
    crypto_currency VARCHAR(100) NOT NULL,
    nr_successful_trades INT NOT NULL,
    nr_successful_cycles INT NOT NULL
)