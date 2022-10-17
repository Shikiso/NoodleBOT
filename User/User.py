class User(object):

    def __init__(self, Money, Items, Effects, Debts, Ownerships):
        self.Money = Money
        self.Items = Items
        self.Effects = Effects
        self.Debts = Debts
        self.Ownerships = Ownerships
        
        self.user_info = (self.Money, self.Items, self.Effects, self.Debts, self.Ownerships)
    
    def add_money(self, amount):
        self.Money += amount
    
    def sub_money(self, amount):
        self.Money -= amount
    
    def add_item(self, item):
        self.Items.append(item)
    
    def sub_item(self, item):
        self.Items.pop(item)
    
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