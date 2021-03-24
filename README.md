# App-TradeBot
App-Tradebot currently includes two applications. Algorithmic trading and Tax Management.

### Algorithmic trading
The application trades using the specified trading strategy. The current available trading strategy is volatility trading. READ the analysis and run a few simulation before running a Live run with real money. 

## Prerequisite 
* Bitstamp Account or Kraken account
* Gmail configured to allow less secure apps
* Docker and Docker Compose OR python3.6+ and a postgressql database setup

## Trading Account Configurations (Only used in live runs)
* Add your account configs to src/services/algorithmic_trading/src/resources/configs/trading_account-configs.ini
* Then run git update-index --assume-unchanged src/services/algorithmic_trading/src/resources/configs/trading_account-configs.ini 

## Trading Strategy Configurations
* Change default configs by altering src/services/algorithmic_trading/src/resources/configs/strategy-config.ini
* Then run git update-index --assume-unchanged src/services/algorithmic_trading/src/resources/configs/strategy-config.ini 

## Taxable Account Configurations (Only used in live runs)
* Add your taxable accounts configs to src/services/tax_management/src/resources/configs/taxable_account-configs.yaml
* Then run git update-index --assume-unchanged src/services/algorithmic_trading/src/resources/configs/taxable_account-configs.yaml

## Docker Run (Recommended)
* sudo docker-compose build (only required first time)
* sudo docker-compose up -d (starts the postgres database)
* sudo docker-compose run app \<args\>
* Use arg -h the show available trading strategies: sudo docker-compose run app -h

## Native Run
* Setup the postgres database. See the docker-compose.yaml for configs
* pip3 install -r requirements.txt
* From the src directory run: python main.py
* Use arg -h the show available trading strategies: python main.py -h
