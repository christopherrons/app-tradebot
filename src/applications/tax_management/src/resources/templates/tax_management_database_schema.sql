CREATE SCHEMA IF NOT EXISTS tax_management;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" SCHEMA tax_management;

CREATE TABLE IF NOT EXISTS tax_management.trades (
  order_id VARCHAR(100) DEFAULT trade_data.uuid_generate_v4() NOT NULL,
  live BOOLEAN NOT NULL,
  exchange VARCHAR(100) NOT NULL,
  datetime TIMESTAMP NOT NULL,
  account_trade_number INT NOT NULL,
  buy BOOLEAN NOT NULL,
  price NUMERIC (20, 10) NOT NULL,
  cash_currency VARCHAR(100) NOT NULL,
  quantity NUMERIC (20, 10) NOT NULL,
  crypto_currency VARCHAR(100) NOT NULL,
  fee NUMERIC(20, 10) NOT NULL,
  gross_trade_value NUMERIC(20, 10) NOT NULL,
  net_trade_value NUMERIC(20, 10) NOT NULL,
  PRIMARY KEY(order_id, exchange, datetime)
)