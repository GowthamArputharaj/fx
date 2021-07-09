import MetaTrader5 as mt5
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
 
login = 67021181
password = "q14d6352C"
server = "RoboForex-ECN"

# establish connection to MetaTrader 5 terminal
# if not mt5.initialize():
if not mt5.initialize(login=login, server=server,password=password):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# check the presence of active orders
orders=mt5.orders_total()
if orders>0:
    print("Total orders=",orders)
else:
    print("Orders not found")
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()