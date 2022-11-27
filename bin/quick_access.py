from Data.data_handler import json, sql

jsonVars = json("./Data/json_data.json") # json class object
jsonItems = json("./Data/items.json")
jsonUsers = json("./Data/users.json")
jsonStores = json("./Data/stores.json")

json_data = [jsonVars, jsonUsers, jsonStores, jsonItems]
# sqlObj = sql() # sql class object

Users = {} # dictionary to store all user information
Items = {} # dictionary to store all items | format = ID:(name, price, exists)
Items_IDs = {} # dictionary to store all items IDs using names | format = name:ID
Stores = {} # dictionary to store all stores information ID:(name, items, sales, worth, profit)

def update_item_amount_existing(id, existing):
    jsonItems.data[id][2] = existing
    jsonUsers.write()

def reload_data():
    for data in json_data:
        data.load_json_data()