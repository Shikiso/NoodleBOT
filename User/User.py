from bin.variables import db

class User(object):

    def __init__(self, DiscordID, Money=0, Items={}, Effects=[], Debts=[], Ownerships=[]):
        self.DiscordID = DiscordID
        self.Money = Money
        self.Items = Items
        self.Effects = Effects
        self.Debts = Debts
        self.Ownerships = Ownerships
        
        self.user_info = (self.DiscordID, self.Money, self.Items, self.Effects, self.Debts, self.Ownerships)
    
    def convert_to_db_string(self, variable):
        string = ''

        if isinstance(variable, dict):
            for key, value in variable.items():
                string += f'-{key},{value}'
        
        elif isinstance(variable, list):
            for value in variable:
                string += f'-{value}'
        
        return string

    def add_money(self, amount):
        self.Money += amount
        db.update_user_info(self.DiscordID, 'money', self.Money)
        return self.Money
    
    def sub_money(self, amount):
        self.Money -= amount
        db.update_user_info(self.DiscordID, 'money', self.Money)
        return self.Money
    
    def add_item(self, item):
        if item not in self.Items:
            self.Items[item] = 1
        else:
            self.Items[item] += 1

        items_string = self.convert_to_db_string(self.Items)
        db.update_user_info(self.DiscordID, 'items', items_string)
    
    def sub_item(self, item):
        if item not in self.Items:
            return False
        else:
            if self.Items[item] - 1 == 0:
                self.Items.pop(item)
            else:
                self.Items[item] -= 1

        items_string = self.convert_to_db_string(self.Items)
        db.update_user_info(self.DiscordID, 'items', items_string)
    
    def add_effect(self, effect):
        self.Effects.append(effect)
    
    def sub_effect(self, effect):
        self.Effects.pop(effect)

    def add_debt(self, debt):
        self.Debts.append(debt)
    
    def sub_debt(self, debt):
        self.Debts.pop(debt)

    def add_ownership(self, ownership):
        self.Ownerships.append(ownership)
    
    def sub_ownership(self, ownership):
        self.Ownerships.pop(ownership)