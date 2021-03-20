# App-TradeBot
Analysis and implementation of cryptocurrency tradebot. The application trades using a simple volatility trading trategy. READ analysis and run a few simulation before running a Live run with real money. 

## Prerequisite 
* Bitstamp Account or Kraken account
* Gmail configured to allow less secure apps
* Docker and Docker Compose OR python3.6+ and a postgressql database setup

## Account Configurations
* Add your account configs to src/services/algorithmic_trading/src/resources/configs/account-config.ini
* Then run git update-index --assume-unchanged src/services/algorithmic_trading/src/resources/configs/account-config.ini 

## Trading Strategy Configurations
* Change default configs by altering src/services/algorithmic_trading/src/resources/configs/strategy-config.ini
* Then run git update-index --assume-unchanged src/services/algorithmic_trading/src/resources/configs/strategy-config.ini 

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
