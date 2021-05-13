# App-TradeBot
App-Tradebot currently includes two applications. Algorithmic trading and Tax Management.

### Algorithmic trading
The application trades using the specified trading strategy. The current available trading strategy is volatility trading.
READ the analysis and run a few simulations before running a Live run with real money. 

### Tax Management
The application calculates the tax to be paid per cryptocurrency per year based on transactions made across different exchanges.
The logic to calculate the tax is based on the countries tax rules. Current available countries are Sweden. 

## Prerequisite 
* Bitstamp Account or Kraken account (Live run only)
* Gmail configured to allow less secure apps
* Docker and Docker Compose OR python3.6+ and a postgreSql database setup

## Trading Account Configurations (Live run only)
* Add your account configs to src/services/algorithmic_trading/src/resources/configs/trading_account-configs.ini
* Then run:
  
  `git update-index --assume-unchanged src/applications/algorithmic_trading/src/resources/configs/trading_account-configs.ini` 

## Trading Strategy Configurations
* Change default configs by altering src/services/algorithmic_trading/src/resources/configs/strategy-config.yaml
* Then run:
  
`git update-index --assume-unchanged src/applications/algorithmic_trading/src/resources/configs/strategy-configs.yaml`

## Taxable Account Configurations (Live run only)
* Add your taxable accounts configs to src/services/tax_management/src/resources/configs/taxable_account-configs.yaml
* Then run:
  
`git update-index --assume-unchanged src/applications/tax_management/src/resources/configs/taxable_account-configs.yaml`

## Docker Run (Recommended)
`sudo docker-compose build (only required first time)`

`sudo docker-compose up -d (starts the postgres database)`

`sudo docker-compose run app \<args\>`

 Use `arg -h` the show available trading strategies: `sudo docker-compose run app -h`

### Linux Users Only
Run as follows to get files with read/write access on the host:

`sudo docker-compose --user $(id -u):$(id -g) run ....`

## Native Run
Set up the postgres database. See the docker-compose.yaml for configs

Install requirements:
`pip3 install -r requirements.txt`

From the src directory run: python main.py
Use `arg -h` the show available trading strategies: `python main.py -h`
