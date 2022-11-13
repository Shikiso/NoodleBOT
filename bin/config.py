from bin.quick_access import jsonVars, jsonUsers, jsonItems, jsonStores
from bin.needed_vars import *
from Items.items_handler import item_handler as ItemHandler
import Data.data_handler # setup json and sql objects

Debug = True # Set to True to allow debug & info logging

Reset = False # Set to True to reset all data

json_data = [jsonVars, jsonUsers, jsonStores, jsonItems]

if Debug:
    log.basicConfig(level=log.DEBUG)

if Reset:
    log.warning("[!] Resetting all data!")
    for i in json_data:
        i.data = {}
        i.write()
    
    log.info("[+] Creating items...")
    ItemHandler().generate_random_price_multiplier()
    ItemHandler().generate_items()
    ItemHandler().save_items_to_database()
    exit()

log.info("[+] Loading items...")
ItemHandler().load_items_from_database()