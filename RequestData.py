'''
Does not stop
'''
from ibapi.client import *
from ibapi.wrapper import *
import threading
import time
import datetime
class SimpleClient(EClient, EWrapper):
    def __init__(self, addr, port, client_id):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.open_orders = []
        self.connect(addr, port, client_id)
        self.t1 = threading.Thread(target=self.run())
        self.t2 = threading.Thread(target=self.disconnect())
        self.stopFlag = threading.Event()

        # Launch the client thread
        # thread = Thread(target=self.run)
        # thread.start()
        # self.reqCurrentTime()
        # self.run()

        # thread = threading.Thread(target=self.ru]n())
        # thread.start()

    def run(self):
        while not self.stopFlag.is_set():
            print('Inside run')
            time.sleep(0.1)  # Small sleep to prevent excessive CPU usage
            # self.disconnect()

    def stop(self):
        self.stopFlag.set()
        self.t1.join()
        self.t2.start()

    @iswrapper
    def currentTime(self, currTime):
        # t = datetime.datetime(currTime)
        print('Current Time: ', currTime)

    @iswrapper
    def error(self, reqId, code, msg):
        return
        # if(self.isConnected()):
        #     print("Connection Successful")
        # print('Error1: {}:{}'.format(code,msg))

    @iswrapper
    def openOrder(self, orderId, contract, order, orderState):
        # print(f"Open Order ID: {orderId}, Contract: {contract.localSymbol}, Action: {order.action}, Quantity: {order.totalQuantity}, Status: {orderState.status}  "
        #       f"{order.orderId} {orderState.completedStatus} Margin: {orderState.initMarginChange} {orderState.commission} {orderState.maintMarginAfter} {orderState.maintMarginChange}" )

        # for pid in order.permId:
        #     openOrderList
        self.open_orders.append([order.permId, contract.localSymbol, order.action, order.totalQuantity,
                                 order.auxPrice, orderState.status])
        print("Inside openOrder")
        print(self.open_orders)
        return self.open_orders

    @iswrapper
    def orderStatus(self, orderId: OrderId, status: str, filled: int, remaining: int, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        # print(f"2: orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")
        # print(f"{avgFillPrice} {filled}")
        return

    @iswrapper
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"3: reqId: {reqId}, contract: {contract}, execution: {execution}")

    @iswrapper
    def nextValidId(self, orderId:int):
        # print(f"Order ID: {orderId}")
        return orderId

    @iswrapper
    def position(self, account:str, contract:Contract, position:float,
                 avgCost:float):
        print(f"{account} {contract.localSymbol} {position} {avgCost} ")

    def WriteToExcel(self, listname, sheetname):
        print("")
        '''
        Code to dump the data from a 2D list into excel
        2D listname & sheetname as parameter write to sheetname
        for row_idx, row_data in enumerate(list_name, start=1):
            for col_idx, cell_value in enumerate(row_data, start=1):
                sheetname.cell(row=row_idx, column=col_idx, value=cell_value)
    
        return sheetname
        '''
    def get_open_orders(self):
        return self.open_orders
        
def main():
    app = SimpleClient('127.0.0.1', 7497, 1000)
    # thread2 = threading.Thread(target=app.currentTime())
    # thread2.start()
    time.sleep(1)
    # app.open_orders = []

    # print(f"Connection Status: ", app.isConnected())
    # t = app.reqCurrentTime()
    app.reqAllOpenOrders()
    # app.reqExecutions(1000, ExecutionFilter())
    # app.reqPositions()

    time.sleep(1)
    '''
    Placing orders
    '''
    # c1 = Contract()

    # o1 = Order()
    # o1 = app.reqIds(1)
    # print(f"Order Id in main: {o1}")
    # o1 = app.placeOrder(orderId, mycontract, myorder)
    # app.reqCompletedOrders()


    app.t1.start()

    # open_orders = app.get_open_orders()
    print("open_orders list")
    for o in app.open_orders:
        print(o)

    time.sleep(1)
    # app.disconnect() # todo thread to disconnect the api
    # app.t1.join()
    # app.t2.start()
    app.stop()

if __name__ == "__main__":
    main()