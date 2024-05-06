import logging
import time
import threading

from Excel_IO import Excel_IO
from Excel_IO import LogicOps
from TWSAPI import TWS_API

if __name__ == "__main__":
    evar = Excel_IO()

    # Make connection to the TWS API
    api = TWS_API()
    api.connect('127.0.0.1', 7496, 101)
    # api.connect('127.0.0.1', 4002, 101)

    print("1: Request Open Orders\n2: Get Strat Patterns from MT4\n3: Place New Orders\n4: Modify Existing Orders")
    choice = input("Enter choice: ")
    choice = int(choice)
    sheet = evar.Setup(choice)
    match choice:
        case 1: # Extract Open Orders to Excel
            # Request All Open Orders
            api.reqAllOpenOrders()
            # Run the api to trigger the wrapper function executions
            # This is done in a separate thread
            t1 = threading.Thread(target=api.run, daemon=True)
            t1.start()

            # Save the orders from list to Excel
            time.sleep(2)
            api.open_orders = LogicOps.RemoveDups(api.open_orders)
            evar.GetExistingOrders(api.open_orders, sheet)
        case 2: # Get Start Patterns from the MT4 file
            evar.GetStratPatterns(sheet)
        case 3: # Issue Orders to IBKR
            list1 = evar.TransferExcelOrders(sheet, "New")
            # print(list1)
            # Issue Orders from Excel to IBKR
            last_oid, list1 = api.IssueOrders(int(evar.last_oid), list1)
            evar.SetLastOrderId(last_oid)   # Save last order id to .ini
            print(f"Last Order Id: {last_oid}, issued {len(list1)} orders")
            logging.info(f"Last Order Id: {last_oid}, issued {len(list1)} orders")
        case 4:
            list1 = evar.TransferExcelOrders(sheet, "Modify")
            list1 = api.ModifyOrders(list1)
        case 5:
            # Request Account Summary
            api.reqAccountSummary(0, 'All', 'SettledCash,AccruedCash,BuyingPower,GrossPositionValue')
            api.reqPositions()
            # Run the api to trigger the wrapper function executions
            # This is done in a separate thread
            t1 = threading.Thread(target=api.run, daemon=True)
            t1.start()

            # Save the orders from list to Excel
            time.sleep(2)
    # Disconnect the API in the main thread
    time.sleep(1)
    api.disconnect()

# todo provide trail price in excel and create trailing stop loss order
# todo 
# reqPositions
# todo create a list of positions with stop & take profit
# todo create a list of open orders with stop & take profit
