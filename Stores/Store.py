from bin.quick_access import jsonStores, Items_IDs, Stores
from bin.needed_vars import *

class Store(object):

    def __init__(self, ID, name, items={}, sales=0, worth=0, profit=0):
        self.ID = ID
        self.name = name
        self.items = items
        self.sales = sales
        self.worth = worth
        self.profit = profit

        if ID not in jsonStores.data:
            jsonStores.data[ID] = {
                                    'name':name,
                                    'items':items,
                                    'sales':sales,
                                    'worth':worth,
                                    'profit':profit
                                    }
            jsonStores.write()
        self.storeData = jsonStores.data[ID]
    
    def change_name(self, new_name):
        self.name = new_name
        self.storeData['name'] = new_name
    
    def check_item(itemName=None, itemID=None):
        item = None
        if itemID:
            item = itemID
        elif itemName:
            if itemName in Items_IDs:
                item = Items_IDs[itemName]
            else:
                return False
        return item
    
    def add_item(self, itemName=None, itemID=None, amount=1):
        item = self.check_item(itemName=itemName, itemID=itemID)
        
        if item in self.storeData['items']:
            self.storeData['items'][item] += 1
        else:
            self.storeData['items'][item] = 1
    
    def sub_item(self, itemName=None, itemID=None, amount=1):
        item = self.check_item(itemName=itemName, itemID=itemID)
        
        if item in self.storeData['items']:
            if self.storeData['items'][item] > 1:
                self.storeData['items'][item] -= 1
                return "break"

        self.storeData['items'].pop(item)

def check_store_exists(storeID=None, storeName=None):
    for store in Stores:
        if storeID:
            if store == storeID:
                return True
            if storeName:
                if Stores[storeID][0] == storeName:
                    return True

    return False

def create_new_store(ID, name):
    storeObj = Store(ID, name)
    Stores[ID] = storeObj