from bin.variables import db, Reset
from random import randint

class random_price_multiplier:
    rpm = 0

    def __init__(self):
        if Reset:
            self.set_rpm()

    def set_rpm(self):
        self.rpm = randint(1000,90000)

def import_items_to_database():
    with open('Items/items.txt', 'r') as f:
        items = f.readlines()

    for item in items:
        db.add_item_to_database((item, 10, 0, 0)) # Name, Price, Amount Owned, Player Made (0 = no)

def increase_amount_owned_of_item(id, amount):
    item = db.get_item(id)
    current_amount = item[4]
    db.update_item_information(id, (item[1], item[2], current_amount+amount, item[4]))
    print(f"[#] Increased item {id} amount_owned from {current_amount} to {current_amount+amount}")

def alter_item_price_based_on_demand(id):
    item = db.get_item(id)
    current_amount = item[4]
    default_price = random_price_multiplier.rpm

    price = default_price / current_amount
    return price