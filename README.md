# App-TradeBot
Analysis and implementation of cryptocurrency tradebot.

## Prerequisite 
* Bitstamp Account or Kraken account
* Active api-key connected to the account 

## Run script instructions
* Run pip3 install -r requirements.txt to install relevant external libraries
* Create a file names ~/.script-config and add the following Add the following information to a:


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

* Type main.py -h for script instructions 
