import websocket
import json
import time
import threading
from order_book import OrderBook
   
order_book = OrderBook()

def on_message(ws, message):
    trade_data = json.loads(message)

   
    if 'bids' in trade_data and 'asks' in trade_data:
        for bid in trade_data['bids']:
            order_book.add_bid(float(bid[0]), float(bid[1]))  
        for ask in trade_data['asks']:
            order_book.add_ask(float(ask[0]), float(ask[1]))  
        order_book.print_order_book() 
    else:
      
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

def run_websocket():
    ws.run_forever()

if __name__ == "__main__":
    symbol = "btcusdt"
    endpoint = f"wss://fstream.binance.com/ws/{symbol}@trade"

    event_timeout = 5

    ws = websocket.WebSocketApp(endpoint, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open

    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()

    start_time = time.time()

    while time.time() - start_time < event_timeout:
        time.sleep(1)

    print(f"Stopping after {event_timeout} seconds")
    ws.close()

    order_book = OrderBook()
    order_book.add_bid(180, 12)
    order_book.add_ask(166, 15)
    order_book.print_order_book()

    matched_quantity = order_book.match_orders()
    print(f"\nMatched Quantity: {matched_quantity}\n")

    order_book.print_order_book()
