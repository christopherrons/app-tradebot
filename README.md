# App-TradeBot
Analysis and implementation of cryptocurrency tradebot. The application trades using a simple volatility trading trategy. READ analysis and run a few simulation before running 

## Prerequisite 
* Bitstamp Account or Kraken account
* Gmail configured to allow less secure apps
* Docker and Docker Compose OR python3.6+ and a postgressql database setup

## Configurations
* Add your configs to src/services/algorithmic_trading/src/resources/configs/script-config.ini
* Then run git update-index --assume-unchanged src/services/algorithmic_trading/src/resources/configs/script-config.ini 

# Docker Run (Recommended)
* sudo docker-compose up --build -d 
* sudo docker-compose run app <args>
* Use arg -h for input options and instructions: sudo docker-compose run app -h

# Native Run
* Setup the postgres database. See the docker-compose.yaml for configs
* pip3 install -r requirements.txt
* From the src directory run: python main.py
* Use arg -h for input options and instructions: python main.py -h
