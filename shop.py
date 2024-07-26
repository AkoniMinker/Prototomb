class Shop:
    def __init__(self):
        # Dictionary to store available items and their costs
        self.items = {
            "Basic Tower": 100,
            "Health Potion": 50,
            "Damage Boost": 75
        }

    def buy_item(self, item_name, player):
        # Check if the requested item is available in the shop
        if item_name in self.items:
            # Get the cost of the item
            cost = self.items[item_name]

            # Check if the player has enough points to buy the item
            if player.score >= cost:
                # Deduct the cost from the player's score
                player.score -= cost

                # Add the item to the player's inventory
                player.collect_item(item_name)

                # Inform the player that the item was bought successfully
                print(f"Bought {item_name}")
            else:
                # Inform the player that they don't have enough points
                print("Not enough points to buy this item")
        else:
            # Inform the player that the requested item is not available
            print("Item not available in the shop")
