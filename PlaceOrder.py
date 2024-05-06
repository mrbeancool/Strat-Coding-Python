'''
Does not stop
Dont know how the flow is arranged
'''
from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
  def __init__(self):
    EClient.__init__(self, self)
    print("Inside init")

  def nextValidId(self, orderId: OrderId):

    mycontract = Contract()
    mycontract.symbol = "GOOG"
    mycontract.secType = "STK"
    mycontract.exchange = "SMART"
    mycontract.currency = "USD"

    self.reqContractDetails(orderId, mycontract)
    print("Inside nextValidId")

  def contractDetails(self, reqId: int, contractDetails: ContractDetails):
    print(f"5: ", contractDetails.contract)

    myorder = Order()
    myorder.orderId = reqId
    myorder.action = "BUY"
    myorder.tif = "GTC"
    myorder.orderType = "LMT"
    myorder.lmtPrice = 125
    myorder.totalQuantity = 10
    myorder.eTradeOnly = ''
    myorder.firmQuoteOnly = ''

    self.placeOrder(myorder.orderId, contractDetails.contract, myorder)


  def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
    # print(f"1: openOrder. orderId: {orderId}, contract: {contract}, order: {order}")

  def orderStatus(self, orderId: OrderId, status: str, filled: int, remaining: int, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
    # print(f"2: orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

  def execDetails(self, reqId: int, contract: Contract, execution: Execution):
    print(f"3: reqId: {reqId}, contract: {contract}, execution: {execution}")

  def TestMethod(self):
    print(f"4 :")

app = TestApp()
app.connect("127.0.0.1", 7497, 100)
app.run()
app.disconnect()