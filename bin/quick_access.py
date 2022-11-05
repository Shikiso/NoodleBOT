from Data.data_handler import json, sql

jsonObj = json() # json class object
sqlObj = sql() # sql class object

Users = {} # dictionary to store all user information
Items = {} # dictionary to store all items | format = ID:(name, price, exists)
Items_IDs = {} # dictionary to store all items IDs using names | format = name:ID

def update_item_amount_existing(id, existing):
    sqlObj.update('items', {'Existing':existing}, ('ID', id))