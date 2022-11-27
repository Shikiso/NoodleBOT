from Stores.Store import Store
from bin.quick_access import Stores, jsonStores
from bin.needed_vars import *

def create_object(storeID):
    name, items, sales, worth, profit = jsonStores.data[storeID]
    storeObj = Store(storeID, name, items, sales, worth, profit)
    Stores[storeID] = storeObj
    
def start():
    log.info("[+] Creating Stores objects...")
    for storeID in jsonStores.data:
        if storeID not in Stores:
            create_object(storeID)