import MetaTrader5 as mt5
# Name: MetaTrader Web Demo
# Server: MetaQuotes-Demo
# Type: Forex Hedged USD
# Login: 5015083861
# Password: slzlug4k
# Investor: 3knqixcs
def get_balance():
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    
    # connect to the trade account specifying a password and a server
    authorized=mt5.login(5015083861, password="slzlug4k",server="MetaQuotes-Demo")
    if authorized:
        account_info=mt5.account_info()
        if account_info!=None:
            # display trading account data 'as is'
            mt5_balance=account_info.balance
            # print(mt5_balance)
            return mt5_balance
    else:
        print("failed to connect to trade account 5015082006, password=\"Tobiloba12\" error code =",mt5.last_error())
    
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
    
def get_equity():
# establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    # connect to the trade account specifying a password and a server
    authorized=mt5.login(5015083861, password="slzlug4k",server="MetaQuotes-Demo")
    if authorized:
        account_info=mt5.account_info()
        if account_info!=None:
            # display trading account data 'as is'
            mt5_equity= account_info.equity
            # print(mt5_equity)
            return mt5_equity
    else:
        print("failed to connect to trade account 5015082006, password=\"Tobiloba12\" error code =",mt5.last_error())

# print(get_equity())
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

def get_profit():
# establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    # connect to the trade account specifying a password and a server
    authorized=mt5.login(5015083861, password="slzlug4k",server="MetaQuotes-Demo")
    if authorized:
        account_info=mt5.account_info()
        if account_info!=None:
            # display trading account data 'as is'
            mt5_profit= account_info.profit
            # print(mt5_profit)
            return mt5_profit
    else:
        print("failed to connect to trade account 5015082006, password=\"Tobiloba12\" error code =",mt5.last_error())

# print(get_equity())
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
