# App-TradeBot
Analysis and implementation of cryptocurrency tradebot.

## Prerequisite 
* Bitstamp Account with a main / sub account (sub account is recommended for more control)
* Active api-key connected to the account 

## Run script instructions
* Run pip3 install -r requirements.txt to install relevant external libraries
* Add the following information to a ~/.script-config
   [Bitstamp]
   apiKey=apiKey
   customerID=customerID
   apiSecret=apiSecret

[User]
   emailSource=email@gmail.com (has to be gmail with less secure apps configured to on)
   emailSourcePassword=password
   emailTarget=target@mail.com


* Create a symlink from the main.py directory: "sudo ln -s $(pwd)/main.py /usr/local/bin/run_trade_bot"
* Type run_trade_bot -h for script instructions 
