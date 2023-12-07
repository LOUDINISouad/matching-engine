import websocket
import json

class OrderBook:
    def __init__(self):
        
        self.bids = []
        self.asks = []

    def add_bid(self, price, quantity):
    
        self.bids.append({"price": price, "quantity": quantity})
        self.bids.sort(key=lambda x: x["price"], reverse=True)

    def add_ask(self, price, quantity):
        
        self.asks.append({"price": price, "quantity": quantity})
        self.asks.sort(key=lambda x: x["price"])

    def match_orders(self):
        
        if self.bids and self.asks:
           
            best_bid = self.bids[0]["price"]
            best_ask = self.asks[0]["price"]

           
            if best_bid >= best_ask:
                
                matched_quantity = min(self.bids[0]["quantity"], self.asks[0]["quantity"])

               
                self.bids[0]["quantity"] -= matched_quantity
                self.asks[0]["quantity"] -= matched_quantity

                
                if self.bids[0]["quantity"] == 0:
                    self.bids.pop(0)
                if self.asks[0]["quantity"] == 0:
                    self.asks.pop(0)

             
                return matched_quantity

      
        return 0

    def print_order_book(self):
        # Print the current state of the order book
        print("Bids:")
        for bid in self.bids:
            print(f"Price: {bid['price']}, Quantity: {bid['quantity']}")
        print("Asks:")
        for ask in self.asks:
            print(f"Price: {ask['price']}, Quantity: {ask['quantity']}")

def on_message(ws, message):
    trade_data = json.loads(message)
    print(f"Trade Event:")
    print(f"Symbol: {trade_data['s']}")
    print(f"Price: {trade_data['p']}")
    print(f"Quantity: {trade_data['q']}")
    print(f"Buyer Maker: {trade_data['m']}")
    print(f"Trade Time: {trade_data['T']}")
    print("")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Closed")

def on_open(ws, *args):
    print("Opened")

if __name__ == "__main__":
    symbol = "btcusdt"
    endpoint = f"wss://fstream.binance.com/ws/{symbol}@trade"

    ws = websocket.WebSocketApp(endpoint, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

   
    order_book = OrderBook()
    order_book.add_bid(180, 12)
    order_book.add_ask(170, 19)
    order_book.print_order_book()

    matched_quantity = order_book.match_orders()
    print(f"\nMatched Quantity: {matched_quantity}\n")

    order_book.print_order_book()
