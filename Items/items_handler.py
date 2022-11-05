'''
This code gets the items from the text file and sorts them in items with prices and a set amount that can be bought.
It will then store the items into a database and create a dictionary of the items for the program to use.
The less of an item exists the more it will cost vise versa.
'''

from random import randint
from bin.needed_vars import *

class item_handler(object):
    from bin.quick_access import jsonObj, sqlObj, Items, Items_IDs

    items_text_file = "./Items/items.txt"
    default_amount_exists = 10000

    def create_id(self):
        return len(self.Items)+1

    def generate_random_price_multiplier(self):
        rpm = randint(1000,1000000)
        self.jsonObj.add_data('rpm', rpm)
        return rpm

    def get_random_price_multiplier(self):
        return self.jsonObj.data['rpm']

    def generate_price(self, exists):
        price = self.get_random_price_multiplier() / exists
        return round(price, 0)

    def create_item(self, item, exists):
        id = self.create_id()
        name = item.strip()
        price = self.generate_price(exists)
        self.Items[id] = [name, price, exists]
        self.Items_IDs[name] = id

    def generate_items(self):
        with open(self.items_text_file, 'r') as f:
            all_items = f.readlines()
        
        for item in all_items:
            self.create_item(item, self.default_amount_exists)
    
    def save_items_to_database(self):
        for item, item_info in self.Items.items():
            id = item
            name = item_info[0]
            price = item_info[1]
            existing = item_info[2]
            self.sqlObj.insert('items', ('ID', 'Name', 'Price', 'Existing'), (id, name, price, existing))
    
    def load_items_from_database(self):
        items = self.sqlObj.select('items', '*', None)

        for item in items:
            id, name, price, existing = item
            self.Items[id] = [name, price, existing]
            self.Items_IDs[name] = id
    
    def update_price_to_demand(self, itemID):
        itemInfo = self.Items[itemID]
        newPrice = self.generate_price(itemInfo[2])
        self.Items[itemID][1] = newPrice
        log.debug(f"Updating price of {itemID} to {newPrice}")
        self.sqlObj.update('items', {'Price':newPrice}, ('ID', itemID))