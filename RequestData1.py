'''
does not return data
'''
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

class MyWrapper(EWrapper):
    def __init__(self):
        EWrapper.__init__(self)
        self.position_data = None

    def position(self, account, contract, position, avgCost):
        """
        Callback method invoked when position data is received.
        """
        print(contract.localSymbol)
        self.position_data = {"account": account, "contract": contract, "position": position, "avgCost": avgCost}

class MyClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def request_positions(self):
        """
        Request positions from TWS or IB Gateway.
        """
        self.reqPositions()

    def get_position_data(self):
        """
        Get position data received from TWS or IB Gateway.
        """
        return self.wrapper.position_data

if __name__ == "__main__":
    wrapper = MyWrapper()
    client = MyClient(wrapper)
    client.connect("127.0.0.1", 7497, clientId=0)  # Connect to TWS or IB Gateway

    # Request positions
    client.request_positions()

    # Wait for some time or perform other operations
    # For demonstration purposes, we'll wait for 5 seconds
    import time
    time.sleep(1)

    # Get position data
    position_data = client.get_position_data()
    print("Position Data:", position_data)

    # Disconnect from TWS or IB Gateway
    client.disconnect()
