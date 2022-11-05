from bin.quick_access import sqlObj, jsonObj, Debug, Reset
from bin.needed_vars import *
from Items.items_handler import item_handler as ItemHandler
import Data.data_handler # setup json and sql objects

def setup():
    log.info("[+] Creating database tables...")
    sqlObj.create_table('users', {'DiscordID':'integer NOT NULL', 'Money':'integer', 'Items':'text'})
    sqlObj.create_table('items', {'ID':'integer NOT NULL', 'Price':'integer', 'Existing':'integer'})

    log.info("[+] Creating items...")
    ItemHandler().generate_random_price_multiplier()
    ItemHandler().generate_items()


if Debug:
    log.basicConfig(level=log.DEBUG)

if Reset:
    log.warning("[!] Resetting all data!")
    sqlObj.drop('users')
    sqlObj.drop('items')

    jsonObj.data = {}
    jsonObj.write()
    exit()

setup()