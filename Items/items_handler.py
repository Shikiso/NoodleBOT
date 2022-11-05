'''
This code gets the items from the text file and sorts them in items with prices and a set amount that can be bought.
It will then store the items into a database and create a dictionary of the items for the program to use.
The less of an item exists the more it will cost vise versa.
'''

from random import randint

class item_handler(object):
    from bin.quick_access import jsonObj

    items_text_file = "./Items/items.txt"
    Items = {} # ID:(name, price, exists)
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
        return round(price, 2)

    def create_item(self, item, exists):
        id = self.create_id()
        name = item.strip()
        price = self.generate_price(exists)
        self.Items[id] = (name, price, exists)

    def generate_items(self):
        with open(self.items_text_file, 'r') as f:
            all_items = f.readlines()
        
        for item in all_items:
            self.create_item(item, self.default_amount_exists)