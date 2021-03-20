CREATE SCHEMA IF NOT EXISTS trade_data;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" SCHEMA trade_data;

CREATE TABLE IF NOT EXISTS trade_data.report (
  order_id VARCHAR(100) DEFAULT trade_data.uuid_generate_v4() NOT NULL,
  live BOOLEAN NOT NULL,
  exchange VARCHAR(100) NOT NULL,
  datetime TIMESTAMP NOT NULL,
  trade_number SERIAL NOT NULL,
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

CREATE TABLE IF NOT EXISTS trade_data.initial_account_value(
    exchange VARCHAR(100) NOT NULL,
    live BOOLEAN NOT NULL,
    initial_account_value_usd NUMERIC(20, 10) NOT NULL,
    initial_account_value_eur NUMERIC(20, 10) NOT NULL,
    PRIMARY KEY(exchange, live)
)