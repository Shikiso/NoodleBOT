from bin.quick_access import jsonUsers
from bin.needed_vars import *

class User(object):

    def __init__(self, DiscordID, Money=1000, Items={}):
        self.DiscordID = DiscordID
        self.Money = Money
        self.Items = Items 

    def add_money(self, amount):
        self.Money += amount
        print(jsonUsers.data)
        jsonUsers.data[str(self.DiscordID)][0] = self.Money
        print(jsonUsers.data)
        jsonUsers.write()

    def sub_money(self, amount):
        self.Money -= amount
        jsonUsers.data[str(self.DiscordID)][0] = self.Money
        jsonUsers.write()
    
    def add_item(self, ID):
        if ID not in self.Items:
            self.Items[ID] = 1
        else:
            self.Items[ID] += 1
        
        jsonUsers.data[str(self.DiscordID)][1] = self.Items
        jsonUsers.write()
    
    def sub_item(self, ID):
        if ID in self.Items:
            if self.Items[ID] -1 == 0:
                self.Items.pop(ID)
            else:
                self.Items[ID] -= 1
        
        jsonUsers.data[str(self.DiscordID)][1] = self.Items
        jsonUsers.write()

def check_if_user_in_database(DiscordID):
    try:
        Users = jsonUsers.data[str(DiscordID)]
        return Users # [money: str, items: {}]
    except:
        return False  
        
def add_user_to_database(user_object):
    log.info("[+] Adding user {} to database".format(user_object.DiscordID))
    jsonUsers.add_data(user_object.DiscordID, [user_object.Money, user_object.Items])