'''
This code gets the items from the text file and sorts them in items with prices and a set amount that can be bought.
It will then store the items into a database and create a dictionary of the items for the program to use.
The less of an item exists the more it will cost vise versa.
'''

from random import randint, choice
from bin.needed_vars import *

class item_handler:
    from bin.quick_access import jsonVars, jsonItems, Items, Items_IDs

    items_text_file = "./Items/items.txt"
    unlimited = -1
    rare = 432596
    legend = 22356
    mythical = 500
    item_amount_choices = [unlimited, unlimited, unlimited, unlimited, rare, rare, rare, legend, legend, mythical]

    def create_id(self):
        return len(self.Items)+1

    def generate_random_price_multiplier(self):
        rpm = randint(1000000,9999999)
        self.jsonVars.add_data('rpm', rpm)
        return rpm

    def get_random_price_multiplier(self):
        return self.jsonVars.data['rpm']

    def generate_price(self, exists):
        if exists == self.unlimited:
            return 100
        price = self.get_random_price_multiplier() / exists
        price *= 100
        return round(price, 2)

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
            if ',' in item:
                item, exists = item.split(',')
                self.create_item(item, int(exists))
            else:
                exists = choice(self.item_amount_choices)
                self.create_item(item, exists)
    
    def save_items_to_database(self):
        for item, item_info in self.Items.items():
            id = item
            name = item_info[0]
            price = item_info[1]
            existing = item_info[2]
            self.jsonItems.add_data(key=id, item=[name, price, existing])
    
    def save_item_to_database(self, name, exists, id=None, price=None):
        if not id:
            id = self.create_id()
        if not price:
            price = self.generate_price(exists)
        self.jsonItems.add_data(key=id, item=[name, price, exists])
    
    def load_items_from_database(self):
        items = self.jsonItems.data

        for itemID in items:
            item = items[itemID]
            name, price, existing = item
            self.Items[itemID] = [name, price, existing]
            self.Items_IDs[name] = itemID
    
    def update_item_info(self, itemID, variableIndex, value):
        self.jsonItems.data[str(itemID)][variableIndex] = value
        self.jsonItems.write()
    
    def update_price_to_demand(self, itemID):
        itemInfo = self.Items[str(itemID)]
        newPrice = self.generate_price(itemInfo[2])
        self.Items[str(itemID)][1] = newPrice
        log.debug(f"Updating price of {itemID} to {newPrice}")
        self.update_item_info(itemID, 1, newPrice)