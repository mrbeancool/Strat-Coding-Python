'''
This file has EClient and EWrapper class and related functions
'''

from ibapi.client import *
from ibapi.wrapper import *
from ib_insync import *
import time
import threading
import datetime

class TWS_API(EClient, EWrapper):
    def __init__(self):
        # EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.open_orders = []
        # self.oid = None

    def disconnect(self):
        print(f"API is disconnected")

    def IssueOrders(self, last_oid, list1):
    # Method to loop through the list and issue orders
    # todo try catch blocks: blank fields
        c1 = Contract()
        c1.exchange = 'IDEALPRO'
        c1.secType = 'CASH'

        main_order = Order()
        main_order.tif = 'GTC'
        main_order.eTradeOnly = ''
        main_order.firmQuoteOnly = ''

        for row in list1:
            if (row[0] is None): # If the currency is none
                break

            c1.symbol = row[0] # counter currency
            c1.currency = row[1] # base currency
            stopPrice = row[6]
            tgtPrice = row[7]

            main_order.action = row[2]
            main_order.orderType = row[3]
            if (main_order.orderType == 'LMT'):
                main_order.lmtPrice = row[5]
            elif (main_order.orderType == 'STP'):
                main_order.auxPrice = row[5]
            elif (main_order.orderType == 'STP LMT'):
                main_order.auxPrice = row[5]
                main_order.lmtPrice = row[5]
            main_order.totalQuantity = row[4]
            main_order.transmit = True
            last_oid += 1
            main_order.orderId = last_oid

            if (stopPrice is not None):  # if stop price is populated
                stop_order = Order()
                if (main_order.action == 'BUY'):
                    stop_order.action = 'SELL'
                elif (main_order.action == 'SELL'):
                    stop_order.action = 'BUY'
                stop_order.orderType = 'STP'
                stop_order.auxPrice = stopPrice
                stop_order.totalQuantity = main_order.totalQuantity
                stop_order.tif = 'GTC'
                stop_order.eTradeOnly = ''
                stop_order.firmQuoteOnly = ''
                stop_order.parentId = main_order.orderId
                last_oid += 1
                stop_order.transmit = True
                stop_order.orderId = last_oid

            if (tgtPrice is not None): # if target price is populated
                tgt_order = Order()
                if (main_order.action == 'BUY'):
                    tgt_order.action = 'SELL'
                elif (main_order.action == 'SELL'):
                    tgt_order.action = 'BUY'
                tgt_order.orderType = 'LMT'
                tgt_order.lmtPrice = tgtPrice
                tgt_order.tif = 'GTC'
                tgt_order.totalQuantity = main_order.totalQuantity
                tgt_order.eTradeOnly = ''
                tgt_order.firmQuoteOnly = ''
                tgt_order.parentId = main_order.orderId
                last_oid += 1
                tgt_order.transmit = True
                tgt_order.orderId = last_oid

            self.placeOrder(main_order.orderId, c1, main_order)
            if (stopPrice is not None): # if stop loss price
                self.placeOrder(stop_order.orderId, c1, stop_order)
            if (tgtPrice is not None): # if target price
                self.placeOrder(tgt_order.orderId, c1, tgt_order)

        return last_oid, list1

    def ModifyOrders (self, list1):
        c1 = Contract()
        c1.exchange = 'IDEALPRO'
        c1.secType = 'CASH'

        main_order = Order()
        main_order.tif = 'GTC'
        main_order.eTradeOnly = ''
        main_order.firmQuoteOnly = ''

        for row in list1:
            if (row[0] is None):  # If the currency is none
                break

            c1.symbol = row[0]  # counter currency
            c1.currency = row[1]  # base currency
            stopPrice = row[6]
            tgtPrice = row[7]

            main_order.action = row[2]
            main_order.orderType = row[3]
            if (main_order.orderType == 'LMT'):
                main_order.lmtPrice = row[5]
            elif (main_order.orderType == 'STP'):
                main_order.auxPrice = row[5]
            elif (main_order.orderType == 'STP LMT'):
                main_order.auxPrice = row[5]
                main_order.lmtPrice = row[5]
            main_order.totalQuantity = row[4]
            main_order.transmit = True
            main_order.orderId = row[9]

            if (stopPrice is not None):  # if stop price is populated
                stop_order = Order()
                if (main_order.action == 'BUY'):
                    stop_order.action = 'SELL'
                elif (main_order.action == 'SELL'):
                    stop_order.action = 'BUY'
                stop_order.orderType = 'STP'
                stop_order.auxPrice = stopPrice
                stop_order.totalQuantity = main_order.totalQuantity
                stop_order.tif = 'GTC'
                stop_order.eTradeOnly = ''
                stop_order.firmQuoteOnly = ''
                stop_order.transmit = True
                stop_order.orderId = row[10]

            if (tgtPrice is not None): # if target price is populated
                tgt_order = Order()
                if (main_order.action == 'BUY'):
                    tgt_order.action = 'SELL'
                elif (main_order.action == 'SELL'):
                    tgt_order.action = 'BUY'
                tgt_order.orderType = 'LMT'
                tgt_order.lmtPrice = tgtPrice
                tgt_order.tif = 'GTC'
                tgt_order.totalQuantity = main_order.totalQuantity
                tgt_order.eTradeOnly = ''
                tgt_order.firmQuoteOnly = ''
                tgt_order.transmit = True
                tgt_order.orderId = row[11]

            if (main_order.orderId is not None):
                self.placeOrder(main_order.orderId, c1, main_order)
            if (tgt_order.orderId is not None): # if target price
                self.placeOrder(tgt_order.orderId, c1, tgt_order)
            if (stop_order.orderId is not None): # if stop loss price
                self.placeOrder(stop_order.orderId, c1, stop_order)

        return list1

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('Error1: {}:{}'.format(errorCode,errorString))

    def openOrder(self, orderId: OrderId, c1: Contract, o1: Order, orderState: OrderState):
        # print(f"1: openOrder. orderId: {orderId}, contract: {contract}, order: {order}")
        # print(f"Inside open order: {o1.permId} {o1.parentId}")
        price = max(o1.auxPrice, o1.lmtPrice) # if stop price is None, then get limit price
        if (o1.parentId == 0):
            self.open_orders.append([c1.symbol, c1.currency, o1.permId, o1.action, o1.orderType,
                                    o1.totalQuantity, price, o1.orderId])
            # print(f"Parent Order, {c1.symbol} {c1.currency} {o1.orderId}")
        else:
            # loop through excel to find the order where parent id is the order id
            # then if BUY and auxPrice of this order < auxPrice of row, then
            # populate as stop price
            self.open_orders.append([c1.symbol, c1.currency, o1.permId, o1.action, o1.orderType,
                                    o1.totalQuantity, price, o1.orderId])
            # print(f"Child Order, {c1.symbol} {c1.currency} {o1.auxPrice} {o1.lmtPrice} {o1.parentId}")

# All below functions are not being used currently
    def orderStatus(self, orderId: OrderId, status: str, filled: int, remaining: int,
                    avgFillPrice: float, permId: int,parentId: int, lastFillPrice: float,
                    clientId: int, whyHeld: str, mktCapPrice: float):
        # print(f"2: orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")
        return

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        # print(f"3: reqId: {reqId}, contract: {contract}, execution: {execution}")
        return

    def tickPrice(self, reqId, field, price, attribs):
        print(f"reqId: {reqId}, field: {field}, price: {price}, attribs: {attribs}")

    def tickSize(self, reqId, field, size):
        print(f"reqId: {reqId}, field: {field}, size: {size}")

    def historicalData(self, reqId, bar):
        ''' Called in response to reqHistoricalData '''
        print('historicalData - Close price: {}'.format(bar.close))

    def accountSummary(self, reqId:int, account:str, tag:str, value:str,
                       currency:str):
        print(f"account: {account}, tag: {tag}, value: {value}, currency: {currency}")

    def position(self, account:str, contract:Contract, position:float,
                 avgCost:float):
        print(f"contract {contract.symbol} {contract.exchange} {position} {avgCost}")

    def RequestRealTimeData(self, list1):
        for row in list1:
            if (row[0] == None):
                break

            c1 = Contract()
            c1 = Forex('EURUSD')
            # c1.exchange = 'IDEALPRO'
            # c1.exchange = 'SMART'
            # c1.secType = 'CASH'
            # c1.secType = 'STK'
            # c1.symbol = row[0]
            # c1.symbol = 'EUR'
            # c1.symbol = 'AMD'
            # c1.currency = row[1]
            # c1.currency = 'USD'
            # c1.localSymbol = 'EURUSD'

            # print(f"reqMktData: {c1.symbol}.{c1.currency}")
            # self.reqMarketDataType(3)
            # self.reqMktData(11, c1, '221', False, False, [])

            # self.reqContractDetails(14, c1)
            self.reqHistoricalData(12, c1, '', '1 M', '1 day', 'MIDPOINT', True, 1, False, [])
        return