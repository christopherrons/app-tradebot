# App-TradeBot
Analysis and implementation of cryptocurrency tradebot.

## Prerequisite 
* Bitstamp Account with a main / sub account (sub account is recommended for more control)
* Active api-key connected to the account 

## Run script instructions
* Run pip3 install -r requirements.txt to install relevant external libraries
* Add the following information to a ~/.script-config


[Bitstamp] <br />
   apiKey=apiKey <br />
   customerID=customerID <br />
   apiSecret=apiSecret <br />
   
[Kraken] <br />
   apiKey=apiKey <br />
   customerID=customerID <br />
   apiSecret=apiSecret <br />

[User] <br />
   emailSource=email@gmail.com (has to be gmail with less secure apps configured to on) <br />
   emailSourcePassword=password <br />
   emailTarget=target@mail.com <br />

* Type run_trade_bot -h for script instructions 
