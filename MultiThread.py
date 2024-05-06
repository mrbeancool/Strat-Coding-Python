from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading
import time

class MyWrapper(EWrapper):
    def __init__(self):
        super().__init__()
        self.account_balance = None
        self.positions = []

    def accountSummary(self, reqId, account, tag, value, currency):
        if tag == "NetLiquidationByCurrency":
            self.account_balance = float(value)

    def position(self, account, contract, pos, avgCost):
        self.positions.append((contract.symbol, pos, avgCost))

class MyClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

class TWS_Manager:
    def __init__(self):
        self.wrapper = MyWrapper()
        self.client = MyClient(self.wrapper)
        self.thread = threading.Thread(target=self.run_tws, daemon=True)

    def run_tws(self):
        self.client.connect("127.0.0.1", 4002, clientId=1)
        self.client.run()

    def start(self):
        self.thread.start()

    def stop(self):
        self.client.disconnect()

    def get_account_balance(self):
        return self.wrapper.account_balance

    def get_positions(self):
        return self.wrapper.positions

def fetch_results(tws_manager):
    while True:
        account_balance = tws_manager.get_account_balance()
        positions = tws_manager.get_positions()
        print("Account Balance:", account_balance)
        print("Positions:", positions)
        time.sleep(5)

if __name__ == "__main__":
    tws_manager = TWS_Manager()
    tws_manager.start()

    result_thread = threading.Thread(target=fetch_results, args=(tws_manager,), daemon=True)
    result_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tws_manager.stop()
