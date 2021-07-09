import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd


login = 67021181
password = "q14d6352C"
server = "RoboForex-ECN"

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize(login=login, password=password, server=server):
	print("initialize() failed, error code =",mt5.last_error())
	quit()
 
symbol = 'EURUSD'

# get the number of deals in history
point = mt5.symbol_info(symbol).point
ask = mt5.symbol_info_tick(symbol).ask
bid = mt5.symbol_info_tick(symbol).bid

print(point, ask, bid)
exit()

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()