import heapq


class OrderBook:
    def __init__(self):
        self.bids = []  
        self.asks = []  

    def add_bid(self, price, quantity):
        heapq.heappush(self.bids, (-price, quantity))

    def add_ask(self, price, quantity):
        heapq.heappush(self.asks, (price, quantity))

    def match_orders(self):
        if self.bids and self.asks:
            best_bid = -self.bids[0][0]  
            best_ask = self.asks[0][0]

            if best_bid >= best_ask:
                matched_quantity = min(self.bids[0][1], self.asks[0][1])
                self.bids[0] = (self.bids[0][0], self.bids[0][1] - matched_quantity)
                self.asks[0] = (self.asks[0][0], self.asks[0][1] - matched_quantity)

                if self.bids[0][1] == 0:
                    heapq.heappop(self.bids)
                if self.asks[0][1] == 0:
                    heapq.heappop(self.asks)

                return matched_quantity

        return 0

    def print_order_book(self):
        print("Bids:")
        for bid in self.bids:
            print(f"Price: {-bid[0]}, Quantity: {bid[1]}")
        print("Asks:")
        for ask in self.asks:
            print(f"Price: {ask[0]}, Quantity: {ask[1]}")
