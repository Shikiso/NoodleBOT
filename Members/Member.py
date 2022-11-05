from bin.quick_access import sqlObj
from bin.needed_vars import *

class User(object):

    def __init__(self, DiscordID, Money=1000, Items={}):
        self.DiscordID = DiscordID
        self.Money = Money
        self.Items = Items 

    def add_money(self, amount):
        self.Money += amount
        sqlObj.update('users', {'Money':self.Money}, ('DiscordID', self.DiscordID))

    def sub_money(self, amount):
        self.Money -= amount
        sqlObj.update('users', {'Money':self.Money}, ('DiscordID', self.DiscordID))
    
    def add_item(self, ID):
        if ID not in self.Items:
            self.Items[ID] = 1
        else:
            self.Items[ID] += 1
        
        sqlObj.update('users', {'Items':str(self.Items)}, ('DiscordID', self.DiscordID))
    
    def sub_item(self, ID):
        if ID in self.Items:
            self.Items[ID] -= 1
        
        sqlObj.update('users', {'Items':str(self.Items)}, ('DiscordID', self.DiscordID))

def check_if_user_in_database(DiscordID):
        Users = sqlObj.select('users', '*', ('DiscordID', DiscordID), True)
        if Users:
            return Users # (user, money, items)
        return False        
        
def add_user_to_database(user_object):
    log.info("[+] Adding user {} to database".format(user_object.DiscordID))
    sqlObj.insert('users', ('DiscordID', 'Money', 'Items'), (user_object.DiscordID, user_object.Money, str(user_object.Items)))