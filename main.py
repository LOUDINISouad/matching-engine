import websocket
import json
#Receive trade events (for btcusdt pairs)
symbol = "btcusdt"
endpoint = f"wss://fstream.binance.com/ws/{symbol}@trade"

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
    ws = websocket.WebSocketApp(endpoint, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
